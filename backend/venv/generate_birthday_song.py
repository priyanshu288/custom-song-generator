import sys
sys.path.append('../jukebox')
import jukebox
# ... rest of the imports
import os
from pyexpat import model
import torch as t
from jukebox.make_models import make_prior, MODELS, make_vqvae
from jukebox.hparams import Hyperparams, setup_hparams
from jukebox.sample import sample_single_window, _sample, load_prompts
from jukebox.utils.dist_utils import setup_dist_from_mpi
from jukebox.utils.torch_utils import empty_cache
import numpy as np

def generate_lyrics(name, details):
    return f"""It's a special day for {name},
    A time to celebrate and cheer,
    {details}
    Happy birthday, we hold you dear!"""

def generate_birthday_song(name, details, artist, genre):
    # Generate lyrics
    lyrics = generate_lyrics(name, details)
    
    # Set up Jukebox
    rank, local_rank, device = setup_dist_from_mpi()
    hps = Hyperparams()
    hps.sr = 44100
    hps.n_samples = 1
    hps.name = 'samples'
    chunk_size = 16
    max_batch_size = 3
    hps.levels = 3
    hps.hop_fraction = [.5,.5,.125]
    hps.sample_length = 1048576
    
    vqvae, *priors = MODELS['5b_lyrics']
    vqvae = make_vqvae(setup_hparams(vqvae, dict(sample_length = 1048576)), device)
    top_prior = make_prior(setup_hparams(priors[-1], dict()), vqvae, device)
    
    # Prepare lyrics and metadata
    artist = artist
    genre = genre
    total_length = 1048576
    offset = 0
    
    metas = [dict(artist = artist,
                  genre = genre,
                  total_length = total_length,
                  offset = offset,
                  lyrics = lyrics)]
    
    # Generate sample
    hps.sample_length = total_length
    sample = sample_single_window(top_prior, vqvae, hps)
    
    # Save as wav file
    jukebox.sample.save_samples(model, device, hps, sample)
    
    return f"samples/sample_0.wav"

# Example usage
name = "Alice"
details = "You bring joy to everyone around"
artist = "The Beatles"
genre = "Rock"

song_path = generate_birthday_song(name, details, artist, genre)
print(f"Birthday song generated and saved at: {song_path}")