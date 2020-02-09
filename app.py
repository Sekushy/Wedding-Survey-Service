from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
import requests

app = Flask(__name__)
ENV = "prod"

if ENV == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0nVerse2016!@localhost/postgres'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wlcajyjwrhlush:dcb023d7790ce27efd3fae77d5e6c24ff1e7eb2fb76d798d7b7b027fa9523e1b@ec2-3-213-192-58.compute-1.amazonaws.com:5432/daqirlcu7lh0sr'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Create a Guest class in which we define our DB columns
class Guest(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key = True)
    guest = db.Column(db.String(200))
    email =  db.Column(db.String(200))
    favorite = db.Column(db.String(200))
    rating =  db.Column(db.Integer)
    comments =  db.Column(db.Text())

    def __init__(self, guest, email, favorite, rating, comments):
        self.guest = guest
        self.email = email
        self.favorite = favorite
        self.rating = rating
        self.comments = comments

# Guest Schema
class GuestSchema(ma.Schema):
    class Meta:
        fields = ('id', 'guest', 'email', 'favorite', 'rating', 'comment')

# Init schema
guest_schema = GuestSchema()
guests_schema = GuestSchema(many=True)

# Initialize the webpage on app run
@app.route('/')
def index():
    return render_template('index.html')

# Add guest to database
@app.route('/submit', methods=['POST'])
def add_guest():
    guest = request.form['guest']
    email = request.form['email']
    favorite = request.form['favorite']
    rating = request.form['rating']
    comments = request.form['comments']

    new_guest = Guest(guest, email, favorite, rating, comments)
    db.session.add(new_guest)
    db.session.commit()

    # TODO
    # Create request that goes to send email in form of  request = requests.get('http://HerokuUrl/email') that triggers a get request for app.py
    request = requests.get('https://wedding-email-service.herokuapp.com/email')

    return render_template('success.html')

# Get all guests
@app.route('/guests', methods=['GET'])
def get_guests():
    all_guests = Guest.query.all()
    results = guests_schema.dump(all_guests)
    return jsonify(results)

# Get guest by id
@app.route('/guest/<id>', methods=['GET'])
def get_guest(id):
    guest = Guest.query.get(id)
    return guest_schema.jsonify(guest)

if __name__ == "__main__":
    app.debug = True
    app.run()