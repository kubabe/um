import requests
from bs4 import BeautifulSoup
import re

def get_word(login = 'sieyo', password = 'jakub16171A', url_word = 'https://dictapi.lexicala.com/search?', source = 'global', language = 'de', morph = 'true', analyzed = 'true', text = 'test'):
    response = requests.get(url_word,
    params={'source': source,
           'language': language,
           'text': text,
           'morph': morph,
           'analyzed': analyzed},
            auth=(login, password))
    json = response.json()
    
    word_instances = []
    
    iteration = 0
        
    for i, a in enumerate(json['results']):
        
        try:
        
            if type(a['headword']) != list and bool(re.match('^[a-zA-ZäöüÄÖÜß]+$', a['headword']['text'])):

                word_instance = {
                    'id':a['id'],
                    'word':a['headword']['text'],
                    'speech_part':a['headword']['pos']
                }

                word_instances.append(word_instance)

            elif type(a['headword']) == list:

                word_instance = {
                    'id':a['id'],
                    'word':a['headword'][0]['text'],
                    'speech_part':a['headword'][0]['pos']
                }

                word_instances.append(word_instance)
                
        except Exception:

            pass

    return word_instances

def get_word_details(login = 'sieyo', password = 'jakub16171A', url_definition = 'https://dictapi.lexicala.com/entries/', word_id = None):
    
    
    if word_id is None:
        
        return 'ID parameter is required.'
    
    else: 
    
        url_id = url_definition + word_id
        response = requests.get(url_id, auth=(login, password))
        json = response.json()

        word_details = {}

        if type(json['headword']) != list:
        
            if json['headword']['pos'] == 'noun':

                word_details['gender'] = json['headword']['gender']
                
        elif type(json['headword']) == list:
            
            if json['headword'][0]['pos'] == 'noun':

                word_details['gender'] = json['headword'][0]['gender']

        definitions_translations = []

        try:

            for i, a in enumerate(json['senses']):

                definitions_translations_instance = {}
                
                try:

                    definitions_translations_instance['definition'] = a['definition']
                
                except Exception:

                    pass

                if type(a['translations']['en']) != list:

                    definitions_translations_instance['translation'] = a['translations']['en']['text']

                elif type(a['translations']['en']) == list:

                    translations_list = []

                    for j, b in enumerate(a['translations']['en']):

                        translations_list.append(b['text'])

                    definitions_translations_instance['translation'] = translations_list

                definitions_translations.append(definitions_translations_instance)

        except Exception:

            pass

        word_details['definitions_translations'] = definitions_translations
    
    return word_details

def combine_words(login = 'sieyo', password = 'jakub16171A', url_word = 'https://dictapi.lexicala.com/search?', url_definition = 'https://dictapi.lexicala.com/entries/', text = 'test'):
    
    results = get_word(login = login, password = password, url_word = url_word, text = text)
    
    for i, a in enumerate(results):
        
        word_id = a['id']
        
        results_details = get_word_details(login = login, password = password, url_definition = url_definition, word_id = word_id)
        
        results[i]['details'] = results_details
        
        if results[i]['speech_part'] == 'noun':
            
            if results[i]['details']['gender'] == 'masculine':
                
                results[i]['article'] = 'der'

                results[i]['full_word'] = 'der ' + results[i]['word']
            
            elif results[i]['details']['gender'] == 'feminine':
                
                results[i]['article'] = 'die'

                results[i]['full_word'] = 'die ' + results[i]['word']
                
            else:
                
                results[i]['article'] = 'das'

                results[i]['full_word'] = 'das ' + results[i]['word']

        else:

            results[i]['full_word'] = results[i]['word']
        
    return results

def combine_words_single(login = 'sieyo', password = 'jakub16171A', url_definition = 'https://dictapi.lexicala.com/entries/', word_id = None):
    
    if word_id is None:
        
        return 'ID parameter is required.'
    
    else: 
    
        url_id = url_definition + word_id
        response = requests.get(url_id, auth=(login, password))
        json = response.json()
        
        word_details_full = {}
        word_details = {}

        word_details_full['id'] = json['id']

        if type(json['headword']) != list:
            
            word_details_full['word'] = json['headword']['text']
            word_details_full['speech_part'] = json['headword']['pos']
        
            if json['headword']['pos'] == 'noun':

                word_details['gender'] = json['headword']['gender']
                
        elif type(json['headword']) == list:
            
            word_details_full['word'] = json['headword'][0]['text']
            word_details_full['speech_part'] = json['headword'][0]['pos']
            
            if json['headword'][0]['pos'] == 'noun':

                word_details['gender'] = json['headword'][0]['gender']
            
        definitions_translations = []

        try:

            for i, a in enumerate(json['senses']):

                definitions_translations_instance = {}
                
                try:

                    definitions_translations_instance['definition'] = a['definition']
                
                except Exception:

                    pass

                if type(a['translations']['en']) != list:

                    definitions_translations_instance['translation'] = a['translations']['en']['text']

                elif type(a['translations']['en']) == list:

                    translations_list = []

                    for j, b in enumerate(a['translations']['en']):

                        translations_list.append(b['text'])

                    definitions_translations_instance['translation'] = translations_list

                definitions_translations.append(definitions_translations_instance)

        except Exception:

            pass

        word_details['definitions_translations'] = definitions_translations
        
        word_details_full['details'] = word_details
        
        if word_details_full['speech_part'] == 'noun':
            
            if word_details_full['details']['gender'] == 'masculine':
                
                word_details_full['article'] = 'der'

                word_details_full['full_word'] = 'der ' + word_details_full['word']
            
            elif word_details_full['details']['gender'] == 'feminine':
                
                word_details_full['article'] = 'die'

                word_details_full['full_word'] = 'die ' + word_details_full['word']
                
            else:
                
                word_details_full['article'] = 'das'

                word_details_full['full_word'] = 'das ' + word_details_full['word']

        else:

            word_details_full['full_word'] = word_details_full['word']
    
    return word_details_full

