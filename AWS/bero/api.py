
import os
from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route('/name', methods=['POST'])
def method():


   stacknames = request.args.get('stacknames')
   os.system('/bin/bash --rcfile sh bero.sh '+ str(stacknames))
   return 'do synthesize'


@app.route('/append', methods=['POST'])
def index():
  classname = request.args.get('classname')
  stackname = request.args.get('stackname')
  path = request.args.get('path')
  accountnumber =request.args.get('accountnumber')
  region = request.args.get('region')  

  with open('/app/app.py','r') as f:
    contents = f.readlines()
  contents.insert(28, str(classname)+ "(app, '" + str(stackname)+ "', env=cdk.Environment(account= '" + str(accountnumber) +"', region='" + str(region)+ "'))\n")
  contents.insert(8, "from " + str(path) + " import " + str(classname) +"\n")
  with open('/app/app.py','w') as f:
    contents = "".join(contents)
    f.write(contents)

    return 'appended a new line with updated paramaters'      

if __name__=='__main__':   
    app.run(port=7001, host='0.0.0.0')