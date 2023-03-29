import pytest

from sqllineage.core.models import Table
from sqllineage.utils.entities import ColumnQualifierTuple
from sqllineage.utils.schemaFetcher import DummySchemaFetcher
from .helpers import assert_table_and_column_lineage_equal

expected = {
    1: (
        {"date_dim", "store_returns", "store", "customer"},
        {"query01"},
        [
            (
                ColumnQualifierTuple("c_customer_id", "<default>.customer"),
                ColumnQualifierTuple("c_customer_id", "query01"),
            )
        ],
        {
            "customer": ["c_customer_id"],
            "store_returns": [
                "sr_customer_sk",
                "sr_store_sk",
                "sr_return_amt",
            ],
        },
    ),
    2: (
        {"web_sales", "catalog_sales", "date_dim"},
        {"query02"},
        [
            (
                ColumnQualifierTuple("ws_ext_sales_price", "<default>.web_sales"),
                ColumnQualifierTuple(
                    "round(mon_sales1 / mon_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", "<default>.web_sales"),
                ColumnQualifierTuple(
                    "round(tue_sales1 / tue_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", "<default>.web_sales"),
                ColumnQualifierTuple(
                    "round(wed_sales1 / wed_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", "<default>.web_sales"),
                ColumnQualifierTuple(
                    "round(thu_sales1 / thu_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", "<default>.web_sales"),
                ColumnQualifierTuple(
                    "round(fri_sales1 / fri_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", "<default>.web_sales"),
                ColumnQualifierTuple(
                    "round(sat_sales1 / sat_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", "<default>.web_sales"),
                ColumnQualifierTuple(
                    "round(sun_sales1 / sun_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", "<default>.catalog_sales"),
                ColumnQualifierTuple(
                    "round(mon_sales1 / mon_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", "<default>.catalog_sales"),
                ColumnQualifierTuple(
                    "round(tue_sales1 / tue_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", "<default>.catalog_sales"),
                ColumnQualifierTuple(
                    "round(wed_sales1 / wed_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", "<default>.catalog_sales"),
                ColumnQualifierTuple(
                    "round(thu_sales1 / thu_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", "<default>.catalog_sales"),
                ColumnQualifierTuple(
                    "round(fri_sales1 / fri_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", "<default>.catalog_sales"),
                ColumnQualifierTuple(
                    "round(sat_sales1 / sat_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", "<default>.catalog_sales"),
                ColumnQualifierTuple(
                    "round(sun_sales1 / sun_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("d_day_name", "<default>.date_dim"),
                ColumnQualifierTuple(
                    "round(mon_sales1 / mon_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("d_day_name", "<default>.date_dim"),
                ColumnQualifierTuple(
                    "round(tue_sales1 / tue_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("d_day_name", "<default>.date_dim"),
                ColumnQualifierTuple(
                    "round(wed_sales1 / wed_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("d_day_name", "<default>.date_dim"),
                ColumnQualifierTuple(
                    "round(thu_sales1 / thu_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("d_day_name", "<default>.date_dim"),
                ColumnQualifierTuple(
                    "round(fri_sales1 / fri_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("d_day_name", "<default>.date_dim"),
                ColumnQualifierTuple(
                    "round(sat_sales1 / sat_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("d_day_name", "<default>.date_dim"),
                ColumnQualifierTuple(
                    "round(sun_sales1 / sun_sales2, 2)", "<default>.query02"
                ),
            ),
            (
                ColumnQualifierTuple("d_week_seq", "<default>.date_dim"),
                ColumnQualifierTuple("d_week_seq1", "<default>.query02"),
            ),
        ],
        {
            "date_dim": ["d_day_name", "d_week_seq"],
        },
    ),
    3: (
        {"date_dim", "store_sales", "item"},
        {"query03"},
        [
            (
                ColumnQualifierTuple("d_year", "date_dim"),
                ColumnQualifierTuple("d_year", "query03"),
            ),
            (
                ColumnQualifierTuple("i_brand_id", "item"),
                ColumnQualifierTuple("brand_id", "query03"),
            ),
            (
                ColumnQualifierTuple("i_brand", "item"),
                ColumnQualifierTuple("brand", "query03"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("sum_agg", "query03"),
            ),
        ],
        {},
    ),
    4: (
        {"catalog_sales", "customer", "web_sales", "date_dim", "store_sales"},
        {"query04"},
        [
            (
                ColumnQualifierTuple("c_preferred_cust_flag", "customer"),
                ColumnQualifierTuple("customer_preferred_cust_flag", "query04"),
            ),
            (
                ColumnQualifierTuple("c_customer_id", "customer"),
                ColumnQualifierTuple("customer_id", "query04"),
            ),
            (
                ColumnQualifierTuple("c_first_name", "customer"),
                ColumnQualifierTuple("customer_first_name", "query04"),
            ),
            (
                ColumnQualifierTuple("c_last_name", "customer"),
                ColumnQualifierTuple("customer_last_name", "query04"),
            ),
        ],
        {
            "customer": [
                "c_customer_id",
                "c_first_name",
                "c_last_name",
                "c_preferred_cust_flag",
                "c_birth_country",
                "c_login",
                "c_email_address",
            ]
        },
    ),
    5: (
        {
            "catalog_page",
            "catalog_returns",
            "catalog_sales",
            "date_dim",
            "store",
            "store_returns",
            "store_sales",
            "web_returns",
            "web_sales",
            "web_site",
        },
        {"query05"},
        [
            (
                ColumnQualifierTuple("cp_catalog_page_id", "catalog_page"),
                ColumnQualifierTuple("id", "query05"),
            ),
            (
                ColumnQualifierTuple("web_site_id", "web_site"),
                ColumnQualifierTuple("id", "query05"),
            ),
            (
                ColumnQualifierTuple("s_store_id", "store"),
                ColumnQualifierTuple("id", "query05"),
            ),
            (
                ColumnQualifierTuple("ws_net_profit", "web_sales"),
                ColumnQualifierTuple("profit", "query05"),
            ),
            (
                ColumnQualifierTuple("cs_net_profit", "catalog_sales"),
                ColumnQualifierTuple("profit", "query05"),
            ),
            (
                ColumnQualifierTuple("ss_net_profit", "store_sales"),
                ColumnQualifierTuple("profit", "query05"),
            ),
            (
                ColumnQualifierTuple("cr_net_loss", "catalog_returns"),
                ColumnQualifierTuple("profit", "query05"),
            ),
            (
                ColumnQualifierTuple("sr_net_loss", "store_returns"),
                ColumnQualifierTuple("profit", "query05"),
            ),
            (
                ColumnQualifierTuple("wr_net_loss", "web_returns"),
                ColumnQualifierTuple("profit", "query05"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", "web_sales"),
                ColumnQualifierTuple("sales", "query05"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", "store_sales"),
                ColumnQualifierTuple("sales", "query05"),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", "catalog_sales"),
                ColumnQualifierTuple("sales", "query05"),
            ),
        ],
        {
            "web_returns": [
                "wr_returned_date_sk",
                "wr_return_amt",
                "wr_net_loss",
            ],
            "store": ["s_store_id"],
            "catalog_page": ["cp_catalog_page_id"],
            "web_site": ["web_site_id"],
        },
    ),
    6: (
        {"customer", "customer_address", "date_dim", "item", "store_sales"},
        {"query06"},
        [
            (
                ColumnQualifierTuple("ca_state", "customer_address"),
                ColumnQualifierTuple("state", "query06"),
            ),
        ],
        {},
    ),
    7: (
        {"customer_demographics", "date_dim", "item", "promotion", "store_sales"},
        {"query07"},
        [
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("i_item_id", "query07"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("agg1", "query07"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", None),
                ColumnQualifierTuple("agg2", "query07"),
            ),
            (
                ColumnQualifierTuple("ss_coupon_amt", None),
                ColumnQualifierTuple("agg3", "query07"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("agg4", "query07"),
            ),
        ],
        {},
    ),
    8: (
        {"customer_address", "date_dim", "store", "store_sales"},
        {"query08"},
        [
            (
                ColumnQualifierTuple("ss_net_profit", None),
                ColumnQualifierTuple("sum(ss_net_profit)", "query08"),
            ),
            (
                ColumnQualifierTuple("s_store_name", None),
                ColumnQualifierTuple("s_store_name", "query08"),
            ),
        ],
        {},
    ),
    9: (
        {"reason", "store_sales"},
        {"query09"},
        [
            (
                ColumnQualifierTuple("ss_net_paid", "store_sales"),
                ColumnQualifierTuple("bucket1", "query09"),
            ),
            (
                ColumnQualifierTuple("ss_ext_discount_amt", "store_sales"),
                ColumnQualifierTuple("bucket1", "query09"),
            ),
            (
                ColumnQualifierTuple("ss_net_paid", "store_sales"),
                ColumnQualifierTuple("bucket2", "query09"),
            ),
            (
                ColumnQualifierTuple("ss_ext_discount_amt", "store_sales"),
                ColumnQualifierTuple("bucket2", "query09"),
            ),
            (
                ColumnQualifierTuple("ss_net_paid", "store_sales"),
                ColumnQualifierTuple("bucket3", "query09"),
            ),
            (
                ColumnQualifierTuple("ss_ext_discount_amt", "store_sales"),
                ColumnQualifierTuple("bucket3", "query09"),
            ),
            (
                ColumnQualifierTuple("ss_net_paid", "store_sales"),
                ColumnQualifierTuple("bucket4", "query09"),
            ),
            (
                ColumnQualifierTuple("ss_ext_discount_amt", "store_sales"),
                ColumnQualifierTuple("bucket4", "query09"),
            ),
            (
                ColumnQualifierTuple("ss_net_paid", "store_sales"),
                ColumnQualifierTuple("bucket5", "query09"),
            ),
            (
                ColumnQualifierTuple("ss_ext_discount_amt", "store_sales"),
                ColumnQualifierTuple("bucket5", "query09"),
            ),
        ],
        {},
    ),
    10: (
        {
            "customer",
            "customer_address",
            "customer_demographics",
            "date_dim",
            "store_sales",
        },
        {"query10"},
        [
            (
                ColumnQualifierTuple("cd_gender", "customer_demographics"),
                ColumnQualifierTuple("cd_gender", "query10"),
            ),
            (
                ColumnQualifierTuple("cd_marital_status", "customer_demographics"),
                ColumnQualifierTuple("cd_marital_status", "query10"),
            ),
            (
                ColumnQualifierTuple("cd_education_status", "customer_demographics"),
                ColumnQualifierTuple("cd_education_status", "query10"),
            ),
            (
                ColumnQualifierTuple("cd_purchase_estimate", "customer_demographics"),
                ColumnQualifierTuple("cd_purchase_estimate", "query10"),
            ),
            (
                ColumnQualifierTuple("cd_credit_rating", "customer_demographics"),
                ColumnQualifierTuple("cd_credit_rating", "query10"),
            ),
            (
                ColumnQualifierTuple("cd_dep_count", "customer_demographics"),
                ColumnQualifierTuple("cd_dep_count", "query10"),
            ),
            (
                ColumnQualifierTuple("cd_dep_employed_count", "customer_demographics"),
                ColumnQualifierTuple("cd_dep_employed_count", "query10"),
            ),
            (
                ColumnQualifierTuple("cd_dep_college_count", "customer_demographics"),
                ColumnQualifierTuple("cd_dep_college_count", "query10"),
            ),
        ],
        {
            "customer_demographics": [
                "cd_gender",
                "cd_demo_sk",
                "cd_marital_status",
                "cd_education_status",
                "cd_purchase_estimate",
                "cd_credit_rating",
                "cd_dep_count",
                "cd_dep_employed_count",
                "cd_dep_college_count",
            ]
        },
    ),
    11: (
        {"customer", "date_dim", "store_sales", "web_sales"},
        {"query11"},
        [
            (
                ColumnQualifierTuple("c_customer_id", None),
                ColumnQualifierTuple("customer_id", "query11"),
            ),
            (
                ColumnQualifierTuple("c_first_name", None),
                ColumnQualifierTuple("customer_first_name", "query11"),
            ),
            (
                ColumnQualifierTuple("c_last_name", None),
                ColumnQualifierTuple("customer_last_name", "query11"),
            ),
            (
                ColumnQualifierTuple("c_preferred_cust_flag", None),
                ColumnQualifierTuple("customer_preferred_cust_flag", "query11"),
            ),
        ],
        {},
    ),
    12: (
        {"item", "date_dim", "web_sales"},
        {"query12"},
        [
            (
                ColumnQualifierTuple("i_current_price", None),
                ColumnQualifierTuple("i_current_price", "query12"),
            ),
            (
                ColumnQualifierTuple("i_item_desc", None),
                ColumnQualifierTuple("i_item_desc", "query12"),
            ),
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("i_item_id", "query12"),
            ),
            (
                ColumnQualifierTuple("i_class", None),
                ColumnQualifierTuple("i_class", "query12"),
            ),
            (
                ColumnQualifierTuple("i_class", None),
                ColumnQualifierTuple("revenueratio", "query12"),
            ),
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("i_category", "query12"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("itemrevenue", "query12"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("revenueratio", "query12"),
            ),
        ],
        {},
    ),
    13: (
        {
            "date_dim",
            "store_sales",
            "store",
            "household_demographics",
            "customer_address",
            "customer_demographics",
        },
        {"query13"},
        [
            (
                ColumnQualifierTuple("ss_ext_wholesale_cost", None),
                ColumnQualifierTuple("sum(ss_ext_wholesale_cost)", "query13"),
            ),
            (
                ColumnQualifierTuple("ss_ext_wholesale_cost", None),
                ColumnQualifierTuple("avg(ss_ext_wholesale_cost)", "query13"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("avg(ss_ext_sales_price)", "query13"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("avg(ss_quantity)", "query13"),
            ),
        ],
        {},
    ),
    14: (
        {"store_sales", "item", "date_dim", "catalog_sales", "web_sales"},
        {"query14"},
        [],
        {},
    ),
    15: (
        {"catalog_sales", "date_dim", "customer_address", "customer"},
        {"query15"},
        [
            (
                ColumnQualifierTuple("ca_zip", "customer_address"),
                ColumnQualifierTuple("ca_zip", "query15"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", "catalog_sales"),
                ColumnQualifierTuple("sum(cs_sales_price)", "query15"),
            ),
        ],
        {"customer_address": ["ca_zip"], "catalog_sales": ["cs_sales_price"]},
    ),
    16: (
        {
            "catalog_sales",
            "call_center",
            "customer_address",
            "date_dim",
            "catalog_returns",
        },
        {"query16"},
        [
            (
                ColumnQualifierTuple("cs_ext_ship_cost", None),
                ColumnQualifierTuple("total_shipping_cost", "query16"),
            ),
            (
                ColumnQualifierTuple("cs_net_profit", None),
                ColumnQualifierTuple("total_net_profit", "query16"),
            ),
            (
                ColumnQualifierTuple("cs_order_number", None),
                ColumnQualifierTuple("order_count", "query16"),
            ),
        ],
        {},
    ),
    17: (
        {"store_returns", "date_dim", "catalog_sales", "item", "store", "store_sales"},
        {"query17"},
        [
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("i_item_id", "query17"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("store_sales_quantitystdev", "query17"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("store_sales_quantitycount", "query17"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("catalog_sales_quantitystdev", "query17"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("catalog_sales_quantitycov", "query17"),
            ),
            (
                ColumnQualifierTuple("sr_return_quantity", None),
                ColumnQualifierTuple("store_returns_quantitystdev", "query17"),
            ),
            (
                ColumnQualifierTuple("i_item_desc", None),
                ColumnQualifierTuple("i_item_desc", "query17"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("store_sales_quantitycov", "query17"),
            ),
            (
                ColumnQualifierTuple("sr_return_quantity", None),
                ColumnQualifierTuple("store_returns_quantitycount", "query17"),
            ),
            (
                ColumnQualifierTuple("sr_return_quantity", None),
                ColumnQualifierTuple("store_returns_quantitycov", "query17"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("store_sales_quantityave", "query17"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("catalog_sales_quantityave", "query17"),
            ),
            (
                ColumnQualifierTuple("sr_return_quantity", None),
                ColumnQualifierTuple("store_returns_quantityave", "query17"),
            ),
            (
                ColumnQualifierTuple("s_state", None),
                ColumnQualifierTuple("s_state", "query17"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("catalog_sales_quantitycount", "query17"),
            ),
        ],
        {},
    ),
    18: (
        {
            "catalog_sales",
            "item",
            "customer_address",
            "customer_demographics",
            "date_dim",
            "customer",
        },
        {"query18"},
        [
            (
                ColumnQualifierTuple("ca_county", None),
                ColumnQualifierTuple("ca_county", "query18"),
            ),
            (
                ColumnQualifierTuple("cs_coupon_amt", None),
                ColumnQualifierTuple("agg3", "query18"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("agg1", "query18"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("agg4", "query18"),
            ),
            (
                ColumnQualifierTuple("cs_net_profit", None),
                ColumnQualifierTuple("agg5", "query18"),
            ),
            (
                ColumnQualifierTuple("c_birth_year", None),
                ColumnQualifierTuple("agg6", "query18"),
            ),
            (
                ColumnQualifierTuple("cs_list_price", None),
                ColumnQualifierTuple("agg2", "query18"),
            ),
            (
                ColumnQualifierTuple("cd_dep_count", "customer_demographics"),
                ColumnQualifierTuple("agg7", "query18"),
            ),
            (
                ColumnQualifierTuple("ca_country", None),
                ColumnQualifierTuple("ca_country", "query18"),
            ),
            (
                ColumnQualifierTuple("ca_state", None),
                ColumnQualifierTuple("ca_state", "query18"),
            ),
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("i_item_id", "query18"),
            ),
        ],
        {},
    ),
    19: (
        {"customer", "date_dim", "store_sales", "store", "customer_address", "item"},
        {"query19"},
        [
            (
                ColumnQualifierTuple("i_manufact", None),
                ColumnQualifierTuple("i_manufact", "query19"),
            ),
            (
                ColumnQualifierTuple("i_brand", None),
                ColumnQualifierTuple("brand", "query19"),
            ),
            (
                ColumnQualifierTuple("i_brand_id", None),
                ColumnQualifierTuple("brand_id", "query19"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("ext_price", "query19"),
            ),
            (
                ColumnQualifierTuple("i_manufact_id", None),
                ColumnQualifierTuple("i_manufact_id", "query19"),
            ),
        ],
        {},
    ),
    20: (
        {"date_dim", "catalog_sales", "item"},
        {"query20"},
        [
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("i_category", "query20"),
            ),
            (
                ColumnQualifierTuple("i_class", None),
                ColumnQualifierTuple("i_class", "query20"),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", None),
                ColumnQualifierTuple("revenueratio", "query20"),
            ),
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("i_item_id", "query20"),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", None),
                ColumnQualifierTuple("itemrevenue", "query20"),
            ),
            (
                ColumnQualifierTuple("i_class", None),
                ColumnQualifierTuple("revenueratio", "query20"),
            ),
            (
                ColumnQualifierTuple("i_item_desc", None),
                ColumnQualifierTuple("i_item_desc", "query20"),
            ),
            (
                ColumnQualifierTuple("i_current_price", None),
                ColumnQualifierTuple("i_current_price", "query20"),
            ),
        ],
        {},
    ),
    21: (
        {"date_dim", "inventory", "warehouse", "item"},
        {"query21"},
        [
            (
                ColumnQualifierTuple("d_date", None),
                ColumnQualifierTuple("inv_after", "query21"),
            ),
            (
                ColumnQualifierTuple("inv_quantity_on_hand", None),
                ColumnQualifierTuple("inv_after", "query21"),
            ),
            (
                ColumnQualifierTuple("inv_quantity_on_hand", None),
                ColumnQualifierTuple("inv_before", "query21"),
            ),
            (
                ColumnQualifierTuple("d_date", None),
                ColumnQualifierTuple("inv_before", "query21"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_name", None),
                ColumnQualifierTuple("w_warehouse_name", "query21"),
            ),
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("i_item_id", "query21"),
            ),
        ],
        {},
    ),
    22: (
        {"item", "date_dim", "inventory"},
        {"query22"},
        [
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("i_category", "query22"),
            ),
            (
                ColumnQualifierTuple("i_class", None),
                ColumnQualifierTuple("i_class", "query22"),
            ),
            (
                ColumnQualifierTuple("i_product_name", None),
                ColumnQualifierTuple("i_product_name", "query22"),
            ),
            (
                ColumnQualifierTuple("inv_quantity_on_hand", None),
                ColumnQualifierTuple("qoh", "query22"),
            ),
            (
                ColumnQualifierTuple("i_brand", None),
                ColumnQualifierTuple("i_brand", "query22"),
            ),
        ],
        {},
    ),
    23: (
        {"item", "catalog_sales", "store_sales", "web_sales", "date_dim", "customer"},
        {"query23"},
        [
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("sum(sales)", "query23"),
            ),
            (
                ColumnQualifierTuple("ws_list_price", None),
                ColumnQualifierTuple("sum(sales)", "query23"),
            ),
            (
                ColumnQualifierTuple("cs_list_price", None),
                ColumnQualifierTuple("sum(sales)", "query23"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("sum(sales)", "query23"),
            ),
        ],
        {},
    ),
    24: (
        {
            "item",
            "store",
            "store_sales",
            "customer_address",
            "store_returns",
            "customer",
        },
        {"query24"},
        [
            (
                ColumnQualifierTuple("s_store_name", None),
                ColumnQualifierTuple("s_store_name", "query24"),
            ),
            (
                ColumnQualifierTuple("c_first_name", None),
                ColumnQualifierTuple("c_first_name", "query24"),
            ),
            (
                ColumnQualifierTuple("ss_net_paid", None),
                ColumnQualifierTuple("paid", "query24"),
            ),
            (
                ColumnQualifierTuple("c_last_name", None),
                ColumnQualifierTuple("c_last_name", "query24"),
            ),
        ],
        {},
    ),
    25: (
        {"item", "store", "date_dim", "store_sales", "store_returns", "catalog_sales"},
        {"query25"},
        [
            (
                ColumnQualifierTuple("sr_net_loss", None),
                ColumnQualifierTuple("store_returns_loss", "query25"),
            ),
            (
                ColumnQualifierTuple("ss_net_profit", None),
                ColumnQualifierTuple("store_sales_profit", "query25"),
            ),
            (
                ColumnQualifierTuple("s_store_name", None),
                ColumnQualifierTuple("s_store_name", "query25"),
            ),
            (
                ColumnQualifierTuple("i_item_desc", None),
                ColumnQualifierTuple("i_item_desc", "query25"),
            ),
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("i_item_id", "query25"),
            ),
            (
                ColumnQualifierTuple("s_store_id", None),
                ColumnQualifierTuple("s_store_id", "query25"),
            ),
            (
                ColumnQualifierTuple("cs_net_profit", None),
                ColumnQualifierTuple("catalog_sales_profit", "query25"),
            ),
        ],
        {},
    ),
    26: (
        {"customer_demographics", "item", "promotion", "date_dim", "catalog_sales"},
        {"query26"},
        [
            (
                ColumnQualifierTuple("cs_list_price", None),
                ColumnQualifierTuple("agg2", "query26"),
            ),
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("i_item_id", "query26"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("agg1", "query26"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("agg4", "query26"),
            ),
            (
                ColumnQualifierTuple("cs_coupon_amt", None),
                ColumnQualifierTuple("agg3", "query26"),
            ),
        ],
        {},
    ),
    27: (
        {"store", "store_sales", "item", "date_dim", "customer_demographics"},
        {"query27"},
        [
            (
                ColumnQualifierTuple("s_state", None),
                ColumnQualifierTuple("s_state", "query27"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("agg4", "query27"),
            ),
            (
                ColumnQualifierTuple("s_state", None),
                ColumnQualifierTuple("g_state", "query27"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("agg1", "query27"),
            ),
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("i_item_id", "query27"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", None),
                ColumnQualifierTuple("agg2", "query27"),
            ),
            (
                ColumnQualifierTuple("ss_coupon_amt", None),
                ColumnQualifierTuple("agg3", "query27"),
            ),
        ],
        {},
    ),
    28: (
        {"store_sales"},
        {"query28"},
        [
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B1_LP", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B5_LP", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B1_CNTD", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B6_CNT", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B4_CNT", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B3_CNT", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B3_CNTD", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B4_CNTD", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B5_CNT", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B6_CNTD", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B6_LP", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B3_LP", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B1_CNT", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B4_LP", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B2_CNTD", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B5_CNTD", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B2_CNT", "query28"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", "store_sales"),
                ColumnQualifierTuple("B2_LP", "query28"),
            ),
        ],
        {},
    ),
    29: (
        {"store", "store_sales", "item", "date_dim", "store_returns", "catalog_sales"},
        {"query29"},
        [
            (
                ColumnQualifierTuple("s_store_name", None),
                ColumnQualifierTuple("s_store_name", "query29"),
            ),
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("i_item_id", "query29"),
            ),
            (
                ColumnQualifierTuple("s_store_id", None),
                ColumnQualifierTuple("s_store_id", "query29"),
            ),
            (
                ColumnQualifierTuple("sr_return_quantity", None),
                ColumnQualifierTuple("store_returns_quantity", "query29"),
            ),
            (
                ColumnQualifierTuple("i_item_desc", None),
                ColumnQualifierTuple("i_item_desc", "query29"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("store_sales_quantity", "query29"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("catalog_sales_quantity", "query29"),
            ),
        ],
        {},
    ),
    30: (
        {"customer", "web_returns", "customer_address", "date_dim"},
        {"query30"},
        [
            (
                ColumnQualifierTuple("c_birth_month", None),
                ColumnQualifierTuple("c_birth_month", "query30"),
            ),
            (
                ColumnQualifierTuple("c_birth_day", None),
                ColumnQualifierTuple("c_birth_day", "query30"),
            ),
            (
                ColumnQualifierTuple("c_birth_country", None),
                ColumnQualifierTuple("c_birth_country", "query30"),
            ),
            (
                ColumnQualifierTuple("c_birth_year", None),
                ColumnQualifierTuple("c_birth_year", "query30"),
            ),
            (
                ColumnQualifierTuple("c_login", None),
                ColumnQualifierTuple("c_login", "query30"),
            ),
            (
                ColumnQualifierTuple("c_first_name", None),
                ColumnQualifierTuple("c_first_name", "query30"),
            ),
            (
                ColumnQualifierTuple("c_customer_id", None),
                ColumnQualifierTuple("c_customer_id", "query30"),
            ),
            (
                ColumnQualifierTuple("c_salutation", None),
                ColumnQualifierTuple("c_salutation", "query30"),
            ),
            (
                ColumnQualifierTuple("c_preferred_cust_flag", None),
                ColumnQualifierTuple("c_preferred_cust_flag", "query30"),
            ),
            (
                ColumnQualifierTuple("c_email_address", None),
                ColumnQualifierTuple("c_email_address", "query30"),
            ),
            (
                ColumnQualifierTuple("c_last_review_date", None),
                ColumnQualifierTuple("c_last_review_date", "query30"),
            ),
            (
                ColumnQualifierTuple("wr_return_amt", None),
                ColumnQualifierTuple("ctr_total_return", "query30"),
            ),
            (
                ColumnQualifierTuple("c_last_name", None),
                ColumnQualifierTuple("c_last_name", "query30"),
            ),
        ],
        {},
    ),
    31: (
        {"date_dim", "store_sales", "customer_address", "web_sales"},
        {"query31"},
        [
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("store_q2_q3_increase", "query31"),
            ),
            (
                ColumnQualifierTuple("d_year", None),
                ColumnQualifierTuple("d_year", "query31"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("store_q1_q2_increase", "query31"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("web_q1_q2_increase", "query31"),
            ),
            (
                ColumnQualifierTuple("ca_county", None),
                ColumnQualifierTuple("ca_county", "query31"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("web_q2_q3_increase", "query31"),
            ),
        ],
        {},
    ),
    32: (
        {"date_dim", "item", "catalog_sales"},
        {"query32"},
        [
            (
                ColumnQualifierTuple("cs_ext_discount_amt", None),
                ColumnQualifierTuple("excess_discount_amount", "query32"),
            )
        ],
        {},
    ),
    33: (
        {
            "customer_address",
            "web_sales",
            "item",
            "date_dim",
            "store_sales",
            "catalog_sales",
        },
        {"query33"},
        [
            (
                ColumnQualifierTuple("i_manufact_id", "item"),
                ColumnQualifierTuple("i_manufact_id", "query33"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("total_sales", "query33"),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", None),
                ColumnQualifierTuple("total_sales", "query33"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("total_sales", "query33"),
            ),
        ],
        {},
    ),
    34: (
        {"store_sales", "date_dim", "store", "household_demographics", "customer"},
        {"query34"},
        [
            (
                ColumnQualifierTuple("c_first_name", None),
                ColumnQualifierTuple("c_first_name", "query34"),
            ),
            (
                ColumnQualifierTuple("c_salutation", None),
                ColumnQualifierTuple("c_salutation", "query34"),
            ),
            (
                ColumnQualifierTuple("c_preferred_cust_flag", None),
                ColumnQualifierTuple("c_preferred_cust_flag", "query34"),
            ),
            (
                ColumnQualifierTuple("c_last_name", None),
                ColumnQualifierTuple("c_last_name", "query34"),
            ),
            (
                ColumnQualifierTuple("ss_ticket_number", None),
                ColumnQualifierTuple("ss_ticket_number", "query34"),
            ),
            (ColumnQualifierTuple("cnt", None), ColumnQualifierTuple("cnt", "query34")),
        ],
        {},
    ),
    35: (
        {
            "store_sales",
            "customer_address",
            "date_dim",
            "customer_demographics",
            "customer",
        },
        {"query35"},
        [
            (
                ColumnQualifierTuple("cd_dep_employed_count", None),
                ColumnQualifierTuple("min(cd_dep_employed_count)", "query35"),
            ),
            (
                ColumnQualifierTuple("cd_gender", None),
                ColumnQualifierTuple("cd_gender", "query35"),
            ),
            (
                ColumnQualifierTuple("cd_dep_count", None),
                ColumnQualifierTuple("min(cd_dep_count)", "query35"),
            ),
            (
                ColumnQualifierTuple("cd_dep_college_count", None),
                ColumnQualifierTuple("max(cd_dep_college_count)", "query35"),
            ),
            (
                ColumnQualifierTuple("cd_dep_employed_count", None),
                ColumnQualifierTuple("max(cd_dep_employed_count)", "query35"),
            ),
            (
                ColumnQualifierTuple("cd_dep_count", None),
                ColumnQualifierTuple("max(cd_dep_count)", "query35"),
            ),
            (
                ColumnQualifierTuple("cd_dep_college_count", None),
                ColumnQualifierTuple("min(cd_dep_college_count)", "query35"),
            ),
            (
                ColumnQualifierTuple("cd_dep_college_count", None),
                ColumnQualifierTuple("avg(cd_dep_college_count)", "query35"),
            ),
            (
                ColumnQualifierTuple("cd_dep_college_count", None),
                ColumnQualifierTuple("cd_dep_college_count", "query35"),
            ),
            (
                ColumnQualifierTuple("ca_state", None),
                ColumnQualifierTuple("ca_state", "query35"),
            ),
            (
                ColumnQualifierTuple("cd_dep_count", None),
                ColumnQualifierTuple("cd_dep_count", "query35"),
            ),
            (
                ColumnQualifierTuple("cd_dep_count", None),
                ColumnQualifierTuple("avg(cd_dep_count)", "query35"),
            ),
            (
                ColumnQualifierTuple("cd_dep_employed_count", None),
                ColumnQualifierTuple("avg(cd_dep_employed_count)", "query35"),
            ),
            (
                ColumnQualifierTuple("cd_dep_employed_count", None),
                ColumnQualifierTuple("cd_dep_employed_count", "query35"),
            ),
            (
                ColumnQualifierTuple("cd_marital_status", None),
                ColumnQualifierTuple("cd_marital_status", "query35"),
            ),
        ],
        {},
    ),
    36: (
        {"store", "store_sales", "date_dim", "item"},
        {"query36"},
        [
            (
                ColumnQualifierTuple("ss_net_profit", None),
                ColumnQualifierTuple("gross_margin", "query36"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("gross_margin", "query36"),
            ),
            (
                ColumnQualifierTuple("ss_net_profit", None),
                ColumnQualifierTuple("rank_within_parent", "query36"),
            ),
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("rank_within_parent", "query36"),
            ),
            (
                ColumnQualifierTuple("i_class", None),
                ColumnQualifierTuple("lochierarchy", "query36"),
            ),
            (
                ColumnQualifierTuple("i_class", None),
                ColumnQualifierTuple("rank_within_parent", "query36"),
            ),
            (
                ColumnQualifierTuple("i_class", None),
                ColumnQualifierTuple("i_class", "query36"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("rank_within_parent", "query36"),
            ),
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("lochierarchy", "query36"),
            ),
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("i_category", "query36"),
            ),
        ],
        {},
    ),
    37: (
        {"catalog_sales", "date_dim", "item", "inventory"},
        {"query37"},
        [
            (
                ColumnQualifierTuple("i_current_price", None),
                ColumnQualifierTuple("i_current_price", "query37"),
            ),
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("i_item_id", "query37"),
            ),
            (
                ColumnQualifierTuple("i_item_desc", None),
                ColumnQualifierTuple("i_item_desc", "query37"),
            ),
        ],
        {},
    ),
    38: (
        {"customer", "store_sales", "date_dim"},
        {"query38"},
        [],
        {},
    ),
    39: (
        {"warehouse", "date_dim", "item", "inventory"},
        {"query39_1", "query39_2"},
        [
            (
                ColumnQualifierTuple("i_item_sk", None),
                ColumnQualifierTuple("i_item_sk_2", "query39_1"),
            ),
            (
                ColumnQualifierTuple("inv_quantity_on_hand", None),
                ColumnQualifierTuple("cov_2", "query39_2"),
            ),
            (
                ColumnQualifierTuple("i_item_sk", None),
                ColumnQualifierTuple("i_item_sk", "query39_2"),
            ),
            (
                ColumnQualifierTuple("inv_quantity_on_hand", None),
                ColumnQualifierTuple("mean_2", "query39_2"),
            ),
            (
                ColumnQualifierTuple("i_item_sk", None),
                ColumnQualifierTuple("i_item_sk", "query39_1"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sk", None),
                ColumnQualifierTuple("w_warehouse_sk", "query39_1"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("d_moy", "query39_2"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("d_moy_2", "query39_2"),
            ),
            (
                ColumnQualifierTuple("inv_quantity_on_hand", None),
                ColumnQualifierTuple("mean_2", "query39_1"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("d_moy", "query39_1"),
            ),
            (
                ColumnQualifierTuple("inv_quantity_on_hand", None),
                ColumnQualifierTuple("cov_2", "query39_1"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("d_moy_2", "query39_1"),
            ),
            (
                ColumnQualifierTuple("i_item_sk", None),
                ColumnQualifierTuple("i_item_sk_2", "query39_2"),
            ),
            (
                ColumnQualifierTuple("inv_quantity_on_hand", None),
                ColumnQualifierTuple("cov", "query39_2"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sk", None),
                ColumnQualifierTuple("w_warehouse_sk_2", "query39_2"),
            ),
            (
                ColumnQualifierTuple("inv_quantity_on_hand", None),
                ColumnQualifierTuple("cov", "query39_1"),
            ),
            (
                ColumnQualifierTuple("inv_quantity_on_hand", None),
                ColumnQualifierTuple("mean", "query39_2"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sk", None),
                ColumnQualifierTuple("w_warehouse_sk_2", "query39_1"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sk", None),
                ColumnQualifierTuple("w_warehouse_sk", "query39_2"),
            ),
            (
                ColumnQualifierTuple("inv_quantity_on_hand", None),
                ColumnQualifierTuple("mean", "query39_1"),
            ),
        ],
        {},
    ),
    40: (
        {"catalog_sales", "catalog_returns"},
        {"query40"},
        [
            (
                ColumnQualifierTuple("d_date", None),
                ColumnQualifierTuple("sales_before", "query40"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("sales_after", "query40"),
            ),
            (
                ColumnQualifierTuple("d_date", None),
                ColumnQualifierTuple("sales_after", "query40"),
            ),
            (
                ColumnQualifierTuple("cr_refunded_cash", None),
                ColumnQualifierTuple("sales_before", "query40"),
            ),
            (
                ColumnQualifierTuple("cr_refunded_cash", None),
                ColumnQualifierTuple("sales_after", "query40"),
            ),
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("i_item_id", "query40"),
            ),
            (
                ColumnQualifierTuple("w_state", None),
                ColumnQualifierTuple("w_state", "query40"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("sales_before", "query40"),
            ),
        ],
        {},
    ),
    41: (
        {"item"},
        {"query41"},
        [
            (
                ColumnQualifierTuple("i_product_name", "item"),
                ColumnQualifierTuple("distinct(i_product_name)", "query41"),
            )
        ],
        {},
    ),
    42: (
        {"store_sales", "date_dim", "item"},
        {"query42"},
        [
            (
                ColumnQualifierTuple("d_year", "date_dim"),
                ColumnQualifierTuple("d_year", "query42"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("sum(ss_ext_sales_price)", "query42"),
            ),
            (
                ColumnQualifierTuple("i_category_id", "item"),
                ColumnQualifierTuple("i_category_id", "query42"),
            ),
            (
                ColumnQualifierTuple("i_category", "item"),
                ColumnQualifierTuple("i_category", "query42"),
            ),
        ],
        {},
    ),
    43: (
        {"store_sales", "date_dim", "store"},
        {"query43"},
        [
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("tue_sales", "query43"),
            ),
            (
                ColumnQualifierTuple("d_day_name", None),
                ColumnQualifierTuple("sat_sales", "query43"),
            ),
            (
                ColumnQualifierTuple("d_day_name", None),
                ColumnQualifierTuple("wed_sales", "query43"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("fri_sales", "query43"),
            ),
            (
                ColumnQualifierTuple("d_day_name", None),
                ColumnQualifierTuple("mon_sales", "query43"),
            ),
            (
                ColumnQualifierTuple("s_store_name", None),
                ColumnQualifierTuple("s_store_name", "query43"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("thu_sales", "query43"),
            ),
            (
                ColumnQualifierTuple("d_day_name", None),
                ColumnQualifierTuple("tue_sales", "query43"),
            ),
            (
                ColumnQualifierTuple("s_store_id", None),
                ColumnQualifierTuple("s_store_id", "query43"),
            ),
            (
                ColumnQualifierTuple("d_day_name", None),
                ColumnQualifierTuple("fri_sales", "query43"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("sun_sales", "query43"),
            ),
            (
                ColumnQualifierTuple("d_day_name", None),
                ColumnQualifierTuple("thu_sales", "query43"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("mon_sales", "query43"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("sat_sales", "query43"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("wed_sales", "query43"),
            ),
            (
                ColumnQualifierTuple("d_day_name", None),
                ColumnQualifierTuple("sun_sales", "query43"),
            ),
        ],
        {},
    ),
    44: (
        {"store_sales", "item"},
        {"query44"},
        [
            (
                ColumnQualifierTuple("i_product_name", "item"),
                ColumnQualifierTuple("worst_performing", "query44"),
            ),
            (
                ColumnQualifierTuple("i_product_name", "item"),
                ColumnQualifierTuple("best_performing", "query44"),
            ),
            (
                ColumnQualifierTuple("ss_net_profit", "store_sales"),
                ColumnQualifierTuple("rnk", "query44"),
            ),
        ],
        {},
    ),
    45: (
        {"customer_address", "item", "date_dim", "customer", "web_sales"},
        {"query45"},
        [
            (
                ColumnQualifierTuple("ca_zip", None),
                ColumnQualifierTuple("ca_zip", "query45"),
            ),
            (
                ColumnQualifierTuple("ws_sales_price", None),
                ColumnQualifierTuple("sum(ws_sales_price)", "query45"),
            ),
            (
                ColumnQualifierTuple("ca_city", None),
                ColumnQualifierTuple("ca_city", "query45"),
            ),
        ],
        {},
    ),
    46: (
        {
            "store_sales",
            "customer_address",
            "date_dim",
            "store",
            "household_demographics",
            "customer",
        },
        {"query46"},
        [
            (
                ColumnQualifierTuple("ca_city", None),
                ColumnQualifierTuple("ca_city", "query46"),
            ),
            (
                ColumnQualifierTuple("c_last_name", None),
                ColumnQualifierTuple("c_last_name", "query46"),
            ),
            (
                ColumnQualifierTuple("ca_city", None),
                ColumnQualifierTuple("bought_city", "query46"),
            ),
            (
                ColumnQualifierTuple("ss_net_profit", None),
                ColumnQualifierTuple("profit", "query46"),
            ),
            (
                ColumnQualifierTuple("ss_coupon_amt", None),
                ColumnQualifierTuple("amt", "query46"),
            ),
            (
                ColumnQualifierTuple("c_first_name", None),
                ColumnQualifierTuple("c_first_name", "query46"),
            ),
            (
                ColumnQualifierTuple("ss_ticket_number", None),
                ColumnQualifierTuple("ss_ticket_number", "query46"),
            ),
        ],
        {},
    ),
    47: (
        {"store", "item", "store_sales", "date_dim"},
        {"query47"},
        [
            (
                ColumnQualifierTuple("i_brand", None),
                ColumnQualifierTuple("avg_monthly_sales", "query47"),
            ),
            (
                ColumnQualifierTuple("s_store_name", None),
                ColumnQualifierTuple("avg_monthly_sales", "query47"),
            ),
            (
                ColumnQualifierTuple("s_company_name", None),
                ColumnQualifierTuple("avg_monthly_sales", "query47"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("nsum", "query47"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("avg_monthly_sales", "query47"),
            ),
            (
                ColumnQualifierTuple("s_store_name", None),
                ColumnQualifierTuple("s_store_name", "query47"),
            ),
            (
                ColumnQualifierTuple("d_year", None),
                ColumnQualifierTuple("d_year", "query47"),
            ),
            (
                ColumnQualifierTuple("d_year", None),
                ColumnQualifierTuple("avg_monthly_sales", "query47"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("d_moy", "query47"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("sum_sales", "query47"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("psum", "query47"),
            ),
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("avg_monthly_sales", "query47"),
            ),
            (
                ColumnQualifierTuple("i_brand", None),
                ColumnQualifierTuple("i_brand", "query47"),
            ),
            (
                ColumnQualifierTuple("s_company_name", None),
                ColumnQualifierTuple("s_company_name", "query47"),
            ),
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("i_category", "query47"),
            ),
        ],
        {},
    ),
    48: (
        {
            "store_sales",
            "customer_address",
            "date_dim",
            "store",
            "customer_demographics",
        },
        {"query48"},
        [
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("sum(ss_quantity)", "query48"),
            )
        ],
        {},
    ),
    49: (
        {
            "store_sales",
            "catalog_returns",
            "catalog_sales",
            "web_returns",
            "store_returns",
            "web_sales",
        },
        {"query49"},
        [
            (
                ColumnQualifierTuple("sr_return_quantity", "store_returns"),
                ColumnQualifierTuple("return_rank", "query49"),
            ),
            (
                ColumnQualifierTuple("ws_net_paid", "web_sales"),
                ColumnQualifierTuple("currency_rank", "query49"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", "web_sales"),
                ColumnQualifierTuple("return_rank", "query49"),
            ),
            (
                ColumnQualifierTuple("sr_return_amt", "store_returns"),
                ColumnQualifierTuple("currency_rank", "query49"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", "catalog_sales"),
                ColumnQualifierTuple("return_ratio", "query49"),
            ),
            (
                ColumnQualifierTuple("ws_item_sk", "web_sales"),
                ColumnQualifierTuple("item", "query49"),
            ),
            (
                ColumnQualifierTuple("wr_return_amt", "web_returns"),
                ColumnQualifierTuple("currency_rank", "query49"),
            ),
            (
                ColumnQualifierTuple("cs_item_sk", "catalog_sales"),
                ColumnQualifierTuple("item", "query49"),
            ),
            (
                ColumnQualifierTuple("sr_return_quantity", "store_returns"),
                ColumnQualifierTuple("return_ratio", "query49"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", "store_sales"),
                ColumnQualifierTuple("return_ratio", "query49"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", "catalog_sales"),
                ColumnQualifierTuple("return_rank", "query49"),
            ),
            (
                ColumnQualifierTuple("wr_return_quantity", "web_returns"),
                ColumnQualifierTuple("return_ratio", "query49"),
            ),
            (
                ColumnQualifierTuple("ss_net_paid", "store_sales"),
                ColumnQualifierTuple("currency_rank", "query49"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", "web_sales"),
                ColumnQualifierTuple("return_ratio", "query49"),
            ),
            (
                ColumnQualifierTuple("ss_item_sk", "store_sales"),
                ColumnQualifierTuple("item", "query49"),
            ),
            (
                ColumnQualifierTuple("cs_net_paid", "catalog_sales"),
                ColumnQualifierTuple("currency_rank", "query49"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", "store_sales"),
                ColumnQualifierTuple("return_rank", "query49"),
            ),
            (
                ColumnQualifierTuple("wr_return_quantity", "web_returns"),
                ColumnQualifierTuple("return_rank", "query49"),
            ),
            (
                ColumnQualifierTuple("cr_return_quantity", "catalog_returns"),
                ColumnQualifierTuple("return_rank", "query49"),
            ),
            (
                ColumnQualifierTuple("cr_return_amount", "catalog_returns"),
                ColumnQualifierTuple("currency_rank", "query49"),
            ),
            (
                ColumnQualifierTuple("cr_return_quantity", "catalog_returns"),
                ColumnQualifierTuple("return_ratio", "query49"),
            ),
        ],
        {},
    ),
    50: (
        {"store_returns", "store_sales", "date_dim", "store"},
        {"query50"},
        [
            (
                ColumnQualifierTuple("s_store_name", None),
                ColumnQualifierTuple("s_store_name", "query50"),
            ),
            (
                ColumnQualifierTuple("ss_sold_date_sk", None),
                ColumnQualifierTuple("0_days", "query50"),
            ),
            (
                ColumnQualifierTuple("sr_returned_date_sk", None),
                ColumnQualifierTuple("1_90_days", "query50"),
            ),
            (
                ColumnQualifierTuple("ss_sold_date_sk", None),
                ColumnQualifierTuple("1_120_days", "query50"),
            ),
            (
                ColumnQualifierTuple("s_street_name", None),
                ColumnQualifierTuple("s_street_name", "query50"),
            ),
            (
                ColumnQualifierTuple("s_suite_number", None),
                ColumnQualifierTuple("s_suite_number", "query50"),
            ),
            (
                ColumnQualifierTuple("sr_returned_date_sk", None),
                ColumnQualifierTuple("0_days", "query50"),
            ),
            (
                ColumnQualifierTuple("s_street_type", None),
                ColumnQualifierTuple("s_street_type", "query50"),
            ),
            (
                ColumnQualifierTuple("ss_sold_date_sk", None),
                ColumnQualifierTuple("1_60_days", "query50"),
            ),
            (
                ColumnQualifierTuple("ss_sold_date_sk", None),
                ColumnQualifierTuple("above120_days", "query50"),
            ),
            (
                ColumnQualifierTuple("s_zip", None),
                ColumnQualifierTuple("s_zip", "query50"),
            ),
            (
                ColumnQualifierTuple("s_street_number", None),
                ColumnQualifierTuple("s_street_number", "query50"),
            ),
            (
                ColumnQualifierTuple("s_state", None),
                ColumnQualifierTuple("s_state", "query50"),
            ),
            (
                ColumnQualifierTuple("sr_returned_date_sk", None),
                ColumnQualifierTuple("1_120_days", "query50"),
            ),
            (
                ColumnQualifierTuple("s_county", None),
                ColumnQualifierTuple("s_county", "query50"),
            ),
            (
                ColumnQualifierTuple("s_company_id", None),
                ColumnQualifierTuple("s_company_id", "query50"),
            ),
            (
                ColumnQualifierTuple("s_city", None),
                ColumnQualifierTuple("s_city", "query50"),
            ),
            (
                ColumnQualifierTuple("sr_returned_date_sk", None),
                ColumnQualifierTuple("1_60_days", "query50"),
            ),
            (
                ColumnQualifierTuple("sr_returned_date_sk", None),
                ColumnQualifierTuple("above120_days", "query50"),
            ),
            (
                ColumnQualifierTuple("ss_sold_date_sk", None),
                ColumnQualifierTuple("1_90_days", "query50"),
            ),
        ],
        {},
    ),
    51: (
        {"web_sales", "store_sales", "date_dim"},
        {"query51"},
        [
            (
                ColumnQualifierTuple("preceding", None),
                ColumnQualifierTuple("store_sales", "query51"),
            ),
            (
                ColumnQualifierTuple("preceding", None),
                ColumnQualifierTuple("web_sales", "query51"),
            ),
            (
                ColumnQualifierTuple("ws_item_sk", None),
                ColumnQualifierTuple("item_sk", "query51"),
            ),
            (
                ColumnQualifierTuple("ws_item_sk", None),
                ColumnQualifierTuple("store_cumulative", "query51"),
            ),
            (
                ColumnQualifierTuple("ws_sales_price", None),
                ColumnQualifierTuple("web_cumulative", "query51"),
            ),
            (
                ColumnQualifierTuple("ss_item_sk", None),
                ColumnQualifierTuple("web_cumulative", "query51"),
            ),
            (
                ColumnQualifierTuple("ws_sales_price", None),
                ColumnQualifierTuple("web_sales", "query51"),
            ),
            (
                ColumnQualifierTuple("d_date", None),
                ColumnQualifierTuple("web_cumulative", "query51"),
            ),
            (
                ColumnQualifierTuple("preceding", None),
                ColumnQualifierTuple("store_cumulative", "query51"),
            ),
            (
                ColumnQualifierTuple("ss_item_sk", None),
                ColumnQualifierTuple("store_sales", "query51"),
            ),
            (
                ColumnQualifierTuple("d_date", None),
                ColumnQualifierTuple("web_sales", "query51"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("store_sales", "query51"),
            ),
            (
                ColumnQualifierTuple("d_date", None),
                ColumnQualifierTuple("store_sales", "query51"),
            ),
            (
                ColumnQualifierTuple("ss_item_sk", None),
                ColumnQualifierTuple("item_sk", "query51"),
            ),
            (
                ColumnQualifierTuple("ss_item_sk", None),
                ColumnQualifierTuple("store_cumulative", "query51"),
            ),
            (
                ColumnQualifierTuple("d_date", None),
                ColumnQualifierTuple("store_cumulative", "query51"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("store_cumulative", "query51"),
            ),
            (
                ColumnQualifierTuple("ws_item_sk", None),
                ColumnQualifierTuple("web_cumulative", "query51"),
            ),
            (
                ColumnQualifierTuple("ws_item_sk", None),
                ColumnQualifierTuple("web_sales", "query51"),
            ),
            (
                ColumnQualifierTuple("preceding", None),
                ColumnQualifierTuple("web_cumulative", "query51"),
            ),
            (
                ColumnQualifierTuple("d_date", None),
                ColumnQualifierTuple("d_date", "query51"),
            ),
        ],
        {},
    ),
    52: (
        {"date_dim", "item", "store_sales"},
        {"query52"},
        [
            (
                ColumnQualifierTuple("i_brand", "item"),
                ColumnQualifierTuple("brand", "query52"),
            ),
            (
                ColumnQualifierTuple("i_brand_id", "item"),
                ColumnQualifierTuple("brand_id", "query52"),
            ),
            (
                ColumnQualifierTuple("d_year", "date_dim"),
                ColumnQualifierTuple("d_year", "query52"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("ext_price", "query52"),
            ),
        ],
        {},
    ),
    53: (
        {"store", "item", "store_sales", "date_dim"},
        {"query53"},
        [
            (
                ColumnQualifierTuple("i_manufact_id", None),
                ColumnQualifierTuple("avg_quarterly_sales", "query53"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("sum_sales", "query53"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("avg_quarterly_sales", "query53"),
            ),
            (
                ColumnQualifierTuple("i_manufact_id", None),
                ColumnQualifierTuple("i_manufact_id", "query53"),
            ),
        ],
        {},
    ),
    54: (
        {
            "customer_address",
            "web_sales",
            "item",
            "store",
            "customer",
            "date_dim",
            "store_sales",
            "catalog_sales",
        },
        {"query54"},
        [],
        {},
    ),
    55: (
        {"item", "store_sales", "date_dim"},
        {"query55"},
        [
            (
                ColumnQualifierTuple("i_brand_id", None),
                ColumnQualifierTuple("brand_id", "query55"),
            ),
            (
                ColumnQualifierTuple("i_brand", None),
                ColumnQualifierTuple("brand", "query55"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("ext_price", "query55"),
            ),
        ],
        {},
    ),
    56: (
        {
            "customer_address",
            "web_sales",
            "item",
            "date_dim",
            "store_sales",
            "catalog_sales",
        },
        {"query56"},
        [
            (
                ColumnQualifierTuple("i_item_id", "item"),
                ColumnQualifierTuple("i_item_id", "query56"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("total_sales", "query56"),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", None),
                ColumnQualifierTuple("total_sales", "query56"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("total_sales", "query56"),
            ),
        ],
        {},
    ),
    57: (
        {"call_center", "catalog_sales", "item", "date_dim"},
        {"query57"},
        [
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("d_moy", "query57"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("sum_sales", "query57"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("psum", "query57"),
            ),
            (
                ColumnQualifierTuple("d_year", None),
                ColumnQualifierTuple("avg_monthly_sales", "query57"),
            ),
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("avg_monthly_sales", "query57"),
            ),
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("i_category", "query57"),
            ),
            (
                ColumnQualifierTuple("cc_name", None),
                ColumnQualifierTuple("avg_monthly_sales", "query57"),
            ),
            (
                ColumnQualifierTuple("cc_name", None),
                ColumnQualifierTuple("cc_name", "query57"),
            ),
            (
                ColumnQualifierTuple("d_year", None),
                ColumnQualifierTuple("d_year", "query57"),
            ),
            (
                ColumnQualifierTuple("i_brand", None),
                ColumnQualifierTuple("avg_monthly_sales", "query57"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("nsum", "query57"),
            ),
            (
                ColumnQualifierTuple("i_brand", None),
                ColumnQualifierTuple("i_brand", "query57"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("avg_monthly_sales", "query57"),
            ),
        ],
        {},
    ),
    58: (
        {"catalog_sales", "item", "store_sales", "date_dim", "web_sales"},
        {"query58"},
        [
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("ws_dev", "query58"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("ss_dev", "query58"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("ss_item_rev", "query58"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("cs_dev", "query58"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("average", "query58"),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", None),
                ColumnQualifierTuple("cs_item_rev", "query58"),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", None),
                ColumnQualifierTuple("cs_dev", "query58"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("ws_dev", "query58"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("ws_item_rev", "query58"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("ss_dev", "query58"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("average", "query58"),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", None),
                ColumnQualifierTuple("ws_dev", "query58"),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", None),
                ColumnQualifierTuple("ss_dev", "query58"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("cs_dev", "query58"),
            ),
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("item_id", "query58"),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", None),
                ColumnQualifierTuple("average", "query58"),
            ),
        ],
        {},
    ),
    59: (
        {"date_dim", "store_sales", "store"},
        {"query59"},
        [
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("mon_sales1 / mon_sales2", "query59"),
            ),
            (
                ColumnQualifierTuple("s_store_name", None),
                ColumnQualifierTuple("s_store_name1", "query59"),
            ),
            (
                ColumnQualifierTuple("d_day_name", None),
                ColumnQualifierTuple("thu_sales1 / thu_sales2", "query59"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("fri_sales1 / fri_sales2", "query59"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("sun_sales1 / sun_sales2", "query59"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("sat_sales1 / sat_sales2", "query59"),
            ),
            (
                ColumnQualifierTuple("d_day_name", None),
                ColumnQualifierTuple("mon_sales1 / mon_sales2", "query59"),
            ),
            (
                ColumnQualifierTuple("d_day_name", None),
                ColumnQualifierTuple("wed_sales1 / wed_sales2", "query59"),
            ),
            (
                ColumnQualifierTuple("d_day_name", None),
                ColumnQualifierTuple("fri_sales1 / fri_sales2", "query59"),
            ),
            (
                ColumnQualifierTuple("s_store_id", None),
                ColumnQualifierTuple("s_store_id1", "query59"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("tue_sales1 / tue_sales2", "query59"),
            ),
            (
                ColumnQualifierTuple("d_day_name", None),
                ColumnQualifierTuple("sun_sales1 / sun_sales2", "query59"),
            ),
            (
                ColumnQualifierTuple("d_day_name", None),
                ColumnQualifierTuple("sat_sales1 / sat_sales2", "query59"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("wed_sales1 / wed_sales2", "query59"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("thu_sales1 / thu_sales2", "query59"),
            ),
            (
                ColumnQualifierTuple("d_day_name", None),
                ColumnQualifierTuple("tue_sales1 / tue_sales2", "query59"),
            ),
            (
                ColumnQualifierTuple("d_week_seq", None),
                ColumnQualifierTuple("d_week_seq1", "query59"),
            ),
        ],
        {},
    ),
    60: (
        {
            "customer_address",
            "web_sales",
            "item",
            "date_dim",
            "store_sales",
            "catalog_sales",
        },
        {"query60"},
        [
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("total_sales", "query60"),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", None),
                ColumnQualifierTuple("total_sales", "query60"),
            ),
            (
                ColumnQualifierTuple("i_item_id", "item"),
                ColumnQualifierTuple("i_item_id", "query60"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("total_sales", "query60"),
            ),
        ],
        {},
    ),
    61: (
        {
            "customer_address",
            "store_sales",
            "date_dim",
            "store",
            "customer",
            "item",
            "promotion",
        },
        {"query61"},
        [
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple(
                    "cast(promotions as decimal(15, 4)) / cast(total as decimal(15, 4)) * 100",
                    "query61",
                ),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("promotions", "query61"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("total", "query61"),
            ),
        ],
        {},
    ),
    62: (
        {"date_dim", "ship_mode", "warehouse", "web_site", "web_sales"},
        {"query62"},
        [
            (
                ColumnQualifierTuple("web_name", None),
                ColumnQualifierTuple("web_name", "query62"),
            ),
            (
                ColumnQualifierTuple("sm_type", None),
                ColumnQualifierTuple("sm_type", "query62"),
            ),
            (
                ColumnQualifierTuple("ws_ship_date_sk", None),
                ColumnQualifierTuple("1_90_days", "query62"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_name", None),
                ColumnQualifierTuple("substr(w_warehouse_name, 1, 20)", "query62"),
            ),
            (
                ColumnQualifierTuple("ws_sold_date_sk", None),
                ColumnQualifierTuple("0_days", "query62"),
            ),
            (
                ColumnQualifierTuple("ws_sold_date_sk", None),
                ColumnQualifierTuple("above120_days", "query62"),
            ),
            (
                ColumnQualifierTuple("ws_sold_date_sk", None),
                ColumnQualifierTuple("1_60_days", "query62"),
            ),
            (
                ColumnQualifierTuple("ws_sold_date_sk", None),
                ColumnQualifierTuple("1_120_days", "query62"),
            ),
            (
                ColumnQualifierTuple("ws_sold_date_sk", None),
                ColumnQualifierTuple("1_90_days", "query62"),
            ),
            (
                ColumnQualifierTuple("ws_ship_date_sk", None),
                ColumnQualifierTuple("0_days", "query62"),
            ),
            (
                ColumnQualifierTuple("ws_ship_date_sk", None),
                ColumnQualifierTuple("above120_days", "query62"),
            ),
            (
                ColumnQualifierTuple("ws_ship_date_sk", None),
                ColumnQualifierTuple("1_60_days", "query62"),
            ),
            (
                ColumnQualifierTuple("ws_ship_date_sk", None),
                ColumnQualifierTuple("1_120_days", "query62"),
            ),
        ],
        {},
    ),
    63: (
        {"store", "item", "store_sales", "date_dim"},
        {"query63"},
        [
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("avg_monthly_sales", "query63"),
            ),
            (
                ColumnQualifierTuple("i_manager_id", None),
                ColumnQualifierTuple("i_manager_id", "query63"),
            ),
            (
                ColumnQualifierTuple("i_manager_id", None),
                ColumnQualifierTuple("avg_monthly_sales", "query63"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("sum_sales", "query63"),
            ),
        ],
        {},
    ),
    64: (
        {
            "household_demographics",
            "customer_demographics",
            "customer_address",
            "income_band",
            "store_sales",
            "date_dim",
            "catalog_returns",
            "store",
            "store_returns",
            "catalog_sales",
            "customer",
            "item",
            "promotion",
        },
        {"query64"},
        [
            (
                ColumnQualifierTuple("i_product_name", None),
                ColumnQualifierTuple("product_name", "query64"),
            ),
            (
                ColumnQualifierTuple("ca_street_number", "customer_address"),
                ColumnQualifierTuple("c_street_number", "query64"),
            ),
            (
                ColumnQualifierTuple("s_store_name", None),
                ColumnQualifierTuple("store_name", "query64"),
            ),
            (
                ColumnQualifierTuple("s_zip", None),
                ColumnQualifierTuple("store_zip", "query64"),
            ),
            (
                ColumnQualifierTuple("ca_street_name", "customer_address"),
                ColumnQualifierTuple("c_street_name", "query64"),
            ),
            (
                ColumnQualifierTuple("ss_coupon_amt", None),
                ColumnQualifierTuple("s31", "query64"),
            ),
            (
                ColumnQualifierTuple("ca_street_name", "customer_address"),
                ColumnQualifierTuple("b_street_name", "query64"),
            ),
            (
                ColumnQualifierTuple("ss_wholesale_cost", None),
                ColumnQualifierTuple("s12", "query64"),
            ),
            (
                ColumnQualifierTuple("ca_city", "customer_address"),
                ColumnQualifierTuple("b_city", "query64"),
            ),
            (
                ColumnQualifierTuple("ca_city", "customer_address"),
                ColumnQualifierTuple("c_city", "query64"),
            ),
            (
                ColumnQualifierTuple("ca_zip", "customer_address"),
                ColumnQualifierTuple("c_zip", "query64"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", None),
                ColumnQualifierTuple("s22", "query64"),
            ),
            (
                ColumnQualifierTuple("ca_zip", "customer_address"),
                ColumnQualifierTuple("b_zip", "query64"),
            ),
            (
                ColumnQualifierTuple("ca_street_number", "customer_address"),
                ColumnQualifierTuple("b_street_number", "query64"),
            ),
            (
                ColumnQualifierTuple("ss_list_price", None),
                ColumnQualifierTuple("s21", "query64"),
            ),
            (
                ColumnQualifierTuple("ss_wholesale_cost", None),
                ColumnQualifierTuple("s11", "query64"),
            ),
            (
                ColumnQualifierTuple("d_year", "date_dim"),
                ColumnQualifierTuple("syear", "query64"),
            ),
            (
                ColumnQualifierTuple("ss_coupon_amt", None),
                ColumnQualifierTuple("s32", "query64"),
            ),
            (
                ColumnQualifierTuple("d_year", "date_dim"),
                ColumnQualifierTuple("syear_2", "query64"),
            ),
        ],
        {},
    ),
    65: (
        {"item", "store_sales", "date_dim", "store"},
        {"query65"},
        [
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("revenue", "query65"),
            ),
            (
                ColumnQualifierTuple("i_wholesale_cost", None),
                ColumnQualifierTuple("i_wholesale_cost", "query65"),
            ),
            (
                ColumnQualifierTuple("s_store_name", None),
                ColumnQualifierTuple("s_store_name", "query65"),
            ),
            (
                ColumnQualifierTuple("i_item_desc", None),
                ColumnQualifierTuple("i_item_desc", "query65"),
            ),
            (
                ColumnQualifierTuple("i_current_price", None),
                ColumnQualifierTuple("i_current_price", "query65"),
            ),
            (
                ColumnQualifierTuple("i_brand", None),
                ColumnQualifierTuple("i_brand", "query65"),
            ),
        ],
        {},
    ),
    66: (
        {
            "date_dim",
            "ship_mode",
            "warehouse",
            "catalog_sales",
            "time_dim",
            "web_sales",
        },
        {"query66"},
        [
            (
                ColumnQualifierTuple("w_warehouse_sq_ft", None),
                ColumnQualifierTuple("sep_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_net_paid_inc_tax", None),
                ColumnQualifierTuple("feb_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_net_paid_inc_tax", None),
                ColumnQualifierTuple("jan_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("sep_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_net_paid_inc_tax", None),
                ColumnQualifierTuple("sep_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("jul_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("nov_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("oct_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("mar_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("mar_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("aug_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("dec_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("dec_net", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("feb_net", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("jan_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("dec_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("apr_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("oct_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("nov_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("feb_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_net_paid_inc_tax", None),
                ColumnQualifierTuple("jun_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_net_paid_inc_tax", None),
                ColumnQualifierTuple("oct_net", "query66"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sq_ft", None),
                ColumnQualifierTuple("jan_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("sep_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("jan_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("jun_net", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("oct_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("mar_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("dec_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("jan_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_net_paid_inc_tax", None),
                ColumnQualifierTuple("may_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("aug_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("jul_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("apr_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("may_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("may_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("jan_net", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("sep_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("jul_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("oct_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("sep_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_net_paid_inc_tax", None),
                ColumnQualifierTuple("aug_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("feb_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("apr_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("feb_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_net_paid_inc_tax", None),
                ColumnQualifierTuple("jul_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("nov_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("aug_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("aug_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("apr_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("mar_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("may_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_net_paid", None),
                ColumnQualifierTuple("may_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_net_paid", None),
                ColumnQualifierTuple("dec_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("may_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("jul_net", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("jan_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_net_paid", None),
                ColumnQualifierTuple("apr_net", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("jan_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("aug_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("may_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("jun_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sq_ft", None),
                ColumnQualifierTuple("jun_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("sep_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("feb_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("nov_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("jun_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("sep_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("jul_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("oct_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("mar_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("apr_net", "query66"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sq_ft", None),
                ColumnQualifierTuple("nov_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_net_paid_inc_tax", None),
                ColumnQualifierTuple("mar_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("may_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("nov_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_net_paid", None),
                ColumnQualifierTuple("jul_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("apr_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sq_ft", None),
                ColumnQualifierTuple("dec_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sq_ft", None),
                ColumnQualifierTuple("oct_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("mar_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("dec_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("oct_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sq_ft", None),
                ColumnQualifierTuple("mar_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("aug_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sq_ft", None),
                ColumnQualifierTuple("feb_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_net_paid", None),
                ColumnQualifierTuple("feb_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_net_paid", None),
                ColumnQualifierTuple("jan_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("dec_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("feb_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("jul_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_net_paid", None),
                ColumnQualifierTuple("sep_net", "query66"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sq_ft", None),
                ColumnQualifierTuple("w_warehouse_sq_ft", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("jan_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("apr_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("feb_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("dec_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("mar_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("sep_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_net_paid", None),
                ColumnQualifierTuple("jun_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_net_paid", None),
                ColumnQualifierTuple("oct_net", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("jun_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("jun_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("jun_net", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("nov_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("oct_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("sep_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_net_paid_inc_tax", None),
                ColumnQualifierTuple("nov_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("feb_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("jan_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("jul_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("dec_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("jul_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("oct_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("may_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("w_city", None),
                ColumnQualifierTuple("w_city", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("may_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("aug_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("nov_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("apr_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("feb_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_net_paid", None),
                ColumnQualifierTuple("aug_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("sep_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("jul_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("oct_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("jun_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("oct_net", "query66"),
            ),
            (
                ColumnQualifierTuple("w_country", None),
                ColumnQualifierTuple("w_country", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("jun_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("dec_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("mar_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("apr_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("jun_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("jul_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("aug_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("feb_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("nov_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("may_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("nov_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("mar_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("may_net", "query66"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sq_ft", None),
                ColumnQualifierTuple("may_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("may_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("jan_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("sep_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("jul_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("oct_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("sep_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("w_county", None),
                ColumnQualifierTuple("w_county", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("jan_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("jan_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sq_ft", None),
                ColumnQualifierTuple("aug_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("w_state", None),
                ColumnQualifierTuple("w_state", "query66"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_name", None),
                ColumnQualifierTuple("w_warehouse_name", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("aug_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("apr_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_net_paid", None),
                ColumnQualifierTuple("mar_net", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("aug_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("aug_net", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("apr_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sq_ft", None),
                ColumnQualifierTuple("jul_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("dec_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("jul_net", "query66"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_sq_ft", None),
                ColumnQualifierTuple("apr_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("jan_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("mar_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("jan_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("sep_net", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("feb_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("nov_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("mar_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("sep_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("may_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_net_paid_inc_tax", None),
                ColumnQualifierTuple("dec_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("aug_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("mar_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("apr_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("jun_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("aug_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_net_paid_inc_tax", None),
                ColumnQualifierTuple("apr_net", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("dec_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("jun_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_net_paid", None),
                ColumnQualifierTuple("nov_net", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("nov_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("apr_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("dec_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("dec_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("nov_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("oct_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("oct_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("jul_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("nov_net", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("mar_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("jun_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("feb_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("may_sales", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("feb_sales_per_sq_foot", "query66"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("jun_sales_per_sq_foot", "query66"),
            ),
        ],
        {},
    ),
    67: (
        {"store", "item", "store_sales", "date_dim"},
        {"query67"},
        [
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("sumsales", "query67"),
            ),
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("i_category", "query67"),
            ),
            (
                ColumnQualifierTuple("i_class", None),
                ColumnQualifierTuple("i_class", "query67"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("sumsales", "query67"),
            ),
            (
                ColumnQualifierTuple("d_qoy", None),
                ColumnQualifierTuple("d_qoy", "query67"),
            ),
            (
                ColumnQualifierTuple("d_year", None),
                ColumnQualifierTuple("d_year", "query67"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("rk", "query67"),
            ),
            (
                ColumnQualifierTuple("i_brand", None),
                ColumnQualifierTuple("i_brand", "query67"),
            ),
            (
                ColumnQualifierTuple("s_store_id", None),
                ColumnQualifierTuple("s_store_id", "query67"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("rk", "query67"),
            ),
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("rk", "query67"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("d_moy", "query67"),
            ),
            (
                ColumnQualifierTuple("i_product_name", None),
                ColumnQualifierTuple("i_product_name", "query67"),
            ),
        ],
        {},
    ),
    68: (
        {
            "household_demographics",
            "customer_address",
            "store_sales",
            "date_dim",
            "store",
            "customer",
        },
        {"query68"},
        [
            (
                ColumnQualifierTuple("c_last_name", None),
                ColumnQualifierTuple("c_last_name", "query68"),
            ),
            (
                ColumnQualifierTuple("c_first_name", None),
                ColumnQualifierTuple("c_first_name", "query68"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("extended_price", "query68"),
            ),
            (
                ColumnQualifierTuple("ss_ext_tax", None),
                ColumnQualifierTuple("extended_tax", "query68"),
            ),
            (
                ColumnQualifierTuple("ca_city", None),
                ColumnQualifierTuple("bought_city", "query68"),
            ),
            (
                ColumnQualifierTuple("ca_city", None),
                ColumnQualifierTuple("ca_city", "query68"),
            ),
            (
                ColumnQualifierTuple("ss_ext_list_price", None),
                ColumnQualifierTuple("list_price", "query68"),
            ),
            (
                ColumnQualifierTuple("ss_ticket_number", None),
                ColumnQualifierTuple("ss_ticket_number", "query68"),
            ),
        ],
        {},
    ),
    69: (
        {
            "customer_demographics",
            "customer_address",
            "store_sales",
            "date_dim",
            "customer",
        },
        {"query69"},
        [
            (
                ColumnQualifierTuple("cd_purchase_estimate", None),
                ColumnQualifierTuple("cd_purchase_estimate", "query69"),
            ),
            (
                ColumnQualifierTuple("cd_credit_rating", None),
                ColumnQualifierTuple("cd_credit_rating", "query69"),
            ),
            (
                ColumnQualifierTuple("cd_gender", None),
                ColumnQualifierTuple("cd_gender", "query69"),
            ),
            (
                ColumnQualifierTuple("cd_marital_status", None),
                ColumnQualifierTuple("cd_marital_status", "query69"),
            ),
            (
                ColumnQualifierTuple("cd_education_status", None),
                ColumnQualifierTuple("cd_education_status", "query69"),
            ),
        ],
        {},
    ),
    70: (
        {"store_sales", "date_dim", "store"},
        {"query70"},
        [
            (
                ColumnQualifierTuple("s_state", None),
                ColumnQualifierTuple("s_state", "query70"),
            ),
            (
                ColumnQualifierTuple("s_county", None),
                ColumnQualifierTuple("s_county", "query70"),
            ),
            (
                ColumnQualifierTuple("ss_net_profit", None),
                ColumnQualifierTuple("total_sum", "query70"),
            ),
        ],
        {},
    ),
    71: (
        {"store_sales", "date_dim", "catalog_sales", "time_dim", "web_sales", "item"},
        {"query71"},
        [
            (
                ColumnQualifierTuple("i_brand", None),
                ColumnQualifierTuple("brand", "query71"),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", None),
                ColumnQualifierTuple("ext_price", "query71"),
            ),
            (
                ColumnQualifierTuple("t_hour", None),
                ColumnQualifierTuple("t_hour", "query71"),
            ),
            (
                ColumnQualifierTuple("t_minute", None),
                ColumnQualifierTuple("t_minute", "query71"),
            ),
            (
                ColumnQualifierTuple("i_brand_id", None),
                ColumnQualifierTuple("brand_id", "query71"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("ext_price", "query71"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("ext_price", "query71"),
            ),
        ],
        {},
    ),
    72: (
        {
            "household_demographics",
            "customer_demographics",
            "date_dim",
            "catalog_returns",
            "warehouse",
            "catalog_sales",
            "item",
            "inventory",
            "promotion",
        },
        {"query72"},
        [
            (
                ColumnQualifierTuple("p_promo_sk", None),
                ColumnQualifierTuple("promo", "query72"),
            ),
            (
                ColumnQualifierTuple("p_promo_sk", None),
                ColumnQualifierTuple("no_promo", "query72"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_name", None),
                ColumnQualifierTuple("w_warehouse_name", "query72"),
            ),
            (
                ColumnQualifierTuple("i_item_desc", None),
                ColumnQualifierTuple("i_item_desc", "query72"),
            ),
            (
                ColumnQualifierTuple("d_week_seq", "date_dim"),
                ColumnQualifierTuple("d_week_seq", "query72"),
            ),
        ],
        {},
    ),
    73: (
        {"household_demographics", "store_sales", "date_dim", "store", "customer"},
        {"query73"},
        [
            (
                ColumnQualifierTuple("c_salutation", None),
                ColumnQualifierTuple("c_salutation", "query73"),
            ),
            (
                ColumnQualifierTuple("c_first_name", None),
                ColumnQualifierTuple("c_first_name", "query73"),
            ),
            (
                ColumnQualifierTuple("c_preferred_cust_flag", None),
                ColumnQualifierTuple("c_preferred_cust_flag", "query73"),
            ),
            (
                ColumnQualifierTuple("c_last_name", None),
                ColumnQualifierTuple("c_last_name", "query73"),
            ),
            (
                ColumnQualifierTuple("ss_ticket_number", None),
                ColumnQualifierTuple("ss_ticket_number", "query73"),
            ),
            (ColumnQualifierTuple("cnt", None), ColumnQualifierTuple("cnt", "query73")),
        ],
        {},
    ),
    74: (
        {"web_sales", "store_sales", "customer", "date_dim"},
        {"query74"},
        [
            (
                ColumnQualifierTuple("c_customer_id", None),
                ColumnQualifierTuple("customer_id", "query74"),
            ),
            (
                ColumnQualifierTuple("c_first_name", None),
                ColumnQualifierTuple("customer_first_name", "query74"),
            ),
            (
                ColumnQualifierTuple("c_last_name", None),
                ColumnQualifierTuple("customer_last_name", "query74"),
            ),
        ],
        {},
    ),
    75: (
        {
            "store_sales",
            "date_dim",
            "catalog_returns",
            "store_returns",
            "catalog_sales",
            "web_sales",
            "item",
            "web_returns",
        },
        {"query75"},
        [
            (
                ColumnQualifierTuple("sr_return_quantity", None),
                ColumnQualifierTuple("curr_yr_cnt", "query75"),
            ),
            (
                ColumnQualifierTuple("cr_return_quantity", None),
                ColumnQualifierTuple("curr_yr_cnt", "query75"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("sales_cnt_diff", "query75"),
            ),
            (
                ColumnQualifierTuple("i_brand_id", None),
                ColumnQualifierTuple("i_brand_id", "query75"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("prev_yr_cnt", "query75"),
            ),
            (
                ColumnQualifierTuple("i_manufact_id", None),
                ColumnQualifierTuple("i_manufact_id", "query75"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("sales_amt_diff", "query75"),
            ),
            (
                ColumnQualifierTuple("d_year", None),
                ColumnQualifierTuple("year", "query75"),
            ),
            (
                ColumnQualifierTuple("wr_return_quantity", None),
                ColumnQualifierTuple("sales_cnt_diff", "query75"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("prev_yr_cnt", "query75"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("curr_yr_cnt", "query75"),
            ),
            (
                ColumnQualifierTuple("wr_return_quantity", None),
                ColumnQualifierTuple("prev_yr_cnt", "query75"),
            ),
            (
                ColumnQualifierTuple("cr_return_quantity", None),
                ColumnQualifierTuple("sales_cnt_diff", "query75"),
            ),
            (
                ColumnQualifierTuple("cr_return_amount", None),
                ColumnQualifierTuple("sales_amt_diff", "query75"),
            ),
            (
                ColumnQualifierTuple("sr_return_quantity", None),
                ColumnQualifierTuple("sales_cnt_diff", "query75"),
            ),
            (
                ColumnQualifierTuple("d_year", None),
                ColumnQualifierTuple("prev_year", "query75"),
            ),
            (
                ColumnQualifierTuple("i_category_id", None),
                ColumnQualifierTuple("i_category_id", "query75"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("curr_yr_cnt", "query75"),
            ),
            (
                ColumnQualifierTuple("i_class_id", None),
                ColumnQualifierTuple("i_class_id", "query75"),
            ),
            (
                ColumnQualifierTuple("sr_return_quantity", None),
                ColumnQualifierTuple("prev_yr_cnt", "query75"),
            ),
            (
                ColumnQualifierTuple("cr_return_quantity", None),
                ColumnQualifierTuple("prev_yr_cnt", "query75"),
            ),
            (
                ColumnQualifierTuple("wr_return_amt", None),
                ColumnQualifierTuple("sales_amt_diff", "query75"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("curr_yr_cnt", "query75"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("sales_cnt_diff", "query75"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("prev_yr_cnt", "query75"),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", None),
                ColumnQualifierTuple("sales_amt_diff", "query75"),
            ),
            (
                ColumnQualifierTuple("wr_return_quantity", None),
                ColumnQualifierTuple("curr_yr_cnt", "query75"),
            ),
            (
                ColumnQualifierTuple("sr_return_amt", None),
                ColumnQualifierTuple("sales_amt_diff", "query75"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("sales_cnt_diff", "query75"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("sales_amt_diff", "query75"),
            ),
        ],
        {},
    ),
    76: (
        {"web_sales", "item", "date_dim", "store_sales", "catalog_sales"},
        {"query76"},
        [],
        {},
    ),
    77: (
        {
            "store_sales",
            "date_dim",
            "store",
            "store_returns",
            "catalog_returns",
            "catalog_sales",
            "web_page",
            "web_sales",
            "web_returns",
        },
        {"query77"},
        [
            (
                ColumnQualifierTuple("ss_net_profit", None),
                ColumnQualifierTuple("profit", "query77"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("sales", "query77"),
            ),
            (
                ColumnQualifierTuple("sr_net_loss", None),
                ColumnQualifierTuple("profit", "query77"),
            ),
            (
                ColumnQualifierTuple("wp_web_page_sk", None),
                ColumnQualifierTuple("id", "query77"),
            ),
            (
                ColumnQualifierTuple("s_store_sk", None),
                ColumnQualifierTuple("id", "query77"),
            ),
            (
                ColumnQualifierTuple("cs_call_center_sk", None),
                ColumnQualifierTuple("id", "query77"),
            ),
        ],
        {},
    ),
    78: (
        {
            "store_sales",
            "date_dim",
            "catalog_returns",
            "store_returns",
            "catalog_sales",
            "web_sales",
            "web_returns",
        },
        {"query78"},
        [
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("ratio", "query78"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("other_chan_qty", "query78"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("ratio", "query78"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("ratio", "query78"),
            ),
            (
                ColumnQualifierTuple("ws_wholesale_cost", None),
                ColumnQualifierTuple("other_chan_wholesale_cost", "query78"),
            ),
            (
                ColumnQualifierTuple("cs_wholesale_cost", None),
                ColumnQualifierTuple("other_chan_wholesale_cost", "query78"),
            ),
            (
                ColumnQualifierTuple("ss_wholesale_cost", None),
                ColumnQualifierTuple("store_wholesale_cost", "query78"),
            ),
            (
                ColumnQualifierTuple("ws_sales_price", None),
                ColumnQualifierTuple("other_chan_sales_price", "query78"),
            ),
            (
                ColumnQualifierTuple("cs_sales_price", None),
                ColumnQualifierTuple("other_chan_sales_price", "query78"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("store_sales_price", "query78"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("other_chan_qty", "query78"),
            ),
            (
                ColumnQualifierTuple("cs_quantity", None),
                ColumnQualifierTuple("other_chan_qty", "query78"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("store_qty", "query78"),
            ),
            (
                ColumnQualifierTuple("ss_customer_sk", None),
                ColumnQualifierTuple("ss_customer_sk", "query78"),
            ),
            (
                ColumnQualifierTuple("ss_item_sk", None),
                ColumnQualifierTuple("ss_item_sk", "query78"),
            ),
            (
                ColumnQualifierTuple("d_year", None),
                ColumnQualifierTuple("ss_sold_year", "query78"),
            ),
        ],
        {},
    ),
    79: (
        {"household_demographics", "store_sales", "date_dim", "store", "customer"},
        {"query79"},
        [
            (
                ColumnQualifierTuple("s_city", "store"),
                ColumnQualifierTuple("substr(s_city,1,30)", "query79"),
            ),
            (
                ColumnQualifierTuple("ss_coupon_amt", None),
                ColumnQualifierTuple("amt", "query79"),
            ),
            (
                ColumnQualifierTuple("c_first_name", None),
                ColumnQualifierTuple("c_first_name", "query79"),
            ),
            (
                ColumnQualifierTuple("ss_net_profit", None),
                ColumnQualifierTuple("profit", "query79"),
            ),
            (
                ColumnQualifierTuple("c_last_name", None),
                ColumnQualifierTuple("c_last_name", "query79"),
            ),
            (
                ColumnQualifierTuple("ss_ticket_number", None),
                ColumnQualifierTuple("ss_ticket_number", "query79"),
            ),
        ],
        {},
    ),
    80: (
        {
            "store_sales",
            "catalog_returns",
            "store_returns",
            "catalog_sales",
            "web_sales",
            "web_returns",
        },
        {"query80"},
        [
            (
                ColumnQualifierTuple("wr_net_loss", None),
                ColumnQualifierTuple("profit", "query80"),
            ),
            (
                ColumnQualifierTuple("ss_net_profit", None),
                ColumnQualifierTuple("profit", "query80"),
            ),
            (
                ColumnQualifierTuple("cp_catalog_page_id", None),
                ColumnQualifierTuple("id", "query80"),
            ),
            (
                ColumnQualifierTuple("ws_net_profit", None),
                ColumnQualifierTuple("profit", "query80"),
            ),
            (
                ColumnQualifierTuple("cr_net_loss", None),
                ColumnQualifierTuple("profit", "query80"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("sales", "query80"),
            ),
            (
                ColumnQualifierTuple("sr_net_loss", None),
                ColumnQualifierTuple("profit", "query80"),
            ),
            (
                ColumnQualifierTuple("ws_ext_sales_price", None),
                ColumnQualifierTuple("sales", "query80"),
            ),
            (
                ColumnQualifierTuple("s_store_id", None),
                ColumnQualifierTuple("id", "query80"),
            ),
            (
                ColumnQualifierTuple("cs_ext_sales_price", None),
                ColumnQualifierTuple("sales", "query80"),
            ),
            (
                ColumnQualifierTuple("web_site_id", None),
                ColumnQualifierTuple("id", "query80"),
            ),
            (
                ColumnQualifierTuple("cs_net_profit", None),
                ColumnQualifierTuple("profit", "query80"),
            ),
        ],
        {},
    ),
    81: (
        {"customer_address", "customer", "catalog_returns", "date_dim"},
        {"query81"},
        [
            (
                ColumnQualifierTuple("ca_suite_number", None),
                ColumnQualifierTuple("ca_suite_number", "query81"),
            ),
            (
                ColumnQualifierTuple("ca_gmt_offset", None),
                ColumnQualifierTuple("ca_gmt_offset", "query81"),
            ),
            (
                ColumnQualifierTuple("c_customer_id", None),
                ColumnQualifierTuple("c_customer_id", "query81"),
            ),
            (
                ColumnQualifierTuple("ca_zip", None),
                ColumnQualifierTuple("ca_zip", "query81"),
            ),
            (
                ColumnQualifierTuple("cr_return_amt_inc_tax", None),
                ColumnQualifierTuple("ctr_total_return", "query81"),
            ),
            (
                ColumnQualifierTuple("ca_county", None),
                ColumnQualifierTuple("ca_county", "query81"),
            ),
            (
                ColumnQualifierTuple("c_last_name", None),
                ColumnQualifierTuple("c_last_name", "query81"),
            ),
            (
                ColumnQualifierTuple("ca_street_number", None),
                ColumnQualifierTuple("ca_street_number", "query81"),
            ),
            (
                ColumnQualifierTuple("ca_state", None),
                ColumnQualifierTuple("ca_state", "query81"),
            ),
            (
                ColumnQualifierTuple("ca_country", None),
                ColumnQualifierTuple("ca_country", "query81"),
            ),
            (
                ColumnQualifierTuple("ca_city", None),
                ColumnQualifierTuple("ca_city", "query81"),
            ),
            (
                ColumnQualifierTuple("ca_location_type", None),
                ColumnQualifierTuple("ca_location_type", "query81"),
            ),
            (
                ColumnQualifierTuple("ca_street_name", None),
                ColumnQualifierTuple("ca_street_name", "query81"),
            ),
            (
                ColumnQualifierTuple("ca_street_type", None),
                ColumnQualifierTuple("ca_street_type", "query81"),
            ),
            (
                ColumnQualifierTuple("c_first_name", None),
                ColumnQualifierTuple("c_first_name", "query81"),
            ),
            (
                ColumnQualifierTuple("c_salutation", None),
                ColumnQualifierTuple("c_salutation", "query81"),
            ),
        ],
        {},
    ),
    82: (
        {"inventory", "store_sales", "date_dim", "item"},
        {"query82"},
        [
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("i_item_id", "query82"),
            ),
            (
                ColumnQualifierTuple("i_current_price", None),
                ColumnQualifierTuple("i_current_price", "query82"),
            ),
            (
                ColumnQualifierTuple("i_item_desc", None),
                ColumnQualifierTuple("i_item_desc", "query82"),
            ),
        ],
        {},
    ),
    83: (
        {"catalog_returns", "item", "web_returns", "date_dim", "store_returns"},
        {"query83"},
        [
            (
                ColumnQualifierTuple("sr_return_quantity", None),
                ColumnQualifierTuple("sr_dev", "query83"),
            ),
            (
                ColumnQualifierTuple("sr_return_quantity", None),
                ColumnQualifierTuple("sr_item_qty", "query83"),
            ),
            (
                ColumnQualifierTuple("cr_return_quantity", None),
                ColumnQualifierTuple("wr_dev", "query83"),
            ),
            (
                ColumnQualifierTuple("sr_return_quantity", None),
                ColumnQualifierTuple("cr_dev", "query83"),
            ),
            (
                ColumnQualifierTuple("wr_return_quantity", None),
                ColumnQualifierTuple("wr_dev", "query83"),
            ),
            (
                ColumnQualifierTuple("wr_return_quantity", None),
                ColumnQualifierTuple("wr_item_qty", "query83"),
            ),
            (
                ColumnQualifierTuple("cr_return_quantity", None),
                ColumnQualifierTuple("average", "query83"),
            ),
            (
                ColumnQualifierTuple("sr_return_quantity", None),
                ColumnQualifierTuple("wr_dev", "query83"),
            ),
            (
                ColumnQualifierTuple("wr_return_quantity", None),
                ColumnQualifierTuple("average", "query83"),
            ),
            (
                ColumnQualifierTuple("wr_return_quantity", None),
                ColumnQualifierTuple("cr_dev", "query83"),
            ),
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("item_id", "query83"),
            ),
            (
                ColumnQualifierTuple("cr_return_quantity", None),
                ColumnQualifierTuple("cr_item_qty", "query83"),
            ),
            (
                ColumnQualifierTuple("sr_return_quantity", None),
                ColumnQualifierTuple("average", "query83"),
            ),
            (
                ColumnQualifierTuple("wr_return_quantity", None),
                ColumnQualifierTuple("sr_dev", "query83"),
            ),
            (
                ColumnQualifierTuple("cr_return_quantity", None),
                ColumnQualifierTuple("cr_dev", "query83"),
            ),
            (
                ColumnQualifierTuple("cr_return_quantity", None),
                ColumnQualifierTuple("sr_dev", "query83"),
            ),
        ],
        {},
    ),
    84: (
        {
            "household_demographics",
            "customer_demographics",
            "customer",
            "income_band",
            "customer_address",
            "store_returns",
        },
        {"query84"},
        [
            (
                ColumnQualifierTuple("c_last_name", None),
                ColumnQualifierTuple("customername", "query84"),
            ),
            (
                ColumnQualifierTuple("c_first_name", None),
                ColumnQualifierTuple("customername", "query84"),
            ),
            (
                ColumnQualifierTuple("c_customer_id", None),
                ColumnQualifierTuple("customer_id", "query84"),
            ),
        ],
        {},
    ),
    85: (
        {
            "web_page",
            "web_sales",
            "reason",
            "customer_demographics",
            "customer_address",
            "web_returns",
            "date_dim",
        },
        {"query85"},
        [
            (
                ColumnQualifierTuple("wr_refunded_cash", None),
                ColumnQualifierTuple("avg(wr_refunded_cash)", "query85"),
            ),
            (
                ColumnQualifierTuple("wr_fee", None),
                ColumnQualifierTuple("avg(wr_fee)", "query85"),
            ),
            (
                ColumnQualifierTuple("ws_quantity", None),
                ColumnQualifierTuple("avg(ws_quantity)", "query85"),
            ),
            (
                ColumnQualifierTuple("r_reason_desc", None),
                ColumnQualifierTuple("substr(r_reason_desc, 1, 20)", "query85"),
            ),
        ],
        {},
    ),
    86: (
        {"web_sales", "date_dim", "item"},
        {"query86"},
        [
            (
                ColumnQualifierTuple("i_class", None),
                ColumnQualifierTuple("i_class", "query86"),
            ),
            (
                ColumnQualifierTuple("ws_net_paid", None),
                ColumnQualifierTuple("total_sum", "query86"),
            ),
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("i_category", "query86"),
            ),
        ],
        {},
    ),
    87: (
        {"customer", "store_sales", "date_dim"},
        {"query87"},
        [],
        {},
    ),
    88: (
        {"store", "time_dim", "store_sales", "household_demographics"},
        {"query88"},
        [],
        {},
    ),
    89: (
        {"store", "item", "store_sales", "date_dim"},
        {"query89"},
        [
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("avg_monthly_sales", "query89"),
            ),
            (
                ColumnQualifierTuple("s_company_name", None),
                ColumnQualifierTuple("s_company_name", "query89"),
            ),
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("i_category", "query89"),
            ),
            (
                ColumnQualifierTuple("i_class", None),
                ColumnQualifierTuple("i_class", "query89"),
            ),
            (
                ColumnQualifierTuple("i_brand", None),
                ColumnQualifierTuple("i_brand", "query89"),
            ),
            (
                ColumnQualifierTuple("i_brand", None),
                ColumnQualifierTuple("avg_monthly_sales", "query89"),
            ),
            (
                ColumnQualifierTuple("d_moy", None),
                ColumnQualifierTuple("d_moy", "query89"),
            ),
            (
                ColumnQualifierTuple("s_store_name", None),
                ColumnQualifierTuple("avg_monthly_sales", "query89"),
            ),
            (
                ColumnQualifierTuple("s_company_name", None),
                ColumnQualifierTuple("avg_monthly_sales", "query89"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("sum_sales", "query89"),
            ),
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("avg_monthly_sales", "query89"),
            ),
            (
                ColumnQualifierTuple("s_store_name", None),
                ColumnQualifierTuple("s_store_name", "query89"),
            ),
        ],
        {},
    ),
    90: (
        {"household_demographics", "time_dim", "web_page", "web_sales"},
        {"query90"},
        [
            (
                ColumnQualifierTuple("amc", None),
                ColumnQualifierTuple("am_pm_ratio", "query90"),
            ),
            (
                ColumnQualifierTuple("pmc", None),
                ColumnQualifierTuple("am_pm_ratio", "query90"),
            ),
        ],
        {},
    ),
    91: (
        {
            "household_demographics",
            "call_center",
            "customer_demographics",
            "catalog_returns",
            "customer",
            "customer_address",
            "date_dim",
        },
        {"query91"},
        [
            (
                ColumnQualifierTuple("cr_net_loss", None),
                ColumnQualifierTuple("Returns_Loss", "query91"),
            ),
            (
                ColumnQualifierTuple("cc_manager", None),
                ColumnQualifierTuple("Manager", "query91"),
            ),
            (
                ColumnQualifierTuple("cc_call_center_id", None),
                ColumnQualifierTuple("Call_Center", "query91"),
            ),
            (
                ColumnQualifierTuple("cc_name", None),
                ColumnQualifierTuple("Call_Center_Name", "query91"),
            ),
        ],
        {},
    ),
    92: (
        {"web_sales", "date_dim", "item"},
        {"query92"},
        [
            (
                ColumnQualifierTuple("ws_ext_discount_amt", None),
                ColumnQualifierTuple("Excess_Discount_Amount", "query92"),
            )
        ],
        {},
    ),
    93: (
        {"store_sales", "store_returns"},
        {"query93"},
        [
            (
                ColumnQualifierTuple("ss_sales_price", None),
                ColumnQualifierTuple("sumsales", "query93"),
            ),
            (
                ColumnQualifierTuple("ss_customer_sk", None),
                ColumnQualifierTuple("ss_customer_sk", "query93"),
            ),
            (
                ColumnQualifierTuple("sr_return_quantity", None),
                ColumnQualifierTuple("sumsales", "query93"),
            ),
            (
                ColumnQualifierTuple("ss_quantity", None),
                ColumnQualifierTuple("sumsales", "query93"),
            ),
        ],
        {},
    ),
    94: (
        {"web_sales", "web_site", "customer_address", "web_returns", "date_dim"},
        {"query94"},
        [
            (
                ColumnQualifierTuple("ws_net_profit", None),
                ColumnQualifierTuple("total_net_profit", "query94"),
            ),
            (
                ColumnQualifierTuple("ws_order_number", None),
                ColumnQualifierTuple("order_count", "query94"),
            ),
            (
                ColumnQualifierTuple("ws_ext_ship_cost", None),
                ColumnQualifierTuple("total_shipping_cost", "query94"),
            ),
        ],
        {},
    ),
    95: (
        {"web_sales", "web_site", "customer_address", "web_returns", "date_dim"},
        {"query95"},
        [
            (
                ColumnQualifierTuple("ws_net_profit", None),
                ColumnQualifierTuple("total_net_profit", "query95"),
            ),
            (
                ColumnQualifierTuple("ws_order_number", "web_sales"),
                ColumnQualifierTuple("order_count", "query95"),
            ),
            (
                ColumnQualifierTuple("ws_ext_ship_cost", None),
                ColumnQualifierTuple("total_shipping_cost", "query95"),
            ),
        ],
        {},
    ),
    96: (
        {"store", "household_demographics", "time_dim", "store_sales"},
        {"query96"},
        [],
        {},
    ),
    97: (
        {"catalog_sales", "date_dim", "store_sales"},
        {"query97"},
        [
            (
                ColumnQualifierTuple("cs_bill_customer_sk", None),
                ColumnQualifierTuple("store_and_catalog", "query97"),
            ),
            (
                ColumnQualifierTuple("cs_bill_customer_sk", None),
                ColumnQualifierTuple("store_only", "query97"),
            ),
            (
                ColumnQualifierTuple("cs_bill_customer_sk", None),
                ColumnQualifierTuple("catalog_only", "query97"),
            ),
            (
                ColumnQualifierTuple("ss_customer_sk", None),
                ColumnQualifierTuple("store_and_catalog", "query97"),
            ),
            (
                ColumnQualifierTuple("ss_customer_sk", None),
                ColumnQualifierTuple("catalog_only", "query97"),
            ),
            (
                ColumnQualifierTuple("ss_customer_sk", None),
                ColumnQualifierTuple("store_only", "query97"),
            ),
        ],
        {},
    ),
    98: (
        {"store_sales", "date_dim", "item"},
        {"query98"},
        [
            (
                ColumnQualifierTuple("i_item_id", None),
                ColumnQualifierTuple("i_item_id", "query98"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("itemrevenue", "query98"),
            ),
            (
                ColumnQualifierTuple("i_current_price", None),
                ColumnQualifierTuple("i_current_price", "query98"),
            ),
            (
                ColumnQualifierTuple("i_item_desc", None),
                ColumnQualifierTuple("i_item_desc", "query98"),
            ),
            (
                ColumnQualifierTuple("i_class", None),
                ColumnQualifierTuple("i_class", "query98"),
            ),
            (
                ColumnQualifierTuple("ss_ext_sales_price", None),
                ColumnQualifierTuple("revenueratio", "query98"),
            ),
            (
                ColumnQualifierTuple("i_category", None),
                ColumnQualifierTuple("i_category", "query98"),
            ),
            (
                ColumnQualifierTuple("i_class", None),
                ColumnQualifierTuple("revenueratio", "query98"),
            ),
        ],
        {},
    ),
    99: (
        {"ship_mode", "warehouse", "call_center", "catalog_sales", "date_dim"},
        {"query99"},
        [
            (
                ColumnQualifierTuple("cs_sold_date_sk", None),
                ColumnQualifierTuple("1_120_days", "query99"),
            ),
            (
                ColumnQualifierTuple("cs_sold_date_sk", None),
                ColumnQualifierTuple("1_90_days", "query99"),
            ),
            (
                ColumnQualifierTuple("sm_type", None),
                ColumnQualifierTuple("sm_type", "query99"),
            ),
            (
                ColumnQualifierTuple("cs_ship_date_sk", None),
                ColumnQualifierTuple("0_days", "query99"),
            ),
            (
                ColumnQualifierTuple("cc_name", None),
                ColumnQualifierTuple("cc_name", "query99"),
            ),
            (
                ColumnQualifierTuple("cs_sold_date_sk", None),
                ColumnQualifierTuple("0_days", "query99"),
            ),
            (
                ColumnQualifierTuple("cs_ship_date_sk", None),
                ColumnQualifierTuple("above120_days", "query99"),
            ),
            (
                ColumnQualifierTuple("w_warehouse_name", None),
                ColumnQualifierTuple("substr(w_warehouse_name, 1, 20)", "query99"),
            ),
            (
                ColumnQualifierTuple("cs_ship_date_sk", None),
                ColumnQualifierTuple("1_60_days", "query99"),
            ),
            (
                ColumnQualifierTuple("cs_sold_date_sk", None),
                ColumnQualifierTuple("above120_days", "query99"),
            ),
            (
                ColumnQualifierTuple("cs_ship_date_sk", None),
                ColumnQualifierTuple("1_120_days", "query99"),
            ),
            (
                ColumnQualifierTuple("cs_sold_date_sk", None),
                ColumnQualifierTuple("1_60_days", "query99"),
            ),
            (
                ColumnQualifierTuple("cs_ship_date_sk", None),
                ColumnQualifierTuple("1_90_days", "query99"),
            ),
        ],
        {},
    ),
}

test_parameters = [(i, expected[i]) for i in range(1, 100)]


def _read_test_sql(number: int) -> str:
    with open(f"sqllineage/data/tpcds/query{number:02d}.sql", "r") as file:
        return file.read()


@pytest.mark.parametrize("index,expected_result", test_parameters)
def test_tpcds_query(index, expected_result):
    sql = _read_test_sql(index)
    sources, targets, column_lineages, table_columns = expected_result

    schema_fetcher = (
        DummySchemaFetcher({str(Table(k)): v for k, v in table_columns.items()})
        if table_columns
        else None
    )

    assert_table_and_column_lineage_equal(
        sql, sources, targets, column_lineages, schema_fetcher
    )
