import os
from flask import Flask, request, render_template, make_response
from pathlib import Path
import zipfile
import uuid
from pathlib import Path
import shutil

app = Flask(__name__)

# create a new directory under ProcessingFolder
# end case scenarios to be handled

processing_folder = os.path.abspath('ProcessingFolder')
if not os.path.isdir(processing_folder):
    os.mkdir(processing_folder)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/uploader', methods=['POST'])
def upload_file():
    if Path(request.files['accept'].filename).suffix == '.zip':
        file_ptr = request.files['accept']
        unique_id = uuid.uuid4()
        package_path = os.path.abspath(f'ProcessingFolder/{unique_id}')
        # package_path = os.path.abspath(processing_folder)
        os.mkdir(package_path)


        with zipfile.ZipFile(file_ptr, 'r') as ref:
            print(ref.namelist())
            # ref.extractall(processing_folder)
            ref.extractall(package_path)
            folder_package = os.listdir(package_path)

        for ev in ref.namelist():
            file_name = ev.split('/')[1]
            new_name = ev.split('/')[0] + "_" + file_name

            os.rename(package_path+'\\'+ev,package_path+'\\'+ new_name)
        for folder in folder_package:

            os.rmdir(package_path + "\\" + folder)

        print('file transfer successfully')
        return {'status': 'success'}

    else:
        return {'status': 'Invalid file type', 'content_type_received':
            f"{Path(request.files['accept'].filename).suffix}"}, 400

# main driver function
if __name__ == '__main__':
    app.run(port=4000)


#step-1 : take