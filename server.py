from flask import Flask, render_template, redirect, redirect, request
from mysqlconnection import MySQLConnector
from datetime import datetime

app = Flask(__name__)
mysql = MySQLConnector(app, 'emaildb')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = {
       'email': request.form['email']
    }
    query = 'SELECT * FROM emails WHERE emails.email = :email'
    print type(mysql.query_db(query,data))
    if mysql.query_db(query,data) == []:
        query = 'INSERT INTO emails(email,updated_at,created_at) VALUES (:email,now(),now())'
        mysql.query_db(query,data)
    else:
        invalid = ''
        invalid += '<div class=invalid>Email is not valid!</div>'
        return render_template('index.html', fail=invalid)
    return redirect('/success')

@app.route('/success')
def success():
    query = 'SELECT * FROM emails;'
    emailString = ''
    resultString = ''
    emails = mysql.query_db(query)
    if emails != []:
        for email in emails:
            emailString += '<p>'+email['email']+' '+str(email['created_at'].strftime('%m/%d/%y %I:%M %p'))+'</p>'
            print type(email['created_at'])
        resultString = ''
        resultString += '<div class=success>The email address you entered ('+emails[-1]['email']+') is a VALID email address! Thank you!</div>'
    return render_template('success.html', entered=emailString, result=resultString)

@app.route('/delete')
def delete():
    query = 'DELETE FROM emails;'
    mysql.query_db(query)
    return redirect('/success')

app.run(debug=True)
