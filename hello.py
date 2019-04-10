from flask import Flask,render_template
from flask_bootstrap import Bootstrap #包含了jQuery
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '我是密钥'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = wtforms.StringField('what is your name?', validators = [DataRequired()])
    submit = wtforms.SubmitField('Submit')

@app.route('/',methods = ['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit(): #如果是一个post请求并且有效返回True ,初次打开页面时提交给服务器的是一个包含空表单的GET请求所以返回False
        name = form.name.data 
        form.name.data = '' #清空name
    return render_template('index.html',current_time = datetime.utcnow(),form = form, name = name) #utc是协调世界时间(coordinated universal time)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name = name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

if __name__ == "__main__":
    app.run(debug = True)   