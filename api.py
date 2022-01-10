from flask import Flask, jsonify, request, abort, Response
from flask_restful import Api, Resource
from flask_cors import CORS
# TODO:  add swagger specs
# from flask_restful_swagger import swagger
from similarites import compute_matrix
from graph import create, createSim
import json

app = Flask(__name__)
api = Api(app)
CORS(app, origins="http://localhost:3000", allow_headers=["Content-Type"])

# @api.route("/users/")
class Protein(Resource):
  def post(self):
    """
      Insert protein similarity in neo4j
    """
    data = request.get_json()
    #print(data['name'])
    
    # Use the function
    create()
    compute_matrix(data['body']['name'])
    createSim(data['body']['seuil'])
    
    return Response(response=json.dumps({"Status": "Data inserted"}),
                  status=200,
                  mimetype='application/json')

# resources 
api.add_resource(Protein, "/protein")

# main
if __name__ == "__main__":
  app.run(debug=True)
