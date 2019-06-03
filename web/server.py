from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

app.debug=True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)


@app.route('/users', methods = ['POST'])
def create_user():
    c =  json.loads(request.form['values'])
    user = entities.User(
        username=c['username'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'

@app.route('/users', methods = ['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'


@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = []
    for user in dbResponse:
        data.append(user)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')

@app.route('/create_test_users', methods = ['GET'])
def create_test_users():
    db_session = db.getSession(engine)
    user = entities.User(name="David", fullname="Lazo", password="1234", username="qwerty")
    db_session.add(user)
    db_session.commit()
    return "Test user created!"

@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        session.delete(user)
    session.commit()
    return "Deleted Message"

@app.route('/static/authenticate', methods = ['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    db_session = db.getSession(engine)
    users = db_session.query(entities.User)

    try:
        user = db_session.query(entities.User).filter(entities.User.username == username).filter(entities.User.password == password).one()
        return render_template("success.html")
    except Exception:
        return render_template("fail.html")

@app.route('/mensajes', methods = ['GET'])
def get_message():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Message)
    data = []
    for message in dbResponse:
        data.append(message)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/mensajes', methods = ['POST'])
def create_message():
    c =  json.loads(request.form['values'])
    mensaje = entities.Message(
        content=c['Message'],
        sent_on=c['sent_on'],
        user_from_id=c['RemitenteID'],
        user_to_id=c['DestinatarioID'],
        user_from=c['Remitente'],
        user_to = c['Destinatario']
    )
    session = db.getSession(engine)
    session.add(mensaje)
    session.commit()
    return 'Created Mensaje'

@app.route('/mensajes', methods = ['PUT'])
def update_mensaje():
    session = db.getSession(engine)
    id = request.form['key']
    mensaje = session.query(entities.Message).filter(entities.Message.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(mensaje, key, c[key])
    session.add(mensaje)
    session.commit()
    return 'Updated mensaje'

@app.route('/create_test_mensaje', methods = ['GET'])
def create_test_mensaje():
    session = db.getSession(engine)
    mensaje = entities.Message(content="Hola", sent_on="Today", user_from_id=1, user_to_id=2, user_from=1, user_to = 2)
    session.add(mensaje)
    session.commit()
    return "Test message created!"

@app.route('/mensajes', methods = ['DELETE'])
def delete_mensaje():
    id = request.form['key']
    session = db.getSession(engine)
    mensajes = session.query(entities.Message).filter(entities.Message.id == id)
    for mensaje in mensajes:
        session.delete(mensaje)
    session.commit()
    return "Deleted Message"

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
