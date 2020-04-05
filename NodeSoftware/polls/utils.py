from django.contrib.auth.hashers import *
from django.contrib.auth import authenticate, login

from .models import Login

def gen_login_data(given_password):
    hasher = get_hasher()
    salt = hasher.salt()
    hashed_password = hasher.encode(given_password, salt)
    login_data = {'salt' : salt, 'hashed_password' : hashed_password}
    return login_data

def authenticate_user(user_ID, entered_password):
    hasher = get_hasher()
    login_data = Login.objects.get(username = user_ID)
    salt = login_data.salt
    hashed_entry = hasher.encode(entered_password, salt)

    if (hashed_entry == login_data.hashed_password):
        return True
    else:
        return False
