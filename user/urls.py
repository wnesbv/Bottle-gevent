
import sqlite3, os
from bottle import (
    run,
    get,
    post,
    request,
    redirect,
    error,
    template,
    auth_basic,
    route,
    Bottle,
)
from composite.parts import con, f_dt, img_creat, img_upload


user = Bottle()

def list_user():
    cur = con.cursor()
    sql = "SELECT * FROM user_table"
    res = cur.execute(sql)
    in_sql = res.fetchall()
    cur.close()
    data = [dict(row) for row in in_sql]
    return data
# ..
@user.route("/")
def user_list():
    res = list_user()
    return template("user/user.html", res=res)


@user.route("/<to_id:int>")
def user_detail(to_id):
    data = (to_id,)
    cur = con.cursor()
    sql = "SELECT * FROM user_table WHERE id=?"
    in_sql = cur.execute(sql, data)
    res = in_sql.fetchall()
    cur.close()
    return template("user/detail.html", res=res)


# .. user post
@user.route("/post-list/<to_id:int>")
def user_post_list(to_id):
    data = (to_id,)
    cur = con.cursor()
    sql = "SELECT * FROM blog_table WHERE user_list=?"
    in_sql = cur.execute(sql, data)
    res = in_sql.fetchall()
    cur.close()
    return template("user/user_post.html", res=res)


# .. creat
@user.route("/user-form")
def creat_user_form():
    return template("creat_post_form.html")


@user.post("/user-form")
def creat_user():
    heading = request.forms.get("name")
    upload = img_creat()
    # ..
    data = heading, upload, f_dt
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO user_table (
            name, upload, generated
        )VALUES (?,?,?)
        """,
        data
    )
    con.commit()
    cur.close()
    return redirect("/user")


# .. update
@user.route("/user-form/<to_id:int>")
def user_form_get(to_id):
    data = (to_id,)
    cur = con.cursor()
    sql = "SELECT * FROM user_table WHERE id=?"
    in_sql = cur.execute(sql, data)
    res = in_sql.fetchall()
    cur.close()
    return template("user/user_form.html", res=res)


@user.post("/post_form/<to_id:int>")
def user_form_post(to_id):
    heading = request.forms.get("title")
    upload = img_upload(to_id)
    # ..
    data = heading, upload, f_dt, to_id
    cur = con.cursor()
    sql = "UPDATE user_table SET name=?, upload=?, changed=? WHERE id=?"
    cur.execute(sql, data)
    con.commit()
    cur.close()
    return redirect(f"/user/{to_id}")


@user.route("/post_delete/<to_id:int>")
def user_delete(to_id):
    data = (to_id,)
    cur = con.cursor()
    sql = "DELETE FROM user_table WHERE id=?"
    cur.execute(sql, data)
    con.commit()
    cur.close()
    return redirect("/user")
