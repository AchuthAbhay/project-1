from flask import Flask,render_template,request

validation = Flask(__name__)

@validation.route("/validation", methods=["GET","POST"])
def index():
    if request.method == "POST":
        print("User =", request.form["uName"])
        print("Phone =", request.form["uPhone"])
        print("Email =", request.form["uEmail"])
                          
    return render_template("validation.html")

validation.run(host="127.0.0.1",port="8080",debug=True)