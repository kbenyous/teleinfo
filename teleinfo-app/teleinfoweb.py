#!/usr/bin/python
# -*- coding: UTF-8 -*-

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

    @app.route('/api/gauges')
    def gauges():
        data = getattr(current_app, 'last_data', dict())

        gauges_model = dict()

        # jauge d'intensite
        current=int(data["IINST"])
        threshold=int(data["ISOUSC"])
        if current < threshold*0.8:
            bgcolor= "#c2f5f5"
        elif current <threshold :
            bgcolor="#f5e4c2"
        else:
            bgcolor="#e82525"
        gauges_model['gauge_intensite'] = {'arcFillInt': data["IINST"],
                                           'arcFillTotal': data["IMAX"],
                                           'colorArcBg':  bgcolor
                                           }



        # jauge de puissance
        gauges_model['gauge_puissance'] = {'arcFillInt': data["PAPP"],
                                           'arcFillTotal': int(data["IMAX"])*230}

        # jauge de index HP
        gauges_model['gauge_index_hp'] = { 'arcFillInt': (int(data["HCHP"])%1000 ),
                                           'arcFillTotal': "1000",
                                           'dialValue': int(data["HCHP"])}

        # jauge de index HC
        gauges_model['gauge_index_hc'] = { 'arcFillInt': (int(data["HCHC"])%1000 ),
                                           'arcFillTotal': "1000",
                                           'dialValue': int(data["HCHC"]) }

        return Response("data: "+json.dumps(gauges_model)+"\n\n", mimetype="text/event-stream")
    @app.route('/api/notify', methods=['POST'])
    def get_notified():

        current_app.last_data = request.get_json()
        print current_app.last_data
        return ''

if __name__ == "__main__":
    app.run(host='0.0.0.0')