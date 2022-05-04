from enum import unique
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# The instance of the flask app
app = Flask(__name__)

# This is the database URI that should be used for connections in this case with dbsqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# To get and use the db variable which is an instance of the SQLAlchemy
db = SQLAlchemy(app)


# Drink model object
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(250))
    # Accesses the object and can return its attributes
    def __repr__(self):
        return f"{self.name} - {self.description}"

# HOME
@app.route('/')
def index():
    return 'Hello'

# GET ALL THE DRINKS IN THE DATABASE
# Applying a GET Request 
# Write the url in the @app.route decorator
@app.route('/drinks')
def get_drinks():
    # Query to access all drinks will be stored in the drinks variable
    drinks = Drink.query.all()
    # Output is an empty list
    output = []
    for drink in drinks:
        # for each drink in drinks add the name and description
        drink_data = {
            'name':drink.name,
            'description': drink.description,
        }
        # add the new new drink and its data to the empty output list
        output.append(drink_data)
    # return the drinks list as output
    return {"drinks":output}

# GET A SPECIFIC DRINK
@app.route('/drinks/<id>')
def get_drink(id):
    # Grab a specific drink by its id if not found then get a 404 error
    drink = Drink.query.get_or_404(id)
    # display the drink's name and description
    return ({
        'name':drink.name,
        'description': drink.description,
        })

# ADD A NEW DRINK
@app.route('/drinks', methods=['POST'])
def add_drink():
    # since we are using python requests
    # I will serialize the data to json format with the requests using request.json
    drink =Drink(name=request.json['name'], description=request.json['description'])
    # add the new drink to the DB
    db.session.add(drink)
    db.session.commit()
    # display the new drink with its id
    return {'id':drink.id}


# DELETE A DRINK FROM THE DB
@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get_or_404(id)
    db.session.delete(drink)
    db.session.commit()
    return {'message':"deleted successfully"}