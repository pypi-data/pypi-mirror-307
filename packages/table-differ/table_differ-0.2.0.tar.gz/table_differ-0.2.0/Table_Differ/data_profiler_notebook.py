#! /usr/bin/env python3

# long-help
"""
Intention here is that this can be imported into a notebook and provides reporting back
"""

# BUILT-INS
import logging
import sys
import os
from datetime import date

# THIRD PARTY
from rich import print as rprint

# PERSONAL
from Table_Differ.modules.pydantic_models import DataProfileArgs


class TableDiffer:
    def __init__(self, conn, args):
        rprint("[bold red blink]START RUN")
        self.conn = conn
        self.args = self.get_args(args)
        result = self.create_data_profile
        self.report(result)

    def get_args(self, args):
        try:
            args = DataProfileArgs(**args)
        except ValidationError as e:
            rprint(e)
        logging.info(args)
        return args


    def create_data_profile(self) -> dict:
        assert self.conn
        cols = spark.sql(f"DESCRIBE {self.args.table_catalog}.{self.args.table_schema}.{self.args.table_name}")
        col_list = [row.col_name for row in cols.select('col_name').collect()]

        result_dict = {
            "SUM": {},
            "MIN": {},
            "MAX": {},
            "AVG": {},
            "UNIQUENESS": {},
            "NULL_PERC": {},
        }

        for field in result_dict:
            select_clause = ""
            where_clause = ""
            for col in col_list:
                comma = ","
                if col == col_list[-1]:
                    comma = ""

                if field == "NULL_PERC":
                    select_clause += f"\n100.0 * SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END) / COUNT(*) AS {col}{comma}"
                elif field == "UNIQUENESS":
                    select_clause += f"\n( COUNT({col}) / COUNT(DISTINCT {col}) ) as {col}{comma}"
                else:
                    select_clause += f" {field}({col}) as {col}{comma}"

            query = f"""
                SELECT
                    {select_clause}
                FROM
                    {self.args.table_catalog}.{self.args.table_schema}.{self.args.table_name}
                {where_clause}
                """
            result_dict[field]["result"] = spark.sql(query).collect()
            result_dict[field]["query"] = query
            return result_dict

    def report(self, result: dict):
        for field in result:
            rprint(f"\n[bold red]{field}", "\n", result[field]["query"], "\n", result[field]["result"])
