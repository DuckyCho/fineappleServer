# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Flask;
from flaskext.mysql import MySQL;
from flask import request, session;
from flask import jsonify;
from flask_login import LoginManager, login_user, UserMixin, make_secure_token;
from itsdangerous import URLSafeTimedSerializer;
import datetime
import time
import json
app = Flask(__name__);

# 초기 설정
app.secret_key = "secret"
login_manager = LoginManager()
mysql = MySQL();
login_serializer = URLSafeTimedSerializer(app.secret_key);
app.config['MYSQL_DATABASE_USER'] = 'root';
app.config['MYSQL_DATABASE_PASSWORD'] = 'next!!@@##$$'
app.config['MYSQL_DATABASE_DB'] = 'finedb';


login_manager.init_app(app);
mysql.init_app(app);

# DB관련 함수

#connectDB
#	mysql db 에 접근하여 cursor를 리턴한다.
#	접근할 db 명, 계정, 비밀번호는 위의 초기설정 부분에서 app.config로 정의
def connectDB():
	cursor = mysql.connect().cursor();
	return cursor;

def newLikeScrap(tableName,columnName,postId,email):
	if tableName == "SCRAP":
		cursor_tmp = connectDB();
		cursor_tmp.execute("select USER_email from POST where postId="+postId+";");
		postAuthor = cursor_tmp.fetchone();
		postAuthor = postAuthor[0];
		if postAuthor == email:
			return;
	conn = mysql.connect();
	cursor = conn.cursor();
	queryToPostTable = "update POST set "+columnName+" = "+columnName+" + 1 where postId="+postId+";";
	queryToDefinedTable = "insert into `"+tableName+"` values("+postId+",'"+email+"');";
	print queryToPostTable;
	print queryToDefinedTable;
	cursor.execute(queryToPostTable);
	conn.commit();
	cursor.execute(queryToDefinedTable);
	conn.commit();

def removeLikeScrap(tableName,columnName,postId,email):
	conn = mysql.connect();
	cursor = conn.cursor();
	queryToPostTable = "update POST set "+columnName+" = "+columnName+" - 1 where postId="+postId+";";
	queryToDefinedTable = "delete from `"+tableName+"` where POST_postId="+postId+" and USER_email='"+email+"';";
	print queryToPostTable;
	print queryToDefinedTable;
	cursor.execute(queryToPostTable);
	conn.commit();
	cursor.execute(queryToDefinedTable);
	conn.commit();

def newCommentOnPost(postId,email,comment):
	conn = mysql.connect();
	cursor = conn.cursor();
	queryToPostTable = "update POST set commentCount = commentCount + 1 where postId="+postId+";";
	queryToCommentTable = "insert into COMMENT (comment,POST_postId,USER_email) values('"+comment+"',"+postId+",'"+email+"');";
	cursor.execute(queryToPostTable);
	cursor.execute(queryToCommentTable);
	conn.commit();

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
		userToken = [self.email, self.password];
		data = login_serializer.dumps(userToken);
		return data;

	@staticmethod
	def getUserFromDB(cursor, email):
		cursor.execute("select * from USER where email='" + email + "'");
		data = cursor.fetchone();
		if data != None:
			user = User(email, data[1]);
			user.active = True;
			user.authenticate = True;
			user.anonymous = False;
			return user;
		else:
			return None;


@login_manager.user_loader
def load_user(email):
	cursor = connectDB();
	return User.getUserFromDB(cursor, email);


@login_manager.token_loader
def load_token(token):
	print "rememberToken : %s" % token;
	cursor = connectDB();
	data = login_serializer.loads(token);
	user = User.getUserFromDB(cursor, data[0]);

	if user != None and data[1] == user.password:
		user.active = True;
		user.authenticate = True;
		user.anonymous = False;
		return user;
	else:
		return None;


def printUserStatus(user, comment):
	print "****comment : %s" % comment;
	print "****userEmail : %s" % user.email;
	print "****userLoginDate : %s" % user.loginDate;


#Application Module

