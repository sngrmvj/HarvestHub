from flask import request, make_response, jsonify
import traceback, datetime, redis, uuid, jwt, os
from models import Purchases, Retailer
from setup import app, db




# >>>> Attributes
# Secret key for JWT token
SECRET_KEY = os.getenv('SECRET_KEY')


""" >>>> APIs """

# ---------------------------------------------------------------------------------------------------------------------
# >>>> Submission of Login Form
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/login', methods=['PUT'])
def login_form():
    authenticated = False  # Replace with your authentication logic

    data = request.get_json()
    data = data['data']
    try:
        retailer_results = Retailer.query.filter_by(email=data['email']).all()
    except Exception as error:
        print(f"Error in fetching the login details - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in fetching the login details - {error}"}), 500
    else:
        username = None
        if retailer_results:
            for item in retailer_results:
                authenticated = item.password == data['password']
                username = item.username


    if authenticated:
        payload = {'email': data['email'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=90)}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # Create a response object
        response = make_response(jsonify({'fullname': username, 'email': data['email'], 'valid': True}))
        # Set a cookie to indicate successful login with 90 minutes of expiry
        response.set_cookie('retailer_token', token, secure=True, expires=datetime.datetime.now() + datetime.timedelta(minutes=90), httponly=True)
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
    data = data['data']
    try:
        retailer = Retailer(email=data['email'], username=data['username'], password=data['password'], address=data['address'], phonenumber=data['phonenumber']) 
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
        result = db.session.execute("SELECT distinct(commodities), price_kg, profit_percent FROM warehouse")

        if not result:
            return jsonify({'error': "Data not retrieved"}), 500

        commodities = []
        # Access the result
        for row in result:
            # Calculate selling price
            selling_price = row.price_kg + (row.price_kg * (row.profit_percent / 100))
            commodities.append([
                row.commodities,
                selling_price
            ])
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

    jwt_token = request.cookies.get('retailer_token')
    if jwt_token:
        try:
            decoded_payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return 'Token expired'
        except jwt.InvalidTokenError:
            return 'Invalid token'
    else:
        return jsonify({'error': 'Not Authorised'}), 401




    try:
        retailer_results = Retailer.query.filter_by(email=decoded_payload['email']).all()

        retailer_email = None
        for retailer in retailer_results:
            retailer_email = retailer.email
        
        purchase_list = Purchases.query.filter_by(retailer_email=retailer_email).all()

        purchases = []
        for item in purchase_list:
            purchases.append([item.purchase_id, item.owner, item.retailer_email, item.retailer_address, item.created_date])
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
    
    jwt_token = request.cookies.get('retailer_token')
    if jwt_token:
        try:
            decoded_payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return 'Token expired'
        except jwt.InvalidTokenError:
            return 'Invalid token'
    else:
        return jsonify({'error': 'Not Authorised'}), 401

    try:
        arguments =  request.args.get('id')
        purchase_order = Purchases.query.filter_by(purchase_id=arguments).all()
        a_purchase = {}
        for purchase in purchase_order:
            a_purchase['purchase_id'] = purchase.purchase_id
            a_purchase['email'] = purchase.retailer_email
            a_purchase['address'] = purchase.retailer_address
            a_purchase['date'] = purchase.created_date
            a_purchase['commodities'] = purchase.commodity # This should be iterated in the frontend
    except Exception as error:
        print(f"Error in retrieveing the particular receipt - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in retrieveing the particular receipt - {error}"}), 500
    else:
        return jsonify({'data': a_purchase}), 200
    

# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/cart', methods=['GET'])
def get_cart():

    jwt_token = request.cookies.get('retailer_token')
    if jwt_token:
        try:
            decoded_payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return 'Token expired'
        except jwt.InvalidTokenError:
            return 'Invalid token'
    else:
        return jsonify({'error': 'Not Authorised'}), 401

    try:
        with redis.Redis(host='localhost', port=6379, db=0, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            retrieved_data = redis_connection.hgetall(decoded_payload['email'])
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

    jwt_token = request.cookies.get('retailer_token')
    if jwt_token:
        try:
            decoded_payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return 'Token expired'
        except jwt.InvalidTokenError:
            return 'Invalid token'
    else:
        return jsonify({'error': 'Not Authorised'}), 401

    try:
        data = request.get_json()
        with redis.Redis(host='localhost', port=6379, db=0, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            redis_connection.hmset(decoded_payload['email'], data)
            retrieved_data = redis_connection.hgetall(decoded_payload['email'])
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

    jwt_token = request.cookies.get('retailer_token')
    if jwt_token:
        try:
            decoded_payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return 'Token expired'
        except jwt.InvalidTokenError:
            return 'Invalid token'
    else:
        return jsonify({'error': 'Not Authorised'}), 401


    try:
        commodity = request.args.get('commodity')
        with redis.Redis(host='localhost', port=6379, db=0, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            retrieved_data = redis_connection.hgetall(decoded_payload['email']) # retrieveing the data for the retailer email
            if retrieved_data:
                retrieved_dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in retrieved_data.items()} # Converting the binary ascii
                del retrieved_dict[commodity] # Deleting
                redis_connection.hmset(decoded_payload['email'], retrieved_dict) # Re-inserting into the redis
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

    jwt_token = request.cookies.get('retailer_token')
    if jwt_token:
        try:
            decoded_payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return 'Token expired'
        except jwt.InvalidTokenError:
            return 'Invalid token'
    else:
        return jsonify({'error': 'Not Authorised'}), 401


    data = request.get_json()
    purchase_id = str(uuid.uuid4())
    is_successful = True

    try:
        retailer_results = Retailer.query.filter_by(email=decoded_payload['email']).all()

        # We need to loop as the retailer_results is an object
        for retailer in retailer_results:
            purchase = Purchases(purchase_id, "HarvestHub_Owner", retailer.email, retailer.address, retailer.phonenumber, datetime.datetime.utcnow, data['commodities'])
            db.session.add(purchase)
            db.session.commit()
    except Exception as error:
        is_successful = False
        print(f"Error in adding the purchase details - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in adding the purchase details - {error}"}), 500

    try:

        update_weight_query = """
            UPDATE warehouse
            SET weight = :new_weight
            WHERE bag_id = :bag_id AND commodity = :commodity
        """
        delete_entry_query = "DELETE FROM warehouse WHERE bag_id = :bag_id"

        print(">>>> Updating the warehouse table")
        for commodity in data['commodities']:
            select_weight_query = "SELECT weight, bag_id FROM warehouse WHERE commodity= :commodity"
            commodity_weight_obj = db.session.execute(select_weight_query,{
                'commodity': commodity[0]
            })
            
            print("/tObtained the weights and bag_ids based on the commodity")
            deleted_bags, supposed_bag_id, new_weight = [], None, None
            for row in commodity_weight_obj:
                if commodity[3] >= row[0]:
                    deleted_bags.append(row[1])
                else:
                    new_weight = row[0] - commodity[3]
                    supposed_bag_id = row[1]
                    break
            
            if supposed_bag_id != None and new_weight != None:
                print("/tObtained the supposed_bag_id and new_weight. This should be updated in the database")
                with app.app_context():
                    db.session.execute(
                        update_weight_query,
                        {
                            'new_weight': new_weight,  # New weight value
                            'bag_id': supposed_bag_id,   # Bag ID to identify the row to update
                            'commodity': commodity[0]
                        }
                    )
                    db.session.commit()

            if len(deleted_bags) > 0:
                print("/t There are deleted bag ids. We need to delete those. Since purchase happened.")
                for delete_bag in deleted_bags:
                    with app.app_context():
                        db.session.execute(
                            delete_entry_query,
                            {  
                                'bag_id': delete_bag   # Bag ID to identify the row to update
                            }
                        )
                        db.session.commit()
    except Exception as error:
        is_successful = False
        print(f"Error in updating the warehouse details about the purchase - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in adding the warehouse details about the purchase - {error}"}), 500
    else:
        print(">>>> Successfully updated the warehouse table after the warehouse insertion")

    try:
        insert_query = """
            INSERT INTO sell_statistics (farmer_id, bag_id, commodity, price_kg, selling_price)
            VALUES (:farmer_id, :bag_id, :commodity, :price_kg, :selling_price)
        """

        for commodity in data['commodities']:
            with app.app_context():
                db.session.execute(insert_query,
                    {
                        'farmer_id': data['farmer_id'],
                        'bag_id': data['bag_id'],
                        'commodity': commodity[0],
                        'price_kg': commodity[1],
                        'selling_price': commodity[2]
                    }
                )
        db.session.commit()
    except Exception as error:
        is_successful = False
        print(f"Error in adding the statistics details about the purchase - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in adding the statistics details about the purchase - {error}"}), 500
    else:
        print(">>>> Successfully updated the statistics table after the warehouse insertion")

    if is_successful:
        return jsonify({'message':'Purchase successful'}), 200
    else:
        return jsonify({'message':'Error in purchasing, please contact the administrator'}), 500

# ---------------------------------------------------------------------------------------------------------------------




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5004, host='0.0.0.0')