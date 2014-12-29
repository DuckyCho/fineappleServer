# -*- coding:utf-8 -*-

import simplejson
import urllib
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Flask;
from flaskext.mysql import MySQL;
from flask import request, session;


app = Flask(__name__);

#초기 설정
mysql = MySQL();
app.config['MYSQL_DATABASE_USER'] = 'root';
app.config['MYSQL_DATABASE_PASSWORD'] = 'next!!@@##$$';
app.config['MYSQL_DATABASE_DB'] = 'finedb';

mysql.init_app(app);

apikey = "ae04be3ff84bfb7d678768b3270dbd5d63741b41"
SEARCH_BASE ="http://apis.daum.net/search/book"

testkey = 1

def search(query, **args):
	args.update({
    	'apikey': apikey,
    	'q': query,
    	'result': '1',
    	'output': 'json'
    	})

	url = SEARCH_BASE + '?' + urllib.urlencode(args)
	result = simplejson.load(urllib.urlopen(url))

	return result['channel']

def getimg(tISBN):
	info = search(tISBN)
	for item in info['item']:
		print item['cover_l_url']
		return item['cover_l_url']


def getISBN(bookNum):
	con = mysql.connect()
	cursor = con.cursor()

	cursor.execute("select ISBN from BOOKINFO where book_num='" + bookNum + "';")
	check_e = cursor.fetchone()

	if check_e == None:
		return 0

	url = getimg(check_e[0])
	
	print '============'
	print url
	print '==========='	
	if url == None:
		print '없는 ISBN : ' + check_e[0]	
	else:
		con = mysql.connect()
		cursor = con.cursor()
	
		query = "update BOOKINFO set cover_img='" + url + "' where book_num='" + bookNum + "';"
		cursor.execute(query)
		con.commit()

@app.route('/save')
def test():
	for i in range (1, 2000):
		string ="L" + str('{:04}'.format(i))	
		getISBN(string)
	return 'success'

if __name__ == "__main__":
	app.run(debug=True, host='10.73.45.83', port=5013);