@app.route("/veryFirstConnect", methods=["POST"])
def veryFirstConnect():
	print request.headers;
	token, session = request.headers.get("Cookie").split(' ');
	tokenName, tokenValue = token.split('=');
	sessionName, sessionValue = session.split('=');
	tokenValue = tokenValue.replace(';', '');
	user = load_token(tokenValue);
	if user != None:
		printUserStatus(user, 'newConnection - /veryFirstConnection');
		email = user.email;
		cursor = connectDB();
		cursor.execute("select attendOrNot from USER where email='" + email + "'");
		userTableData = cursor.fetchone();
		cursor.execute("select * from BOOKLIST_READ where USER_email='" + email + "'");
		readTableData = cursor.fetchone();
		cursor.execute("select * from BOOKLIST_WISH where USER_email='" + email + "'");
		wishTableData = cursor.fetchone();
		if userTableData[0] is None:
			return "InitProfile";
		elif (readTableData is None) and (wishTableData is None):
			return "MainTab";
		else:
			return "MainTab"
	else:
		return "Login";


@app.route("/login", methods=["POST"])
def login():
	email = request.form.get('email');
	password = request.form.get('password');
	cursor = connectDB();
	user = User.getUserFromDB(cursor, email);
	if user != None and user.password == password:
		login_user(user, remember=True, force=False);
		cursor = connectDB();
		cursor.execute("select attendOrNot from USER where email='" + email + "'");
		userTableData = cursor.fetchone();
		cursor.execute("select * from BOOKLIST_READ where USER_email='" + email + "'");
		readTableData = cursor.fetchone();
		cursor.execute("select * from BOOKLIST_WISH where USER_email='" + email + "'");
		wishTableData = cursor.fetchone();
		if userTableData[0] is None:
			return "InitProfile";
		elif (readTableData is None) and (wishTableData is None):
			return "MainTab";
		else:
			return "MainTab"
	else:
		return "LoginFail";



#initProfile
@app.route("/initProfile", methods=["POST"])
def initProfile():
	print request.headers
	tokenName,token = request.headers.get("Cookie").split("=");
	conn = mysql.connect();
	cursor = conn.cursor();
	user = load_token(token);
	email = user.email;
	attendOrNot = request.form.get('attendOrNot');
	semesterNum = request.form.get('semesterNum');
	majorFirst = request.form.get('majorFirst');
	majorSecond = request.form.get('majorSecond');
	if majorSecond == '\\N':
		majorSecond = 'DEFAULT';
	result = cursor.execute("update USER set attendOrNot="+attendOrNot+", semesterNum="+semesterNum+", majorNameFirst="+majorFirst+", majorNameSecond="+majorSecond+" where email='"+email+"'");
	conn.commit();
	return str(result);



#register
@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		name = request.form['userName']

		con = mysql.connect()
		cursor = con.cursor()

		query = "insert into USER \
        	(email, password, userName) values \
        	('" + email + "', '" + password + "', '" + name + "');"

		cursor.execute(query)
		con.commit()

		print("success!")
		return "OK! Query"
	
	return "Error"


@app.route('/register/email', methods=['POST'])
def check_Email():
	email = request.form['email']

	con = mysql.connect()
	cursor = con.cursor()

	cursor.execute("select * from USER where email='" + email + "';")
	check_e = cursor.fetchone()

	if check_e is None:
		print("None")
		return "None"
	else:
		return "exist"

@app.route('/bookDetail', methods=['POST','GET'])
def book_Detail():
	book_num = request.form['book_num']

	con = mysql.connect()
	cursor = con.cursor()

	cursor.execute("select * from BOOKINFO where book_num='" + book_num + "';")

	result = cursor.fetchone()

	print result

	return result


@app.route('/count', methods=['POST'])
def count():
	ISBN = request.form['ISBN']

	con = mysql.connect()
	cursor = con.cursor()

	cursor.execute("select READ_count,WISH_count from ISBN_PREFER where bookISBN='" + ISBN + "';")

	result = [];

	colums = tuple([d[0] for d in cursor.description])

	for row in cursor:
		result.append(dict(zip(colums,row)))

	print(result)

	return json.dumps(result)

@app.route('/setBookFirst', methods=['POST','GET'])
def setBookFirst():

	cursor = connectDB();
	
	print 'connetctDB'

	cursor.execute("select name,author,book_num,cover_img,ISBN from BOOKINFO order by rand() limit 15;")

	result = [];

	colums = tuple([d[0] for d in cursor.description])

	for row in cursor:
		result.append(dict(zip(colums,row)))

	print(result)

	#현재 한글 깨짐 현상 있
	return json.dumps(result)


@app.route('/readBook',methods=['POST','GET'])

