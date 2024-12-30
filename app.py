from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

feedbacks = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feedbacks')
def view_feedbacks():
    return render_template('feedbacks.html', feedbacks=feedbacks)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    message = data.get('feedback')
    if name and message:
        feedback_data = {'name': name, 'message': message}
        feedbacks.append(feedback_data)
        socketio.emit('new_feedback', feedback_data)
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('initial_feedbacks', {'feedbacks': feedbacks})

@app.route('/qrcode')
def qrcode():
    return render_template('qrcode.html', domain=request.host_url.rstrip('/'))

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5200, host='0.0.0.0')