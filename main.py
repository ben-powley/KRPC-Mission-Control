from flask import Flask, render_template, request, jsonify
import time
import krpc

#KRPC Config

conn = krpc.connect(name='KRPC')
vessel = conn.space_center.active_vessel
ref_frame = vessel.orbit.body.reference_frame

met = conn.add_stream(getattr, vessel, 'met')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')

print('CONNECTED TO SPACE CENTER')

#Flask Config

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/krpc/telem', methods=['GET'])
def krpc__telem():
    if request.method == 'GET':
        return jsonify(met=round(met()), altitude=round(altitude()), apoapsis=round(apoapsis()))
