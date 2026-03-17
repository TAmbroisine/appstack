import functools

from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

bp = Blueprint('tasks', __name__)

@bp.route('/tasks', methods=('GET', 'POST', 'DELETE'))
def tasks():
    if request.method == 'GET':
        task = get_db().execute(
            'SELECT id, task, created FROM tasks ORDER BY created DESC'
        ).fetchall()
        return task
    if request.method == 'POST':
        task = request.form['task']
        error = None

        if not task:
            error = 'Task is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                    'INSERT INTO tasks (task) VALUES (?)',
                    (task)
            )
            db.commit()

    return render_template("tbd")
