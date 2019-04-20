from flask import Flask,render_template,session,redirect,url_for,flash
from flask_bootstrap import Bootstrap #包含了jQuery
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
import wtforms,os,pymysql
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail,Message


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Cogi:123@129.204.25.212/cogi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'q935462955@163.com'
app.config['MAIL_PASSWORD'] = 'q885427637' #'uknlhbmbttmmbeca'
app.config['SECRET_KEY'] = '我是密钥'
db = SQLAlchemy(app)
migrate = Migrate(app,db)
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)

@app.shell_context_processor
def make_shell_context():
        return dict(db = db, User = User, Role = Role)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    users = db.relationship('User',backref = 'role', lazy = 'dynamic')
    

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64),unique =True, index = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(FlaskForm):
    name = wtforms.StringField('what is your name?', validators = [DataRequired()])
    submit = wtforms.SubmitField('Submit')

@app.route('/email_send_charactor/')
def email_send_charactor():
    message = Message(subject = 'hello flask-mail',sender = 'q935462955@163.com',recipients = ['935462955@qq.com'],body = 'flask-mail测试代码')
    try:
        with app.app_context():
            mail.send(message)
        return '发送成功，请查收'
    except Exception as e:
        print(e)
        return '发送失败'

@app.route('/',methods = ['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit(): #如果是一个post请求并且有效返回True ,初次打开页面时提交给服务器的是一个包含空表单的GET请求所以返回False
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data,role_id = 3)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',current_time = datetime.utcnow(),form = form, name = session.get('name'),known = session.get('known',False)) #utc是协调世界时间(coordinated universal time)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name = name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

@app.route('/map')
def showmap():
    return render_template('main.html')

if __name__ == "__main__":
    app.run(debug = True)   