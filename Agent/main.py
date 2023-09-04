from flask import Flask, render_template, request, redirect, url_for, make_response
import json, uuid, datetime, redis, traceback, os, copy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:root@postgres:5432/harvesthub'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
        login_query = text("SELECT password FROM agent WHERE email= :email")
        result = db.session.execute(login_query, {"email": data['email']})
    except Exception as error:
        print(f"Error in fetching the login details - {error} \n\n{traceback.format_exc()}")
        return redirect(url_for('agent_page', message= f'Error in fetching the login details - {error}'))
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
        response.set_cookie('agent_email', request.form.get('email'), secure=True, expires=datetime.datetime.now() + datetime.timedelta(minutes=90))
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
        id_query = text("SELECT agent_id FROM agent WHERE email= :email")
        result = db.session.execute(id_query, {"email": request.form.get('agent_email')})
        for item in result:
            agent_id = item[0]
            break
    except Exception as error:
        print(f"Error in fetching the cart - {error} \n\n{traceback.format_exc()}")
    
    data = {
        "commodity": request.form.get('commodity').capitalize(),
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
        with redis.Redis(host='redis', port=6379, db=1, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            # redis_connection.hdel(data['agent_id'], 'items')
            retrieved_data = redis_connection.hgetall(data['agent_id'])
            if retrieved_data:
                # Deserialize the 'items' field value back into a list
                if b'items' in retrieved_data and len(retrieved_data[b'items']) > 0:
                    stored_list = json.loads(retrieved_data[b'items'].decode('utf-8'))
                    stored_list.append(data) # Append the data to the retrievd list
                    redis_connection.hset(data['agent_id'], 'items', json.dumps(stored_list)) # Store it back to the redis
                else:
                    print(retrieved_data)
                    redis_connection.hset(data['agent_id'], 'items', json.dumps([data]))
            else:
                # Use HMSET to set the serialized list as a value for the 'items' field
                redis_connection.hset(data['agent_id'], 'items', json.dumps([data]))
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
# >>>> Send Truck API
# ---------------------------------------------------------------------------------------------------------------------------------
@app.route('/agent/truck', methods=['GET'])
def send_truck_to_owner():

    isTruckSent, agent_id = False, None

    try:
        id_query = text("SELECT agent_id FROM agent WHERE email= :email")
        result = db.session.execute(id_query, {"email": request.cookies.get('agent_email')})
        for item in result:
            agent_id = item[0]
    except Exception as error:
        print(f"Error in fetching the cart - {error} \n\n{traceback.format_exc()}")

    if agent_id:
        value = send_truck(agent_id)

        if not value:
            return redirect(url_for('agent_page', message="Error in sending the truck"))
        else:
            isTruckSent = True
    else:
        return redirect(url_for('agent_page', message="Error in fetching the id of the agent"))
    
    if isTruckSent:
        return redirect(url_for('agent_page', message="Truck sent successfully"))


# ---------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Logout API
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/agent/logout', methods=['GET'])
def logout():
    response = make_response(redirect(url_for('agent_page', message="Successfully logged out!!")))
    response.delete_cookie('login_status')
    response.delete_cookie('agent_email')
    return response
# ---------------------------------------------------------------------------------------------------------------------



def send_truck(agent_id):

    """ 
        The idea is we use this function to update the agent_farmer database, we empty the agent_id's with empty []
        Once agent_farmer is updated we add them in another database of redis the updated created date. 
        Once the created date is read by the owner we remove the created date from the redis and fetch the items from the agent_farmer for which owner adds to warehouse.
    """

    truck_id = str(uuid.uuid4())
    info_to_owner = None

    try:
        with redis.Redis(host='redis', port=6379, db=1, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            retrieved_data = redis_connection.hgetall(agent_id)
            if retrieved_data:
                if b'items' in retrieved_data and len(retrieved_data[b'items']) > 0:
                    stored_list = json.loads(retrieved_data[b'items'].decode('utf-8'))
                    if not stored_list:
                        return False
                    info_to_owner = copy.deepcopy(stored_list)

                agent_farmer_query = text("INSERT INTO agent_farmer (agent_id, farmer_id, truck_id, bag_id, owner, commodity, price_kg, weight, created_date) VALUES (:agent_id, :farmer_id, :truck_id, :bag_id, :owner, :commodity, :price_kg, :weight, :created_date)")

            if len(stored_list) > 0:
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
                                'commodity': item['commodity'].capitalize(),
                                'price_kg': item['price'],
                                'weight': item['weight'],
                                'created_date': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                            }
                        )
                        db.session.commit()

            redis_connection.hset(agent_id, 'items', '')
    except Exception as error:
        print(f"Error in fetching the cart - {error} \n\n{traceback.format_exc()}")
        return False 
    else:
        if info_to_owner:
            try:
                print(stored_list)
                with redis.Redis(host='redis', port=6379, db=2, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
                    if len(stored_list) > 0:
                        for item in stored_list: 
                            temp = {
                                'agent_id': item['agent_id'],  # New weight value
                                'farmer_id': item['farmer_id'],   # Bag ID to identify the row to update
                                'truck_id': truck_id,
                                'bag_id': item['bag_id'],
                                'owner': 'HarvestHub_Owner',
                                'commodity': item['commodity'].capitalize(),
                                'price_kg': item['price'],
                                'weight': item['weight'],
                                'created_date': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                            }
                            redis_connection.hset('new_commoditites', item['bag_id'], json.dumps(temp))
                    print(f"Insertion into redis for database 2 - {item['bag_id']}")
                return True
            except Exception as error:
                print(f"Error in insertion to the redis database 2")
        
# ---------------------------------------------------------------------------------------------------------------------------------




if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0')

