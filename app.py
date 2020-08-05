#!/usr/bin/env python3

import os
import time
import datetime
from flask import Flask, render_template



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', message="Piper Wave3 Personal Project")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

