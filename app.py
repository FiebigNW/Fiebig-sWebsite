import os
import subprocess, logging, shlex
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import uuid
import yt_dlp
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__)
CORS(app)

# Set the ffmpeg location (assuming Homebrew installation)
os.environ['FFMPEG_LOCATION'] = '/usr/local/bin/ffmpeg'  # Adjust this path if needed

#Processes the audio file with spleeter
@app.route('/api/process_audio', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    stems = request.form.get('stems')

    if not file or not stems:
        return jsonify({'error': 'Missing file or stems parameter'}), 400

    # Save the uploaded file to a temporary location
    temp_file_path = os.path.join('uploads', file.filename)
    file.save(temp_file_path)

    # Full path to spleeter
    spleeter_path = '/Users/nicholasfiebig/anaconda3/envs/spleeter-env/bin/spleeter'

    output_folder = 'output_audio'

    try:
        # Run spleeter command
        subprocess.run([spleeter_path, 'separate', '-p', f'spleeter:{stems}', '-o', output_folder, temp_file_path], check=True)

        # Get the paths to the separated stems
        stem_paths = []
        for root, dirs, files in os.walk(os.path.join(output_folder, file.filename.split('.')[0])):
            for file in files:
                if file.endswith('.wav'):  # Check for the separated audio files
                    stem_paths.append(f'{root}/{file}')

        return jsonify({'message': 'Audio processed successfully!', 'files': stem_paths})

    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Spleeter processing failed: {str(e)}'}), 500
    finally:
        # Optionally clean up the temporary uploaded file
        os.remove(temp_file_path)

# Function to download and convert a YouTube video
@app.route('/api/youtube_converter', methods=['POST'])
def download_youtube():
    url = request.form.get('url') or request.json.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    output_dir = os.path.join("output_audio", str(uuid.uuid4()))  # Use 'output_audio' folder
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'audio')
            mp3_filename = f"{title}.mp3"
            mp3_path = os.path.join(output_dir, mp3_filename)

        return jsonify({'message': 'Download and conversion complete', 'file_path': mp3_path})

    except yt_dlp.utils.DownloadError as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


#Function to upload the audio file 
@app.route('/api/UploadFile', methods=['POST'])
def upload_file():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # If no file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Ensure the file is a valid audio file
    allowed_extensions = {'mp3', 'wav'}
    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
        # Create an 'uploads' directory if it doesn't exist
        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        
        # Respond with a success message and the file path
        return jsonify({'message': 'File uploaded successfully!', 'filePath': file_path}), 200
    
    return jsonify({'error': 'Invalid file format, only mp3 or wav are allowed'}), 400

# Function to run download in a thread
def download_youtube_threaded():
    # Create a thread to handle the download and conversion
    download_thread = threading.Thread(target=download_youtube)
    download_thread.start()

# Function to run audio processing in a thread
def process_audio_threaded():
    # Create a thread to handle the audio processing
    audio_thread = threading.Thread(target=process_audio)
    audio_thread.start()

if __name__ == '__main__':
    app.run(debug=True, port=5001, host="0.0.0.0")


