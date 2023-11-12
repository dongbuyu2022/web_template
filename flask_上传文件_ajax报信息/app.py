from flask import Flask

'''
可以继续对html进行美化
'''

UPLOAD_FOLDER = 'E:\\test'   # 用于指定上传到XXX(服务器端哪个盘)

app = Flask(__name__)
app.secret_key = "zijishezhiyigemima" # 自己设置一个密码
# 用于指定上传到XXX(服务器端哪个盘)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#设置文件大小的上限,目前设置的是16mb
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024