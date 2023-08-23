from flask import Flask, Response, render_template, request, redirect, url_for, make_response, jsonify
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
# >>>> Submission of Login Form
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/login', methods=['PUT'])
def login_form():
    authenticated = False  # Replace with your authentication logic

    data = request.get_json()

    # TODO - need to check the data with the database The message is getting appended in the URL We need to make sure that is correct

    if authenticated:
        # Create a response object
        response = make_response(jsonify({'message': 'Authentication successful'}))
        # Set a cookie to indicate successful login with 90 minutes of expiry
        response.set_cookie('retailer_login_status', 'success', secure=True,
                            expires=datetime.datetime.now() + datetime.timedelta(minutes=90))
        return response
    else:
        return custom_response({"error": "Not Authenticated"}, 404)


# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Submission of register Form
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/register', methods=['POST'])
def register():

    data = request.get_json()

    # TODO - need to check the data with the database The message is getting appended in the URL We need to make sure that is correct


    return jsonify({"data": "Registered successfully"})

    # if authenticated:
    #     # Create a response object
    #     response = make_response(jsonify({'message': 'Authentication successful'}))
    #     # Set a cookie to indicate successful login with 90 minutes of expiry
    #     response.set_cookie('retailer_login_status', 'success', secure=True,
    #                         expires=datetime.datetime.now() + datetime.timedelta(minutes=90))
    #     return response
    # else:
    #     return custom_response({"error": "Not Authenticated"}, 404)


# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Display all the commodities
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/commodties', methods=['GET'])
def get_all_commodities():

    # TODO - Code to add it in the database
    
    return jsonify({'data':""})

# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/receipts', methods=['GET'])
def get_all_receipts():

    # TODO - Code to add it in the database
    
    return jsonify({'data':""})

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/receipt', methods=['GET'])
def get_receipt():

    # TODO - Code to add it in the database
    
    return jsonify({'data':""})

# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/receipt', methods=['GET'])
def get_receipt():

    # TODO - Code to add it in the database
    
    return jsonify({'data':""})

# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/cart', methods=['GET'])
def get_cart():

    # TODO - Code to add it in the redis
    
    return jsonify({'data':""})

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/cart', methods=['PUT'])
def add_to_cart():

    # TODO - Code to add it in the redis
    
    return jsonify({'data':""})

# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/cart', methods=['DELETE'])
def delete_from_cart():

    # TODO - Code to add it in the redis
    
    return jsonify({'data':""})

# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# >>>> Get all the receipts
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/retailer/purchase', methods=['PUT'])
def purchase():

    # TODO - Code to add it in the database
    
    return jsonify({'data':""})

# ---------------------------------------------------------------------------------------------------------------------




if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')



""" 
1. Receipts and receipt page
2. Sign up
3. Login 
4. Cart
5. Display all the vegetables
"""