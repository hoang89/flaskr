import sqlite3
from contextlib import closing

from flask import Flask, request, session, g, redirect, url_for, abort, render_template,flash
from simple_page import simple_page
from system.system import system_information


#configuration database
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
PROPAGATE_EXCEPTIONS = True



app = Flask(__name__)
app.config.from_object(__name__)
app.register_blueprint(simple_page)
app.register_blueprint(system_information)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()



@app.before_request
def before_request():
    g.db = connect_db()
    app.logger.debug('Function before request execute: '+ request.path )


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select title,text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template("show_entries.html", entries=entries)

@app.route('/add', methods=["GET","POST"])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute("insert into entries(title, text) values(?,?)", [request.form['title'], request.form['text']])
    g.db.commit()
    flash("New entry was  success addded")
    return redirect(url_for('show_entries'))


@app.route('/redirect', methods=['GET', 'POST'])
def test_re():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    error=None
    if request.method == "POST":
        if request.form['username'] != app.config['USERNAME']:
            error = "Invalid username"
        elif request.form['password'] != app.config['PASSWORD']:
            error = "Invalid password"
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logout')
    return redirect(url_for('show_entries'))

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

if __name__ == '__main__':
    app.run(debug=True)