def readBook():

	result = request.get_json()

	#bookInfoInNext_book_num = request.form['book_num']

	#cursor = connectDB()

	# 리드북에 포함되어 있나 확인하고 넣는다. O(n)
	#cursor.execute("insert USER_email, bookISBN values \ '"+email+"','"+bookInfoInNext_book_num+"' from BOOKLIST_READ;")

	# 넣은 후에 확인한다?

	return 'OK!'



@app.route('/wishBook', methods=['POST','GET'])

def wishBook():

	#USER_email = user.email

	email = request.form['email']

	bookInfoInNext_book_num = request.form['book_num']

	cursor = connectDB();

	cursor.execute("insert USER_email, bookISBN values \
		'"+email+"','"+bookInfoInNext_book_num+"' from BOOKLIST_WISH;")

	return 'OK!'



@app.route("/timeline",methods=["GET","POST"])
def timeline():
	count = request.headers.get("Count");
	count = count.replace(';','');
	if(int(count) == -1):
		cursor_count = connectDB();
		cursor_count.execute("select postId from POST order by postId desc limit 1;");	
		count = cursor_count.fetchone();
		count = str(count[0]+1);
	print request.headers;
	cursor = connectDB();
	cursor_new = connectDB();
	cursor_new2 = connectDB();
	cursor.execute("select * from POST join USER on POST.USER_email=USER.email left join (select * from BOOKINFO group by ISBN) as BI on POST.postISBN = BI.ISBN where postId<"+count+" order by postId desc limit 30;");
	dataFromDB = cursor.fetchall();
	dataArr = [];
	dataDict = {};
	keys = ['name','like','scrap','comment','bookTitle','postImg','post','comment1userName','comment1','postId','ISBN'];
	for postRow in dataFromDB:
		dataDict[keys[0]]=postRow[10];
		dataDict[keys[1]]=postRow[5];
		dataDict[keys[2]]=postRow[6];
		dataDict[keys[3]]=postRow[7];
		dataDict[keys[4]]=postRow[16];
		dataDict[keys[5]]=postRow[2];
		dataDict[keys[6]]=postRow[1];
		dataDict[keys[7]]='\N';
		dataDict[keys[8]]='\N';
		dataDict[keys[9]]=postRow[0];
		dataDict[keys[10]]=postRow[4];
		cursor_new.execute("select * from COMMENT where POST_postId='"+str(postRow[0])+"'");
		commentRow = cursor_new.fetchmany(1);
		j = 0;
		while j < 1 and j < len(commentRow):
			cursor_new2.execute("select userName from USER where email='"+commentRow[j][3]+"'");
			commentUserName = cursor_new2.fetchone();
			dataDict[keys[7]] = commentUserName[0];
			dataDict[keys[8]] = commentRow[j][1];
			j += 1;
		dataArr.append(dataDict);
		dataDict = dict();
	return json.dumps(dataArr);

@app.route("/getMyLikePostInfo",methods=["POST"])
def getMyLikePostInfo():
	tokenName,token = request.headers.get("Cookie").split("=");
	user = load_token(token);
	email = user.email;
	cursor = connectDB();
	cursor.execute("select * from `LIKE` where USER_email='"+email+"';");
	dataFromDB = cursor.fetchall();
	dataDict = {};
	for row in dataFromDB:
		dataDict[row[0]] = "IN";

	return json.dumps(dataDict);


