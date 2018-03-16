from app import app

# for shell context
from app import db
from app.blueprints.user.models import User, ToDoList, KeepDoList

@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'User': User,
            'ToDoList': ToDoList,
            'KeepDoList': KeepDoList,
            }

if __name__ == '__main__':
    app.run(debug=True)
