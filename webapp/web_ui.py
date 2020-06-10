from flask import Flask, render_template, request, redirect
from backend_agent import BackendAgent
import logging
import json
import arrow

# LOGGER
LOGGING_LOGGER_NAME = 'web_ui'
LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = '%(asctime)s : %(module)s (%(funcName)s) : %(levelname)s : %(message)s'

SERVER_THREADED = True     # Flask debug server in multi-threading mode
HOST_PORT = 5001
REFRESH_TIMEOUT = 3


app = Flask(__name__)
app.secret_key = 'AXXA1Zr98j/3yX R~XHH!jmN]LWX/,?RI'
app.debug = False

retry = True


@app.route('/aps')
def all_clients():
    return render_template('access_points.html')


@app.route('/')
def system_status():
    return render_template('system_status.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/aps/list')
def homing_ajax():
    network_list = []
    ap_list = agent.get_last_aps()
    for ap in ap_list:
        ap_bssid = ap.split('-')[0]
        ap_name = ap.split('-')[1]
        rssi = ap_list[ap].split(',')[0]
        timestamp = arrow.get(float(ap_list[ap].split(',')[1]) / 1000).format("DD/MM/YYYY HH:mm:SS")

        network_list.append({'ssid': ap_name, 'rssi': rssi,
                             'bssid': ap_bssid.upper(), 'timestamp': timestamp})

    response = app.response_class(
        response=json.dumps(network_list),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/statistics')
def statistics():
    print str(agent.get_distance())
    return json.dumps(agent.get_distance())



if '__main__' == __name__:

    logger = logging.getLogger(LOGGING_LOGGER_NAME)

    # Our agent for redis and CNC commands - thread getting status each 2 sec
    logger.info('Starting backend thread')
    agent = BackendAgent()

    logger.info('Starting web server')

    app.run(host='0.0.0.0', port=HOST_PORT, debug=False, use_reloader=False, threaded=SERVER_THREADED)


