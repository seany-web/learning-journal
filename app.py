from flask import Flask, g, redirect, render_template, url_for, abort

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
    """Gets all Journal Entries and displays them on the index page"""
    entries = models.JournalEntry.select()
    return render_template('index.html', entries=entries)


@app.route('/entries/new', methods=('GET', 'POST'))
def new_entry():
    """Displays a form to the user to create a new Journal Entry"""
    form = forms.JournalEntryForm()
    if form.validate_on_submit():
        models.JournalEntry.create(
            title=form.title.data,
            date_created=form.created_date.data,
            time_spent=form.time_spent.data,
            content_learnt=form.content_learnt.data.strip(),
            resources=form.resources.data.strip()
        )
        return redirect('/entries')
    return render_template('new.html', form=form)


@app.route('/entries/<int:id>')
def get_entry(id):
    """Displays details information about a given Journal Entry"""
    entries = models.JournalEntry.select().where(
        models.JournalEntry.id == id
    )
    if entries.count() == 0:
        abort(404)
    return render_template('detail.html', entries=entries)


@app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
def edit_entry(id):
    """Displays a form so the user can edit a given Journal Entry"""
    try:
        entry = models.JournalEntry.get(
            models.JournalEntry.id == id
        )
    except models.DoesNotExist:
        abort(404)
    else:
        form = forms.JournalEntryForm(obj=entry)
        if form.validate_on_submit():
            entry.title = form.title.data
            entry.date_created = form.created_date.data
            entry.time_spent = form.time_spent.data
            entry.content_learnt = form.content_learnt.data
            entry.resources = form.resources.data
            entry.save()
            return redirect(url_for('index'))
    return render_template('edit.html', form=form, entry=entry)


@app.route('/entries/<int:id>/delete')
def delete_entry(id):
    """Deletes a given Journal Entry"""
    try:
        entry = models.JournalEntry.get(
            models.JournalEntry.id == id
        )
        entry.delete_instance()
        return redirect(url_for('index'))
    except models.DoesNotExist:
        abort(404)


@app.errorhandler(404)
def not_found(error):
    """Displays a custom 404 error message if the page cannot be found"""
    return render_template('404.html'), 404


if __name__ == '__main__':
    models.initialise()
    app.run(debug=DEBUG, host=HOST, port=PORT)
