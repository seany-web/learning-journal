from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired

from models import JournalEntry

class JournalEntryForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired()]
    )
    created_date = DateField(
        'Date (DD/MM/YYYY)', format='%d/%m/%Y', validators=[DataRequired()]
    )
    time_spent = IntegerField(
        'Time Spent (Minutes)', validators=[DataRequired()]
    )
    content_learnt = TextAreaField(
        'What you learnt', validators=[DataRequired()]
    )   
    resources = TextAreaField(
        'Useful Resources to Remember'
    )