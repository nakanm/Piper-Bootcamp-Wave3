import boto
import os
from flask import Flask
import redis

r = redis.Redis(host='', port='', password='')

app = Flask(__name__)

ecs_access_key_id = ''  
ecs_secret_key = ''

## Open a session with your ECS
session = boto.connect_s3(ecs_access_key_id, ecs_secret_key, host='')  

## Get hold of your bucket
bname = ''
b = session.get_bucket(bname)


@app.route('/')
def mainmenu():
    value=r.get('RPIvalue')

    begin_page = """
    <html>
    <head>
        <style>
        body {background-image: url("static/backgr2.jpg");} 
        </style>
    </head>
    <body>
    <center><h1>Summer Mealtime</h1>"""
	
    mid_page = ""
    for photo in b.list():
        #print(photo.key)
        k = b.get_key(photo)
        ##Don't forget to pull the metadata and use it to build the album
        #author = k.get_metadata('author')
        mid_page += """<hr><h2>{}</h2>
        <img src="http://131030155286710005.public.ecstestdrive.com/bname/{}"
        width=1000><br>
	<h2>the current distance is {}cm<h2><br>""".format(photo.key, photo.key,value)
		
    end_page = """
    <a href="/history.html">Summer Mealtime Histroty</a><br>
    </center>
    </body>
    </html>"""

    return begin_page + mid_page + end_page

@app.route('/history.html')
def history():
    #diagram=str(r.hgetall("RPIvalueHistory"))
    

    response = """<br><h1>Distance History<h1><br>""" + """<h2>Date-Time  : distance<h2><br>"""
    response += str(r.hgetall("RPIvalueHistory")).replace(",","<br>").replace("{","").replace("}","<br>").replace("'","")
    response +=  """<a href="/"><h2>Back to TOP<h2></a>"""

    return response

     

if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', '5000')), threaded=True)

