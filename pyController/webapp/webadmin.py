""" Provides an admin dashboard """

from flask import Flask, render_template, redirect, url_for, request, json

app = Flask('FactoryAdmin')

def start_webapp():
    """ Start the webserver """
    # TODO: look at 'production' server implementation
    # Look at https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
    global app
    app.run(host="0.0.0.0", port=10002, threaded=True) # Blocking
    print("HI do you see me?")


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
        print("order posted")
        print(req)
    
    return redirect("/")

@app.route("/favicon.ico")
# https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/
def favicon():
    """ Serve favicon """
    print("favicon here")


if __name__ == "__main__":
    start_webapp()
