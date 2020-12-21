from flask import Flask
from flask import request
app = Flask(__name__)
import requests
from database_operations import DatabaseOps
from svg_generator import SVG_Generator
import uuid

database_ops = DatabaseOps()

@app.route('/',methods=['POST'])
def process_post_request():
    token = request.args.get('token')
    #print(token)
    req_data = request.json
    model = req_data.get('model',None)
    epoch = req_data.get('epoch', None)
    loss = req_data.get('loss', None)
    accuracy = req_data.get('accuracy', None)
    if (model!= None):
        res = database_ops.insert_or_update_graph_into_database(token, model)
        if res:
            return ('', 200)
        else:
            return ('',500)
    elif ((epoch!= None) and (loss!=None) and (accuracy !=None)):
        res = database_ops.insert_metrics_into_database(token,epoch,loss,accuracy)
        if res:
            return ('', 200)
        else:
            return ('',500)
    return ('',400)

@app.route('/',methods=['GET'])
def process_get_request():
    token = request.args.get('token',None)
    if(token != None):
        return (database_ops.get_data(token),200)
    else:
        return (str(uuid.uuid4()),200)

@app.route('/',methods=['DELETE'])
def delete_token_and_values():
    token = request.args.get('token', None)
    if (token != None):
        return (database_ops.delete_on_token(token), 200)




if __name__ == '__main__':
    app.run()
