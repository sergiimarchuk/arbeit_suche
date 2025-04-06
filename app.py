from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  
# Updated initialization pattern for version 3.x
db = SQLAlchemy()
db.init_app(app)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(100), nullable=False)
    stadt = db.Column(db.String(100), nullable=False)
    index_stadt = db.Column(db.Integer, nullable=True)
    strasse = db.Column(db.String(100), nullable=False)
    ort = db.Column(db.Integer, nullable=True)
    date_gekommen = db.Column(db.DateTime, nullable=True)
    date_email = db.Column(db.DateTime, nullable=True)
    detail = db.Column(db.String(1000), nullable=True)
    status = db.Column(db.String(500), nullable=True)
    transport = db.Column(db.String(500), nullable=True)
    
    def __repr__(self):
        return '<Company %r>' % self.id
    
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")
    
@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "user page :" + name + ' ' + str(id)

@app.route('/base')
def base():
    return render_template("base.html")

@app.route('/add-company', methods=['POST','GET'])
def add_company():
    if request.method == "POST":
        companyname = request.form['companyname']
        stadt = request.form['stadt']
        
        # Convert index_stadt to integer or None if empty
        index_stadt_str = request.form['index_stadt']
        index_stadt = int(index_stadt_str) if index_stadt_str.strip() else None
        
        strasse = request.form['strasse']
        
        # Convert ort to integer or None if empty
        ort_str = request.form['ort']
        ort = int(ort_str) if ort_str.strip() else None
        
        # Convert date strings to datetime objects
        date_gekommen_str = request.form['date_gekommen']
        date_email_str = request.form['date_email']
        
        # Parse dates if not empty
        date_gekommen = datetime.strptime(date_gekommen_str, '%Y-%m-%d') if date_gekommen_str.strip() else None
        date_email = datetime.strptime(date_email_str, '%Y-%m-%d') if date_email_str.strip() else None
        
        status = request.form['status']
        transport = request.form['transport']
        
        # Create company object with proper types
        company = Company(
            companyname=companyname, 
            stadt=stadt, 
            index_stadt=index_stadt, 
            strasse=strasse, 
            ort=ort, 
            date_gekommen=date_gekommen, 
            date_email=date_email, 
            status=status,
            transport=transport
        )
        
        try:
            db.session.add(company)
            db.session.commit()
            return redirect('/add-company')
        except Exception as e:
            # Print the error for debugging
            print(f"Error occurred: {e}")
            return f"An error occurred: {e}"
        
    else:
        return render_template("add-company.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)