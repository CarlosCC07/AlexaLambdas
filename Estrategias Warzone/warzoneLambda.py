# Based on guide by Uros Ralevic, check it out if you want a step-by-step guide on
# configuring an Alexa Skill. Link:
# https://medium.com/crowdbotics/how-to-build-a-custom-amazon-alexa-skill-step-by-step-my-favorite-chess-player-dcc0edae53fb

import json
import random

#------------------------------Definitions--------------------------------

warzone_maps = ["Verdansk", "Rebirth Island", "Contrato", "Rebirth", "Alcatraz", "Contratos", "Contract"]

locations_verdansk = ["Dam", "Military Base", "Quarry", "Airport", "TV Station", "Storage Town", "Superstore", "Stadium", "Lumber", "Farmland", "Boneyard", 
"Train Station", "Hospital", "Downtown", "Promenade East", "Promenade West", "Hills", "Park", "Port", "Prison", "Aborda el tren"]

locations_rebirth = ["Bioweapon Labs", "Decon Zone", "Chemical Eng.", "Harbor", "Prison Block", "Shore", "Construction Site", "Headquarters", 
"Nova 6 Factory", "Living Quarters", "Security Area"]

contract_list = ["Bounty", "Scavenger", "Supply Run", "Recon", "Most Wanted"]


#------------------------------Lambda--------------------------------

def lambda_handler(event, context):
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()

#------------------------------Request Handler Functions--------------------------------

def on_start():
    print("Session Started.")

def on_launch(event):
    onlunch_MSG = "Bienvenido a Estrategias Warzone."
    reprompt_MSG = "¿Quieres saber dónde iniciar o qué contrato tomar?"
    card_TEXT = "Elige una modalidad, ya sea mapa o contrato."
    card_TITLE = "Elegir modalidad"
    return output_json_builder_with_reprompt_and_card(onlunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def on_end():
    print("Session Ended.")

#-----------------------------Intent Request-------------------------------

def intent_scheme(event):
    
    intent_name = event['request']['intent']['name']

    if intent_name == "startMap":
        return start_map(event)        
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)

#---------------------------Intent Handler-------------------------------

def start_map(event):
    name=event['request']['intent']['slots']['locWarzone']['value']
    warzone_maps_lower=[w.lower() for w in warzone_maps]
    if name.lower() in warzone_maps_lower:
        reprompt_MSG = "¿Quieres saber dónde iniciar o qué contrato tomar?"
        card_TEXT = "Elegiste " + name.lower()
        card_TITLE = "Elegiste " + name.lower()
        if name.lower() == "verdansk":
            rNum = random.randint(0, 20)
            mapResponse = locations_verdansk[rNum]
        elif name.lower() == "rebirth island" or name.lower() == "rebirth" or name.lower() == "alcatraz":
            rNum = random.randint(0, 10)
            mapResponse = locations_rebirth[rNum]
        elif name.lower() == "contrato" or name.lower() == "contratos" or name.lower() == "contract":
            rNum = random.randint(0, 4)
            mapResponse = contract_list[rNum]
        return output_json_builder_with_reprompt_and_card(mapResponse, card_TEXT, card_TITLE, reprompt_MSG, True)
    else:
        wrongname_MSG = "Lo siento, no entendí. Por favor, vuelve a intentar."
        reprompt_MSG = "¿Quieres saber dónde iniciar o qué contrato tomar?"
        card_TEXT = "Elección no válida."
        card_TITLE = "Elección no válida."
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
        
def stop_the_skill(event):
    stop_MSG = "Gracias por usar Estrategias Warzone."
    reprompt_MSG = ""
    card_TEXT = "Gracias."
    card_TITLE = "Gracias."
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
    
def assistance(event):
    assistance_MSG = "Te puedo ayudar a elegir una ubicación dónde empezar o un contrato si tú y tu equipo están indecisos. Puedes elegir entre los mapas Verdansk y Rebirth Island, o bien preguntar por un contrato."
    reprompt_MSG = "¿Quieres saber dónde iniciar o qué contrato tomar?"
    card_TEXT = "Texto de referencia"
    card_TITLE = "Ayuda"
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def fallback_call(event):
    fallback_MSG = "Lo siento, no entendí. Por favor, vuelve a intentar."
    reprompt_MSG = "¿Quieres saber dónde iniciar o qué contrato tomar?"
    card_TEXT = "Elección no válida."
    card_TITLE = "Elección no válida."
    return output_json_builder_with_reprompt_and_card(fallback_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

#------------------------------Responses--------------------------------

def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict

def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict
    
def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict    

def response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

def output_json_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value)
    return response_dict