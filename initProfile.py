from flask import Flask, request
from flask_login import (LoginManager, login_required, login_user, current_user, logout_user, UserMixin)

app = Flask(__name__)
mysql = MySQL()
cursor = mysql.connect().cursor();
cursor.execute("select * from USER where email='" + email"'")
data = cursor.fetchone()

@app.route("/initProfile", methods=["POST"])

class InitProfile(user):

	def initProfile():

		time.sleep(5);
		print request.headers;
		token,session = request.headers.get("Cookie").split(' ');
		tokenName, tokenValue = token.split('=');
		sessionName, sessionValue = session.split('=');
		tokenValue = tokenValue.replace(';','');

		email = user.email;


		attendOrNot = request.form['attendOrNot'];
		semesterNum = request.form['semesterNum'];
		majorFirst = request.form['majorFirst'];
		majorSecond = request.form['majorFirst'];

		updateProfile(current_email, attendOrNot, semesterNum, majorFirst, majorSecond);

		checkUpdated = updateProfile(current_email, attendOrNot, semesterNum, majorFirst, majorSecond);

		if checkUpdated == 1:
			return "Done!";
		else:
			return "Something Wrong!";

	def updateProfile(current_email, attendOrNot, semesterNum, majorFirst, majorSecond):
		cursor = connect.DB();
		cursor.execute("update USER set attendOrNot='"+attendOrNot"', semesterNum='"+semesterNum"', majorFirst='"+majorFirst"', majorSecond='"+majorSecond"' where email='"+current_email"'");
