## make it so the server alwasy returns a json
##json will have stock names and predictions
from flask import Flask, request
from flask_restful import Resource, Api
from resources.score import Score
from resources.generate import Generate
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
api = Api(app)

def job():
    """ Function for test purposes. """
    print("Scheduler is alive!")

sched = BackgroundScheduler( {'apscheduler.timezone': 'UTC'}, daemon=True)
sched.add_job(job, "cron", day_of_week="mon-fri", hour = "12")
sched.add_job(job, 'cron', day_of_week="mon-fri", hour = "22")
sched.start()



api.add_resource(Score, '/score')
api.add_resource(Generate, '/generate')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
