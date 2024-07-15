import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [name, setName] = useState('');
    const [details, setDetails] = useState('');
    const [artist, setArtist] = useState('The Beatles');
    const [genre, setGenre] = useState('Rock');
    const [isLoading, setIsLoading] = useState(false);
    const [audioUrl, setAudioUrl] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        console.log("Sending request to backend");
        try {
            const response = await axios.post('http://localhost:5000/generate-song', 
                { name, details, artist, genre },
                { responseType: 'blob' }
            );
            console.log("Received response from backend");
            const url = window.URL.createObjectURL(new Blob([response.data]));
            setAudioUrl(url);
        } catch (error) {
            console.error('Error generating song', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="App">
            <h1>Custom Birthday Song Generator</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Name: </label>
                    <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
                </div>
                <div>
                    <label>Details: </label>
                    <input type="text" value={details} onChange={(e) => setDetails(e.target.value)} required />
                </div>
                <div>
                    <label>Artist Style: </label>
                    <input type="text" value={artist} onChange={(e) => setArtist(e.target.value)} />
                </div>
                <div>
                    <label>Genre: </label>
                    <input type="text" value={genre} onChange={(e) => setGenre(e.target.value)} />
                </div>
                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Generating...' : 'Generate Song'}
                </button>
            </form>
            {isLoading && <p>Generating song... This may take a while.</p>}
            {audioUrl && (
                <div>
                    <h2>Generated Song</h2>
                    <audio controls src={audioUrl} />
                </div>
            )}
        </div>
    );
}

export default App;