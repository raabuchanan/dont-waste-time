from flask import Flask, jsonify, session
from flask import render_template, request, redirect, url_for
app = Flask(__name__, static_url_path='/static')

@app.route("/c/", methods=['GET'])
def search():
    keyword = request.args.get('q')
    keyword = clean_keyword(keyword)
    page = request.args.get('p')

@app.route("/", methods=['GET'])
def home():
    return render_template("Sample.html")

@app.route("/reset", methods=['POST'])
def reset():
    print "reset!"
    last_offset = 0
    return 

last_offset = 0
recording = False

@app.route("/", methods=['POST'])
def receive():
    global recording
    global last_offset

    j = request.get_json()
    for i in j:
        if i['Offset'] > last_offset and 'DisplayText' in i:
            dt = i['DisplayText']
            if dt == "Start.":
                recording = True
                print "start recording..."
            elif dt == "Stop.":
                recording = False
                print "stop recording..."
            if recording:
                print dt
            last_offset = i['Offset']
    return render_template("Sample.html")

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8000, debug=True)


