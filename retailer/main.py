from flask import request, make_response, jsonify
import traceback, datetime, redis, uuid, jwt, os, json, copy
from models import Purchases, Retailer
from setup import app, db
from sqlalchemy.sql import text
from sqlalchemy import and_




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
        # Todo - Set cookie is not working need to see this
        response.set_cookie('retailer_token', token, secure=True, expires=datetime.datetime.now() + datetime.timedelta(minutes=90))
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
        result = db.session.execute(text("SELECT distinct(commodity) FROM warehouse"))

        if not result:
            return jsonify({'error': "Data not retrieved"}), 500

        commodities = []
        # Access the result
        for row in result:
            commodities.append(row[0])
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

    email = request.args['email']
    try:
        purchase_list = Purchases.query.filter_by(retailer_email=email).all()

        purchases = []
        for item in purchase_list:
            purchases.append({
                'Date': item.created_date,
                'Purchase Id':item.purchase_id,
                'commodity': item.commodity
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


    try:
        purchase_id_condition = Purchases.purchase_id == request.args['id']
        commodity_condition = Purchases.commodity == request.args['commodity']
        query = Purchases.query.filter(and_(purchase_id_condition, commodity_condition))
        purchase_order = query.all()
        purchase_details = []
        for purchase in purchase_order:
            a_purchase = {}
            a_purchase['purchase_id'] = purchase.purchase_id
            a_purchase['email'] = purchase.retailer_email
            a_purchase['address'] = purchase.retailer_address
            a_purchase['date'] = purchase.created_date
            a_purchase['price'] = purchase.price
            a_purchase['weight'] = purchase.weight
            a_purchase['commodities'] = purchase.commodity # This should be iterated in the frontend
            purchase_details.append(a_purchase)
    except Exception as error:
        print(f"Error in retrieveing the particular receipt - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in retrieveing the particular receipt - {error}"}), 500
    else:
        return jsonify({'data': purchase_details}), 200
    

# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/cart', methods=['GET'])
def get_cart():

    email = request.args['email']
    try:
        with redis.Redis(host='redis', port=6379, db=0, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            retrieved_data = redis_connection.hgetall(email)
            if retrieved_data:
                # Deserialize the 'items' field value back into a list
                if b'items' in retrieved_data and len(retrieved_data[b'items']) > 0:
                    stored_list = json.loads(retrieved_data[b'items'].decode('utf-8'))
                    return jsonify({'data': stored_list}), 200
    except Exception as error:
        print(f"Error in fetching the cart - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in fetching the cart - {error}"}), 500
    
    return jsonify({'message': "Cart not available"}), 404

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/cart', methods=['PUT'])
def add_to_cart():

    email = request.args['email']
    BAG_IDS, PURCHASE_ITEMS, STORED_LIST, TOTAL_WEIGHT = [], {}, [], 0
    data = request.get_json()

    try:
        with redis.Redis(host='redis', port=6379, db=3, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            # redis_connection.hdel('bag_ids', 'items')
            retrieved_data = redis_connection.hgetall('bag_ids')
            if retrieved_data:
                if b'items' in retrieved_data:
                    stored_list = json.loads(retrieved_data[b'items'].decode('utf-8'))
                    BAG_IDS = copy.deepcopy(stored_list)
    except Exception as error:
        print(f"Error in fetching the bag_ids - {error} \n\n{traceback.format_exc()}")


    try:
        with redis.Redis(host='redis', port=6379, db=0, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            retrieved_data = redis_connection.hgetall(email)
            if retrieved_data:
                if b'items' in retrieved_data and len(retrieved_data[b'items']) > 0:
                    stored_list = json.loads(retrieved_data[b'items'].decode('utf-8'))
                    for item in stored_list:
                        PURCHASE_ITEMS[item['commodity']] = item
    except Exception as error:
        print(f"Error in fetching the bag_ids - {error} \n\n{traceback.format_exc()}")


    try:
        sql_query = text("SELECT * FROM warehouse WHERE commodity = :commodity ORDER BY commodity")
        # Execute the query and fetch the results
        rows_with_commodity = db.session.execute(sql_query, {"commodity": data['data']['item']})

        for row in rows_with_commodity:
            TOTAL_WEIGHT += row.weight 
    except Exception as error:
        print(f"Error in fetching the total_weights - {error} \n\n{traceback.format_exc()}")
    else:
        if data['data']['item'] in PURCHASE_ITEMS:
            if (TOTAL_WEIGHT - int(PURCHASE_ITEMS[data['data']['item']]['weight'])) < int(data['data']['quantity']):
                return jsonify({'message': f"Quantity of {TOTAL_WEIGHT - PURCHASE_ITEMS[data['data']['item']]['weight']} kgs is available for the {data['data']['item']}"}), 404
        elif TOTAL_WEIGHT < int(data['data']['quantity']):
            return jsonify({'message': f"Quantity of {TOTAL_WEIGHT} kgs is available for the {data['data']['item']}"}), 404


    try:
        # Construct the native SQL query
        sql_query = text("SELECT * FROM warehouse WHERE commodity = :commodity ORDER BY commodity")
        # Execute the query and fetch the results
        rows_with_commodity = db.session.execute(sql_query, {"commodity": data['data']['item']})

        if data['data']['item'] in PURCHASE_ITEMS:
            redis_insert = PURCHASE_ITEMS[data['data']['item']]
            redis_insert['farmer_id'] = set(redis_insert['farmer_id'])
            redis_insert['deleted_bags'] = set(redis_insert['deleted_bags'])
        else:
            redis_insert = {
                'farmer_id': set(), 'bag_id': {}, 'weight': 0, 'price': 0, 'commodity': data['data']['item'], 'deleted_bags': set(), 'left_over_weight': {},
            }
        for row in rows_with_commodity:
            
            
            if row.bag_id in redis_insert['deleted_bags']:
                continue

            selling_price = row.price_kg + (row.price_kg * (row.profit_percent / 100))
            data['data']['quantity'] = int(data['data']['quantity'])

            if data['data']['quantity'] <= 0:
                break
            if row.weight > data['data']['quantity']:
                redis_insert['farmer_id'].add(row.farmer_id)
                if row.bag_id in redis_insert['left_over_weight']:
                    temp = int(row.weight - data['data']['quantity'] - redis_insert['bag_id'][row.bag_id])
                    if temp <= 0: 
                        redis_insert['deleted_bags'].add(row.bag_id)
                        del redis_insert['bag_id'][row.bag_id]
                        del redis_insert['left_over_weight'][row.bag_id]
                    else:
                        redis_insert['left_over_weight'][row.bag_id] = row.weight - data['data']['quantity'] - redis_insert['bag_id'][row.bag_id]
                else:
                    redis_insert['left_over_weight'][row.bag_id] = row.weight - data['data']['quantity']
                if row.bag_id in redis_insert['bag_id'] and row.bag_id not in redis_insert['deleted_bags']:
                    redis_insert['bag_id'][row.bag_id] += data['data']['quantity'] 
                elif row.bag_id not in redis_insert['deleted_bags']:
                    redis_insert['bag_id'][row.bag_id] = data['data']['quantity']
                redis_insert['weight'] += int(data['data']['quantity'])
                redis_insert['price'] += redis_insert['weight'] * selling_price
            elif row.weight < data['data']['quantity']:
                redis_insert['farmer_id'].add(row.farmer_id)
                if row.bag_id in redis_insert['bag_id']:
                    data['data']['quantity'] += redis_insert['bag_id'][row.bag_id]
                    redis_insert['weight'] = 0
                    redis_insert['price'] = 0
                    del redis_insert['bag_id'][row.bag_id]
                    del redis_insert['left_over_weight'][row.bag_id]
                redis_insert['deleted_bags'].add(row.bag_id)
                redis_insert['weight'] += row.weight
                redis_insert['price'] += redis_insert['weight'] * selling_price
            elif row.weight == data['data']['quantity']:
                redis_insert['farmer_id'].add(row.farmer_id)
                if row.bag_id in redis_insert['bag_id']:
                    data['data']['quantity'] += redis_insert['bag_id'][row.bag_id]
                    redis_insert['weight'] = 0
                    redis_insert['price'] = 0
                    del redis_insert['bag_id'][row.bag_id]
                    del redis_insert['left_over_weight'][row.bag_id]
                redis_insert['deleted_bags'].add(row.bag_id)
                redis_insert['weight'] += row.weight
                redis_insert['price'] += redis_insert['weight'] * selling_price
            data['data']['quantity'] -= row.weight
            BAG_IDS.append(row.bag_id)

        redis_insert['farmer_id'] = list(redis_insert['farmer_id'])
        redis_insert['deleted_bags']= list(redis_insert['deleted_bags'])
        PURCHASE_ITEMS[data['data']['item']] = redis_insert
        STORED_LIST.extend(list(PURCHASE_ITEMS.values()))
        with redis.Redis(host='redis', port=6379, db=0, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            redis_connection.hset(email, 'items', json.dumps(STORED_LIST))
    except Exception as error:
        print(f"Error in fetching the cart - {error} \n\n{traceback.format_exc()}")
        return jsonify({'error': f"Error in fetching the cart - {error}"}), 500
    
    try:
        with redis.Redis(host='redis', port=6379, db=3, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            redis_connection.hset('bag_ids', 'items', json.dumps(BAG_IDS))
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
    email = request.args['email']

    try:
        commodity = request.args.get('commodity')
        with redis.Redis(host='redis', port=6379, db=0, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            # redis_connection.hdel(email, 'items')
            retrieved_data = redis_connection.hgetall(email) # retrieveing the data for the retailer email
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
                    redis_connection.hset(email, 'items', json.dumps(stored_list)) # Re-inserting into the redis
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

    email = request.args['email']
    purchase_id = str(uuid.uuid4())
    is_successful = True

    PURCHASE_ITEMS, BAG_IDS = None, None

    try:
        with redis.Redis(host='redis', port=6379, db=0, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
            retrieved_data = redis_connection.hgetall(email)
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
        redis_connection.hset(email, 'items', '') # Store it back to the redis

    
    try:
        with redis.Redis(host='redis', port=6379, db=3, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
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
            retailer_results = Retailer.query.filter_by(email=email).all()
            # We need to loop as the retailer_results is an object
            if len(retailer_results) == 0:
                raise Exception("Looks like logged out. Please log in")

            for retailer in retailer_results:
                purchase = Purchases(
                    purchase_id=purchase_id, 
                    owner="HarvestHub_Owner", 
                    retailer_email=retailer.email, 
                    retailer_address=retailer.address, 
                    retailer_phonenumber=retailer.phonenumber, 
                    commodity=item['commodity'], 
                    price=item['price'], 
                    weight=item['weight'],
                    created_date=datetime.datetime.now()
                )
                db.session.add(purchase)
                db.session.commit()
        except Exception as error:
            is_successful = False
            print(f"Error in adding the purchase details - {error} \n\n{traceback.format_exc()}")
            return jsonify({'error': f"Error in adding the purchase details - {error}"}), 500


        try:
            insert_query = text("""
                INSERT INTO sell_statistics (farmer_id, bag_id, owner, commodity, price_kg, profit_percent, weight, selling_price, created_date)
                VALUES (:farmer_id, :bag_id, :owner, :commodity, :price_kg, :profit_percent, :weight, :selling_price, :created_date)
            """)
            select_weight_query = text("SELECT * FROM warehouse WHERE commodity= :commodity AND bag_id= :bag_id")
            
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
                        row.profit_percent,
                        row.weight, # Weight
                        (row.weight) * (row.price_kg + (row.price_kg * (row.profit_percent / 100))) # Selling price
                    ])

            for bagId in list(item['bag_id']):
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
                        row.profit_percent,
                        item['bag_id'][bagId], # Weight
                        (item['bag_id'][bagId]) * (row.price_kg + (row.price_kg * (row.profit_percent / 100))) # Selling price
                    ])

            for detail in details:
                print(f"/tEntry into Sell Statistics - {detail[1]}" )
                with app.app_context():
                    db.session.execute(insert_query,
                        {
                            'farmer_id': detail[0],
                            'bag_id': detail[1],
                            'owner': "HarvestHub_Owner",
                            'commodity': detail[3],
                            'price_kg': detail[4],
                            'profit_percent': detail[5],
                            'weight': detail[6],
                            'selling_price': detail[7],
                            'created_date': datetime.datetime.now()
                        }
                    )
                    db.session.commit()
        except Exception as error:
            is_successful = False
            print(f"Error in adding the statistics details about the purchase - {error} \n\n{traceback.format_exc()}")
            return jsonify({'error': f"Error in adding the statistics details about the purchase - {error}"}), 500
        else:
            print(">>>> Successfully updated the statistics table after the warehouse insertion")


        try:
            print(">>>> Updating the warehouse table")
            if len(item['deleted_bags']) > 0:
                for bagID in list(item['deleted_bags']):
                    delete_entry_query = text("DELETE FROM warehouse WHERE bag_id = :bag_id")
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

            with redis.Redis(host='redis', port=6379, db=3, password=os.getenv('REDIS_PASSWORD')) as redis_connection:
                redis_connection.hset('bag_ids', 'items', json.dumps(BAG_IDS))

            for bags in item['bag_id']:
                update_weight_query = text("UPDATE warehouse SET weight = :new_weight WHERE bag_id = :bag_id AND commodity = :commodity")
                if item['bag_id'] != None:
                    print("/tObtained the Bag id which is the latest. This should be updated in the database")
                    with app.app_context():
                        db.session.execute(
                            update_weight_query,
                            {
                                'new_weight': item['left_over_weight'][bags],  # New weight value
                                'bag_id': bags,   # Bag ID to identify the row to update
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