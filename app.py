from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  
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
    all_events = db.Column(db.Text, nullable=True)
    
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

@app.route('/ups')
def ups():
    return render_template("ups.html")

@app.route('/error')
def error_page():
    # Get the error message from the query parameter
    error_message = request.args.get('error_message', '')
    
    # Pass error message to errors.html template
    return render_template("errors/errors.html", error_message=error_message)

@app.route('/report')
def report():
    companyname = Company.query.order_by(Company.all_events).all();
    return render_template("report.html", companyname=companyname)

@app.route('/add-company', methods=['POST', 'GET'])
def add_company():
    if request.method == "POST":
        companyname = request.form['companyname']
        
        # Check if company name is empty
        if not companyname.strip():
            # If empty, redirect to the error page with an error message
            error_message = "Company name cannot be empty"
            return redirect(url_for('error_page', error_message=error_message))
        
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
        all_events = request.form['all_events']
        
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
            transport=transport,
            all_events=all_events
        )
        
        try:
            db.session.add(company)
            db.session.commit()
            return redirect('/add-company')
        except Exception as e:
            # Print the error for debugging
            print(f"Error occurred: {e}")
            #return f"An error occurred: {e}"
            return redirect('/ups')
        
    else:
        return render_template("add-company.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)