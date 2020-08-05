import os
import uuid
from flask import Flask

app = Flask(__name__)
my_uuid = str(uuid.uuid1())

@app.route('/')
def mainmenu():

    response = """
    <html>
    <body>
     <h1><u>Welcome to the Page</u></h1>
     <h3>
     <ul>
     redis cloud 
     </ul>
     </h3>
    </body>
    </html>
    """.format(my_uuid)

    return response

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
