#! usr/bin/env python3

# BUILT IN
from datetime import date
from typing_extensions import Self

# THIRD PARTY
from pydantic import BaseModel, ValidationError
from pydantic import field_validator, model_validator

# PERSONAL
from Table_Differ.modules import gnome

class Args(BaseModel):
# Database
    db_host:                str         = None
    db_port:                str         = None
    db_name:                str         = None
    db_user:                str         = None
    db_path:                str         = None
    db_type:                str         = "databricks"

# Table Info
    table_initial:          str 
    table_secondary:        str
    table_diff:             str         = "__diff_table__" + str(date.today()).replace("-","_") + "__"
    schema_name:            str         = "revenue_dev"
    key_cols:               list[str]
    comp_cols:              list[str]   = None
    ignore_cols:            list[str]   = None
    initial_table_alias:    str         = "origin"
    secondary_table_alias:  str         = "comparison"
    except_rows:            list[str]   = None

# System
    local_db:               bool        = False
    print_tables:           bool        = False
    report_mode:            bool        = False
    print_query:            bool        = True
    gnome:                  bool        = False
    log_level:              str         = "warning"


    @field_validator('key_cols')
    @classmethod
    def check_key_len(cls, v):
        max_length = 10
        if len(v) > 10:
            raise ValueError(f"too many columns supplied, max: {max_length}")
        return v


    @field_validator('log_level')
    @classmethod
    def check_log_level(cls, v):
        log_levels =  ["debug", "info", "warning", "error", "critical"]
        if v.lower() not in log_levels:
            raise ValueError(f"value must be one of: {log_levels}")
        return v

    @field_validator('gnome')
    @classmethod
    def gnome_mode(cls, v):
        if v:
            gnome.activate()

    @model_validator(mode='after')
    def either_comp_or_ignore(self) -> Self:
        comp_cols   = self.comp_cols
        ignore_cols = self.ignore_cols
        if not comp_cols and not ignore_cols:
            raise ValueError("Either comp or ignore columns are required")
        if comp_cols and not ignore_cols:
            return
        if ignore_cols and not comp_cols:
            return


class DataProfileArgs(BaseModel):
    table_name:             str
    table_schema:           str
    table_catalog:          str         = "main"

    where_clause:           str         = None
