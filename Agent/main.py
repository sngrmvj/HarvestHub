from flask import Flask, Response, render_template, request, redirect, url_for, make_response
import json, uuid, datetime

app = Flask(__name__)

""" >>>> Function Calls """


# ------------------------------------------------- Custom Response Function ------------------------------------------------------

def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )


# ---------------------------------------------------------------------------------------------------------------------------------


""" >>>> APIs """


# ---------------------------------------------------------------------------------------------------------------------------------
# >>>> Redirect URI to make sure the app starts with /agent
# ---------------------------------------------------------------------------------------------------------------------------------
@app.route("/")
def root():
    return redirect(url_for('agent_page'))


# ---------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------
# >>>> First API to get Called
# ---------------------------------------------------------------------------------------------------------------------------------
@app.route("/agent/")
def agent_page():
    login_status = request.cookies.get('login_status')
    print(login_status)
    arg_message = request.args.get('message')  # Passed during redirect
    if not arg_message:
        arg_message = "Welcome"
    if login_status != 'success':
        # Here in this case if the cookie is not there we need to make sure that agent logs in
        return render_template('login.html', message=arg_message)
    else:
        return render_template('index.html', message=arg_message)


# ---------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------
# >>>> Submission of Login Form
# ---------------------------------------------------------------------------------------------------------------------------------
@app.route('/agent/login', methods=['PUT', 'POST'])
def login_form():
    authenticated = False  # Replace with your authentication logic
    data = {
        "email": request.form.get('email'),
        "password": request.form.get('password'),
    }

    print(data)

    # TODO - need to check the data with the database The message is getting appended in the URL ... We need to make sure that is correct

    if authenticated:
        # Create a response object
        response = make_response(redirect(url_for('agent_page', message="Successfully logged In!!")))
        # Set a cookie to indicate successful login with 90 minutes of expiry
        response.set_cookie('login_status', 'success', secure=True, expires=datetime.datetime.now() + datetime.timedelta(minutes=90))
        return response
    else:
        return redirect(url_for('agent_page', message='Authentication failed'))


# ---------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------
# >>>> Submission of Bag Data
# ---------------------------------------------------------------------------------------------------------------------------------
@app.route('/agent/submit', methods=['POST'])
def insert_commodity_bag():
    data = {
        "commodity": request.form.get('commodity'),
        "flag": False,
        "price": float(request.form.get('price')),
        "weight": float(request.form.get('weight')),
        "bag_id": str(uuid.uuid4()),
        "farmer_id": request.form.get('farmer_id'),
        "agent_id": request.form.get('agent_id'),
    }

    print(data)

    # TODO - The data successfully added
    return redirect(url_for('agent_page', message='Data successfully added'))


# ---------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0')

# TODO
# 1. Send Truck
# 2. Agent-ID automation
# 3. Insertions into database.
