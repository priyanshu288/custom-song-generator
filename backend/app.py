from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore

app = Flask(__name__)
CORS(app)

@app.route('/generate-song', methods=['POST'])
def generate_song():
    data = request.json
    name = data.get('name')
    details = data.get('details')
    
    # Here you would call your AI music generation function
    # For now, let's just return a dummy response
    generated_song = f"Generated song for {name} with details: {details}"
    
    return jsonify({"song": generated_song})

if __name__ == '__main__':
    app.run(debug=True)