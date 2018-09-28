from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import sqlite3

app = Flask(__name__)
api = Api(app)
data = sqlite3.connect('chinook.db', check_same_thread=False)
conn = data.cursor()


class list_employees(Resource):
    def get(self):
        query = conn.execute("select firstname from employees;")
        result = {'first_name': [i[0] for i in query.fetchall()]}
        request_ip_addr = request.remote_addr
        return result

class profile(Resource):
    def get(self, firstname):
        query = conn.execute("select * from employees where firstname = '%s'" % firstname)
        result = {'data': [dict(zip(('id', 'lastname', 'firstname', 'title', 'report', 'birthday',
            'hiredate', 'address'), i)) for i in query]}
        return result

    def put(self, firstname):
        report = request.form['report']
        query = conn.execute("UPDATE employees SET reportsto = '%s'" % report)
        data.commit()
        return '', 201

    def post(self, firstname):
        lastname = request.form['lastname']
        title = request.form['title']
        report = request.form['report']
        birthday = request.form['birthday']
        hiredate = request.form['hiredate']
        address = request.form['address']
        query = conn.execute("INSERT INTO employees (EmployeeId, lastname, firstname, title, reportsto, birthdate, hiredate, address) VALUES (?,?,?,?,?,?,?,?)", (1535,lastname,firstname,title,report,birthday,hiredate,address))
        data.commit()
        return '', 201

api.add_resource(list_employees, '/names')
api.add_resource(profile, '/names/<firstname>')

if __name__ == '__main__':
    app.run(debug=True)