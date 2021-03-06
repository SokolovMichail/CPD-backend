from flask import Flask
from flask import request
app = Flask(__name__)
from database_operations import DatabaseOps

database_ops = DatabaseOps()

@app.route('/',methods=['POST'])
def process_post_request():
    token = request.args.get('token',None)
    if(token != None):
        token = token.lower()
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
        token = token.lower()
        return (database_ops.get_data(token),200)
    else:
        return database_ops.generate_token()

@app.route('/',methods=['DELETE'])
def delete_token_and_values():
    token = request.args.get('token', None)
    if(token != None):
        token = token.lower()
        res = database_ops.delete_on_token(token)
        if (res):
            return ('', 200)
        else:
            return ('',500)


if __name__ == '__main__':
    app.run()