@app.route("/mypost",methods=["GET","POST"])
def mypost():
	count = request.headers.get("Count");
	count = count.replace(';','');
	print count
	if(int(count) == -1):
		cursor_count = connectDB();
		cursor_count.execute("select postId from POST order by postId desc limit 1;");	
		count = cursor_count.fetchone();
		count = str(count[0]+1);
	tokenName,token = request.headers.get("Cookie").split("=");
	user = load_token(token);
	email = user.email;
	print request.headers;
	cursor = connectDB();
	cursor_new = connectDB();
	cursor_new2 = connectDB();
	cursor.execute("select * from POST join USER on POST.USER_email=USER.email left join (select * from BOOKINFO group by ISBN) as BI on POST.postISBN = BI.ISBN where postId<"+count+" && USER_email='"+email+"' order by postId desc limit 30;");
	dataFromDB = cursor.fetchall();
	dataArr = [];
	dataDict = {};
	keys = ['name','like','scrap','comment','bookTitle','postImg','post','comment1userName','comment1','postId','ISBN'];
	for postRow in dataFromDB:
		dataDict[keys[0]]=postRow[10];
		dataDict[keys[1]]=postRow[5];
		dataDict[keys[2]]=postRow[6];
		dataDict[keys[3]]=postRow[7];
		dataDict[keys[4]]=postRow[16];
		dataDict[keys[5]]=postRow[2];
		dataDict[keys[6]]=postRow[1];
		dataDict[keys[7]]='\N';
		dataDict[keys[8]]='\N';
		dataDict[keys[9]]=postRow[0];
		dataDict[keys[10]]=postRow[4];
		cursor_new.execute("select * from COMMENT where POST_postId='"+str(postRow[0])+"'");
		commentRow = cursor_new.fetchmany(1);
		j = 0;
		while j < 1 and j < len(commentRow):
			cursor_new2.execute("select userName from USER where email='"+commentRow[j][3]+"'");
			commentUserName = cursor_new2.fetchone();
			dataDict[keys[7]] = commentUserName[0];
			dataDict[keys[8]] = commentRow[j][1];
			j += 1;
		dataArr.append(dataDict);
		dataDict = dict();
	
	cursor.execute("select * from SCRAP where USER_email='"+email+"' && POST_postId<"+count+";");
	dataFromDB = cursor.fetchall();
	for row in dataFromDB:
		dataDict = dict();
		postId = str(row[0]);
		cursor.execute("select * from POST where postId="+postId+";");
		postData = cursor.fetchone();
		post = postData[1];
		postImg = postData[2];
		ISBN = postData[4];
		like = postData[5];
		scrap = postData[6];
		comment = postData[7];
		cursor.execute("select name from BOOKINFO where ISBN='"+ISBN+"';");
		bookTitle = cursor.fetchone();
		if bookTitle != None:
			bookTitle = str(bookTitle[0]);
		cursor.execute("select * from USER where email='"+email+"';");
		userData = cursor.fetchone();
		name = userData[2];
		cursor.execute("select * from COMMENT where POST_postId="+postId+";");
		commentData = cursor.fetchone();
		if commentData != None:
			comment1 = commentData[1];
			cursor.execute("select userName from USER where email='"+commentData[3]+"';");
			comment1userName = cursor.fetchone();
			comment1userName = comment1userName[0];
		else:
			comment1 = '\N';
			comment1userName = '\N';
		dataDict[keys[0]] = name;
		dataDict[keys[1]] = like;
		dataDict[keys[2]] = scrap;
		dataDict[keys[3]] = comment;
		dataDict[keys[4]] = bookTitle;
		dataDict[keys[5]] = postImg;
		dataDict[keys[6]] = post;
		dataDict[keys[7]] = comment1userName;
		dataDict[keys[8]] = comment1;
		dataDict[keys[9]] = postId;
		dataDict[keys[10]] = ISBN;
		dataDict['scrapByMe'] = 'yes';
		dataArr.append(dataDict);
	return json.dumps(dataArr);

@app.route("/timelineButton", methods=["POST"])
def timelineButton():
	print request.headers
	action = request.form.get('action');
	buttonType = request.form.get('type');
	necessaryValue = request.form.get('key');
	print action
	print buttonType
	print necessaryValue
	tokenName,token = request.headers.get("Cookie").split("=");
	user = load_token(token);
	email = user.email;
	#if action is 1 == 버튼이 활성화 상태인 경우
	if int(action) is 1:
		if buttonType == "like" or buttonType == "scrap":
			columnName = buttonType+"Count";
			tableName = buttonType.upper();
			newLikeScrap(tableName,columnName,necessaryValue,email);
		else:
			postId,comment = necessaryValue.split('/');
			postId = postId[6:];
			comment = postId[7:];
			newCommentOnPost(postId,email,comment);
	#action is 0 == 버튼이 비활성화로 바뀐 경우
	else:
		if buttonType == "like" or buttonType == "scrap":
			columnName = buttonType+"Count";
			tableName = buttonType.upper();
			removeLikeScrap(tableName,columnName,necessaryValue,email);
		
		print "delete";
	
	return "done";


@app.route("/test", methods=["GET", "POST"])
def test():
	return "test load!!";


if __name__ == "__main__":
	app.run(debug=True, host='10.73.45.83', port=5010);


