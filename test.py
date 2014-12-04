from flask import Flask, request, session
from flaskext.mysql import MySQL
import json

#코드 리펙토링은 진행하지 않음. 일단 테스트 용으로 제작함.

app = Flask(__name__)

# 사용자 정보를 받기 

# 봤어요 버튼에 대한 요청 구현

@app.route('/read_it', method=['POST'])
def read_it():
	email = user.email #사용자 정보 받기
	book_num = request.form['book_num'] #클라이언트에서 선택한 Book의 Book Number가지고 오기

	con = mysql.connect()
	cursor = con.cursor()

	query = "insert into BOOKLIST_READ \
	(email, book_num) values \
	('" + email +"', '" + book_num + "');"

	cursor.execute(query)
	con.commit()

	print("success! read book")
	return "OK"

# 보고싶어요 버튼에 대한 요청 구현

@app.route('/wish_it', method=['POST'])
def wish_it():
	email = user.email
	book_num = request.form['book_num']
	
	con = mysql.connect()
	cursor = con.cursor()

	query = "insert into BOOKLIST_WISH \
	(email, book_num) values \
	('" + email +"', '" + book_num + "');"

	cursor.execute(query)
	con.commit()

	print("success! wish book")
	return "OK"

# 봤어요 버튼 취소에 대한 상태 업데이트 구현

@app.route('/read_it/delete', methods=['POST'])
def read_it_delete():
	email = user.email
	book_num = request.form['book_num']

	con = mysql.connect()
	cursor = con.cursor()

	query = "delete from BOOKLIST_READ \
	where email = '" + email + "' and book_num = '" + book_num + "' "

	cursor.execute(query)
	con.commit()

	print("delete success! read book")
	return "OK"

# 보고싶어요 버튼 취소에 대한 상태 업데이트 구현

@app.route('/wish_it/delete', methods=['POST'])
def wish_it_delete():
	email = user.email
	book_num = request.form['book_num']

	con = mysql.connect()
	cursor = con.cursor()

	query = "delete from BOOKLIST_WISH \
	where email = '" + email + "' and book_num = '" + book_num + "' "

	cursor.execute(query)
	con.commit()

	print("delete success! wish book")
	return "OK"

# 초기 책 정보를 받아서 클라에게 전달하기

# 로딩 과정 책 선별하기

