from flask import Flask, render_template, request, redirect, url_for, jsonify
import random, string

app = Flask(__name__)



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Helper Functions
# ---------------------------------------------------------------------------------------------------------------------
def generate_id(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Redirect URI to make sure the app starts with /owner
# ---------------------------------------------------------------------------------------------------------------------
@app.route("/")
def root():
    return redirect(url_for('owner_page'))

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> First API to get Called
# ---------------------------------------------------------------------------------------------------------------------
@app.route("/owner/")
def owner_page():
    arg_message = request.args.get('message')  # Passed during redirect
    if not arg_message:
        arg_message = "Welcome"

    return render_template('index.html', message=arg_message)

# ---------------------------------------------------------------------------------------------------------------------
    

# ---------------------------------------------------------------------------------------------------------------------
# >>>> Add Agent page
# ---------------------------------------------------------------------------------------------------------------------
@app.route("/owner/agent")
def agent_page():
    arg_message = request.args.get('message')  # Passed during redirect
    if not arg_message:
        arg_message = "Welcome"
    return render_template('add_agent.html', message=arg_message)

# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Add Farmer page
# ---------------------------------------------------------------------------------------------------------------------
@app.route("/owner/farmer")
def farmer_page():
    arg_message = request.args.get('message')  # Passed during redirect
    if not arg_message:
        arg_message = "Welcome"
    return render_template('add_farmer.html', message=arg_message)

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Add Agent details to DB
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/owner/add_agent', methods=['POST'])
def add_agent():
    data = {
        "email": request.form.get('email'),
        "password": request.form.get('password'),
        "name": request.form.get('name'),
        'id': generate_id()
    }

    # TODO - Code to add it in the database


    return redirect(url_for('agent_page', message='Successfully added'))

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Add Farmer details to DB
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/owner/add_farmer', methods=['POST'])
def add_farmer():
    data = {
        "email": request.form.get('email'),
        "password": request.form.get('password'),
        "name": request.form.get('name'),
        'id': generate_id()
    }

    # TODO - Code to add it in the database


    return redirect(url_for('farmer_page', message='Successfully added'))

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Add Commodtities
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/owner/add_commodities', methods=['POST'])
def add_commodities():

    # TODO - Code to add it in the database

    return redirect(url_for('owner_page', message='Added the commodity to the database'))

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get the monthly statistics
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/owner/statistics', methods=['GET'])
def get_monthly_statistics():

    # TODO - Code to add it in the database
    
    return redirect(url_for('owner_page', message='Added the commodity to the database'))

# ---------------------------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    app.run(debug=True, port=5003, host='0.0.0.0')


