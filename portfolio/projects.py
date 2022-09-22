from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from portfolio.auth import login_required
from portfolio.db import get_db

bp = Blueprint('projects', __name__)


@bp.route('/projects/')
def projects():
    db = get_db()
    all_projects = db.execute(
        'SELECT p.id, title, body, technologies, created, author_id, username'
        ' FROM project p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('projects/projects.html', projects=all_projects)


@bp.route('/projects/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        technologies = request.form['technologies']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO project (title, body, technologies, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, technologies, g.user['id'])
            )
            db.commit()
            return redirect(url_for('projects.projects'))

    return render_template('projects/create.html')


def get_project(id, check_author=True):
    project = get_db().execute(
        'SELECT p.id, title, body, technologies, created, author_id, username'
        ' FROM project p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if project is None:
        abort(404, f"Project id {id} doesn't exist.")

    if check_author and project['author_id'] != g.user['id']:
        abort(403)

    return project


@bp.route('/projects/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    project = get_project(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        technologies = request.form['technologies']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE project SET title=?, body =?, technologies = ?'
                ' WHERE id = ?',
                (title, body, technologies, id)
            )
            db.commit()
            return redirect(url_for('projects.projects'))

    return render_template('projects/update.html', project=project)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_project(id)
    db = get_db()
    db.execute('DELETE FROM project WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('projects.projects'))
