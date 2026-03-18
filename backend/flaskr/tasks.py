import functools

from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from sqlalchemy import text

from flaskr.db import get_db

bp = Blueprint('tasks', __name__)

@bp.route('/api/tasks', methods=('GET', 'POST'))
def tasks_list():

    if request.method == 'POST':
        data = request.get_json()
        task = data.get('task')
        error = None

        if not task:
            error = 'Task is required.'

        if error is not None:
            return {'error': error}, 400
        else:
            db = get_db()
            db.execute(
                text('INSERT INTO tasks (task) VALUES (:task)'),
                {'task': task}
            )
            db.commit()
            return {'success': True}
    elif request.method == 'GET':
        result = get_db().execute(
            text('SELECT id, task, created FROM tasks ORDER BY created DESC')
        ).fetchall()
        # Convert Row objects to dictionaries
        return [{'id': row[0], 'task': row[1], 'created': row[2]} for row in result]
    else:
        return {'error': 'Method not allowed'}, 405

@bp.route('/api/tasks/<int:task_id>', methods=('DELETE',))
def delete_task(task_id):
    error = None

    if not task_id:
        error = 'Task ID is required.'

    if error is not None:
        return {'error': error}, 400
    else:
        db = get_db()
        db.execute(
            text('DELETE FROM tasks WHERE id = :id'),
            {'id': task_id}
        )
        db.commit()
        return {'success': True}
