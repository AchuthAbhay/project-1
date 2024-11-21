from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def random_gen():
    random_value = random.randint(0,10000)
    return render_template('index.html', random_value = random_value)

app.run(debug = True, port = 8080)