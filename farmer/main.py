from flask import Flask, render_template, request, redirect, url_for, make_response
import datetime, traceback
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:root@postgres:5432/harvesthub'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



""" >>>> APIs """


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Redirect URI to make sure the app starts with /farmer
# ---------------------------------------------------------------------------------------------------------------------
@app.route("/")
def root():
    return redirect(url_for('farmer_page'))


# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> First API to get Called
# ---------------------------------------------------------------------------------------------------------------------
@app.route("/farmer/")
def farmer_page():
    login_status = request.cookies.get('farmer_login_status')
    arg_message = request.args.get('message')  # Passed during redirect
    if not arg_message:
        arg_message = "Welcome"
    if login_status != 'success':
        # Here in this case if the cookie is not there we need to make sure that farmer logs in
        return render_template('login.html', message=arg_message)
    else:
        email = request.cookies.get('farmer_email')
        all_receipts = get_receipts(email)
        if not all_receipts:
            arg_message = "Error in fetching the receipts. Please contact the administrator"
        return render_template('index.html', message=arg_message, row_data=all_receipts)


# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Submission of Login Form
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/farmer/login', methods=['PUT', 'POST'])
def login_form():
    authenticated = False  # Replace with your authentication logic
    data = {
        "email": request.form.get('email'),
        "password": request.form.get('password'),
    }

    try:
        login_query = text("SELECT password FROM farmer WHERE email= :email")
        result = db.session.execute(login_query, {"email": data['email']})
    except Exception as error:
        print(f"Error in fetching the login details - {error} \n\n{traceback.format_exc()}")
        return redirect(url_for('farmer_page', message= f'Error in fetching the login details - {error}'))
    else:
        row = result.fetchone()
        if row:
            if row[0] == data['password']:
                authenticated = True
        else:
            return redirect(url_for('farmer_page', message='User not available'))

    if authenticated:
        # Create a response object
        response = make_response(redirect(url_for('farmer_page', message="Successfully logged In!!")))
        # Set a cookie to indicate successful login with 90 minutes of expiry
        response.set_cookie('farmer_login_status', 'success', secure=True, expires=datetime.datetime.now() + datetime.timedelta(minutes=90))
        response.set_cookie('farmer_email', request.form.get('email'), secure=True, expires=datetime.datetime.now() + datetime.timedelta(minutes=90))
        return response
    else:
        return redirect(url_for('farmer_page', message='Authentication failed'))


# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Logout API
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/farmer/logout', methods=['GET'])
def logout():
    response = make_response(redirect(url_for('farmer_page', message="Successfully logged out!!")))
    response.delete_cookie('farmer_login_status')
    response.delete_cookie('farmer_email')
    return response
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Fetch the list of receipts for the farmer
# ---------------------------------------------------------------------------------------------------------------------
def get_receipts(email):

    all_receipts, farmer_id = [], None

    try:
        get_id_query = text("SELECT farmer_id FROM farmer WHERE email= :email")
        result = db.session.execute(get_id_query, {'email': email})
        for item in result:
            farmer_id = item[0]
    except Exception as error:
        print(f"Failed to get the details of the farmer - {error}\n\n{traceback.format_exc()}")
        return []

    try:
        receipts_query = text("SELECT agent_id, farmer_id, truck_id, bag_id, owner, commodity, price_kg, weight, created_date FROM agent_farmer WHERE farmer_id= :farmer_id")
        result = db.session.execute(receipts_query, {'farmer_id': farmer_id})
        for row in result:
            all_receipts.append({
                'Agent ID': row.agent_id, 
                'Farmer ID': row.farmer_id, 
                'Truck ID': row.truck_id, 
                'Bag ID': row.bag_id, 
                'Owner': row.owner, 
                'Commodity': row.commodity, 
                'Selling Price': row.price_kg, 
                'Bag Weight': row.weight, 
                'Total Price': row.price_kg * row.weight,
                'Date of sell': row.created_date
            })
    except Exception as error:
        print(f"Error in fetching the all receipt details - {error} \n\n{traceback.format_exc()}")

    return all_receipts



# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Display of the receipt
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/farmer/receipt', methods=['POST'])
def display_receipt():

    username, receipt_data = None, {}

    try:
        pass
        # username_query = "SELECT username FROM farmer WHERE farmer_id= :farmer_id"
        # result = db.session.execute(username_query, {"farmer_id": farmer_id})
        # for row in result:
        #     username = row[0]

        # receipt_query = "SELECT agent_id, farmer_id, truck_id, bag_id, owner, commodity, price_kg, created_date FROM agent_farmer WHERE farmer_id=:farmer_id AND bag_id= :bag_id"
        # result = db.session.execute(receipt_query, {"bag_id": bag_id, "farmer_id": farmer_id})

        # for row in result:
        #     receipt_data['farmer'] = username
        #     receipt_data['agent_id'] = row[0]
        #     receipt_data['truck_id'] = row[2]
        #     receipt_data['bag_id'] = row[3]
        #     receipt_data['owner'] = row[4]
        #     receipt_data['commodity'] = row[5]
        #     receipt_data['price_kg'] = row[6]
        #     receipt_data['created_date'] = row[7]
    except Exception as error:
        print(f"Error in fetching the receipt details - {error} \n\n{traceback.format_exc()}")
    else:
        print(">>>> Receipt data retrieved")
        return render_template('receipt.html', data=receipt_data)


# ---------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True, port=5002, host='0.0.0.0')
