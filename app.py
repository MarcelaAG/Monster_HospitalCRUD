from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
# import mysql.connector
# import sqlalchemy


app =  Flask(__name__)
app.secret_key = "The Secret Key" 
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# engine = sqlalchemy.create_engine('mysql+mysqlconnector://mab:123789456@localhost') # connect to server
# engine.execute("CREATE DATABASE crud") #create db
# engine.execute("USE crud") # select new db


# cnx = mysql.connector.connect(user='mab', password='123789456',
#                               host='127.0.0.1',
#                               database='crud')
# cnx.close()

# #SqlAlchemy database config with Mysql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://mab:123789456@localhost/crud'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

 # Create SQL object and pass app
db = SQLAlchemy(app)

#Create model table for CRUD database
class Patients(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    last_name = db.Column(db.String(100))
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    telephone = db.Column(db.Integer)
    email = db.Column(db.String(100)) 

    def __init__(self, last_name, name, address, telephone, email):
        self.last_name = last_name    
        self.name = name
        self.address = address
        self.telephone = telephone
        self.email = email
 
 #This is the index route to
#query on all the patient data
@app.route('/')
def Index():
        all_data = Patients.query.all()
        return render_template('index.html', patients = all_data)

 #This is the rdv route to
#patient appointments
@app.route('/rdvs')
def see_rdvs():
       
        return render_template('rdvs.html')       

        #how do I get to rdvs.html???

# This  is the add new data route for inserting data to sqlite database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
        last_name = request.form['last_name']
        name = request.form['name']
        address = request.form['address']
        telephone = request.form['telephone']
        email = request.form['email']

 
        my_data = Patients(last_name, name, address, telephone, email)
        db.session.add(my_data)
        db.session.commit()

        flash('Patient sucessfully added') # My message will show up when new patient is added
 
        # flash("Patient  Inserted Successfully")
 
        return redirect(url_for('Index'))
 
 #this is the update route to update patient info
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_data = Patients.query.get(request.form.get('id'))

        my_data.last_name = request.form['last_name']
        my_data.name = request.form['name']
        my_data.address = request.form['address']
        my_data.telephone = request.form['telephone']
        my_data.email = request.form['email']
 
        db.session.commit()
        flash("Patient info Updated Successfully")
 
        return redirect(url_for('Index'))

#This route is for deleting a patient
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Patients.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Patient file deleted successfully")
 
    return redirect(url_for('Index'))
         

if __name__ == "__main__":
    app.run(debug=True)