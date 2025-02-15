import itertools
from typing import Iterator, List, Optional, Tuple, Union

from sqlparse import tokens
from sqlparse.engine.grouping import _group, group_functions
from sqlparse.sql import (
    Case,
    Comment,
    Comparison,
    Function,
    Identifier,
    Parenthesis,
    TokenList,
    Where,
)
from sqlparse.tokens import DML, Keyword, Name, Wildcard
from sqlparse.utils import imt, recurse

from sqllineage.utils.entities import SubQueryTuple
from sqllineage.utils.helpers import escape_identifier_name


def is_token_negligible(token: TokenList) -> bool:
    # utility to skip tokens like whitespace or comment
    return token.is_whitespace or isinstance(token, Comment)


def remove_parenthesis_between_union(token: Parenthesis) -> Parenthesis:
    """
    remove parenthesis around subqueries between union
    Example:
        INPUT: ((SELECT col1 FROM tab2) UNION ALL (SELECT col1 FROM tab3))
        OUTPUT: (SELECT col1 FROM tab2 UNION ALL SELECT col1 FROM tab3)
    """
    # pre-compute the idx of UNION/UNION ALL
    offsets = [-1]
    while True:
        offset, _ = token.token_next_by(
            m=[(Keyword, "UNION ALL"), (Keyword, "UNION")], idx=offsets[-1]
        )
        if offset is not None:
            offsets.append(offset)
        else:
            break
    expand_parenthesis_idx = set()
    for i, offset in enumerate(offsets[1:]):
        if i == 0:
            # first union idx, we need to handle the previous parenthesis
            pre_idx, sub_token = token.token_prev(idx=offset)
            if isinstance(sub_token, Parenthesis):
                expand_parenthesis_idx.add(pre_idx)
        # then all post parenthesis handled for each union
        post_idx, sub_token = token.token_next(idx=offset)
        if isinstance(sub_token, Parenthesis):
            expand_parenthesis_idx.add(post_idx)
    if expand_parenthesis_idx:
        updated_tokens = []
        for i, sub_token in enumerate(token.tokens):
            if i in expand_parenthesis_idx:
                inner_paren = get_innermost_parenthesis(sub_token)
                updated_tokens.extend(inner_paren.tokens[1:-1])
            else:
                updated_tokens.append(sub_token)
        token.tokens = updated_tokens
    return token


def get_innermost_parenthesis(token: Parenthesis) -> Parenthesis:
    # in case of subquery in nested parenthesis, find the innermost one first
    while True:
        idx, sub_paren = token.token_next_by(i=Parenthesis)
        if sub_paren is not None and (
            idx == 1
            or (idx > 1 and all(is_token_negligible(t) for t in token.tokens[1:idx]))
        ):
            # either the subsequent parenthesis is closely followed or there is only whitespace/comment in between
            token = sub_paren
        else:
            break
    return token


def is_subquery(token: TokenList) -> bool:
    flag = False
    if isinstance(token, Parenthesis):
        token = get_innermost_parenthesis(token)
        # check if innermost parenthesis contains SELECT
        _, sub_token = token.token_next_by(m=(DML, "SELECT"))
        if sub_token is not None:
            flag = True
    return flag


def is_values_clause(token: Parenthesis) -> bool:
    for t in token.tokens:
        if is_token_negligible(t):
            continue
        if t.match(Keyword, "VALUES"):
            return True
    return False


def get_identifier_name_and_parent(identifier: Identifier) -> Tuple[str, Optional[str]]:
    """
    rewrite identifier's get_real_name and get_parent_name method, by matching the last dot instead of the first dot,
    so that the real name for a.b.c will be c instead of b, and parent will be a.b
    """
    dot_idx, _ = identifier._token_matching(
        lambda token: imt(token, m=(tokens.Punctuation, ".")),
        start=len(identifier.tokens),
        reverse=True,
    )

    if not dot_idx:
        # if no dot in identifier, could be subquery with alias, e.g. (SELECT ...) as xxx
        # retrieve the alias as the real name, no parent name
        # most of the time 'xxx' after 'as' should be a simple identifier, but sometime is recognized as a keyword
        subquery = [
            token for token in identifier.tokens if isinstance(token, Parenthesis)
        ]
        alias_identifier = [
            token for token in identifier.tokens if isinstance(token, Identifier)
        ]
        alias_keyword = [
            token
            for token in identifier.tokens
            if token.is_keyword and token.normalized != "AS"
        ]
        if len(subquery) == 1 and len(alias_identifier) == 1:
            return alias_identifier[0]._get_first_name(real_name=True), None
        if len(subquery) == 1 and len(alias_keyword) == 1:
            return alias_keyword[0].value, None

    real_name = identifier._get_first_name(dot_idx, real_name=True)
    parent_name = (
        "".join(
            [
                escape_identifier_name(token.value)
                for token in identifier.tokens[:dot_idx]
            ]
        )
        if dot_idx
        else None
    )

    return real_name, parent_name


