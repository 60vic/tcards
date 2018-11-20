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
    a = ['','Страхователь', 'Медучреждение', 'Иное']
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
    
@app.route('/search2db', methods = ['POST'])
def search2db():
	tel = request.args.get('tel','')
	mob = request.args.get('mob','')
	fio = request.args.get('fio','')
	role = request.args.get('role','')
	pos = request.args.get('pos','')
	org = request.args.get('org','')
	org_ = request.args.get('org_','')
	soft = request.args.get('soft','')
	conn = sqlite3.connect('site.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	cur.execute('SELECT rowid,tel,mob,fio,org FROM cards WHERE tel like ? AND mob like ? AND fio  like ? AND role  like ? AND pos  like ? AND org like ? AND org_ like ? AND soft  like ? LIMIT 10',
	("%"+tel+"%","%"+mob+"%","%"+fio+"%","%"+role+"%","%"+pos+"%","%"+org+"%","%"+org_+"%","%"+soft+"%"))
	result = cur.fetchall()
	conn.close()
	return jsonify(result = result)


@app.route('/save2db')
def save2db():
	tel = request.args.get('tel')
	mob = request.args.get('mob')
	fio = request.args.get('fio')
	role = request.args.get('role')
	pos = request.args.get('pos')
	org = request.args.get('org')
	org_ = request.args.get('org_')
	soft = request.args.get('soft')
	conn = sqlite3.connect('site.db')
	conn.execute('INSERT INTO cards VALUES (?,?,?,?,?,?,?,?)',
	(tel,mob,fio,role,pos,org,org_,soft))
	conn.commit()
	conn.close()
	return jsonify(result=[mob,tel,fio,role,pos,org,org_,soft])
