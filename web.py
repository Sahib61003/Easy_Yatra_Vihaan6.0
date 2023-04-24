from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL
import yaml
from flask_session import Session
from werkzeug.utils import secure_filename
import os
import cv2
import io


app = Flask(__name__)

db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['name']
        email = userDetails['email']
        password = userDetails['password']
        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO credentials(Name, Email_Id, Password) VALUES (%s,%s,%s)",(username, email, password))       
            mysql.connection.commit()

        return render_template('index.html')
    return render_template('login.html')

app.config['UPLOAD_FOLDER'] = "E:\images_folderS"
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #userDetails = request.form.get
        passport = request.form.get('passport')
        visa = request.form.get('visa')
        age = request.form.get('age')
        arrival = request.form.get('arrival')
        departure = request.form.get('departure')
        terminal = request.form.get('terminal')
        flight = request.form.get('flight')
        passenger = request.files['passenger']
        #print("\n\n\n")
        print(passenger)
        #print("\n\n\n")
        file = secure_filename(passenger.filename)
        basedir = os.path.abspath(os.path.dirname(__file__))
        #passenger.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename=filename))
        passenger.save(app.config['UPLOAD_FOLDER'] + passenger.filename)
        #cv2.FileStorage.(passenger, app.config['UPLOAD_FOLDER'] + "/" + passenger.filename, cv2.FileStorage_FORMAT_AUTO)
        #cv2.FileStorage
        #buffer = io.BytesIO()
        #cv2.imwrite(buffer, passenger)
        #img_bytes = buffer.getvalue()
        #with open(passenger.filename, 'wb') as f:
            #f.write(img_bytes)
        
        

        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO passengerinfo (PassportNumber, VisaNumber, Age, ArrivalTime, DepartureTime, TerminalNumber, FlightNumber, PassengerUID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (passport, visa, age, arrival, departure, terminal, flight, passenger))       
            mysql.connection.commit()
        
    
        return render_template('profile.html')
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST`':
        name = request.form['Name']
        
        # connect to the database
        cur = mysql.connection.cursor()
        
        # execute a query to fetch the email and password for the given name
        cur.execute("SELECT email, password FROM credentials WHERE name = %s", (name))
        
        # fetch the first row from the query result
        row = cur.fetchone()
        print(row)
        # close the database connection
        cur.close()
        
        if row:
            email = row[0]
            password = row[1]
            print(email, password)
            return render_template('profile.html', name=name, email=email, password=password)
        else:
            return render_template('not_found.html', name=name)
    else:
        name = request.form['Name']
        
        # connect to the database
        cur = mysql.connection.cursor()
        
        # execute a query to fetch the email and password for the given name
        cur.execute("SELECT email, password FROM credentials WHERE name = %s", (name))
        
        # fetch the first row from the query result
        row = cur.fetchone()
        print(row)
        # close the database connection
        cur.close()
        
        if row:
            email = row[0]
            password = row[1]
            print(email, password)
            return render_template('profile.html', name=name, email=email, password=password)
        else:
            return render_template('not_found.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
