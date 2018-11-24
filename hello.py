from flask import Flask, jsonify, render_template, request
import sqlite3
app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/_get_init')
def get_roles():
    a = ['','Страхователь', 'Медучреждение']
    b = ['','Бухгалтер', 'Кадровик', 'Компьютерщик', 'Руководитель']
    return jsonify(roles=a,positions=b)


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/')
def index():
	return render_template('index.html')
	conn = sqlite3.connect('site.db')
	cur = conn.cursor()
	cur.execute('SELECT rowid,* FROM cards WHERE rowid = ?',
	(rowid,))
	result = cur.fetchall()
	conn.close()
	return jsonify(result = result)
	
@app.route('/carddel', methods = ['POST'])
def carddel():
	rowid = int(request.form['rowid'])
	conn = sqlite3.connect('site.db')
	conn.row_factory = dict_factory
	conn.execute('DELETE FROM cards WHERE rowid = ?',
	(rowid,))
	conn.commit()
	conn.close()
	return jsonify(result = 'ok')
    
@app.route('/get2rowid', methods = ['POST'])
def get2rowid():
	rowid = int(request.form['rowid'])
	conn = sqlite3.connect('site.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	cur.execute('SELECT rowid,* FROM cards WHERE rowid = ?',
	(rowid,))
	result = cur.fetchall()
	conn.close()
	return jsonify(result = result)


@app.route('/search2db', methods = ['POST'])
def search2db():
	tel = request.form.get('tel','')
	mob = request.form.get('mob','')
	fio = request.form.get('fio','')
	role = request.form.get('role','')
	pos = request.form.get('pos','')
	org = request.form.get('org','')
	org_ = request.form.get('org_','')
	soft = request.form.get('soft','')
	conn = sqlite3.connect('site.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	cur.execute('SELECT rowid,tel,mob,fio,org FROM cards WHERE tel like ? AND mob like ? AND fio  like ? AND role  like ? AND pos  like ? AND org like ? AND org_ like ? AND soft  like ? LIMIT 10',
	("%"+tel+"%","%"+mob+"%","%"+fio+"%","%"+role+"%","%"+pos+"%","%"+org+"%","%"+org_+"%","%"+soft+"%"))
	result = cur.fetchall()
	conn.close()
	return jsonify(result = result)


@app.route('/save2db', methods = ['POST'])
def save2db():
	tel = request.form.get('tel','')
	mob = request.form.get('mob','')
	fio = request.form.get('fio','')
	role = request.form.get('role','')
	pos = request.form.get('pos','')
	org = request.form.get('org','')
	org_ = request.form.get('org_','')
	soft = request.form.get('soft','')
	conn = sqlite3.connect('site.db')
	if not tel and not mob:
		return jsonify(error='phone not present')
	cur = conn.cursor()
	cur.execute('SELECT rowid FROM cards WHERE tel = ?',(tel,))
	if len(cur.fetchall()) > 0:
		return jsonify(error='tel in base')
	cur.execute('SELECT rowid FROM cards WHERE mob = ?',(mob,))
	if len(cur.fetchall()) > 0:
		return jsonify(error='mob in base')
	if not fio:
		return jsonify(error='fio is empty')	
	conn.execute('INSERT INTO cards VALUES (?,?,?,?,?,?,?,?)',
	(tel,mob,fio,role,pos,org,org_,soft))
	conn.commit()
	conn.close()
	return jsonify(request.form)
	#return jsonify(result=[mob,tel,fio,role,pos,org,org_,soft])
