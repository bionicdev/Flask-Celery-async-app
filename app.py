from random import choice

from flask import Flask
from flask_celery import make_celery
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECRET'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/celery_async'
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'db+mysql://root:root@localhost/celery_tasks'

db = SQLAlchemy(app)

celery = make_celery(app)


class Results(db.Model):
	id = db.Column('id', db.Integer, primary_key=True)
	data = db.Column('data', db.String(50))


@app.route('/insertData')
def insertData():
	insert.delay()

	return 'I send an async request to insert data into database.'


@app.route('/process/<name>')
def process(name):
	reverse.delay(name)

	return 'I sent an async request!'	


@celery.task(name='celery_example.reverse')
def reverse(string):
	return string[::-1]

@celery.task(name='celery_example.insert')
def insert():
	data = str()

	for item in range(500):
		data = ''.join(choice('ABCD') for i in range(10))
		
		result = Results(data=data)
		db.session.add(result)
		db.session.commit()

	return 'Done!!!'


if __name__=='__main__':
	app.run(debug=True)


# celery -A app.celety worker --loglevel=info	