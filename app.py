from flask import Flask, g, redirect, render_template, url_for

import models
import forms

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = '#&Fiujg73KDusr$%WfihnfFWgnfvER'

@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return(response)


@app.route('/')
@app.route('/entries')
def index():
    stream = models.JournalEntry.select()
    return render_template('index.html', stream=stream)


@app.route('/entries/new', methods=('GET', 'POST'))
def new_entry():
    form = forms.JournalEntryForm()
    if form.validate_on_submit():
        models.JournalEntry.create(
            title = form.title.data,
            date_created = form.created_date.data,
            time_spent = form.time_spent.data,
            content_learnt = form.content_learnt.data.strip(),
            resources = form.resources.data.strip()
        )
        return redirect('/entries')
    return render_template('new.html', form=form)


@app.route('/entries/<int:id>')
def get_entry(id):
    return render_template('detail.html')


@app.route('/entries/<int:id>/edit')
def edit_entry(id):
    return render_template('edit.html')


@app.route('/entries/<int:id>/delete')
def delete_entry(id):
    return render_template('index.html')


if __name__ == '__main__':
    models.initialise()
    app.run(debug=DEBUG, host=HOST, port=PORT)