from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length


class ToDoForm(FlaskForm):
    task = StringField('Do Something', validators=[
                       Length(min=3, message='Do something.'),
                       Length(max=70, message='Uh-oh, try to keep it simple.')])
    submit = SubmitField('Do it')
