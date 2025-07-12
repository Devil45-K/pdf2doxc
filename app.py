from flask import Flask, render_template, request, send_file
from pdf2docx import Converter
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    file = request.files['pdf_file']
    if file.filename.endswith('.pdf'):
        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(pdf_path)
        
        docx_filename = file.filename.replace('.pdf', '.docx')
        docx_path = os.path.join(CONVERTED_FOLDER, docx_filename)
        
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()

        return send_file(docx_path, as_attachment=True)

    return "Invalid file format. Please upload a PDF."

if __name__ == '__main__':
    app.run(debug=True)
