from flask import Flask, render_template, request
import os
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import *
#from threading import Thread
from ftplib import FTP
import ftplib
import urllib

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#print("APP_ROOT: ",APP_ROOT)

#--------------------ftp------------------------#
ftp = FTP("localhost") #адрес ftp-сервера
login_user = "user1" #логин
login_pass = "12351235" #пароль
ftp.login(login_user,login_pass)
sub_dir = ''

#Функция, проверающаяя существуование директории, в текущей папке.
def directory_exists(check_dir):
    files = []
    exists = False
    try:
        files = ftp.nlst(sub_dir)
        for file in files:
            if file == check_dir:
                exists = True
        if exists == False:
            ftp.mkd(check_dir)
    except ftplib.error_perm:
        print ("Error")

directory_exists('uploads')

#основная страница загрузки файлов на ftp-сервер
@app.route("/")
def index():
    return render_template("upload.html")

#отображение файлов в папке "uploads"
@app.route("/files")
def dir_viewer():

    req_path = "uploads"
    files_toview = []
    files = []
    try:
        files = ftp.nlst(req_path)
        for file in files:
            files_toview.append(file.split('/')[1])
    except ftplib.error_perm:
        print ("Error")

    return render_template('files.html', files=files_toview)

#загрузка файла выбранного пользователем
@app.route("/upload", methods=['POST'])
def upload():
    req_path = "uploads"
    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([req_path,filename])
        file.save(filename)
        file.close()

        fh = open(filename,'rb')
        ftp.storbinary('STOR ' + destination, fh)
        fh.close()
        os.remove(filename)

    return render_template("complete.html")

#скачивание файла с ftp-сервера, по нажатию (так же без обновления страницы)
@app.route("/download", methods=['POST'])
def download():
    req_path = "uploads"
    filename = request.form['download_file']
    destination = "/".join(['downloads',filename])
    data = urllib.request.urlretrieve('ftp://{0}:{1}@localhost/{2}/{3}'.format(login_user,login_pass,req_path,filename), destination)

    return render_template("complete.html")

pyqt = QApplication(sys.argv)
web = QWebView()

if __name__ == "__main__":
    #app.run(port=5000, debug=False)
    web.load(QUrl("http://127.0.0.1:5000/"))
    web.show()

    app_thread = Thread(target=app.run)
    app_thread.daemon = True
    app_thread.start()

    sys.exit(pyqt.exec_())
