from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.blueprints.dashboard.forms import ToDoForm
from app.blueprints.user.models import User, ToDoList

bp_dashboard = Blueprint('bp_dashboard', __name__)


@bp_dashboard.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ToDoForm()
    user = User.find_by_username(current_user.username)
    todolist = user.todolist.order_by(ToDoList.status.desc(),
                                      ToDoList.timestamp.desc()
                                      )
    if form.validate_on_submit():
        todo = ToDoList(task=form.task.data,
                        status='incomplete',
                        user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        flash('Your ToDo is alive', 'alert alert-success')
        return redirect(url_for('bp_dashboard.dashboard'))
    return render_template('dashboard.html', form=form, todolist=todolist)


# another consideration: add login_required?
@bp_dashboard.route('/drop-todo', methods=['GET', 'POST'])
def drop_todo():
    # currently todo id is not specific for each user
    if request.method == 'POST':
        if current_user.is_authenticated:
            todo_id = request.form['todo_id']
            todo = ToDoList.find_by_id(int(todo_id))
            db.session.delete(todo)
            db.session.commit()
            return 'Successfully dropped.', 200
    abort(404)


@bp_dashboard.route('/update-todo', methods=['GET', 'POST'])
def update_todo():
    if request.method == 'POST':
        if current_user.is_authenticated:
            # get request data
            todo_id = request.form['todo_id']
            task = request.form['task']
            status = request.form['status']
            # create todo instance
            todo = ToDoList.find_by_id(int(todo_id))
            if not status == "":
                todo.status = status
            if not task == "":
                todo.task = task
            db.session.commit()
            return 'Successfully updated.', 200
    abort(404)
