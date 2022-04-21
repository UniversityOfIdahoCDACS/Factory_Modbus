""" Provides an admin dashboard """

import os
import sys
import threading
from flask import Flask, render_template, redirect, send_file, url_for, request, json
import waitress  # Production webserver

# Append parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from job_data import JobData

# starting value for 
job_id = 500
order_id = 8000


app = Flask('FactoryAdmin')

class webapp_callbacks():
    def __init__(self):
        self._add_order_cb = None
        self._factory_command_cb = None
        self.orchastrator = None

    def set_add_order_cb(self, func):
        self._add_order_cb = func

    def add_order_cb(self, job_data):
        if self._add_order_cb:
            self._add_order_cb(job_data)

    def set_factory_command_cb(self, func):
        self._factory_command_cb = func

    def factory_command(self):
        if self._factory_command_cb:
            self._factory_command_cb()

    def set_orchastrator(self, func):
        self.orchastrator = func


def worker():
    """ Worker thread to run webapp """
    # Look at https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
    global app
    app.run(host="0.0.0.0", port=10002, threaded=True) # Development server
    #waitress.serve(app, host='0.0.0.0', port=10002)     # Production server
    print("HI do you see me?")  

def start_webapp():
    """ Start the webserver """
    worker_thread.start()

def stop_webapp():
    """ Stop the webserver """
    pass


@app.route("/")
@app.route("/index")
def serve_root():
    return render_template("index.html")

# https://github.com/ColorlibHQ/AdminLTE/releases
# https://github.com/tbotnz/flask-AdminLTE
# https://adminlte.io/themes/v3/pages/UI/timeline.html#
# http://localhost:10001/starter#

@app.route("/myfunction_1")
# https://syntaxfix.com/question/1571/flask-calling-python-function-on-button-onclick-event
def myfunction_1():
    print("hello there from myfunction_1")
    return "Nothing"

@app.route("/create-order", methods=["GET", "POST"])
# https://pythonise.com/series/learning-flask/flask-working-with-forms
def create_order():
    """ Create order for factory """
    print("create-order submitted")
    if request.method == "POST":
        req = request.form
        print(req)
        # checkbox does not show when faulst
        # check if not exist and consider it false
        try:
            job = JobData(job_id=job_id, order_id=order_id, color=req['order_color'], cook_time=int(req['order_CookTime']), sliced=True)
        except TypeError:
            print("Browser sent bad info")
            return redirect("/")
        except AttributeError as e:
            print(e)
            print("Data did not validate")
            return redirect("/")
        else:
            print("Sending job order to Orchastrator")
            #callbacks.add_order_cb(job)
            callbacks.orchastrator.add_job_callback(job)

    return redirect("/")

@app.route("/favicon.ico")
# https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/
def favicon():
    """ Serve favicon """
    print("favicon here")
    return send_file('favicon.ico', mimetype='image/vnd.microsoft.icon')


callbacks = webapp_callbacks()
worker_thread = threading.Thread(target=worker)

if __name__ == "__main__":
    worker()
