from flask import request, make_response, jsonify
import traceback, datetime, redis, uuid, jwt, os, json, copy
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
        result = db.session.execute("SELECT distinct(commodities) FROM warehouse")

        if not result:
            return jsonify({'error': "Data not retrieved"}), 500

        commodities = []
        # Access the result
        for row in result:
            # selling_price = row.price_kg + (row.price_kg * (row.profit_percent / 100))
            commodities.extend(row.commodities)
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
            purchases.append({
                'Date': item.created_date,
                'Purchase Id':item.purchase_id
            })
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
            if retrieved_data:
                # Deserialize the 'items' field value back into a list
                if b'items' in retrieved_data:
                    stored_list = json.loads(retrieved_data[b'items'].decode('utf-8'))
                    return jsonify({'data': stored_list}), 200
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
    
    BAG_IDS = None
    try:
        with redis.Redis(host='localhost', port=6379, db=3, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            retrieved_data = redis_connection.hgetall('bag_ids')
            if retrieved_data:
                if b'items' in retrieved_data:
                    stored_list = json.loads(retrieved_data[b'items'].decode('utf-8'))
                    BAG_IDS = copy.deepcopy(stored_list)
    except Exception as error:
        print(f"Error in fetching the bag_ids - {error} \n\n{traceback.format_exc()}")


    try:
        data = request.get_json()
        # Construct the native SQL query
        sql_query = "SELECT * FROM warehouse WHERE commodity = :commodity ORDER BY commodity"
        # Execute the query and fetch the results
        rows_with_commodity = db.session.execute(sql_query, {"commodity": data['commodity']}).fetchall()
        if rows_with_commodity:
            return jsonify({"message": "Item out of stock"}), 404
        redis_insert = {
            'farmer_id': set(), 'bag_id': None, 'weight': 0, 'price': 0, 'commodity': data['item'], 'deleted_bags': set(), 'left_over_weight': None,
        }
        for row in rows_with_commodity:
            selling_price = row.price_kg + (row.price_kg * (row.profit_percent / 100))

            if BAG_IDS and row.bag_id not in BAG_IDS:
                # The idea is to avoid the usage of same bag_id across multiple people until purchase
                # We are not updating it in database as it should be updated only once the purchase happens.
                if row.weight > data['quantity']:
                    redis_insert['farmer_id'].add(row.farmer_id)
                    redis_insert['bag_id'] = row.bag_id
                    redis_insert['weight'] += (row.weight - data['quantity'])
                    redis_insert['price'] += redis_insert['weight'] * selling_price
                    redis_insert['left_over_weight'] = row.weight - data['quantity']
                elif row.weight < data['quantity']:
                    redis_insert['farmer_id'].add(row.farmer_id)
                    redis_insert['deleted_bags'].add(row.bag_id)
                    redis_insert['weight'] += row.weight
                    redis_insert['price'] += redis_insert['weight'] * selling_price
                elif row.weight == data['quantity']:
                    redis_insert['farmer_id'].add(row.farmer_id)
                    redis_insert['deleted_bags'].add(row.bag_id)
                    redis_insert['weight'] += row.weight
                    redis_insert['price'] += redis_insert['weight'] * selling_price
                data['quantity'] -= row.weight
                BAG_IDS.append(row.bag_id)

        if data['quantity'] > 0:
            return jsonify({'message': f"Quantity of {redis_insert['weight']} kgs is available for the {data['item']}"}), 404

        with redis.Redis(host='localhost', port=6379, db=0, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            retrieved_data = redis_connection.hgetall(decoded_payload['email'])
            if retrieved_data:
                if b'items' in retrieved_data:
                    stored_list = json.loads(retrieved_data[b'items'].decode('utf-8'))
                    stored_list.append(redis_insert) # Append the data to the retrievd list
                    redis_connection.hmset(decoded_payload['email'], {'items': json.dumps([stored_list])}) # Store it back to the redis
                else:
                    redis_connection.hmset(decoded_payload['email'], {'items': json.dumps([redis_insert])})
            else:
                raise Exception("Error in adding the element to the cart")
    except Exception as error:
        print(f"Error in fetching the cart - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in fetching the cart - {error}"}), 500
    
    try:
        with redis.Redis(host='localhost', port=6379, db=3, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            redis_connection.hmset(decoded_payload['email'], {'items': json.dumps([BAG_IDS])})
    except Exception as error:
        print(f"Error in setting the bag_ids - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in setting the bag_ids - {error}"}), 500
    
    return jsonify({'message': f"Successfully added to the cart"}), 200


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
                if b'items' in retrieved_data:
                    stored_list = json.loads(retrieved_data[b'items'].decode('utf-8'))
                    index = None
                    for i in range(len(stored_list)):
                        if stored_list[i]['commodity'] == commodity:
                            index = i 
                            break
                    if index == None:
                        return jsonify({'message': "Item not available to delete"}), 404
                    del stored_list[index]
                    redis_connection.hmset(decoded_payload['email'], {'items': json.dumps([stored_list])}) # Re-inserting into the redis
                    return jsonify({'message': f'{commodity} deleted from the cart', 'data': stored_list}), 200
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


    purchase_id = str(uuid.uuid4())
    is_successful = True

    PURCHASE_ITEMS, BAG_IDS = None, None

    try:
        with redis.Redis(host='localhost', port=6379, db=0, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            retrieved_data = redis_connection.hgetall(decoded_payload['email'])
            if retrieved_data:
                if b'items' in retrieved_data:
                    stored_list = json.loads(retrieved_data[b'items'].decode('utf-8'))
                    PURCHASE_ITEMS = copy.deepcopy(stored_list)
            else:
                raise Exception('Looks like Cart is empty')
    except Exception as error:
        is_successful = False
        print(f"Error in fetching the cart - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in fetching the cart - {error}"}), 500
    else:
        redis_connection.hmset(decoded_payload['email'], {'items': json.dumps([])}) # Store it back to the redis

    
    try:
        with redis.Redis(host='localhost', port=6379, db=3, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            retrieved_data = redis_connection.hgetall('bag_ids')
            if retrieved_data:
                if b'items' in retrieved_data:
                    stored_list = json.loads(retrieved_data[b'items'].decode('utf-8'))
                    BAG_IDS = copy.deepcopy(stored_list)
    except:
        print(f"Error in fetching the bag_ids - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in fetching the bag_ids- {error}"}), 500


    for item in PURCHASE_ITEMS:
        try:
            
            retailer_results = Retailer.query.filter_by(email=decoded_payload['email']).all()
            # We need to loop as the retailer_results is an object
            for retailer in retailer_results:
                purchase = Purchases(purchase_id, "HarvestHub_Owner", retailer.email, retailer.address, retailer.phonenumber, datetime.datetime.utcnow, item['commodity'], item['price'])
                db.session.add(purchase)
                db.session.commit()
        except Exception as error:
            is_successful = False
            print(f"Error in adding the purchase details - {error} \n\n{traceback.format_exc()}")
            return jsonify({'error': f"Error in adding the purchase details - {error}"}), 500

        try:
            print(">>>> Updating the warehouse table")
            if len(item['deleted_bags']) > 0:
                for bagID in list(item['deleted_bags']):
                    delete_entry_query = "DELETE FROM warehouse WHERE bag_id = :bag_id"
                    print(f"/tBagID - {bagID} is getting removed from the Warehouse")
                    with app.app_context():
                        db.session.execute(
                            delete_entry_query,
                            {  
                                'bag_id': bagID   # Bag ID to identify the row to update
                            }
                        )
                        db.session.commit()
                    
                    if BAG_IDS != None:
                        BAG_IDS.remove(bagID)

            with redis.Redis(host='localhost', port=6379, db=3, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
                redis_connection.hmset(decoded_payload['email'], {'items': json.dumps([BAG_IDS])})

            update_weight_query = "UPDATE warehouse SET weight = :new_weight WHERE bag_id = :bag_id AND commodity = :commodity"
            if item['bag_id'] != None:
                print("/tObtained the Bag id which is the latest. This should be updated in the database")
                with app.app_context():
                    db.session.execute(
                        update_weight_query,
                        {
                            'new_weight': item['left_over_weight'],  # New weight value
                            'bag_id': item['bag_id'],   # Bag ID to identify the row to update
                            'commodity': item['commodity']
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
            select_weight_query = "SELECT * FROM warehouse WHERE commodity= :commodity AND bag_id= :bag_id"
            
            details = []
            for bagId in list(item['deleted_bags']):
                commodity_weight_obj = db.session.execute(select_weight_query,{
                    'commodity': item['commodity'],
                    'bag_id': bagId
                })
        
                for row in commodity_weight_obj:
                    details.append([
                        row.farmer_id,
                        row.bag_id,
                        "HarvestHub_Owner",
                        row.commodity,
                        row.price_kg,
                        (row.weight) * (row.price_kg + (row.price_kg * (row.profit_percent / 100)))
                    ])
            else:
                commodity_weight_obj = db.session.execute(select_weight_query,{
                    'commodity': item['commodity'],
                    'bag_id': item['bag_id']
                })
        
                for row in commodity_weight_obj:
                    details.append([
                        row.farmer_id,
                        row.bag_id,
                        "HarvestHub_Owner",
                        row.commodity,
                        row.price_kg,
                        (item['left_over_weight']) * (row.price_kg + (row.price_kg * (row.profit_percent / 100)))
                    ])

            for detail in details:
                with app.app_context():
                    db.session.execute(insert_query,
                        {
                            'farmer_id': detail[0],
                            'bag_id': detail[1],
                            'commodity': detail[3],
                            'price_kg': detail[4],
                            'selling_price': detail[5]
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



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/validate', methods=['GET'])
def validate_user():
    jwt_token = request.cookies.get('retailer_token')
    if jwt_token:
        try:
            decoded_payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
            return jsonify({'message': "Success"}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
            return 
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    else:
        return jsonify({'error': 'Not Authorised'}), 401

# ---------------------------------------------------------------------------------------------------------------------




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5004, host='0.0.0.0')