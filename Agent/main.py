
from flask import Flask, Response
import json

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


app.route("/agent/")
def ping():
    return custom_response({"message": "You are connected"}, 200)


# TODO 
# 1. We need to have 2 pages, 1 is login and 1 is insert 
# 2. We need to track the inactivity and ask him to login.



if __name__ == "__main__":
    app.run(debug=True, port=5001)