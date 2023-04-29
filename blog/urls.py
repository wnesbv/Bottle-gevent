
import os, sqlite3
from bottle import request, redirect, template, Bottle
from composite.parts import (
    con,
    f_dt,
    visited,
    img_creat,
    post_file,
    img_upload,
)


blog = Bottle()


@blog.route("/<to_id:int>")
def post_to_id(to_id):
    data = (to_id,)
    cur = con.cursor()
    sql = "SELECT * FROM blog_table WHERE id=?"
    in_sql = cur.execute(sql, data)
    res = in_sql.fetchall()
    cur.close()
    return res


@blog.route("/")
def blog_list():
    cur = con.cursor()
    sql = "SELECT * FROM blog_table"
    in_sql = cur.execute(sql)
    res = in_sql.fetchall()
    cur.close()
    return template("blog/blog.html", res=res)


@blog.route("/<to_id:int>")
def post_detail(to_id):
    res = post_to_id(to_id)
    return template("blog/detail.html", res=res)


# .. creat
@blog.route("/post-form")
@visited()
def creat_post_form():
    return template("blog/creat_post_form.html")


@blog.post("/post-form")
#@visited()
def creat_post():
    heading = request.forms.get("title")
    description = request.forms.get("story")
    upload = img_creat()
    # ..
    original = upload
    removed = original.replace(".", "", 1)
    # ..
    data = heading, description, removed, f_dt
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO blog_table (
            title, story, upload, generated
        )VALUES (?,?,?,?)
        """,
        data
    )
    con.commit()
    cur.close()
    return redirect("/blog")


# .. update
@blog.route("/post-form/<to_id:int>")
def post_form_get(to_id):
    res = post_to_id(to_id)
    return template("blog/post_form.html", res=res)


@blog.post("/post-form/<to_id:int>")
def post_form_update(to_id):
    title = request.forms.get("title")
    story = request.forms.get("story")
    upload = img_upload(to_id)
    # ..
    original = upload
    removed = original.replace(".", "", 1)
    # ..
    data = title, story, removed, f_dt, to_id
    cur = con.cursor()
    sql = "UPDATE blog_table SET title=?, story=?, upload=?, changed=? WHERE id=?"
    cur.execute(sql, data)
    con.commit()
    cur.close()
    return redirect(f"/blog/{to_id}")


@blog.route("/post-delete/<to_id:int>")
def post_delete(to_id):
    data = (to_id,)
    cur = con.cursor()
    sql = "DELETE FROM blog_table WHERE id=?"
    cur.execute(sql, data)
    con.commit()
    cur.close()
    return redirect("/blog")


# .. img delete
def img_update(upload, to_id):
    data = upload, to_id
    cur = con.cursor()
    sql = "UPDATE blog_table SET upload=? WHERE id=?"
    cur.execute(sql, data)
    con.commit()
    cur.close()


@blog.route("/img-delete/<to_id:int>")
def img_delete(to_id):
    original = post_file(to_id)
    upload = "." + original
    # ..
    img_update(upload, to_id)
    # ..
    file_delete = post_file(to_id)
    os.remove(file_delete)
    while True:
        upload = None
        # ..
        img_update(upload, to_id)
        # ..
        return redirect(f"/blog/{to_id}")
