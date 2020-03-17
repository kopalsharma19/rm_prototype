from pymongo import MongoClient
from flask import Flask, render_template, request, url_for
import os 
from flask_pymongo import PyMongo
from FlaskWebProject6 import app


@app.route('/')
@app.route('/admin')
def admin():
    return render_template('admin.html')


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
