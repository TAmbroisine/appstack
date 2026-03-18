import functools

from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
)

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
                    'INSERT INTO tasks (task) VALUES (?)',
                    (task,)
            )
            db.commit()
            return {'success': True}
    elif request.method == 'GET':
        tasks = get_db().execute(
            'SELECT id, task, created FROM tasks ORDER BY created DESC'
        ).fetchall()
        return [dict(task) for task in tasks]
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
                'DELETE FROM tasks WHERE id = ?',
                (task_id,)
        )
        db.commit()
        return {'success': True}
