from celery import Celery
import time


app = Celery('tasks', 
	broker='amqp://localhost//', 
	backend='db+mysql://root:root@localhost/celery_tasks')

@app.task
def reverse(string):
	time.sleep(10)

	return string[::-1]

# celery -A tasks worker --loglevel=inf	