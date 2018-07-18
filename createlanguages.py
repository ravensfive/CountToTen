# create the bean json from scratch

#import json
import json

# setup json
def setupJson() :
    global languagedata
    languagedata = {}
    languagedata['languages'] = []

#setupJson()

# add language to the json
def addlanguagetoJson(language,number,value,phonetic) :
    languagedata['languages'].append = {'language':[language],'numbers':[{number:[{'value':[value],'phonetic':[phonetic]}]}]}
    print(languagedata)
    with open('language.json', 'w') as outfile:  
        json.dump(languagedata, outfile) 

def interpretJson():
    with open('language.json') as json_file :  
        languagedata = json.load(json_file)
    
    #print(languagedata)
    speech_output = ""
    #for l in languagedata['languages']
    print(languagedata['languages'])
    #print (languagedata['languages'][0]['german'][0]['2'][0]['value'])

    chosen_language = "german"

    try:
        for n in range(0,2):

                speech_output = ""

                value = languagedata['languages'][0][chosen_language][0][str(n+1)][0]['value']
                phonetic = languagedata['languages'][0][chosen_language][0][str(n+1)][0]['phonetic']    
                
                speech_output = '<phoneme alphabet="ipa" ph="' + phonetic + '">' + value + '</phoneme>'
    except:
        speech_output = "mismatch"

    print (speech_output)

#interpretJson()

def testnumbers():
            
        num2words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten'}

        # extract slot value
        
        #chosen_number = num2words[intent['slots']['translationnumber']['value']]
        chosen_number = num2words[1]
        print(chosen_number)

testnumbers()