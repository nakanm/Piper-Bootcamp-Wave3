#!/usr/bin/env python3

import os
import time
import datetime
from ftplib import FTP
hostname  = "your hostname url"
ftp_account = "your ftp accout user"
ftp_passward = "your ftp password"

ftp = FTP(hostname,  ftp_account, ftp_passward)
with open("./templates/index.html", "rb") as f:
     ftp.storlines("STOR ./index.html", f)
with open("./static/graph1.png", "rb") as f:
    ftp.storbinary("STOR ./static/graph1.png", f)
with open("./static/graph2.png", "rb") as f:
    ftp.storbinary("STOR ./static/graph2.png", f)
with open("./static/graph3.png", "rb") as f:
    ftp.storbinary("STOR ./static/graph3.png", f)
with open("./static/graph4.png", "rb") as f:
    ftp.storbinary("STOR ./static/graph4.png", f)
with open("./static/graph5.png", "rb") as f:
    ftp.storbinary("STOR ./static/graph5.png", f)

ftp.close()
