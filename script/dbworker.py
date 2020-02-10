# coding: utf-8

from vedis import Vedis
import config

## Trying to find out the "state" of the user from the database
# Пытаемся узнать из базы «состояние» пользователя
def get_current_state(user_id):
    with Vedis(config.db_file) as db:
        try:
            return db[user_id].decode()
        except KeyError:  # If for some reason there wasn't such a key
            return config.States.S_START.value  # default value - start of dialogue

# Save the current "state" of the user in our database
def set_state(user_id, value):
    with Vedis(config.db_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            # 
            return False
