from flask import render_template, request, redirect, url_for
import random, string, traceback, redis, os
from setup import app, db
from models import Farmer, Agent, SellStatistics, WareHouse



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
    
    data = fetch_new_commodities()

    return render_template('index.html', message=arg_message, data=data)

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
    try:
        agent = Agent(agent_id=generate_id(), username=request.form.get('name'), email=request.form.get('email'), password=request.form.get('password'))
        db.session.add(agent)
        db.session.commit()
    except Exception as error:
        print(f"Error in addition of agent - {error}")
        message = f"Error in addition of agent - {error}"
    else:
        message = 'Agent successfully added'

    return redirect(url_for('agent_page', message=message))

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Add Farmer details to DB
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/owner/add_farmer', methods=['POST'])
def add_farmer():
    try:
        farmer = Farmer(farmer_id=generate_id(), username=request.form.get('name'), email=request.form.get('email'), password=request.form.get('password'))
        db.session.add(farmer)
        db.session.commit()
    except Exception as error:
        print(f"Error in addition of farmer - {error}")
        message = f"Error in addition of farmer - {error}"
    else:
        message = 'Farmer successfully added'

    return redirect(url_for('farmer_page', message=message))

# ---------------------------------------------------------------------------------------------------------------------




# ---------------------------------------------------------------------------------------------------------------------

def fetch_new_commodities():

    try:
        with redis.Redis(host='localhost', port=6379, db=2, password=os.getenv('REDIS_PASSWORD')) as redis_connection: 
            retrieved_data = redis_connection.hgetall("new_commoditites")
            if retrieved_data:
                retrieved_dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in retrieved_data.items()}
            else:
                raise Exception("Data not retrieved from redis")
    except Exception as error:
        print(f"Error in getting the date from redis for the owner - {error} \n\n{traceback.format_exc()}")
    else:
        temp = []
        for item in retrieved_dict:
            temp.append(retrieved_dict[item])
    
    return {}

# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Add Commodtities
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/owner/add_commodity', methods=['PUT'])
def add_commodity():

    insertion_successful = True

    try:
        # First we are removing the element from the redis
        with redis.Redis(host='localhost', port=6379, db=2, password=os.getenv('REDIS_PASSWORD')) as redis_connection: 
            retrieved_data = redis_connection.hgetall("new_commoditites")
            if retrieved_data:
                retrieved_dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in retrieved_data.items()}
                del retrieved_dict[request.form.get('bag_id')]
                redis_connection.hmset("new_commoditites", retrieved_dict)
            else:
                raise Exception(f"Data not retrieved from redis")
    except Exception as error:
        print(f"Error in retrieval / insertion to the redis - {error} \n\n{traceback.format_exc()}")
        insertion_successful = False

    try:
        warehouse = WareHouse(
            agent_id=request.form.get('agent_id'),
            farmer_id=request.form.get('farmer_id'),
            bag_id=request.form.get('bag_id'),
            owner=request.form.get('owner'),
            commodity=request.form.get('commodity'),
            price_kg=request.form.get('price_kg'),
            weight=request.form.get('weight'),
            delivered=True,
            profit_percent=request.form.get('profit_percent')
        )
        db.session.add(warehouse)
        db.session.commit()
    except Exception as error:
        print(f"Error in adding the details to the warehouse for farmer id - {{request.form.get('farmer_id')}} / Bag id - {request.form.get('bag_id')} - {error} - \n\n{traceback.format_exc()}")
        insertion_successful = False

    message = 'Added the commodity to the database'
    if not insertion_successful:
        message = "insertion is not successful"

    return redirect(url_for('owner_page', message=message))

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get the monthly statistics
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/owner/statistics', methods=['GET'])
def get_monthly_statistics():

    try:
        sell_statistics = SellStatistics.query.all() 
        row_data = []
        for item in sell_statistics:
            row_data.append({
                "Bag ID": item.bag_id,
                "Farmer ID": item.farmer_id,
                "Commodity": item.commodity,
                "Price kg": item.price_kg,
                "Selling Price" : item.selling_price,
                "Date of sell": item.created_date
            })
    except Exception as error:
        print(f"Error in fetching the statistics - {error} \n\n {traceback.format_exc()}")
    
    return render_template('statistics.html', row_data=row_data)

# ---------------------------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003, host='0.0.0.0')


