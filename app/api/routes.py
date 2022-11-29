from flask import Blueprint, request
from .controller.iepf2UploadController import IEPF2Controller
from dotenv import load_dotenv
import os

load_dotenv()

UPLOAD_PATH = os.getenv("UPLOAD_PATH")

api = Blueprint('api', __name__, url_prefix='/api')
  
@api.route('/uploader', methods = ['POST'])
def upload_file():
    iepf2controller = IEPF2Controller()
    file_paths = []
    if request.method == 'POST':
        file_type = request.form.get("fileType")
        files = request.files.getlist("file")
        
        if files[0].filename == '':
            result = { "data": [], "message": "No file selected"}
            return result

        if file_type == 'iepf2':
            for f in files: 
                f.save(UPLOAD_PATH+file_type + "/" + f.filename)
                file_paths.append(UPLOAD_PATH + file_type + "/" + f.filename)
            result = iepf2controller.insert_excel_data(file_paths, file_type)
        else:
            result = { "data": [], "message": "wrong file type"} 

        return result

@api.route('/multiple-dividend', methods = ['POST'])
def multiple_dividend():
    pass