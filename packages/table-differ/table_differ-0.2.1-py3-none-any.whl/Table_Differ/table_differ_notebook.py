#! /usr/bin/env python3

# long-help
"""
Intention here is that this can be imported into a notebook and provides reporting back

to be used in databricks notebook
"""

# BUILT-INS
import logging
import sys
import os
from datetime import date

# THIRD PARTY
from rich import print as rprint
from pydantic import BaseModel, ValidationError
from pydantic import field_validator, model_validator

# PERSONAL
from Table_Differ.modules.create_diff_table import DiffWriter
from Table_Differ.modules.exceptions import InvalidArgument, MissingArgument
from Table_Differ.modules.pydantic_models import Args


class TableDiffer:
    def __init__(self, conn, args):
        rprint("[bold red blink]START RUN")
        self.conn = conn
        self.args = self.get_args(args)
        self.create_diff_table()

    def get_args(self, args):
        try:
            args = Args(**args)
        except ValidationError as e:
            rprint(e)
        logging.info(args)
        return args


    def create_diff_table(self):
        assert self.conn
        tables = DiffWriter(args = self.args, conn = self.conn)
        tables.create_diff_table()

