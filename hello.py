from flask import Flask, jsonify, render_template, request
import sqlite3
app = Flask(__name__)

card_fields = [{'name':'Id','type':'input','field':'rowid','edit':False,'db':False},
{'name':'Телефон','type':'input','field':'tel'},
{'name':'Мобильный','type':'input','field':'mob'},
{'name':'Почта','type':'input','field':'email'},
{'name':'ФИО','type':'input','field':'fio'},
{'name':'Организация','type':'input','field':'org'},
{'name':'Роль','type':'select','field':'role','select_items':['','Страхователь', 'Медучреждение','Разработчик, ТП']},
{'name':'Должность','type':'select','field':'pos','select_items':['','Бухгалтер', 'Кадровик', 'Компьютерщик', 'Руководитель','Регистратура','Врач']},
{'name':'ПО','type':'input','field':'soft'},
{'name':'Заметки','type':'input','field':'etc'}]

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/_get_init')
def get_roles():
    a = ['','Страхователь', 'Медучреждение']
    b = ['','Бухгалтер', 'Кадровик', 'Компьютерщик', 'Руководитель']
    c = ['','Сертификат юрлица','Сертификат ФСС','Криптопровайдер','АРМ ЛПУ','Оформление']
    return jsonify(roles=a,positions=b,reqcats=c)


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/')
def index():
	return render_template('index.html', fields=card_fields)

	
@app.route('/carddel', methods = ['POST'])
def carddel():
	rowid = int(request.form['rowid'])
	conn = sqlite3.connect('site.db')
	conn.row_factory = dict_factory
	conn.execute('DELETE FROM cards WHERE rowid = ?',
	(rowid,))
	conn.commit()
	conn.close()
	return jsonify(reply={'good': 'card deleted'})
    
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

@app.route('/orgauto')
def orgauto():
	term = request.args.get('term').upper()
	conn = sqlite3.connect('site.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	cur.execute('SELECT org FROM cards WHERE org LIKE ? GROUP BY org ORDER BY org  LIMIT 20',
	("%"+term+"%",))
	result = cur.fetchall()
	conn.close()
	result1 = []
	for p in result:
		result1.append(p['org'])	
	return jsonify(result1)			

@app.route('/search2db', methods = ['POST'])
def search2db():
	tel = request.form.get('tel','')
	mob = request.form.get('mob','')
	email = request.form.get('email','').upper()
	fio = request.form.get('fio','').upper()
	role = request.form.get('role','')
	pos = request.form.get('pos','')
	org = request.form.get('org','').upper()
	soft = request.form.get('soft','').upper()
	etc = request.form.get('etc','').upper()
	conn = sqlite3.connect('site.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	cur.execute('SELECT rowid,tel,mob,fio,org FROM cards WHERE tel like ? AND mob like ? AND fio  like ? AND role  like ? AND pos  like ? AND org like ? AND email like ? AND soft  like ? AND etc like ? LIMIT 20',
	("%"+tel+"%","%"+mob+"%","%"+fio+"%","%"+role+"%","%"+pos+"%","%"+org+"%","%"+email+"%","%"+soft+"%","%"+etc+"%"))
	result = cur.fetchall()
	conn.close()
	return jsonify(result = result)


@app.route('/save2db', methods = ['POST'])
def save2db():
	rowid = request.form.get('rowid','')
	if rowid:
		rowid = int(rowid)
	tel = request.form.get('tel','')
	mob = request.form.get('mob','')
	email = request.form.get('email','').upper()
	fio = request.form.get('fio','').upper()
	role = request.form.get('role','')
	pos = request.form.get('pos','')
	org = request.form.get('org','').upper()
	soft = request.form.get('soft','').upper()
	etc = request.form.get('etc','').upper()
	conn = sqlite3.connect('site.db')
	if not tel and not mob:
		return jsonify(reply={'error': 'phone not present'})
	if not fio:
		return jsonify(reply={'error': 'fio is empty'})	
	if rowid:
		conn.execute('UPDATE cards SET tel = ?, mob = ?, fio = ?,role = ?, pos = ?,org = ?,email = ?,soft = ?,etc = ? WHERE rowid = ?',(tel,mob,fio,role,pos,org,email,soft,etc,rowid))
		conn.commit()
		return jsonify(reply={'good': 'card updated'})
	else:
		cur = conn.cursor()
		cur.execute('SELECT rowid FROM cards WHERE tel = ?',(tel,))
		if tel and len(cur.fetchall()) > 0:
			return jsonify(reply={'error': 'phone in base, load a card'})
		cur.execute('SELECT rowid FROM cards WHERE mob = ?',(mob,))
		if mob and len(cur.fetchall()) > 0:
			return jsonify(reply={'error': 'mob in base, load a card'})
		conn.execute('INSERT INTO cards (tel,mob,email,fio,role,pos,org,soft,etc) VALUES (?,?,?,?,?,?,?,?,?)',(tel,mob,email,fio,role,pos,org,soft,etc))
		conn.commit()
		return jsonify(reply={'good': 'card added'})
	conn.close()
