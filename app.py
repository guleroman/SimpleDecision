from flask import Flask, jsonify, request, json, make_response, send_file
import time
import numpy as np
import pandas as pd
from sentimental import Sentimental

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
sent = Sentimental()

@app.route('/api/social', methods=['POST'])
def main():
    start_time = time.time()
    data_post = json.loads(request.data) 
    sentence = data_post['content']
    result = sent.analyze(sentence)
    
    print("--- %s seconds ---" % (time.time() - start_time))
    return (jsonify(result))
    #return('ok')   
#-------------------------------------------------------------------------
if __name__ == '__main__':

    app.run(debug=False,threaded = True, host='0.0.0.0', port=7080)