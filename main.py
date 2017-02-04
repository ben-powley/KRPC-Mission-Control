from flask import Flask, render_template, request, jsonify
import time
import krpc

#KRPC Config

conn = krpc.connect(name='KRPC - TELEMETRY DISPLAY')

vessel = conn.space_center.active_vessel
ref_frame = vessel.orbit.body.reference_frame

name = vessel.name

met = conn.add_stream(getattr, vessel, 'met')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
speed = conn.add_stream(getattr, vessel.flight(ref_frame), 'speed')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')

#Flask Config

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/krpc/telem', methods=['GET'])
def krpc__telem():
    if request.method == 'GET':
        return jsonify(vessel_name=name, met=round(met()), altitude=round(altitude()), speed=round(speed()), apoapsis=round(apoapsis()), periapsis=round(periapsis()))
