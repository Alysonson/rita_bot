# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import pandas as pd

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher



class ActionLocalizarProcesso(Action):

    def name(self) -> Text:
        return "localizar_processo"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        processos = pd.read_csv("../data/processos_eventos.csv")

        processo_id = tracker.latest_message.text

        numero, ano = processo_id.split("/")

        processo = processos[processos.numero == numero & processos.ano == ano]

        ret_numero = processo['NumeroProcesso']
        ret_ano = processo['AnoProcesso']
        ret_assunto = processo['Assunto']

        dispatcher.utter_message(text="Encontrei um processo com número {}, ano {}, assunto {}".format(ret_numero, ret_ano, ret_assunto))

        return []
