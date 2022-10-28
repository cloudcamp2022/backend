from flask import Flask
from flask_cors import CORS
import pymysql
import os
import opentracing
from flask_opentracing import FlaskTracing

from flask import Flask, jsonify
from jaeger_client import Config
from flask_opentracing import FlaskTracer

app = Flask(__name__)

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


def initialize_tracer():
    "Tracing setup method"
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
        },
        service_name='tasks-service')
    return config.initialize_tracer()


tracing = FlaskTracer(lambda: initialize_tracer(), True, app)


@app.route("/hello")
def hello():
    host = os.environ['DB_HOST']
    user = os.environ['DB_USER']
    password = os.environ['MYSQL_ROOT_PASSWORD']
    db = os.environ['DB_NAME']
    conn = pymysql.connect(host=host, user=user, db=db,
                           password=password, charset='utf8')
    curs = conn.cursor()
    sql = "select * from student";
    curs.execute(sql)
    rows = curs.fetchall()
    print(rows)
    conn.commit()
    conn.close()

    result = {"code": 200, "message": rows}
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
