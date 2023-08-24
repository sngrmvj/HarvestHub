from flask import request, make_response, jsonify
import traceback, datetime, redis, uuid
from models import Purchases, Retailer
from setup import app, db




# >>>> Attributes
GET_ALL_COMMODITIES = "SELECT distinct(commodities) FROM warehouse"



""" >>>> APIs """

# ---------------------------------------------------------------------------------------------------------------------
# >>>> Submission of Login Form
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/login', methods=['PUT'])
def login_form():
    authenticated = False  # Replace with your authentication logic

    data = request.get_json()
    try:
        retailer_results = Retailer.query.filter_by(supplier_email=data['email']).all()
    except Exception as error:
        print(f"Error in fetching the login details - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in fetching the login details - {error}"}), 500
    else:
        if retailer_results:
            authenticated = retailer_results.check_password(data['password'])

    if authenticated:
        # Create a response object
        response = make_response(jsonify({'message': 'Authentication successful'}))
        # Set a cookie to indicate successful login with 90 minutes of expiry
        response.set_cookie('retailer_login_status', 'success', secure=True, expires=datetime.datetime.now() + datetime.timedelta(minutes=90))
        return response
    else:
        return jsonify({"error": "Not Authenticated"}), 404


# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Submission of register Form
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/register', methods=['POST'])
def register():

    data = request.get_json()
    try:
        retailer = Retailer(data['email'], data['username'], data['password'], data['address'], data['phonenumber']) 
        db.session.add(retailer)
        db.session.commit()
    except Exception as error:
        print(f"Error in fetching the login details - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in fetching the login details - {error}"}), 500


    return jsonify({"data": "Registered successfully"})


# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Display all the commodities
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/commodties', methods=['GET'])
def get_all_commodities():
    try:
        # Run native SQL query
        result = db.session.execute(GET_ALL_COMMODITIES)

        if not result:
            return jsonify({'error': "Data not retrieved"}), 500

        commodities = []
        # Access the result
        for row in result:
            commodities.append(row)
        else:
            return jsonify({'data': commodities}), 200
    except Exception as error:
        print(f"Error in fetching the get_all_commodities - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in fetching the all commodties - {error}"}), 500

# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/receipts', methods=['GET'])
def get_all_receipts():

    arguments =  request.args.get('email')
    try:
        retailer_results = Retailer.query.filter_by(email=arguments).all()

        retailer_email = None
        for retailer in retailer_results:
            retailer_email = retailer.email
        
        purchase_list = Purchases.query.filter_by(retailer_email=retailer_email).all()

        purchases = []
        for item in purchase_list:
            # Todo - This should exclude the commodities.
            purchases.append(item)
    except Exception as error:
        print(f"Error in retrieveing the all receipts - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in retrieveing the all receipts - {error}"}), 500
    else:
        return jsonify({'data': purchases}), 200

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/receipt', methods=['GET'])
def get_receipt():

    arguments =  request.args.get('id')

    try:
        purchese_order = Purchases.query.filter_by(purchase_id=arguments).all()
        purchase = []
        for item in purchese_order:
            # Todo - This should include the commodities of a particular order
            purchase.append(item)
    except Exception as error:
        print(f"Error in retrieveing the particular receipt - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in retrieveing the particular receipt - {error}"}), 500
    else:
        return jsonify({'data': purchase}), 200
    

# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/cart', methods=['GET'])
def get_cart():

    try:
        with redis.Redis(host='localhost', port=6379, db=0, password=None) as redis_connection:
            retrieved_data = redis_connection.hgetall('<retailer_email>')
            # Convert the retrieved bytes to a Python dictionary
            retrieved_dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in retrieved_data.items()}
            if retrieved_dict:
                return jsonify({'data':retrieved_dict}), 200
            else:
                return jsonify({'message': "Cart not available"}), 404
    except Exception as error:
        print(f"Error in fetching the cart - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in fetching the cart - {error}"}), 500

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/cart', methods=['PUT'])
def add_to_cart():
    data = request.get_json()

    try:
        with redis.Redis(host='localhost', port=6379, db=0, password=None) as redis_connection:
            redis_connection.hmset('<retailer_email>', data)
            retrieved_data = redis_connection.hgetall('<retailer_email>')
            if retrieved_data:
                return jsonify({"message":"Added to the cart"}), 200
            else:
                raise Exception("Error in adding the element to the cart")
    except Exception as error:
        print(f"Error in fetching the cart - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in fetching the cart - {error}"}), 500

# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/cart', methods=['DELETE'])
def delete_from_cart():
    commodity = request.args.get('commodity')
    try:
        with redis.Redis(host='localhost', port=6379, db=0, password=None) as redis_connection:
            retrieved_data = redis_connection.hgetall('<retailer_email>') # retrieveing the data for the retailer email
            if retrieved_data:
                retrieved_dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in retrieved_data.items()} # Converting the binary ascii
                del retrieved_dict[commodity] # Deleting
                redis_connection.hmset('<retailer_email>', retrieved_dict) # Re-inserting into the redis
                return jsonify({"message":"Added to the cart"}), 200
            else:
                return jsonify({'message': "Cart data not available"}), 404
    except Exception as error:
        print(f"Error in fetching the cart - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in fetching the cart - {error}"}), 500


# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/purchase', methods=['PUT'])
def purchase():

    data = request.get_json()
    purchase_id = str(uuid.uuid4())

    try:
        retailer_results = Retailer.query.filter_by(email=data['email']).all()

        # We need to loop as the retailer_results is an object
        for retailer in retailer_results:
            purchase = Purchases(purchase_id, "HarvestHub_Owner", retailer.email, retailer.address, retailer.phonenumber, datetime.datetime.utcnow, data['commodities'])
            db.session.add(purchase)
            db.session.commit()
    except Exception as error:
        print(f"Error in adding the purchase details - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in adding the purchase details - {error}"}), 500

    try:
        pass
        # Todo - Retrive the details based on the bag_id, farmer_id, agent_id, commodity based on the data['commodities]
    except Exception as error:
        print(f"Error in updating the warehouse details about the purchase - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in adding the warehouse details about the purchase - {error}"}), 500

    try:
        pass
        # Todo - Retrive the details based on the bag_id, farmer_id, agent_id, commodity based on the data['commodities]
    except Exception as error:
        print(f"Error in adding the statistics details about the purchase - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in adding the statistics details about the purchase - {error}"}), 500

    
    return jsonify({'data':""})

# ---------------------------------------------------------------------------------------------------------------------




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000, host='0.0.0.0')





