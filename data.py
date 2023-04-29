
import bcrypt
from composite.parts import f_dt


salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(b"password", salt)


d_user = [
    ("First user name", "one@gmail.com", hashed, f"{f_dt}"),
    ("Second user name", "two@gmail.com", hashed, f"{f_dt}"),
]
d_blog = [
    ("First post title", "First post story", f"{f_dt}", "1"),
    ("Second post title", "Second post story", f"{f_dt}", "2"),
]
d_chat = [
    ("First chat story", f"{f_dt}", "1"),
    ("Second chat story", f"{f_dt}", "2"),
]
