from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
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
    # model = openai.AudioModel.from_pretrained("large-v3")
    # audio = openai.Audio(file=open(filepath, "rb"))
    model = whisper.load_model("large-v3")
    result = model.transcribe(filepath)

    # The 'segments' part of the result contains timestamps and the text
    segments = result["segments"]

    # Prepare the transcript in SRT format
    srt_format_transcript = ""
    for index, segment in enumerate(segments, start=1):
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]

        # Convert timestamps from seconds to the SRT time format HH:MM:SS,ms
        start_srt = f"{int(start // 3600):02d}:{int(start % 3600 // 60):02d}:{int(start % 60):02d},{int(start % 1 * 1000):03d}"
        end_srt = f"{int(end // 3600):02d}:{int(end % 3600 // 60):02d}:{int(end % 60):02d},{int(end % 1 * 1000):03d}"

        srt_format_transcript += f"{index}\n{start_srt} --> {end_srt}\n{text}\n\n"

    transcript_filename = os.path.basename(filepath) + '.txt'
    transcript_path = os.path.join(
        app.config['TRANSCRIPTS_FOLDER'], transcript_filename)
    with open(transcript_path, 'w') as f:
        f.write(srt_format_transcript)
    return transcript_filename


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
