def test_add(app):
    sql = app.add_sql("tb_user", {"id": 1})
    assert sql == "INSERT INTO `tb_user` id values (%(id)s);"


def test_add_many_items(app):
    sql = app.add_sql("tb_user", {"id": 1, "name": "lily"})
    assert sql == "INSERT INTO `tb_user` id,name values (%(id)s,%(name)s);"


def test_add_wrong_type(app):
    try:
        app.add_sql("tb_user", [{"id": 1}])
        assert False
    except:
        assert True


def test_delete_sql(app):
    sql, args = app.delete_sql("tb_user", {"id": 1})
    assert sql == "DELETE FROM tb_user WHERE `id`=%(id)s"
    assert args == {'id': 1}


def test_delete_sql_with_in(app):
    sql, args = app.delete_sql("tb_user", {"id": 1}, in_dict={"age": [1, 2]})
    assert sql == "DELETE FROM tb_user WHERE `id`=%(id)s AND `age` in %(age)s"
    assert args == {'id': 1, "age": [1, 2]}


def test_delete_sql_only_in(app):
    sql, args = app.delete_sql("tb_user", in_dict={"age": [1, 2]})
    assert sql == "DELETE FROM tb_user WHERE `age` in %(age)s"
    assert args == {"age": [1, 2]}


def test_delete_sql_with_no_conditions(app):
    try:
        sql, args = app.delete_sql("tb_user")
        assert False
    except:
        assert True


def test_update_sql(app):
    sql, args = app.update_sql("tb_user", {"id": 2}, {"id": 1})
    assert sql == "UPDATE `tb_user` SET `id`=%(update_id)s WHERE `id`=%(id)s"
    assert args == {'id': 1, 'update_id': 2}


def test_update_sql_with_in(app):
    sql, args = app.update_sql("tb_user", {"id": 2, "age": 3, "name": "ltj"}, {"id": 1}, in_dict={"age": [1, 2]})
    assert sql in [
        "UPDATE `tb_user` SET `id`=%(update_id)s,`age`=%(update_age)s,`name`=%(update_name)s WHERE `id`=%(id)s AND `age` in %(age)s",
        "UPDATE `tb_user` SET `age`=%(update_age)s,`id`=%(update_id)s,`name`=%(update_name)s WHERE `id`=%(id)s AND `age` in %(age)s"]
    assert args == {'id': 1, 'update_id': 2, "update_age": 3, "update_name": "ltj", "age": [1, 2]}


def test_update_sql_only_in(app):
    sql, args = app.update_sql("tb_user", {"id": 2, "age": 3, "name": "ltj"}, in_dict={"age": [1, 2]})
    assert sql in [
        "UPDATE `tb_user` SET `id`=%(update_id)s,`age`=%(update_age)s,`name`=%(update_name)s WHERE `age` in %(age)s",
        "UPDATE `tb_user` SET `age`=%(update_age)s,`id`=%(update_id)s,`name`=%(update_name)s WHERE `age` in %(age)s"]
    assert args == {'update_id': 2, "update_age": 3, "update_name": "ltj", "age": [1, 2]}


def test_update_sql_no_conditions(app):
    try:
        sql, args = app.update_sql("tb_user", {"id": 1})
        assert False
    except:
        assert True


def test_select_sql_with_no_items(app):
    sql, args = app.select_sql("tb_user")
    assert sql == "SELECT * FROM `tb_user`"
    assert args == {}


def test_select_sql_only_items(app):
    sql, args = app.select_sql("tb_user", ["id", "name"])
    assert sql == "SELECT `id`,`name` FROM `tb_user`"
    assert args == {}


def test_select_sql_with_only_in(app):
    sql, args = app.select_sql("tb_user", in_dict={"age": [1, 2]})
    assert sql == "SELECT * FROM `tb_user` WHERE `age` in %(age)s"
    assert args == {"age": [1, 2]}


def test_select_sql_with_no_items(app):
    sql, args = app.select_sql("tb_user")
    assert sql == "SELECT * FROM `tb_user`"
    assert args == {}


def test_select_sql_with_no_items(app):
    sql, args = app.select_sql("tb_user")
    assert sql == "SELECT * FROM `tb_user`"
    assert args == {}
