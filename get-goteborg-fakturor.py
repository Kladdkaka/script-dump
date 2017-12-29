# code is terrible i know, dont complain :]

import requests
import xmltodict
import os
from pprint import pprint
import re

def is_excel_format(t):
    if t == 'application/vnd.ms-excel' or t == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        return True
    else:
        return False

if not os.path.exists('temp'):
    os.makedirs('temp')

data = requests.get('https://catalog.goteborg.se/store/search?type=solr&query=resource:https\://catalog.goteborg.se/store/6/resource/75&limit=1xml').json()
urls = [entry['value'] for entry in data['resource']['children'][0]['metadata']['https://catalog.goteborg.se/store/6/resource/75']['http://www.w3.org/ns/dcat#distribution']]

pprint(urls)

urls_to_download = []

for url in urls:
    r = requests.get(url)
    data = xmltodict.parse(r.text)

    #pprint(data)

    #pprint(data['rdf:RDF']['dcat:Distribution']['dcterms:format'] )

    _format = data['rdf:RDF']['dcat:Distribution']['dcterms:format']

    is_excel = None

    #pprint(_format)
    
    if isinstance(_format, list):
        is_excel = any([is_excel_format(x) for x in _format])
    elif is_excel_format(data['rdf:RDF']['dcat:Distribution']['dcterms:format']):
        is_excel = True
    else:
        is_excel = False
        #print(url)
    
    print(is_excel, url)

    if is_excel:
        urls_to_download.append(data['rdf:RDF']['dcat:Distribution']['dcat:downloadURL']['@rdf:resource'])

pprint(urls_to_download)

for url in urls_to_download:
    r = requests.get(url)
    fname = 'temp/' + re.findall("filename=\"(.+)\"", r.headers['content-disposition'])[0].split('\\')[-1]

    print(fname)

    with open(fname, 'wb') as f:
        f.write(r.content)
