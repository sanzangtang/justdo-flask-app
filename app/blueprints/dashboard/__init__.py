from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.blueprints.dashboard.forms import ToDoForm, KeepDoForm
from app.blueprints.user.models import User, ToDoList
from flask import session
from flask import g

bp_dashboard = Blueprint('bp_dashboard', __name__)


def pagination_builder(pag_obj, query, **kwargs):
    next_page = pag_obj.next_num
    prev_page = pag_obj.prev_num
    total_pages = pag_obj.pages
    if total_pages == 0:
        total_pages = 1  # default at 1 page
    if prev_page is None:
        prev_page = total_pages  # total number of pages

    # should change this hard coded url, but leave it for now
    next_url = url_for('bp_dashboard.dashboard', **{query: next_page})
    prev_url = url_for('bp_dashboard.dashboard', **{query: prev_page})

    # default
    pag_args = {'next_url': next_url,
                'prev_url': prev_url,
                'total_pages': total_pages
                }

    # update additional keyword arguments if any
    pag_args.update(kwargs)
    return pag_args


@bp_dashboard.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    # initialize the current user
    user = User.find_by_username(current_user.username)

    # initialize forms
    todo_form = ToDoForm()
    keepdo_form = KeepDoForm()

    # query url '?todopage=' and '?keepdopage='
    todo_page = request.args.get('todopage', 1, type=int)
    keepdo_page = request.args.get('keepdopage', 1, type=int)

    # initialize pagination objects and build necessary arguments
    todolist = user.todolist.order_by(ToDoList.status.desc(),
                                      ToDoList.timestamp.desc()
                                      ).paginate(todo_page, 8, False)
    keepdolist = user.keepdolist.paginate(keepdo_page, 8, False)
    todo_args = pagination_builder(
        todolist, 'todopage', form=todo_form, page=todo_page, todolist=todolist.items)
    keepdo_args = pagination_builder(
        keepdolist, 'keepdopage', form=keepdo_form, page=keepdo_page, keepdolist=keepdolist.items)

    # initialize session keys for the first time
    # will not run those lines afterwards
    # those session keys will be used in generating templates
    if not 'todolist_collapse' in session:
        session['todolist_collapse'] = 'in'  # default expand todolist panel
        session['keepdolist_collapse'] = 'in' # default expand keepdolist panel

    return render_template('dashboard.html', todo_args=todo_args, keepdo_args=keepdo_args)


@bp_dashboard.route('/session', methods=['POST'])
def session_manager():
    if current_user.is_authenticated:
        # iterate through the requested form and set session cookies
        for key in request.form:
            # Important: the variable name sent from frontend must be consistent with backend
            session[key] = request.form[key]
        return 'Session updated.', 200


# since there are two forms on the same page
# thus separating the routes for handling them
@bp_dashboard.route('/add-todo', methods=['POST'])
def add_todo():
    if current_user.is_authenticated:
        todo_form = ToDoForm()
        if todo_form.validate_on_submit():
            todo = ToDoList(task=todo_form.task.data,
                            status='incomplete',
                            user_id=current_user.id)
            db.session.add(todo)
            db.session.commit()
            flash('Your ToDo is alive', 'alert alert-success')
        else:
            # easy way to show errors after redirecting
            flash(todo_form.task.errors[0], 'alert alert-danger')
        return redirect(url_for('bp_dashboard.dashboard'))


@bp_dashboard.route('/drop-todo', methods=['POST'])
def drop_todo():
    if current_user.is_authenticated:
        todo_id = request.form['todo_id']
        todo = ToDoList.find_by_id(int(todo_id))
        db.session.delete(todo)
        db.session.commit()
        return 'Successfully dropped.', 200


@bp_dashboard.route('/update-todo', methods=['POST'])
def update_todo():
    if current_user.is_authenticated:
        # get data
        todo_id = request.form['todo_id']
        task = request.form['task']
        status = request.form['status']

        # create a todo instance and update its data
        todo = ToDoList.find_by_id(int(todo_id))
        if status != "":
            todo.status = status
        if task != "":
            todo.task = task
        db.session.commit()
        return 'Successfully updated.', 200


@bp_dashboard.route('/add-keepdo', methods=['POST'])
def add_keepdo():
    return 'add keepdo'


@bp_dashboard.route('/drop-keepdo', methods=['POST'])
def drop_keepdo():
    return 'drop keepdo'


@bp_dashboard.route('/update-keepdo', methods=['POST'])
def update_keepdo():
    return 'update keepdo'
