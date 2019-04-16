import os 
import time 

from flask import Flask, request, render_template
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

def get_db_creds():
    db = "reel_time_db"
    username = "myadmin"
    password = "Reeltime!"
    hostname = "reel-time-db.chr9q1gt6nxw.us-east-1.rds.amazonaws.com"
    port = 3306
    return db, username, password, hostname, port

def create_table():


    print 'tryig to create table'
    print ''

    # Check if table exists or not. Create and populate it only if it does not exist.
    db, username, password, hostname, port = get_db_creds()
    table_ddl = 'CREATE TABLE fishes(area varchar(100), location varchar(100), species varchar(100), amount INT UNSIGNED NOT NULL, PRIMARY KEY (species))'

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=hostname, port=port,
                                      database=db)
    except Exception as exp:
        print(exp)
        import MySQLdb
        #try:
        cnx = MySQLdb.connect(unix_socket=hostname, user=username, passwd=password, port=port, db=db)
        #except Exception as exp1:
        #    print(exp1)

    cur = cnx.cursor()

    try:
        cur.execute(table_ddl)
        cnx.commit()
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

    print "********FORM*******"
    print request.form
    print ''

    area = request.form.get('area')
    location = request.form.get('location')
    species = request.form.get('species')
    curr_amount = request.form.get('amount')
    other = request.form.get('other_species')
    if(species == 'Other'):
    	species = request.form.get('other_species')

    # db, username, password, hostname, port = get_db_creds()

    print area, location, species, curr_amount, other 

    create_table()

    cnx = ''
    try:
        cnx = mysql.connector.connect(user="myadmin", password="Reeltime!",
                                      host="reel-time-db.chr9q1gt6nxw.us-east-1.rds.amazonaws.com", port=3306, 
                                      database="reel_time_db")
    except Exception as exp:
        print(exp)
        import MySQLdb
        cnx = MySQLdb.connect(unix_socket=hostname, user=username, passwd=password, db=db, port=port)

    cur = cnx.cursor()
    cur0 = cnx.cursor(buffered=True)
    sql = ("SELECT * FROM fishes WHERE species = '%s'" % (species) )
    cur0.execute(sql)
    if(cur0.rowcount > 0):
        sql = ("UPDATE fishes SET amount = amount + curr_amount WHERE location = '%s' AND species = '%s'" % (location, species))
    else:
    	sql = ("INSERT INTO fishes (area, location, species, amount) VALUES (%s, %s, %s, %s)")
    	val = (area, location, species, curr_amount)
    try:
        cur.execute(sql, val)
        cnx.commit()
        return render_template('log.html', message="Catch successfully logged!")
    except Exception as exp:
        return render_template('log.html', message="Catch could not be logged." + str(exp))


if __name__ == "__main__":
    app.run(host = "0.0.0.0")