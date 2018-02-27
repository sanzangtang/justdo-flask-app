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
    page = request.args.get('page', 1, type=int)
    user = User.find_by_username(current_user.username)
    # todolist pagination
    todolist = user.todolist.order_by(ToDoList.status.desc(),
                                      ToDoList.timestamp.desc()
                                      ).paginate(page, 8, False)
    next_page = todolist.next_num
    prev_page = todolist.prev_num
    total_pages = todolist.pages
    if total_pages == 0:
        total_pages = 1 # defualt at least 1 page
    if prev_page is None:
        prev_page = total_pages # total number of pages
    next_url = url_for('bp_dashboard.dashboard', page=next_page)
    prev_url = url_for('bp_dashboard.dashboard', page=prev_page)

    if form.validate_on_submit():
        todo = ToDoList(task=form.task.data,
                        status='incomplete',
                        user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        flash('Your ToDo is alive', 'alert alert-success')
        return redirect(url_for('bp_dashboard.dashboard'))
    return render_template('dashboard.html', form=form, todolist=todolist.items,
                           next_url=next_url, prev_url=prev_url, page=page,
                           total_pages=total_pages)


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
