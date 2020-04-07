from . import models
import datetime
import hashlib


def hash_code(s, salt='Login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_code_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.confirmString.objects.create(code=code, user=user)
    return code
