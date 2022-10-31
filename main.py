from flask_cors import CORS
import pymysql
import os
from flask import Flask
from jaeger_client import Config
import logging
from flask_opentracing import FlaskTracer


def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={ # usually read from some yaml config
            'sampler': {'type': 'const', 'param': 1, },
            'logging': True,
            'reporter_batch_size': 1,
        },
        service_name=service,
    )
    return config.initialize_tracer()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
tracer = init_tracer('backend')
flask_tracer = FlaskTracer(tracer, True, app, ['url','url_rule','method','path','environ.HTTP_X_REAL_IP'])


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
