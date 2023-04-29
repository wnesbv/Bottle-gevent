import sqlite3
from data import d_user, d_blog, d_chat

con = sqlite3.connect("sqlite.db")


def creat_table():
    cur = con.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS user_table(
            id INTEGER PRIMARY KEY,
            name TEXT VARCHAR(30) UNIQUE NOT NULL,
            mail TEXT VARCHAR(30) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            upload TEXT,
            email_verified BOOLEAN DEFAULT(FALSE),
            is_active  BOOLEAN DEFAULT(FALSE),
            generated DATETIME NOT NULL,
            changed DATETIME);
        CREATE TABLE IF NOT EXISTS blog_table(
            id INTEGER PRIMARY KEY,
            title TEXT VARCHAR(30) UNIQUE NOT NULL,
            story TEXT VARCHAR(200) NOT NULL,
            upload TEXT,
            generated DATETIME NOT NULL,
            changed DATETIME,
            user_list INTEGER,
            FOREIGN KEY(user_list) REFERENCES user_table(id));
        CREATE TABLE IF NOT EXISTS chat_table(
            id INTEGER PRIMARY KEY,
            story TEXT VARCHAR(200),
            choice_room TEXT VARCHAR(30),
            upload TEXT,
            generated DATETIME,
            changed DATETIME,
            user_list INTEGER,
            FOREIGN KEY(user_list) REFERENCES user_table(id));
        """
    )
    cur.executemany(
        "INSERT INTO user_table (name, mail, password, generated) VALUES(?,?,?,?)", d_user)
    cur.executemany(
        "INSERT INTO blog_table (title, story, generated, user_list) VALUES(?,?,?,?)", d_blog)
    cur.executemany(
        "INSERT INTO chat_table (story, generated, user_list) VALUES(?,?,?)", d_chat)
    con.commit()
    con.close()



creat_table()
