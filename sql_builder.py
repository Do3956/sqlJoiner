# -*- coding: utf-8 -*-
"""
__author__ = 'do'
__mtime__ = '2019/1/12'
__content__ = 'mysql语句生成器'

只是实现一些简单操作组合
介于不想使用orm可是又嫌直接SQL太繁琐的一点改进

或者下一步会使用SQLAlchemy的基本操作，但同样不会使用外键，项目大了就各种问题。
因此跨表问题仍需手写SQL。
"""


def format_where(conditions=None, in_dict=None):
    """
    整理条件查询语句
    :param conditions: dict
    :return: `id`=%(id)s AND `age`=%(age)s

    如果以后要扩展，注意同一个key使用多次，sql_args 的值会被覆盖问题
    """
    assert conditions or in_dict

    sql_args = {}
    sql_list = []
    if conditions:
        sql_list = list(map(lambda x: "`%s`=%%(%s)s" % (x, x), conditions.keys()))
        sql_args.update(conditions)
    if in_dict:
        sql_list.extend(list(map(lambda x: "`%s` in %%(%s)s" % (x, x), in_dict.keys())))
        sql_args.update(in_dict)

    sql = ' AND '.join(sql_list)

    return sql, sql_args


def format_update(update_data):
    """
    生成更新语句
    :param update_data: dict
    :return: `id`=%(id)s, `age`=%(age)s
    """
    sql_list = []
    sql_args_update = {}
    for x in update_data.keys():
        sql_list.append("`%s`=%%(update_%s)s" % (x, x))
        sql_args_update["update_%s" % x] = update_data[x]

    sql = ','.join(sql_list)
    return sql, sql_args_update


def format_select_items(items):
    """
    生成更新语句
    :param items: None or List
    :return: id, age
    """
    if not items:
        items = "*"
    else:
        item_list = []
        for i in items:
            i = i.join(["`", "`"])
            item_list.append(i)
        items = ",".join(item_list)
    return items


# -------------------------------- 生成 增删改查 SQL语句 ----------------------------------
def add_sql(table, new_data):
    """
    添加数据，此接口可以用于添加多条数据，只要调用executeMany， sql参数用[{new_data1}, {new_data1}] 即可。
    但是之前测试过, 同样写入1W数据，先处理好sql, executeOne 比 executeMany快（均只有一次SQL调用）。
    如果在意性能，可以用 executeOne 。
    :return:
    """
    assert type(new_data) == dict

    key_list = []
    value_list = []

    for _k in new_data.keys():
        key_list.append(_k)
        value_list.append("%%(%s)s" % _k)

    sql = """INSERT INTO `%s` %s values (%s);""" % (table, ",".join(key_list), ",".join(value_list))
    return sql


def delete_sql(table, conditions=None, in_dict=None):
    """
    :param table: 表名
    :param conditions: dict
    :param in_dict: dict
    :return:
    """

    sql_where, sql_args = format_where(conditions, in_dict)
    sql = "DELETE FROM %s WHERE %s" % (table, sql_where)
    return sql, sql_args


def select_sql(table, items=None, conditions=None, in_dict=None):
    """
    :param table: 表名
    :param items: 需要查询的项目
    :param conditions: dict
    :param in_dict: dict

    :return:
    """

    sql_args = {}
    sql = "SELECT %s FROM `%s`" % (format_select_items(items), table)
    if conditions or in_dict:
        sql_where, sql_args = format_where(conditions, in_dict)
        sql = "%s WHERE %s" % (sql, sql_where)

    return sql, sql_args


def update_sql(table, update_data, conditions=None, in_dict=None):
    """
    :param table: 表名
    :param update_data: dict
    :param conditions: dict
    :param in_dict: dict

    :return:
    """

    sql_where, sql_args = format_where(conditions, in_dict)
    sql_update, sql_args_update = format_update(update_data)
    sql_args.update(sql_args_update)
    sql = "UPDATE `%s` SET %s WHERE %s" % (table, sql_update, sql_where)

    return sql, sql_args

