import os
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import pytesseract

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def extract_arabic_text(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='ara')
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            text = extract_arabic_text(filepath)
            return render_template('index.html', image_url=filepath, extracted_text=text)
    return render_template('index.html', image_url=None, extracted_text=None)

if __name__ == "__main__":
    app.run(debug=True)
