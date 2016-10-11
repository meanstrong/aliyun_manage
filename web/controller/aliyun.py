# -*- coding:utf-8 -*-
import os

from flask import request, Response, redirect, url_for, render_template, g
from werkzeug import secure_filename

from web import app
from .api import ecs

__author__ = 'Rocky Peng'


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/send_file", methods=["GET", "POST"])
def send_file():
    if request.method == "POST":
        f = request.files['file']
        if f :
            filename=secure_filename(f.filename)
            src = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(src)
            dest = request.form.get("path")
            instance = request.args.get("InstanceId")
            ecs.SendFile(instance, src, dest)
            return redirect(url_for('send_file'))

    return render_template("send_file.html")

@app.route("/exec_command", methods=["GET"])
def exec_command():
    return render_template("exec_command.html")
