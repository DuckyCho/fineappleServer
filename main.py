# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Flask;
from flaskext.mysql import MySQL;
from flask import request, session;
from flaskext.flask_login import LoginManager, login_user, UserMixin, make_secure_token;
#from flaskext.flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin, confirm_login, fresh_login_required
from flaskext.flask_itsdangerous import URLSafeTimedSerializer;
import datetime
import time

app = Flask(__name__);

#초기 설정
app.secret_key = "scret"
login_manager = LoginManager()
mysql = MySQL();
login_serializer = URLSafeTimedSerializer(app.secret_key);
app.config['MYSQL_DATABASE_USER'] = 'scret';
app.config['MYSQL_DATABASE_PASSWORD'] = 'secret';
app.config['MYSQL_DATABASE_DB'] = 'secret';

login_manager.init_app(app);
mysql.init_app(app);

#DB관련 함수

#connectDB
#	mysql db 에 접근하여 cursor를 리턴한다.
#	접근할 db 명, 계정, 비밀번호는 위의 초기설정 부분에서 app.config로 정의
def connectDB():
	cursor = mysql.connect().cursor();
	return cursor;


#User 클래스와 관련 함수
class User(UserMixin):
	#User class
	#  Variables
	#    email : string (encoding UTF-8)
	#    password : string (encoding UTF-8, encrypted by using sha1)
	#    active, authenticate, anonymous : bool
	#    loginDate :  datetime (datetime.utcnow)
	def __init__(self, email, password):
		self.email = email.encode('utf8');
		self.password = password;
		
		if email == "":
			self.anonymous = True;
		else:
			self.anonymous = False;
		self.active = False;
		self.authenticate = False;
		self.loginDate = datetime.datetime.utcnow();

	def is_active(self):
		return self.active;
	def is_authenticated(self):
		return self.authenticate;
	def is_anonymous(self):
		return self.anonymous;
	def get_id(self):
		return self.email;
	def get_auth_token(self):
		userToken = [self.email,self.password];
		data = login_serializer.dumps(userToken);
		return data;
	@staticmethod
	def getUserFromDB(cursor,email):
		cursor.execute("select * from USER where email='"+email+"'");
		data = cursor.fetchone();
		if data != None:
			user = User(email,data[1]);
			user.active = True;
			user.authenticate = True;
			user.anonymous = False;
			return user;
		else:
			return None;

@login_manager.user_loader
def load_user(email):
	cursor = connectDB();
	return User.getUserFromDB(cursor,email);

@login_manager.token_loader
def load_token(token):
	print "rememberToken : %s"%token;
	cursor = connectDB();
	data = login_serializer.loads(token);
	user = User.getUserFromDB(cursor,data[0]);

	if user != None and data[1] == user.password:
		user.active = True;
		user.authenticate = True;
		user.anonymous = False;
		return user;
	else:
		return None;

def printUserStatus(user,comment):
	print "****comment : %s" %comment;
	print "****userEmail : %s" %user.email;
	print "****userLoginDate : %s" %user.loginDate;



#Application Module

@app.route("/veryFirstConnect", methods=["POST"])
def veryFirstConnect():
	time.sleep(5);
	print request.headers;
	token,session = request.headers.get("Cookie").split(' ');
	tokenName, tokenValue = token.split('=');
	sessionName, sessionValue = session.split('=');
	tokenValue = tokenValue.replace(';','');
	user = load_token(tokenValue);
	if user != None:
		printUserStatus(user,'newConnection - /veryFirstConnection');
		email = user.email;
		cursor = connectDB();
		cursor.execute("select * from USER where email='"+email+"'");
		userTableData = cursor.fetchone();
		cursor.execute("select * from BOOKLIST_READ where userID='"+email+"'");
		readTableData = cursor.fetchone();
		cursor.execute("select * from BOOKLIST_WISH where userID='"+email+"'");
		wishTableData = cursor.fetchone();
		if userTableData is None:
			return "initProfile";
		elif (readTableData is None) and (wishTableData is None):
			return "setBookFirst";
		else:
			return "recommend"
	else:
		return "login";

@app.route("/login", methods=["POST"])
def login():
	time.sleep(5);
	email = request.form.get('email');
	password = request.form.get('password'); 
	cursor = connectDB();
	user = User.getUserFromDB(cursor,email);
	if user!=None and user.password == password:
		login_user(user,remember = True,force = False);
		return "YES";
	else:
		return "NO";


@app.route("/test", methods=["GET", "POST"])
def test():
	return "test load!!";


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5009);

