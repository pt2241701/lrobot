from flask import Flask, request, jsonify
import json
from flask_ngrok import run_with_ngrok
app = Flask(__name__)
run_with_ngrok(app)
content = ''
distance = ''
status = 'False'
long = ''
lat = ''
@app.route('/api', methods=['GET'])
def get_content():
    key = request.args.get('key')
    if key == 'text':
        return jsonify({'content': content, 'distance': distance, 'status' : status, 'long': long, 'lat' : lat})
    else:
        return 'Invalid key', 400

@app.route('/api', methods=['POST'])
def update_content():
    global content
    content = request.form.get('content')
    global distance
    distance = request.form.get('distance')
    global status
    status = request.form.get('status')
    global long
    long = request.form.get('long')
    global lat
    lat = request.form.get('lat')
    with open('data.json', 'w', encoding='utf8') as f:
        json.dump({
                    'content': content, 'distance': distance, 'status' : status, 'long': long, 'lat' : lat
                }, f, ensure_ascii=False)
    return 'Content updated', 200
"""
status là khi xe chạy xong thì cái esp8266 ở bánh xe phải 
POST lên content là 0 distance là 0 và status là True để bên map nhận về
nếu là True thì mới map mới POST lên tiếp content và distance

"""
if __name__ == '__main__':
    app.run()
#curl -X POST -d "content=yourContent&distance=yourDistance" http://your-ngrok-url/api