import os 
import time 

from flask import Flask, request, render_template
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

def get_db_creds():
    db = os.environ.get("DB", None) or os.environ.get("database", None)
    username = os.environ.get("USER", None) or os.environ.get("username", None)
    password = os.environ.get("PASSWORD", None) or os.environ.get("password", None)
    hostname = os.environ.get("HOST", None) or os.environ.get("dbhost", None)
    return db, username, password, hostname

def create_table():
    # Check if table exists or not. Create and populate it only if it does not exist.
    db, username, password, hostname = get_db_creds()
    table_ddl = 'CREATE TABLE fishes(area TEXT, location TEXT, species TEXT, amount INT UNSIGNED NOT NULL AUTO_INCREMENTINT, PRIMARY KEY (species))'

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=hostname,
                                      database=db)
    except Exception as exp:
        print(exp)
        import MySQLdb
        #try:
        cnx = MySQLdb.connect(unix_socket=hostname, user=username, passwd=password, db=db)
        #except Exception as exp1:
        #    print(exp1)

    cur = cnx.cursor()

    try:
        cur.execute(table_ddl)
        cnx.commit()
        populate_data()
    except mysql.connector.Error as err:

        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/log")
def log_catch():
    return render_template("log.html")

@app.route('/log_catch', methods=['POST'])
def add_to_db():
    print("Received request.")
    area = request.form['area']
    location = request.form['location']
    species = request.form['species']
    curr_amount = request.form['amount']
    other = request.form['other_species']
    if(species == 'Other'):
    	species = request.form['other_species']

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=hostname,
                                      database=db)
    except Exception as exp:
        print(exp)
        import MySQLdb
        cnx = MySQLdb.connect(unix_socket=hostname, user=username, passwd=password, db=db)

    cur = cnx.cursor()
    cur0 = cnx.cursor(buffered=True)
    sql = ("SELECT * FROM fishes WHERE species = '%s" % (species) )
    cur0.execute(sql)
    if(cur0.rowcount > 0):
        sql = ("UPDATE fishes SET amount = amount + curr_amount WHERE location = '%s' AND species = '%s'" % (location, species))
    else:
    	sql = ("INSERT INTO fishes (area, location, species, curr_amount) VALUES (%s, %s, %s, %s)")
    	val = (area, location, species, amount)
    try:
        cur.execute(sql, val)
        cnx.commit()
        return render_template('index.html', message="Catch successfully logged!")
    except Exception as exp:
        return render_template('index.html', message="Catch could not be logged." + str(exp))


if __name__ == "__main__":
    app.run(host = "0.0.0.0")