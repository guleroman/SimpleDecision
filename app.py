from flask import Flask, jsonify, request, json, make_response, send_file
import requests,bs4
import time
import re
from sentimental import Sentimental
import pymorphy2
import json
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
sent = Sentimental()
morph = pymorphy2.MorphAnalyzer()

API_KEY = "abf14d0b25b6fb82ea3a316353fdb9d06eaf5d76"
BASE_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/{}"

def suggest(query, resource, count=10):
    url = BASE_URL.format(resource)
    headers = {"Authorization": "Token {}".format(API_KEY), "Content-Type": "application/json"}
    data = {"query": query, "count": count}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()

@app.route('/api/social', methods=['POST'])
def main():
    start_time = time.time()
    data_post_mas = json.loads(request.data)
    company_data_yes_no = data_post_mas['company_data']
    result_mas = {}
    for j in range(len(data_post_mas['data'])):
        result = {}
        data_post = data_post_mas['data'][j]
        #print ('ok - ',j)
        link = data_post['url']
        if (link is not None) and (link[:14] != 'https://vk.com'):
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
        if (company_name != '') and (company_data_yes_no == True):
            try:
                company_data = suggest(company_name, "party", count=1)
                result.update({"company_data":company_data})
            except:
                pass
        #print(result)
        result_mas.update({j:result})
        
        #print(result_mas)
    print("--- %s seconds ---" % (time.time() - start_time))
    return (jsonify(result_mas))
    #return('ok')   
#-------------------------------------------------------------------------
if __name__ == '__main__':

    app.run(debug=False,threaded = True, host='0.0.0.0', port=7777)