def get_identifier_fullname_normalized(identifier: Identifier) -> str:
    """
    get identifier's fullname by joining parent_name and real_name from get_identifier_name_and_parent()
    normalized to lowercase
    """
    real_name, parent_name = get_identifier_name_and_parent(identifier)
    return (f"{parent_name}.{real_name}" if parent_name else real_name).lower()


def get_subquery_parentheses(
    token: Union[Identifier, Function, Where]
) -> List[SubQueryTuple]:
    """
    Retrieve subquery list
    the returned list is either empty when no subquery parsed or list of [parenthesis, alias] tuple
    """
    subquery = []
    as_idx, as_ = token.token_next_by(m=(Keyword, "AS"))
    # get all token subgroups that does not start with an Identifier,
    # e.g. table name with column definitions "table1 (col1, col2)".
    sublist = [
        s for s in token.get_sublists() if not isinstance(s.tokens[0], Identifier)
    ]
    if as_ is not None and len(sublist) == 1:
        # CTE: tbl AS (SELECT 1)
        target = sublist[0]
    else:
        if isinstance(token, Function):
            # CTE without AS: tbl (SELECT 1)
            target = token.tokens[-1]
        elif isinstance(token, Where):
            # WHERE col1 IN (SELECT max(col1) FROM tab2)
            target = token
        else:
            # normal subquery: (SELECT 1) tbl
            target = token.token_first(skip_cm=True)
    if isinstance(target, (Case, Where)):
        # CASE WHEN (SELECT count(*) from tab1) > 0 THEN (SELECT count(*) FROM tab1) ELSE -1
        for tk in target.get_sublists():
            if isinstance(tk, Comparison):
                if is_subquery(tk.left):
                    subquery.append(SubQueryTuple(tk.left, tk.left.get_real_name()))
                if is_subquery(tk.right):
                    subquery.append(SubQueryTuple(tk.right, tk.right.get_real_name()))
            elif is_subquery(tk):
                subquery.append(SubQueryTuple(tk, token.get_real_name()))
    elif is_subquery(target):
        target = remove_parenthesis_between_union(target)
        subquery = [
            SubQueryTuple(
                get_innermost_parenthesis(target),
                get_identifier_fullname_normalized(token),
            )
        ]
    return subquery


def get_parameters(token: Function):
    """
    This is a replacement for sqlparse.sql.Function.get_parameters(), which produces problematic result for:
        if(col1 = 'foo' AND col2 = 'bar', 1, 0)
    This implementation ignores the constant parameter as we don't need them for column lineage for now
    """
    if isinstance(token, Window):
        return token.get_parameters()
    else:
        return [
            tk for tk in token.tokens[-1].tokens if tk.is_group or tk.ttype == Wildcard
        ]


class Window(Function):
    """window function + OVER keyword + window defn"""

    def get_parameters(self) -> Iterator[TokenList]:
        return itertools.chain(
            get_parameters(self.get_window_function()),
            self.get_window_defn().get_sublists(),
        )

    def get_window_function(self) -> Function:
        return self.tokens[0]

    def get_window_defn(self) -> Parenthesis:
        return self.tokens[-1]


@recurse(Window)
def group_window(tlist):
    def match(token):
        return token.is_keyword and token.normalized == "OVER"

    def valid_prev(token):
        return isinstance(token, Function)

    def valid_next(token):
        return isinstance(token, Parenthesis)

    def post(tlist, pidx, tidx, nidx):
        return pidx, nidx

    _group(
        tlist, Window, match, valid_prev, valid_next, post, extend=False, recurse=False
    )


@recurse(Function)
def group_functions_as(tlist):
    """
    This function is to allow parsing columns in functions with CTAS syntax like:
        CREATE TABLE tbl1 AS SELECT coalesce(t1.col1, 0) AS col1 FROM t1;
    The code is mostly taken from original sqlparse.sql.group_functions by
    replacing with one condition.

    This is no longer needed if this PR get merged:
    https://github.com/andialbrecht/sqlparse/pull/662
    """
    has_create = False
    has_table = False
    has_as = False
    for tmp_token in tlist.tokens:
        if tmp_token.value == "CREATE":
            has_create = True
        if tmp_token.value == "TABLE":
            has_table = True
        if tmp_token.value == "AS":
            has_as = True
    if not has_create or not has_table or not has_as:
        return

    tidx, token = tlist.token_next_by(t=Name)
    while token:
        nidx, next_ = tlist.token_next(tidx)
        if isinstance(next_, Parenthesis):
            tlist.group_tokens(Function, tidx, nidx)
        tidx, token = tlist.token_next_by(t=Name, idx=tidx)


def group_function_with_window(tlist):
    group_functions(tlist)
    group_functions_as(tlist)
    group_window(tlist)
