import os

from app import app
from flask import Flask, flash, request, redirect, render_template, jsonify
from werkzeug.utils import secure_filename

# 允许那些文件名上传
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','zip'])


def allowed_file(filename):
    # 此函数应该检查文件名以确定文件类型是否被允许
    # 例如，你可以检查文件扩展名是否在你希望接受的扩展名列表中
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('file-upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return jsonify({'message': '未检测到文件'}), 400

    files = request.files.getlist('files[]')

    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors[file.filename] = '文件类型错误'

    if success and errors:
        errors['message'] = '一半成功一半失败,请查验'
        return jsonify(errors), 206  # Partial Content
    elif success:
        return jsonify({file.filename: '已经成功上传到了服务器'}), 201
    else:
        return jsonify({'message': f'{file.filename}  --->文件上传失败', 'errors': errors}), 400


if __name__ == "__main__":
    app.run()