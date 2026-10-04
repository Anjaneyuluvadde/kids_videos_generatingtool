import os
import time
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024 # 500 MB max

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-puzzle', methods=['POST'])
def generate_puzzle_video():
    puzzle_type = request.form.get('puzzle_type', 'guess_animal')
    theme = request.form.get('theme', 'cartoon')
    duration = int(request.form.get('duration', 10))
    images = request.files.getlist('images')

    saved_images = []
    if images:
        for img in images:
            if img.filename:
                filename = secure_filename(img.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                img.save(filepath)
                saved_images.append(filepath)

    if not saved_images and puzzle_type != 'emoji_puzzle':
        return jsonify({"success": False, "message": "Please upload at least one image for this game mode."})

    try:
        from modules.puzzle_generator import generate_puzzle
        from modules.video_renderer import render_puzzle_video
        
        results = []
        
        # If no images, but emoji puzzle, generate without image
        if not saved_images and puzzle_type == 'emoji_puzzle':
            puzzle_data = generate_puzzle(puzzle_type, None, theme, duration)
            output_filename = render_puzzle_video(puzzle_data, app.config['OUTPUT_FOLDER'])
            results.append(f"/outputs/{output_filename}")
        else:
            if puzzle_type == 'guess_animal' and len(saved_images) > 1:
                from modules.guess_the_animal_engine import generate_guess_animal_video_multi
                output_filename = generate_guess_animal_video_multi(saved_images, theme, duration, app.config['OUTPUT_FOLDER'])
                results.append(f"/outputs/{output_filename}")
            elif puzzle_type == 'hidden_object' and len(saved_images) > 1:
                from modules.hidden_object_engine import generate_hidden_object_video_multi
                output_filename = generate_hidden_object_video_multi(saved_images, theme, duration, app.config['OUTPUT_FOLDER'])
                results.append(f"/outputs/{output_filename}")
            else:
                # Batch process images (Single image or other types)
                for img_path in saved_images:
                    puzzle_data = generate_puzzle(puzzle_type, img_path, theme, duration)
                    
                    if puzzle_type == 'guess_animal':
                        from modules.guess_the_animal_engine import generate_guess_animal_video
                        output_filename = generate_guess_animal_video(img_path, theme, duration, app.config['OUTPUT_FOLDER'])
                    elif puzzle_type == 'hidden_object':
                        from modules.hidden_object_engine import generate_hidden_object_video_multi
                        output_filename = generate_hidden_object_video_multi([img_path], theme, duration, app.config['OUTPUT_FOLDER'])
                    else:
                        output_filename = render_puzzle_video(puzzle_data, app.config['OUTPUT_FOLDER'])
                        
                    results.append(f"/outputs/{output_filename}")

        if not results:
             return jsonify({"success": False, "message": "No valid data to generate puzzle."})

        return jsonify({
            "success": True, 
            "message": "Puzzle video(s) generated successfully!", 
            "videos": results
        })

    except Exception as e:
        import traceback
        try:
            with open('error_log.txt', 'w') as f:
                f.write(traceback.format_exc())
        except:
            pass
        return jsonify({"success": False, "message": str(e)})

@app.route('/outputs/<filename>')
def serve_output(filename):
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    return send_file(filepath)

@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    print("==================================================")
    print("AI KIDS PUZZLE VIDEO PLATFORM IS RUNNING!")
    print("Open your browser and go to: http://127.0.0.1:5000")
    print("==================================================")
    app.run(host='127.0.0.1', port=5000, debug=True)
