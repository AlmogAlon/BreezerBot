from flask import Flask, render_template, request, redirect
from backend_agent import BackendAgent
import logging
import json

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
    title = 'Environment'
    return render_template('access_points.html', title=title)


@app.route('/aps/list')
def homing_ajax():
    agent.get_last_aps()

    network_list = [{'ssid': 'Gita Technologies', 'rssi': '-20',
                     'bssid': 'AA:AA:AA:AA:AA:AA', 'timestamp': '1111'}]
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



@app.route('/')
def system_status():

    title = 'Dashboard'

    # getting data from agent
    """

    known_clients = data.known_clients
    visible_aps = data.visible_aps
    visible_associated = data.visible_associated
    visible_unassociated = data.visible_unassociated

    state = data.mission

    if data.gps_fix > 0 :
        gps_fix = "GPS Fixed"
    else:
        gps_fix = "GPS is not fixed"

    battery = data.battery_percentage
    power = data.power_source
    mobile = data.mobile
    tag_battery = ""

    if 0 <= battery < 25:
        tag_battery = str(battery) + "% <i class='fa fa-battery-empty'></i>" + " </div>"

    elif 25 <= battery < 50:
        tag_battery = str(battery) + "% <i class='fa fa-battery-quarter'></i>" + " </div>"

    elif 50 <= battery < 75:
        tag_battery = str(battery) + "% <i class='fa fa-battery-three-quarters'></i>" + " </div>"

    elif 75 <= battery <= 100:
        tag_battery = str(battery) + "% <i class='fa fa-battery-full'></i>" + " </div>"

    tag_top_battery = "<a href='javascript:void(0)' onclick=''>" + tag_battery
    tag = ""

    if power == 0:
        # Internal Battery
        tag = "<i class='fa fa-plug'></i>" + tag + " "

    if mobile != "":
        # Got Blue tooth device connected
        tag = tag + "<i class='fa fa-bluetooth-b'></i>" + " "

    sensor_comps = tag + tag_top_battery
    """
    distance = agent.distance
    return render_template('system_status.html', distance=distance)


if '__main__' == __name__:

    logger = logging.getLogger(LOGGING_LOGGER_NAME)

    # Our agent for redis and CNC commands - thread getting status each 2 sec
    logger.info('Starting backend thread')
    agent = BackendAgent()

    logger.info('Starting web server')

    app.run(host='0.0.0.0', port=HOST_PORT, debug=False, use_reloader=False, threaded=SERVER_THREADED)


