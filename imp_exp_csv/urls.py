
import os, sqlite3, csv
from bottle import get, post, route, request, redirect, template, view, Bottle
from composite.parts import con, visited


filecsv = Bottle()


def dump_user(to_id):
    data = (to_id,)
    cur = con.cursor()
    sql = "SELECT * FROM user_table WHERE id=?"
    res = cur.execute(sql, data)
    row = res.fetchone()
    cur.close()
    return row


def dump_blog(to_id):
    data = (to_id,)
    cur = con.cursor()
    sql = "SELECT * FROM blog_table WHERE user_list=?"
    res = cur.execute(sql, data)
    row = res.fetchone()
    cur.close()
    return row


# ..
def import_blog(data):
    cur = con.cursor()
    sql = "INSERT INTO blog_table (title, story, generated, user_list) VALUES (?,?,?,?)"
    res = cur.executemany(sql, data)
    con.commit()
    cur.close()
    return res


# ..
@filecsv.route("/dump-user/<to_id:int>")
def export_csv_user(to_id):
    with open("static/csv/csv_user.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "id",
            "name",
            "mail",
            "password",
            "upload",
            "email_verified",
            "is_active",
            "generated",
            "changed",
        ]

        i = dump_user(to_id)

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        dump = {
            "id": i[0],
            "name": i[1],
            "mail": i[2],
            "password": i[3],
            "upload": i[4],
            "email_verified": i[5],
            "is_active": i[6],
            "generated": i[7],
            "changed": i[8],
        }
        writer.writeheader()
        writer.writerow(dump)
        csvfile.close()
        return redirect("/messages?msg=Export csv User OK..!")


@filecsv.route("/dump-blog/<to_id:int>")
def export_csv_blog(to_id):
    with open("static/csv/csv_blog.csv", "w", newline="", encoding="utf-8") as csvfile:
        i = dump_blog(to_id)
        fieldnames = [
            "id",
            "title",
            "story",
            "upload",
            "generated",
            "changed",
            "user_list",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        dump = {
            "id": i[0],
            "title": i[1],
            "story": i[2],
            "upload": i[3],
            "generated": i[4],
            "changed": i[5],
            "user_list": i[6],
        }
        writer.writeheader()
        writer.writerow(dump)
        csvfile.close()
        return redirect("/messages?msg=Export csv blog OK..!")


@filecsv.route("/import-blog-csv")
def import_csv_blog():
    with open("static/csv/csv_blog.csv", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        data = [
            (
                i["title"],
                i["story"],
                str(i["generated"]),
                i["user_list"],
            )
            for i in reader
        ]
        import_blog(data)
        csvfile.close()
        return redirect("/messages?msg=Import csv OK..!")
