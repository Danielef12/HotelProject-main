from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'Merda',
    'host': 'mongodb://localhost:27017',
}

db = MongoEngine(app)


class Prenotazione(db.Document):
    username = db.StringField(required=True)
    room_type = db.StringField(required=True)
    arrival_date = db.DateField(required=True)
    departure_date = db.DateField(required=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/services.html")
def services():
    return render_template("services.html")


@app.route("/hotel.html")
def hotel():
    return render_template("hotel.html")


@app.route("/contact.html", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/prenota", methods=['GET', 'POST'])
def prenota():
    if request.method == 'POST':
        username = request.form['username']
        room_type = request.form['room-type']
        arrival_date = request.form['arrival-date']
        departure_date = request.form['departure-date']

        prenotazione = Prenotazione(
            username=username,
            room_type=room_type,
            arrival_date=arrival_date,
            departure_date=departure_date
        )
        prenotazione.save()
        return redirect(url_for('conferma'))
    return render_template('index.html')


@app.route('/conferma', methods=['GET', 'POST'])
def conferma():
    return render_template('conferma.html')


if __name__ == "__main__":
    app.run(debug=True)
