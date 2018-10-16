from flask_wtf import Form,FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
class LoginForm(FlaskForm):
    name=StringField('账户:',validators=[DataRequired()])
    password=StringField('密码:',validators=[DataRequired()])
    submit=SubmitField('登录')
    cancel=SubmitField('重置')