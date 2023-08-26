from flask import Flask, Response, render_template, request, redirect, url_for, make_response
import json, uuid, datetime, redis, traceback, os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
TRUCK_WEIGHT = 50000



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

    try:
        login_query = "SELECT password FROM agent WHERE email= :email"
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
            return redirect(url_for('agent_page', message='User not available'))

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

    global TRUCK_WEIGHT
    isTruckSent, agent_id = False, None

    try:
        id_query = "SELECT agent_id FROM agent WHERE email= :email"
        result = db.session.execute(id_query, {"email": request.form.get('agent_email')})
        row = result.fetchone()
        if row:
            agent_id = row[0]
    except Exception as error:
        print(f"Error in fetching the cart - {error} \n\n{traceback.format_exc()}")
    
    data = {
        "commodity": request.form.get('commodity'),
        "flag": False,
        "price": float(request.form.get('price')),
        "weight": float(request.form.get('weight')),
        "bag_id": str(uuid.uuid4()),
        "farmer_id": request.form.get('farmer_id'),
        "agent_id": agent_id
    }

    if (TRUCK_WEIGHT - data['weight']) < 0:
        value = send_truck(agent_id)
        if not value:
            return redirect(url_for('agent_page', message="Error in sending the truck"))
        else:
            isTruckSent = True
    else:
        TRUCK_WEIGHT = TRUCK_WEIGHT - data['weight']

    try:
        with redis.Redis(host='localhost', port=6379, db=1, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            retrieved_data = redis_connection.hgetall(data['agent_id'])
            if retrieved_data:
                # Deserialize the 'items' field value back into a list
                if b'items' in retrieved_data:
                    stored_list = json.loads(retrieved_data[b'items'].decode('utf-8'))
                    stored_list.append(data) # Append the data to the retrievd list
                    redis_connection.hmset(data['agent_id'], {'items': json.dumps([stored_list])}) # Store it back to the redis
                else:
                    print("Looks like the items key not available in the key retrieved")
            else:
                # Use HMSET to set the serialized list as a value for the 'items' field
                redis_connection.hmset(data['agent_id'], {'items': json.dumps([data])})
                # Setting the list as the data so that we can keep on add the bags to the list till the truck weight goes down
    except Exception as error:
        print(f"Error in adding the bag - {error} \n\n{traceback.format_exc()}")
        return redirect(url_for('agent_page', message=error))
    else:
        message = "Bag data successfully added"
        if isTruckSent:
            message = 'Truck is sent and data successfully added to new bag.'
        return redirect(url_for('agent_page', message=message))


# ---------------------------------------------------------------------------------------------------------------------------------





# ---------------------------------------------------------------------------------------------------------------------------------
# >>>> Submission of Bag Data
# ---------------------------------------------------------------------------------------------------------------------------------
# @app.route('/agent/truck', methods=['POST'])
def send_truck(agent_id):


    """ 
        The idea is we use this function to update the agent_farmer database, we empty the agent_id's with empty []
        Once agent_farmer is updated we add them in another database of redis the updated created date. 
        Once the created date is read by the owner we remove the created date from the redis and fetch the items from the agent_farmer for which owner adds to warehouse.
    """

    truck_id = str(uuid.uuid4())

    try:
        with redis.Redis(host='localhost', port=6379, db=1, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            retrieved_data = redis_connection.hgetall(agent_id)
            if retrieved_data:
                if b'items' in retrieved_data:
                    stored_list = json.loads(retrieved_data[b'items'].decode('utf-8'))

                agent_farmer_query = "INSERT INTO agent_farmer (agent_id, farmer_id, truck_id, bag_id, owner, commodity, price_kg, weight) VALUES (:agent_id, :farmer_id, :truck_id, :bag_id, :owner, :commodity, :price_kg, :weight)"

                for item in stored_list:
                    with app.app_context():
                        db.session.execute(
                            agent_farmer_query,
                            {
                                'agent_id': item['agent_id'],  # New weight value
                                'farmer_id': item['farmer_id'],   # Bag ID to identify the row to update
                                'truck_id': truck_id,
                                'bag_id': item['bag_id'],
                                'owner': 'HarvestHub_Owner',
                                'commodity': item['commodity'],
                                'price_kg': item['price'],
                                'weight': item['weight']
                            }
                        )
                        db.session.commit()
            redis_connection.hmset(agent_id, {'items': json.dumps([])})
    except Exception as error:
        print(f"Error in fetching the cart - {error} \n\n{traceback.format_exc()}")
        return False 
    else:
        return True


# ---------------------------------------------------------------------------------------------------------------------------------






if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0')

