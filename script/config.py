# coding: utf-8

from enum import Enum

TOKEN = '1004026853:AAH7TyM-PhWKoR8j0XZcraIyKTIif0pqFbs'
db_file = "database.vdb"


class States(Enum):
    """
    Используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)

    Use the Vedis database, in which the stored values are always strings,
    so here we will also use strings (str)
    """
    S_START = "0"  # Start a new dialogue
    S_ENTER_NAME = "1"
    S_ENTER_AGE = "2"
    #S_SEND_PIC = "3"
