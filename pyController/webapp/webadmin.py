""" Provides an admin dashboard """

import os
import sys
import threading
from flask import Flask, render_template, redirect, send_file, url_for, request, json
import waitress  # Production webserver

# Append parent directory to import path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) # Directory of this script
sys.path.insert(0, os.path.dirname(SCRIPT_DIR))

from job_data import JobData

app = Flask('FactoryAdmin', static_url_path="/static", static_folder=SCRIPT_DIR + '/static', template_folder=SCRIPT_DIR + '/templates')

class WebappStorage():
    """ This class holds function callbacks, objects and attributes.
    These may be needed by both this webapp and outside objects like pyController
    Using this as flask apps can't easily be packaged into a class
    """
    def __init__(self):
        self.orchastrator = None
        self.job_id = 0
        self.order_id = 0

    def get_a_job_id(self):
        """ Return a job id then increment """
        val = self.job_id
        self.job_id += 1
        return val

    def get_an_order_id(self):
        """ Return a order id then increment """
        val = self.order_id
        self.order_id += 1
        return val

    def set_orchastrator(self, obj):
        """ Called to set the orchastrator object """
        self.orchastrator = obj

    def add_job_cb(self, job_data):
        """ Adds job to orchastrator """
        if self.orchastrator:
            self.orchastrator.add_job_callback(job_data)

    def factory_command(self):
        """ Universal factory command function in orchastrator"""
        if self.orchastrator:
            self.orchastrator.factory_command_callback()


def worker():
    """ Worker thread to run webapp """
    # Look at https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
    global app
    # app.run(host="0.0.0.0", port=10002, threaded=True) # Development server
    waitress.serve(app, host='0.0.0.0', port=8080)     # Production server
    print("HI do you see me?")

def start_webapp():
    """ Start the webserver """
    worker_thread.start()


# https://github.com/ColorlibHQ/AdminLTE/releases
# https://github.com/tbotnz/flask-AdminLTE
# https://adminlte.io/themes/v3/pages/UI/timeline.html#
# http://localhost:10001/starter#

#############################
## App calls
############################

@app.route("/myfunction_1")
# https://syntaxfix.com/question/1571/flask-calling-python-function-on-button-onclick-event
def myfunction_1():
    """ Test Function """
    print("hello there from myfunction_1")
    #inv = webapp_storage.orchastrator.inventory.get_inventory()
    status = webapp_storage.orchastrator.factory.status_detailed()
    print(status)
    return "Nothing"

@app.route("/reset_inventory")
def reset_inventory():
    """ Reset factory inventory """
    print("Resetting inventory")
    webapp_storage.orchastrator.inventory.preset_inventory()
    return "Nothing"

@app.route("/reset_factory")
def reset_factory():
    """ Reset factory modules """
    print("Resetting factory")
    webapp_storage.orchastrator.factory.reset_factory()
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
            job = JobData(job_id=webapp_storage.get_a_job_id(), order_id=webapp_storage.get_an_order_id(),
                          color=req['order_color'], cook_time=int(req['order_CookTime']), sliced=True)
        except TypeError:
            print("Browser sent bad info")
            return redirect("/")
        except AttributeError as e:
            print(e)
            print("Data did not validate")
            return redirect("/")
        else:
            print("Sending job order to Orchastrator")
            webapp_storage.add_job_cb(job)

    return redirect("/")

#############################
## App routing
############################

@app.route("/")
@app.route("/index")
def serve_root():
    """ Serve root index """
    inv = webapp_storage.orchastrator.inventory.get_inventory()
    factory_status = webapp_storage.orchastrator.factory.status_detailed()
    print("root inv: %s" % inv)
    return render_template("index.html", inv=inv,
                            factory_status=factory_status['factory_status'],
                            module_status=factory_status['modules_statuses'])


@app.route("/favicon.ico")
# https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/
def favicon():
    """ Serve favicon """
    print("favicon here")
    return send_file(SCRIPT_DIR + '/favicon.ico', mimetype='image/vnd.microsoft.icon')


webapp_storage = WebappStorage()
worker_thread = threading.Thread(target=worker, daemon=True)

if __name__ == "__main__":
    start_webapp()
