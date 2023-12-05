from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
import smtplib

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'Merda',
    'host': 'mongodb://localhost:27017',
}

db = MongoEngine(app)


def invia_email(nome, emaill, messaggio):
    server_smtp = "smtp.gmail.com"
    porta_smtp = 587

    mittente = "danielefiocca19899@gmail.com"
    password = "tudnxwpezjwhazed"

    oggetto = f"Nuovo messaggio da {nome}"
    corpo = f"Nome: {nome}\nEmail: {emaill}\n\nMessaggio:\n{messaggio}"
    messaggio_email = f"Subject: {oggetto}\n\n{corpo}"

    try:
        with smtplib.SMTP(server_smtp, porta_smtp) as server:
            server.starttls()
            server.login(mittente, password)
            server.sendmail(mittente, mittente, messaggio_email)
        print("Email inviata con successo!")
    except Exception as e:
        print(f"Errore durante l invio del messaggio: {e}")


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
        nome = request.form['nome']
        emaill = request.form['emaill']
        messaggio = request.form['messaggio']

        invia_email(nome, emaill, messaggio)
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/prenota", methods=['GET', 'POST'])
def prenotazione():
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

    username = request.args.get('username')
    room_type = request.args.get('room_type')
    arrival_date = request.args.get('arrival_date')
    departure_date = request.args.get('departure_date')

    room = Prenotazione.objects.order_by('-id').first()

    return render_template('conferma.html', prenotazione=room)


@app.route('/prenotazione.html')
def booking():
    return render_template('prenotazione.html')


if __name__ == "__main__":
    app.run(debug=True)
