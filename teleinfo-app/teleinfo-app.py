from flask import Flask
from flask import jsonify, request, g
import json
from flask import current_app, render_template, Response
app = Flask(__name__)

with app.app_context():

    @app.route('/')
    def main():
        return render_template('gauges.html')

    @app.route('/api/dump')
    def dump():
        result = getattr(current_app, 'last_data', dict())
        return json.dumps(result)

    @app.route('/gauge/intensite')
    def gauge_intensite():
        data = getattr(current_app, 'last_data', dict())
        result = dict()
        result['max']=data["IMAX"]
        result['curr']=data["IINST"]
        result['threshold']=data["ISOUSC"]

        return Response("data: "+json.dumps(result)+"\n\n", mimetype="text/event-stream")

    @app.route('/api/notify', methods=['POST'])
    def get_notified():

        current_app.last_data = request.get_json()
        print current_app.last_data
        return ''
