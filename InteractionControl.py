# main python program
import json, re

# lambda function handler - including specific reference to our skill
def lambda_handler(event, context):
    # if skill ID does not match my ID then raise error
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.3b35e9d8-27ec-4849-8304-a89b144a020a"):
        raise ValueError("Invalid Application ID")

    # test if session is new
    if event["session"]["new"]: 
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    # test and set session status
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

# define session start
def on_session_started(session_started_request, session):
    print ("Starting new session")

# define session launch
def on_launch(launch_request, session):
    return get_welcome_response()

# control intent call 
def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "CountToTen":
        return count_to_ten(intent)
    elif intent_name == "GetNumber":
        return get_number(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

# define end session
def on_session_ended(session_ended_request, session):
    print("Ending session")

# handle end of session
def handle_session_end_request():
    card_title = "Thanks"
    speech_output = 'Goodbye, <phoneme alphabet="ipa" ph="tʃaʊ">Ciao</phoneme>, <phoneme alphabet="ipa" ph="ʁə.vwaʁ">Au Revior</phoneme>,' +   " be sure to come back soon and practice"
    should_end_session = True
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response({}, build_speechlet_response(card_title, speech_output, card_output, None, should_end_session))

# define welcome intent
def get_welcome_response():
    session_attributes = {}
    card_title = "Count to ten"
    speech_output = 'Hello, <phoneme alphabet="ipa" ph="ɔ.la">Hola</phoneme>,  <phoneme alphabet="ipa" ph="bɒn.ˈʒʊə">Bonjour</phoneme>,' +  " I'm here to help you learn to count in different languages, just ask me if " \
                    " I can count to ten in your chosen language, at the moment I can count to 10 in German, English, French, Spanish and Italian"   
    reprompt_text = "Hey, just say count to ten in your chosen language"
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# define count to ten intent
def count_to_ten(intent):
    session_attributes = {}

    with open('language.json') as json_file :  
        languagedata = json.load(json_file)

    # test if bean exists in json
    if 'language' in intent['slots']:
        
        # extract slot value
        chosen_language = intent['slots']['language']['value']
        
        if chosen_language != "" :
            chosen_language = str(intent['slots']['language']['value']).lower()
            # set card title - appears on the show and spot
            card_title = "Count to ten : " + chosen_language.title()
            # set up temporary speech output
            speech_output = "Ok, counting to ten in "+ chosen_language.title() + ", get ready to repeat after me "
            # try and load language from json file, looping to build one to ten string
            try:
                for n in range(0,10):
                    
                    # extract value and phonetics ready to build string
                    value = languagedata['languages'][0][chosen_language][0][str(n+1)][0]['value']
                    phonetic = languagedata['languages'][0][chosen_language][0][str(n+1)][0]['phonetic']    
                    
                    # build speech string
                    speech_output = speech_output + ", " + '<phoneme alphabet="ipa" ph="' + phonetic + '">' + value + '</phoneme>' + generatebreakstring(1500,"ms")

                    if n == 9 :
                        speech_output = speech_output + ", I think you did great, what language would you like now?"
            
            # if language doesn't match then load default error response
            except:
                card_title = "I'm sorry"
                speech_output = "I'm sorry, I'm not sure I have learnt that language yet, at the moment I know German, English, Spanish, Italian and French, which language did you want?"
        else:
            speech_output = "I'm sorry, I'm not sure I have learnt that language yet, at the moment I know German, English, Spanish, Italian and French, which language did you want?"
    else:
        speech_output = "I'm sorry, I'm not sure I have learnt that language yet, at the moment I know German, English, Spanish, Italian and French, which language did you want?"

    should_end_session = False

    reprompt_text = ""

    speech_output = "<speak>" + speech_output + "</speak>"

    card_output = cleanssml(speech_output)

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session)) 

def get_number(intent):
    session_attributes = {}

    card_title = "Number"

    with open('language.json') as json_file :  
        languagedata = json.load(json_file)

    # test if bean exists in json
    if 'language' in intent['slots']:
        
        num2words = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten'}


        # extract slot value
        chosen_language = intent['slots']['language']['value']
        if chosen_language != "" :
            chosen_language = str(intent['slots']['language']['value']).lower()
            chosen_number = intent['slots']['translationnumber']['value']

            #chosen_number = num2words[int(chosen_number)]

            try:

                phonetic = languagedata['languages'][0][chosen_language][0][chosen_number][0]['phonetic']
                value = languagedata['languages'][0][chosen_language][0][chosen_number][0]['value']
            
                # set card title - appears on the show and spot
                card_title = chosen_number + ' in ' + chosen_language.title()
                speech_output = chosen_number + ' in ' + chosen_language.title() + ' is ' + generatebreakstring(500,"ms") + '<phoneme alphabet="ipa" ph="' + phonetic + '">' + value + '</phoneme>' + ", would you like to know anymore?"
            
            # if language doesn't match then load default error response
            except:
                speech_output = "I'm sorry, I can't find that number, at the moment I know how to count to 10 in German, English, Spanish, Italian and French, which language did you want?"
        else:
            speech_output = "I'm sorry, I can't find that number, at the moment I know how to count to 10 in German, English, Spanish, Italian and French, which language did you want?"
    else:
        speech_output = "I'm sorry, I can't find that number, at the moment I know how to count to 10 in German, English, Spanish, Italian and French, which language did you want?"

    should_end_session = False

    reprompt_text = ""

    speech_output = "<speak>" + speech_output + "</speak>"

    card_output = cleanssml(speech_output)

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session)) 

    
# build message response
def build_speechlet_response(title, output, cardoutput, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "SSML",
            "ssml":  output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": cardoutput
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

# build response
def build_response(session_attributes, speechlet_response):
    return {
    "version": "1.0",
    "sessionAttributes": session_attributes,
    "response": speechlet_response }

# function to generate the ssml needed for a break
def generatebreakstring(pause, timetype):
    # generate the SSML string for break with dynamic length
    breakstring = '<break time="' + str(pause) + timetype + '"/>'
    return breakstring

# function to automatically remove ssml markup, needed to generate the card output - which is what is shown on screen
def cleanssml(ssml):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', ssml)
    return cleantext

