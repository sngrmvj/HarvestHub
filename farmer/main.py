from flask import Flask, Response, render_template, request, redirect, url_for, make_response
import json, uuid, datetime

app = Flask(__name__)


""" >>>> Function Calls """


# ------------------------------------------------- Custom Response Function ------------------------------------------

def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )


# ---------------------------------------------------------------------------------------------------------------------


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
    if login_status == 'success':
        # Here in this case if the cookie is not there we need to make sure that farmer logs in
        return render_template('login.html', message=arg_message)
    else:
        return render_template('index.html', message=arg_message)


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

    print(data)

    # TODO - need to check the data with the database The message is getting appended in the URL We need to make sure that is correct

    if authenticated:
        # Create a response object
        response = make_response(redirect(url_for('farmer_page', message="Successfully logged In!!")))
        # Set a cookie to indicate successful login with 90 minutes of expiry
        response.set_cookie('farmer_login_status', 'success', secure=True, expires=datetime.datetime.now() + datetime.timedelta(minutes=90))
        return response
    else:
        return redirect(url_for('farmer_page', message='Authentication failed'))


# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Fetch the list of receipts for the farmer
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/farmer/allReceipts', methods=['GET'])
def get_receipts():
    data = {}

    # TODO - The data successfully fetched and stored it in the global variable. Here the farmer has to use his ID

    return redirect(url_for('display_receipt', data=data))


# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Display of the receipt
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/farmer/receipt', methods=['PUT'])
def display_receipt():
    data = request.form.get('data')
    # TODO = Please check this
    return render_template('receipt.html', message=data)


# ---------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True, port=5002, host='0.0.0.0')
