from flask import Blueprint, request
from ..controller.iepf2UploadController import IEPF2Controller
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
        file_type = request.form.get("file_type")
        files = request.files.getlist("file[]")
        if file_type == 'iepf2':
            for f in files: 
                f.save(UPLOAD_PATH+file_type + "/" + f.filename)
                file_paths.append(UPLOAD_PATH+file_type + "/" + f.filename)
            result = iepf2controller.insert(file_paths)
        else:
            result = { "data": [], "message": "wrong file type"} 
        return result