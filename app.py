from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
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

#Create model table for Patients database
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

# This is my RDV table 
class RDV(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    patient_id =  db.Column(db.Integer, db.ForeignKey('patients.id'))
    last_name = db.Column(db.String(100))
    name = db.Column(db.String(100))
    rdv_date =db.Column(db.String(100))
    rdv_time = db.Column(db.Integer)
    doctor = db.Column(db.String(100))

    def __init__(self, patient_id, last_name, name, rdv_date, rdv_time, doctor):
        self.patient_id = patient_id
        self.last_name = last_name
        self.name = name
        self.rdv_date = rdv_date
        self.rdv_time = rdv_time
        self.doctor = doctor
 
 #This is the index route to query on all the patient data
@app.route('/')
def Index():
        all_data = Patients.query.all()
        return render_template('index.html', patients = all_data)

#This is the rdv route to query patient appointments
@app.route('/rdvs', methods = ['GET'])
def see_rdvs():
    all_rdv = RDV.query.all()
    return render_template('rdvs.html', rdv = all_rdv)

# This is the route to see  patient rdv(s) in rdv html page 
@app.route('/rdvs/<id>/', methods = ['GET'])
def rdvs(id):
    #if request.method == 'GET':

        # results = Patients.query.join(RDV, Patients.id == RDV.patient_id)\
        # .add_columns(Patients.last_name, Patients.name, RDV.rdv_date, RDV.rdv_time, RDV.doctor)\
        # .filter (Patients.id == id)    
        # results.last_name=['last_name']
        # results.name=['name']
        # results.rdv_date=['rdv_date']
        # results.rdv_time=['rdv_time']
        # results.doctor = ['doctor']
       
        results = RDV.query.filter_by(patient_id=id)
        return render_template('rdvs.html', rdv = results)


# This is the route to add new rdv  via html modal form
@app.route('/new', methods = ['POST'])
def new():
 
    if request.method == 'POST':
        patient_id= request.form['id']
        last_name = request.form['last_name']
        name = request.form['name']
        rdv_date = request.form['rdv_date']
        rdv_time = request.form['rdv_time']
        doctor = request.form['doctor']
    
        my_data = RDV(patient_id, last_name, name, rdv_date, rdv_time, doctor)
        db.session.add(my_data)
        db.session.commit()

        flash('Appointment sucessfully added') # My message will show up when new rdv is added
 
        return redirect(url_for('Index'))

# This  is the route to add new patient via html modal form
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


 # This is the route to edit patient rdv
@app.route('/editRdv', methods = ['GET', 'POST'])
def editRdv():

     if request.method == 'POST':
        my_data = RDV.query.get(request.form.get('id'))
        
        my_data.last_name = request.form['last_name']
        my_data.name = request.form['name']
        my_data.rdv_date = request.form['rdv_date']
        my_data.rdv_time = request.form['rdv_time']
        my_data.doctor = request.form['doctor']

        db.session.commit()
        flash("Patient RDV Updated Successfully")
 
        return redirect(url_for('see_rdvs'))
       
 
 # This is the route to update patient info
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

# This route is for deleting a rdv
@app.route('/deleteRdv/<id>/', methods = ['GET', 'POST'])
def deleteRdv(id):
    my_data = RDV.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Patient appointment deleted successfully")
 
    return redirect(url_for('see_rdvs'))

# This route is for deleting a patient
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Patients.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Patient file deleted successfully")
 
    return redirect(url_for('Index'))
         



if __name__ == "__main__":
    app.run(debug=True)