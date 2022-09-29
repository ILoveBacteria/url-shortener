from flask import send_from_directory
from app import app


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'icon/favicon.ico')


@app.route('/android-chrome-192x192.png')
def android_chrome_192():
    return send_from_directory('static', 'icon/android-chrome-192x192.png')


@app.route('/android-chrome-512x512.png')
def android_chrome_512():
    return send_from_directory('static', 'icon/android-chrome-512x512.png')


@app.route('/mstile-70x70.png')
def mstile_70():
    return send_from_directory('static', 'icon/mstile-70x70.png')


@app.route('/mstile-144x144.png')
def mstile_144():
    return send_from_directory('static', 'icon/mstile-144x144.png')


@app.route('/mstile-150x150.png')
def mstile_150():
    return send_from_directory('static', 'icon/mstile-150x150.png')


@app.route('/mstile-310x310.png')
def mstile_310():
    return send_from_directory('static', 'icon/mstile-310x310.png')


@app.route('/mstile-310x150.png')
def mstile_310_150():
    return send_from_directory('static', 'icon/mstile-310x150.png')
