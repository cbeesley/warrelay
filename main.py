from flask import Flask, url_for, request
from flask import render_template
import json
#Need to have "Requests" installed
import requests
from requests.auth import HTTPBasicAuth

#Set this to point to the configuration file you want to use.
with open('sampleconfig.json') as data_file:
    configFile = json.load(data_file)

app = Flask(__name__)
app.debug = True
temp_file_path = configFile['warpath']
"""
The following route is for the bamboo job
that recives a war then saves it
"""
@app.route('/warloader/text/deploy', methods=['PUT'])
def upload_file():
    # returns a 400 if any of these are missing
    tag = request.args['tag']
    path = request.args['path']
    
    
    if tag == None:
        return 'FAIL - Tag %s is not mapped to any host in the configuration file'
    deployUrl = configFile['deploymentUrls'][tag]
    username = configFile['deploymentCredentials'][tag][0]
    password = configFile['deploymentCredentials'][tag][1]

    if request.method == 'PUT':
        f = open(temp_file_path, 'wb')
        f.write(request.data)
        f.close()
        payload = {'path': path, 'update': 'true'}
        files = {'file': open(temp_file_path, 'rb')}
        r = requests.put(deployUrl, files=files, params=payload, auth=HTTPBasicAuth(username, password))
        deployResponse =  r.text

    # Add your processing code here to copy the war to a final destination restart the server, or other
    # system tasks
    
    # Need to tell sender everything is awesome
    return 'OK - Deployed application at context path /debug'

"""
Run this as a python app for local dev, otherwise
run server.py for actual production
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0')