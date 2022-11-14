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

# This is the home page 
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("home.html")

# This is the menu page
@app.route("/menu/", methods=['GET', 'POST'])
def menu():
    cur.execute("SELECT * FROM food")
    food = cur.fetchall()
    # Pass food to the menu page 
    return render_template("menu.html", food = food)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    # db.ping(reconnect=True)
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'firstName' in request.form and 'password1' in request.form:
        # Create variables for easy access
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        # Check if account exists using MySQL
        # cur = conection.cursor(cursors.DictCursor)
        cur.execute(f"SELECT * FROM customers WHERE name = '{firstName}' AND password1 = '{password1}'")
        account = request.form.to_dict()
        # Fetch one record and return result
        account = cur.fetchall()

        # If account exists in accounts table in out database
        if account:
        #     # Create session data, we can access this data in other routes
            for row in account:
                customer_id = list(row)[0]
                firstName = list(row)[2]
                session['customer_id'] = customer_id
                session['firstName'] = firstName
                customer_id = session['customer_id']
                firstName = session['firstName']
                session['loggedin'] = True

                 
            # session['customer_id'] = request.form.get('customer_id')
            # session['firstName'] = request.form.get('firstName')
            # session['email'] = request.form.get('email')
            # session['phone'] = request.form.get('phone')
            # session['address'] = request.form.get('address')
            # session['password1'] = request.form.get('password1')
            # session['password2'] = request.form.get('password2')

            return redirect(url_for('menu'))

        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password!', category='error')
            # msg = 'Incorrect username/password!'
    return render_template('login.html')

@app.route("/signUp/", methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        customer_id = None
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        phone = request.form.get('phone')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be grater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be grater than 1 characters.', category='error')
        elif len(phone) != 8:
            flash('Phone number have to be 5 number.', category='error')
        elif password1 != password2:
            flash('Password don\'s match.', category='error')
        elif len(password1) < 6:
            flash('Password must be at least 6 characters.', category='error')
        else:
            cur.execute("INSERT INTO customers VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(customer_id, email, firstName, phone, address, password1, password2))

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
#    Redirect to login page
   return redirect(url_for('login'))


def printOut():
    cur.execute('select * from customers')
    for row in cur.fetchall():
        print(f'customer_id {row[0]} eamil {row[1]} name {row[2]} phone  {row[3]} address {row[4]} password1 {row[5]} password2 {row[5]}')

# printOut()


if __name__ == "__main__":
    app.run(debug=True)