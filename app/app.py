import datetime

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/app/v1/details', methods=['GET'])
def details():
    return jsonify({
        'data': "hellow world",
        'time': str(datetime.datetime.now()),
    })


@app.route('/app/v1/healthz')
def healthz():
    return jsonify({
        'status': "ok"
    },200)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')