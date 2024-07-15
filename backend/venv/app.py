from flask import Flask, request, jsonify, send_file
from flask_cors import CORS # type: ignore
import os
from generate_birthday_song import generate_birthday_song

app = Flask(__name__)
CORS(app)

@app.route('/generate-song', methods=['POST'])
def generate_song():
    data = request.json
    name = data.get('name')
    details = data.get('details')
    artist = data.get('artist', 'The Beatles')  # Default artist
    genre = data.get('genre', 'Rock')  # Default genre
    
    try:
        song_path = generate_birthday_song(name, details, artist, genre)
        return send_file(song_path, mimetype="audio/wav", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)