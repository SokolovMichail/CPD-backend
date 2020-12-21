import json
import psycopg2
import urllib.parse as urlparse
import os
from svg_generator import SVG_Generator

INSERT_QUERY_GRAPH = """INSERT INTO graphstorage (token, graph) 
VALUES (%s, %s) 
ON CONFLICT (token) DO UPDATE 
  SET token = excluded.token, 
      graph = excluded.graph;commit;"""

INSERT_QUERY_METRICS = """INSERT INTO metricsstorage (token,epoch,loss,accuracy) 
VALUES (%s, %s,%s,%s) RETURNING token;commit; """

SELECT_QUERY_GRAPH = '''select graph from graphstorage where token = %s;'''

SELECT_METRICS_GRAPH = '''select epoch,loss,accuracy from metricsstorage where token = %s order by epoch asc ;'''

DELETE_QUERY_GRAPH = '''delete from graphstorage where token = %s;'''

DELETE_QUERY_METRICS = '''delete from metricsstorage where token = %s;'''



class DatabaseOps:
    def __init__(self,use_config=False,config_file = "config.json"):
        self.svg_generator = SVG_Generator()
        self.settings = None
        self.use_config = use_config
        with open(config_file) as json_data_file:
            self.settings = json.load(json_data_file)

    def connect(self):
        if (self.use_config):
            database = self.settings["postgresql"]["database"]
            host = self.settings["postgresql"]["host"]
            user = self.settings["postgresql"]["user"]
            password = self.settings["postgresql"]["password"]
            port = self.settings["postgresql"]["port"]
            conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port
            )
            return conn
        else:
            url = urlparse.urlparse(os.environ['DATABASE_URL'])
            dbname = url.path[1:]
            user = url.username
            password = url.password
            host = url.hostname
            port = url.port

            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            return conn

    def data_to_json(self,model,metrics):
        res = []
        for metric in metrics:
            res.append({"epoch":metric[0],"loss":metric[1], "accuracy":metric[2]})
        return json.dumps({"model":model,"metrics":res})

    def get_data(self,token,svg_gen):
        conn = None
        result = ''''''
        try:
            conn = self.connect()
            curr = conn.cursor()
            curr.execute(SELECT_QUERY_GRAPH, (token,))
            #conn.commit()
            graph = (curr.fetchone())
            curr.execute(SELECT_METRICS_GRAPH, (token,))
            metrics = curr.fetchall()
            result = self.data_to_json(self.svg_generator.generate_svg(token,graph[0]),metrics)
            print("OK")
        except (psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if (conn != None):
                conn.close()
            return result

    def insert_metrics_into_database(self, token, epoch,loss,accuracy):
        conn = None
        result = False
        try:
            conn = self.connect()
            curr = conn.cursor()
            curr.execute(INSERT_QUERY_METRICS, (token, epoch,loss,accuracy,))
            conn.commit()
            result = True
        except (psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if (conn!=None):
                conn.close()
            return result

    def insert_or_update_graph_into_database(self, token, graph):
        conn = None
        result = False
        try:
            conn = self.connect()
            curr = conn.cursor()
            curr.execute(INSERT_QUERY_GRAPH, (token, graph,))
            conn.commit()
            result = True
        except (Exception,psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if (conn != None):
                conn.close()
            return result

    def delete_on_token(self,token):
        conn = None
        result = False
        try:
            conn = self.connect()
            curr = conn.cursor()
            curr.execute(DELETE_QUERY_METRICS, (token,))
            conn.commit()
            curr.execute(DELETE_QUERY_GRAPH, (token,))
            conn.commit()
            result = True
        except (psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if (conn != None):
                conn.close()
            return result



