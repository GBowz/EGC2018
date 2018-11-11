import pip
import requests
from flask import Flask
#app = Flask(__name__)
##curl -sX GET egchallenge.tech/epoch
##{
##  "current_epoch": 3000,
##  "prediction_epoch": 3001,
##  "timestamp": 0
##}
##curl -sX @app.route( 'egchallenge.tech/epoch' )
##@app.route( 'egchallenge.tech/epoch' )
#$ curl -sX GET @app.route('egchallenge.tech/epoch',methods=['GET'])
#app.run(debug=True)
#{
#  "current_epoch": 3000,
#  "prediction_epoch": 3001,
#  "timestamp": 0
#}
response = requests.get('http://egchallenge.tech/instruments')
json = response.json()
print(json[0])
