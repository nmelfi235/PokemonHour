# This file will add an email to the subscriber list
# where they will receive a Pokémon every hour
import sender
from flask import Flask, render_template, request

app = Flask(__name__)


# Will send an email with a Pokémon to sepcified route
@app.route("/", methods=['POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        if email != "":
            sender.subscribe(email)
    return render_template('form.html')


app.run(host="0.0.0.0", port=8080)