def get_noun_declension(noun_url = 'https://www.verbformen.com/declension/nouns/?', word = 'test'):
    
    page = requests.get(noun_url,
                       params={'w': word})
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    table_divs = soup.select('body > article > div:nth-child(1) > div.rAbschnitt > div > section > div.rAufZu > div.vDkl > div.vTbl')
    
    declension = {'singular':{
                'nominativ':'',
                'genitiv':'',
                'dativ':'',
                'akkusativ':''},
              'plural':{
                'nominativ':'',
                'genitiv':'',
                'dativ':'',
                'akkusativ':''},
              }
    
    regex = re.compile('[^a-zA-ZäöüÄÖÜß/()]')
    
    for i, div in enumerate(table_divs):
        table = div.select('table')[0]
        rows = table.find_all('tr')
        for j, row in enumerate(rows):
            line = row.find_all('td')
            form = ''
            for k, word in enumerate(line):
                if k == 0:
                    form += regex.sub('', word.text.strip())
                else:
                    form += ' ' + regex.sub('', word.text.strip())
            declension[list(declension.keys())[i]][list(declension[list(declension.keys())[i]].keys())[j]] = form
    
    return declension

def get_verb_conjugation(verb_url = 'https://www.verbformen.com/conjugation/?', word = 'test'):
    
    page = requests.get(verb_url,
                       params={'w': word})
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    divs = soup.select('body > article > div:nth-child(1) > div.rAbschnitt > div > section')
    table_divs = list(divs)[2].select('div.rAufZu > div.vTbl')

    conjugation = {'present':{
                'ich':'',
                'du':'',
                'ersiees':'',
                'wir':'',
                'ihr':'',
                'sie':''},
              'imperfect':{
                'ich':'',
                'du':'',
                'ersiees':'',
                'wir':'',
                'ihr':'',
                'sie':''},
              'perfect':{
                'ich':'',
                'du':'',
                'ersiees':'',
                'wir':'',
                'ihr':'',
                'sie':''},
              'pluperfect':{
                'ich':'',
                'du':'',
                'ersiees':'',
                'wir':'',
                'ihr':'',
                'sie':''}, 
              'future':{
                'ich':'',
                'du':'',
                'ersiees':'',
                'wir':'',
                'ihr':'',
                'sie':''},
              'future perfect':{
                'ich':'',
                'du':'',
                'ersiees':'',
                'wir':'',
                'ihr':'',
                'sie':''},
              }

    regex = re.compile('[^a-zA-ZäöüÄÖÜß/()]')
    
    for i, div in enumerate(table_divs):
        table = div.select('table')[0]
        rows = table.find_all('tr')
        for j, row in enumerate(rows):
            line = row.find_all('td')
            form = ''
            for k, word in enumerate(line):
                if k == 0:
                    pass
                elif k == 1:
                    form += regex.sub('', word.text.strip())
                else:
                    form += ' ' + regex.sub('', word.text.strip())
            conjugation[list(conjugation.keys())[i]][list(conjugation[list(conjugation.keys())[i]].keys())[j]] = form
            
    return conjugation

def get_total(login = 'sieyo', password = 'jakub16171A', url_definition = 'https://dictapi.lexicala.com/entries/', noun_url = 'https://www.verbformen.com/conjugation/?', verb_url = 'https://www.verbformen.com/conjugation/?', word_id = None):
    
    if word_id is None:
        
        return 'ID parameter is required.'
    
    else: 
    
        word_json = combine_words_single(login = login, password = password, url_definition = url_definition, word_id = word_id)

        word = word_json['word']

        speech_part = word_json['speech_part']

        if speech_part == 'noun':
            declension = get_noun_declension(noun_url = noun_url, word = word)
            word_json['details']['declension'] = declension
        elif speech_part == 'verb':
            conjugation = get_verb_conjugation(verb_url = verb_url, word = word)
            word_json['details']['conjugation'] = conjugation
        else:
            pass
    
        return word_json