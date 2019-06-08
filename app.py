from flask import Flask, jsonify, request, json, make_response, send_file
import requests,bs4
import time
import re
from sentimental import Sentimental
import pymorphy2

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
sent = Sentimental()
morph = pymorphy2.MorphAnalyzer()

@app.route('/api/social', methods=['POST'])
def main():
    start_time = time.time()
    data_post = json.loads(request.data) 
    link = data_post['url']
    if link is not None:
        ss = requests.get(link)     #Переназначение мыла
        bb = bs4.BeautifulSoup(ss.text, "html.parser")
        text = bb.findAll({'p' : True}) #Выборка значений в тегах "p"
        selectText = ''
        for i in range(len(text)):      #Слепляем обрубки строк
            selectText = selectText + ' ' + text[i].getText()

    else:
        selectText = data_post['content']
    company_name = ''
    for nnn in ['ОАО','ПАО','ЗАО','ООО']:
        if selectText.partition(nnn)[2] != '':
            if selectText.partition(nnn)[2][1:][0] == '«':
                company_name = selectText.partition(nnn)[2].partition('«')[2].partition('»')[0]
            elif selectText.partition(nnn)[2][1:][0] == '\"':
                company_name = selectText.partition(nnn)[2].partition('\"')[2].partition('\"')[0]
            elif selectText.partition(nnn)[2][1:][0] == '\'':
                company_name = selectText.partition(nnn)[2].partition('\'')[2].partition('\'')[0]
            else:
                company_name = selectText.partition(nnn)[2][1:].partition(' ')[0]
        if company_name != '' :
            break
    words = [morph.parse(word)[0].normal_form for word in re.findall(r'\w+', selectText)]
    #sentence_2 = {" ".join(words)}
    sentence = " ".join(words)
    result = sent.analyze(sentence)
    result.update({"company":company_name})

    print("--- %s seconds ---" % (time.time() - start_time))
    return (jsonify(selectText,result))
    #return('ok')   
#-------------------------------------------------------------------------
if __name__ == '__main__':

    app.run(debug=False,threaded = True, host='0.0.0.0', port=7777)
