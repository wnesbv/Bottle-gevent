
import json
from bottle import (
    Bottle,
    template,
    request,
)
from geventwebsocket import WebSocketError
from composite.parts import con, f_dt, visited, who_is_who


chat = Bottle()


def save_msg(story):
    user_list = who_is_who()[0]

    data = (story, f_dt, user_list)
    cur = con.cursor()
    sql = "INSERT INTO chat_table (story, generated, user_list)VALUES (?,?,?)"
    cur.execute(sql, data)
    con.commit()
    cur.close()
    return data

def save_img(upload):
    user_list = who_is_who()[0]
    img = f"/static/chat/{upload}"

    data = (img, f_dt, user_list)
    cur = con.cursor()
    sql = "INSERT INTO chat_table (upload, generated, user_list)VALUES (?,?,?)"
    cur.execute(sql, data)
    con.commit()
    cur.close()
    return data


# .. user


@chat.route("/")
@visited()
def chat_all_get():
    user_list = who_is_who()[0]
    # ..
    cur = con.cursor()
    cur.execute("SELECT * FROM chat_table")
    res = cur.fetchall()
    cur.close()
    return template("chat/chat.html", res=res, user_list=user_list)


# ..


clients = set()

def broadcast(msg):
    user = who_is_who()[2]
    for client in [*clients]:
        try:
            client.send(msg)
            print("send..! user.. {} client..{}".format(user, client))
            print("wsock.. cont = {}".format(len(clients)))
        except WebSocketError as exc:
            print("Error..! {}".format(exc))
            clients.remove(client)
            print("remove..! {}".format(client))


@chat.route("/websocket")
def my_chat():
    wsock = request.environ.get("wsgi.websocket")

    while True:
        user = who_is_who()[2]
        clients.add(wsock)
        msg = wsock.receive()
        print("receive..! user.. {}".format(user))

        if not msg:
            break

        data = json.loads(msg)

        if data.get("fle"):
            save_img(data.get("fle"))
            print("save file..!")
        if data.get("msg"):
            save_msg(data.get("msg"))
            print("save msg..!")
        msg = json.dumps(data)
        broadcast(msg)

# .. group


@chat.route("/group")
@visited()
def group_chat_index():
    cur = con.cursor()
    cur.execute("SELECT * FROM chat_table")
    res = cur.fetchall()
    cur.close()
    return template("chat/group_chat.html", res=res)


@chat.route("/groupchat")
def group_chat():
    wsock = request.environ.get("wsgi.websocket")

    while True:
        data = wsock.receive()

        if not data:
            break

        wsock.send(data)
        save_msg(data)
        print("msg..!", data)
