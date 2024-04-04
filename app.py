from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
import openai
import whisper

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
TRANSCRIPTS_FOLDER = 'transcripts'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TRANSCRIPTS_FOLDER'] = TRANSCRIPTS_FOLDER

# Ensure upload and transcripts directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPTS_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            transcript_filename = transcribe_file(filepath)
            return redirect(url_for('download_file', filename=transcript_filename))
    return render_template('upload.html')

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['TRANSCRIPTS_FOLDER'], filename)

def transcribe_file(filepath):
    #model = openai.AudioModel.from_pretrained("large-v3")
    #audio = openai.Audio(file=open(filepath, "rb"))
    model = whisper.load_model("large-v3")
    result = model.transcribe(filepath)

    # The 'segments' part of the result contains timestamps and the text
    segments = result["segments"]

    # Prepare the transcript with timestamps
    transcript_with_timestamps = ""
    for segment in segments:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        transcript_with_timestamps += f"{start}-{end}: {text}\n"

    transcript_filename = os.path.basename(filepath) + '.txt'
    transcript_path = os.path.join(app.config['TRANSCRIPTS_FOLDER'], transcript_filename)
    with open(transcript_path, 'w') as f:
        f.write(transcript_with_timestamps)
    return transcript_filename

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

