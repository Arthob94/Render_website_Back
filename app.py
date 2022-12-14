import json
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))

    def __init__(self, name, city):
        self.name = name
        self.city = city


@app.route('/students/', methods=['GET', 'POST', 'DELETE'])
@app.route('/students/<id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def crude_students(id=0):
    if request.method == 'POST':
        request_data = request.get_json()
        # print(request_data['city'])
        city = request_data['city']
        name = request_data['name']
        newStudent = Students(name, city)
        db.session.add(newStudent)
        db.session.commit()
        return "a new record was create"
    if request.method == 'GET':
        res = []
        for student in Students.query.all():
            res.append(
                {"city": student.city, "id": student.id, "name": student.name})
        return (json.dumps(res))
    if request.method == 'DELETE':  # not implemented yet
        me = Students.query.get(id)
        db.session.delete(me)
        db.session.commit()
        return "row deleted"
    if request.method == 'PUT':  # not implemented yet
        me = Students.query.get(id)
        request_data = request.get_json()
        # print(request_data['city'])
        me.city = request_data['city']
        me.name = request_data["name"]
        db.session.commit()

        return {'msg': 'row updated'}


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
