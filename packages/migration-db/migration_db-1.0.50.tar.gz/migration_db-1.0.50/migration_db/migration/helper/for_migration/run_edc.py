# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 2022/6/19 17:15
@Description: Description
@File: run_edc.py
"""
from migration.core.build_test_platform_data import build_external_condition_mapping, get_data
from migration.core.build_update_sql import BuildUpdateSQL
from migration.db.base_db import BaseDb

if __name__ == '__main__':
    data_base = "eclinical_edc_dev_830"
    # data_source = DataSourceRoute().build_config("dev03", use_config_obj=False)
    data_source = dict(host="localhost", port=3306, db="eclinical_test_platform", password="admin123",
                       user="root")
    test_platform = dict(host="localhost", port=3306, db="eclinical_test_platform", password="admin123",
                         user="root")
    external_condition_fields_mapping = build_external_condition_mapping(test_platform)
    data = get_data(test_platform, 5)
    table_actions = BaseDb(test_platform).fetchall(
        f"SELECT * FROM eclinical_table_action WHERE is_delete=FALSE AND system_id=5;") or list()
    config_info = dict(data=data, external_condition_fields_mapping=external_condition_fields_mapping,
                       table_actions=table_actions)
    _path = BuildUpdateSQL(data_base, data_source).build(config_info)
    print(_path)
