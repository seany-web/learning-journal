import datetime

from peewee import *

DATABASE = SqliteDatabase('learningjournal.db')

class JournalEntry(Model):
    title = CharField()
    date_created = DateField()
    time_spent = IntegerField()
    content_learnt = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-date_created',)


def initialise():
    DATABASE.connect()
    DATABASE.create_tables([JournalEntry], safe=True)
    DATABASE.close()