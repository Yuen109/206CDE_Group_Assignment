from flask import Flask, redirect, url_for, render_template, request, session, flash
import cx_Oracle

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'random string'

# Comment out if you use window
cx_Oracle.init_oracle_client(lib_dir="/Users/yuen/Downloads/instantclient_19_8")

try:
    conection = cx_Oracle.connect("G3_team006/ceG3_team006@144.214.177.102/xe")
except cx_Oracle.DatabaseError as er:
    print('There is an error in the Oracle database:', er)

cur = conection.cursor()

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route("/menu/", methods=['GET', 'POST'])
def menu():
    return render_template("menu.html")

@app.route('/login/profile/', methods=['GET', 'Post'])
def profile():
    db.ping(reconnect=True)
    # Check if user is loggedin
    if 'loggedin' in session:
    #     We need all the account info for the user so we can display it on the profile page
        cur = db.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT * FROM customers WHERE customer_id = %s', (session['id']))
        account = cur.fetchone()

    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cur = db.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT * FROM products WHERE user_name = %s AND customer_id = %s', (session['firstName'], session['id']))
        profile = cur.fetchall()

        # Show the profile page with account info
    return render_template('profile.html', account = account, profile = profile)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    # db.ping(reconnect=True)
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'firstName' in request.form and 'password1' in request.form:
        # Create variables for easy access
        firstName = request.form['firstName']
        password1 = request.form['password1']
        # Check if account exists using MySQL
        # cur = db.cursor(pymysql.cursors.DictCursor)
        cur.execute(f"SELECT * FROM customers WHERE name = '{firstName}' AND password1 = '{password1}'")
        # Fetch one record and return result
        account = cur.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['customer_id'] = account['customer_id']
            session['firstName'] = account['name']
            session['email'] = account['email']
            session['phone'] = account['phone']
            session['address'] = account['address']
            session['password1'] = account['password1']
            session['password2'] = account['password2']
            return redirect(url_for('menu'))

        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password!', category='error')
            # msg = 'Incorrect username/password!'
    return render_template('login.html')

@app.route("/signUp/", methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        phoneNum = request.form.get('phone')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be grater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be grater than 1 characters.', category='error')
        elif len(phoneNum) != 8:
            flash('Phone number have to be 5 number.', category='error')
        elif password1 != password2:
            flash('Password don\'s match.', category='error')
        elif len(password1) < 6:
            flash('Password must be at least 6 characters.', category='error')
        else:
            # cur = db.cursor()
            cur.execute("INSERT INTO customers (name, email, phone_num, address, password1, password2) VALUES ('%s', '%s', %s, '%s', '%s', '%s')", (firstName, email, phoneNum, address, password1, password2))

            try:
                cur.execute('commit')
                # print("Successfully inserted")
                flash('Create successfully')
                return redirect(url_for('login'))
            except:
                cur.rollback()
            
            cur.close()
            flash('Account created.', category='success')    

    return render_template("signUp.html")

@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   flash('You logout successfully!')
   # Redirect to login page
   return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)