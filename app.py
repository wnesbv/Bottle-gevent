
import gevent.monkey; gevent.monkey.patch_all()
from geventwebsocket.handler import WebSocketHandler

from bottle import (
    run,
    request,
    template,
    Bottle,
    GeventServer
)


from chat.urls import chat

from auth.urls import auth
from blog.urls import blog
from user.urls import user

from imp_exp_csv.urls import filecsv

from composite.parts import parts


app = Bottle()

app.mount("/auth", auth)
app.mount("/blog", blog)
app.mount("/chat", chat)
app.mount("/user", user)
app.mount("/csv", filecsv)

app.mount("/static", parts)


users = set()


@app.route("/")
def index():
    return template("index.html")

@app.route("/messages")
def messages():
    msg = request.query["msg"]
    return template("messages.html", msg=msg)


if __name__ == "__main__":

    run(
        app,
        host="127.0.0.1",
        port=8080,
        server=GeventServer,
        handler_class=WebSocketHandler,
        reloader=True,
    )
