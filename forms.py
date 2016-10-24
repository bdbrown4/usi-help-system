from flask_wtf import Form
from wtforms import StringField,BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid=StringField('openid',validators=[DataRequired()])
    remember_me=BooleanField('remember_me',default=False)

class ItemForm(Form):
    item=StringField('item',validators=[DataRequired()])

class DelForm(Form):
    id=StringField('id',validators=[DataRequired()])

# EditForm used for editing
class EditForm(Form):
    id = StringField('id', validators=[DataRequired()])
    editItem = StringField('item', validators=[DataRequired()])
