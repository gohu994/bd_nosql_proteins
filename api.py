from flask import Flask, jsonify, request, abort, Response
from flask_cors import CORS
from flask_restful import Api, Resource
# TODO:  add swagger specs
# from flask_restful_swagger import swagger
import stats,graph,similarites
from neo4j import GraphDatabase

import json

app = Flask(__name__)
api = Api(app)
CORS(app, origins="http://localhost:3000", allow_headers=[
    "Content-Type"])

# @api.route("/users/")
class Protein(Resource):
  def post(self):
    """
      Insert protein similarity in neo4j
    """
    data = request.get_json()
    print(data['body']['name'])

    # check if lonely, returns response if not
    driver = GraphDatabase.driver("bolt://localhost:7687")
    session = driver.session()
    q_0 = "MATCH p=(:Prot {entry: '" + data['body']['name'] + "'})-[r:SIMI]-() WHERE r.value[0] > " + str(
        data['body']['seuil']) + " RETURN count(p)"
    res_0 = session.run(q_0).data()[0]['count(p)']
    if res_0 == 0:
        # Use the function
        lstSimilaire = similarites.compute_matrix(data['body']['name'], data['body']['seuil'])
        #graph.create()
        #graph.createSim(data['body']['name'], data['body']['seuil'])
        if (len(lstSimilaire) > 1):
            for elt in lstSimilaire:
                print("elt : ",elt)
                hb = similarites.compute_matrix(elt,data['body']['seuil'])
        return Response(response=json.dumps({"Status": "Data already inserted"}),
                        status=200,
                        mimetype='application/json')
    else:

        return Response(response=json.dumps({"Status": "Data inserted"}),
                      status=200,
                      mimetype='application/json')

# resources 
class Stats(Resource):
  def get(self):
    print("Stats")

    # Use the function
    numberIsolated = stats.getNumberIsolated()
    numberLinked = stats.getNumberLinked()
    numberLabelled = stats.getNumberLabelled()
    numberUnlabelled = stats.getNumberUnlabelled()

    return Response(response=json.dumps({"numberIsolated":numberIsolated, "numberLinked":numberLinked, "numberLabelled":numberLabelled, "numberUnlabelled":numberUnlabelled}),
                  status=200,
                  mimetype='application/json')

class Clean(Resource):
  def post(self):
    print("Clean")

    # Use the function
    graph.delete()
    graph.create()

    return Response(response=json.dumps({"Status": "Graph cleaned"}),
                  status=200,
                  mimetype='application/json')

# resources 
api.add_resource(Protein, "/protein")
api.add_resource(Stats, "/stats")
api.add_resource(Clean, "/clean")

# main
if __name__ == "__main__":
  app.run(debug=True)
