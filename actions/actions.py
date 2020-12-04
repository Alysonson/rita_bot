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
        return "action_localizar_processo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        processos = pd.read_csv("data/processos_eventos.csv", sep=";")

        processos.to_csv('teste.csv')

        processo_id = tracker.latest_message['text']

        numero, ano = processo_id.split("/")

        processo = processos[(processos['NumeroProcesso'] == int(
            numero)) & (processos['AnoProcesso'] == int(ano))]

        try:
            ret_numero = processo['NumeroProcesso'].values[0]
            ret_ano = processo['AnoProcesso'].values[0]
            ret_assunto = processo['Assunto'].values[0]

            dispatcher.utter_message(text="Encontrei um processo com número {}, ano {}, assunto {}.".format(
                ret_numero, ret_ano, ret_assunto))
        except:
            dispatcher.utter_message(
                text="Não encontrei o seu processo, procurei ({}) {}/{}".format(processo_id, numero, ano))

        return []

class ActionUltimaInformacao(Action):
    def name(self) -> Text:
        return "action_ultima_informacao"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            dispatcher.utter_message(text="A última peça juntada ao processo XXXXXX/XXXX foi publicada no dia XX/XX/XXXX pelo setor XXX (Evento 9). Para visualizar a peça processual acesse o link www.tce.rn.gov.br/processo/xxxxx.pdf")
        except:
            dispatcher.utter_message(
                text="Erro")

        return []


class ActionInformacaoCorpoTecnico(Action):
    def name(self) -> Text:
        return "action_informacao_corpo_tecnico"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            dispatcher.utter_message(text="O processo XXXXXX/XXXX possui a(s) seguinte(s) peça(s) juntada(s) aos autos pela unidade técnica XXX:")
        except:
            dispatcher.utter_message(
                text="Erro")

        return []


class ActionInformacaoMPTC(Action):
    def name(self) -> Text:
        return "action_informacao_mptc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            dispatcher.utter_message(text="O processo XXXXXX/XXXX possui a(s) seguinte(s) peça(s) juntada(s) aos autos pelo MPTC:")
        except:
            dispatcher.utter_message(
                text="Erro")

        return []


class ActionDecisoes(Action):
    def name(self) -> Text:
        return "action_decisoes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            dispatcher.utter_message(text="O processo XXXXXX/XXXX possui as seguintes Decisões/Acórdãos:")
        except:
            dispatcher.utter_message(
                text="Erro")

        return []


class ActionContatoSetorAtual(Action):
    def name(self) -> Text:
        return "action_contato_setor_atual"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            dispatcher.utter_message(text="O processo encontra-se no setor XXXXXXXXX. As informações de contato deste setor são:")
        except:
            dispatcher.utter_message(
                text="Erro")

        return []


class ActionContatoGabineteRelator(Action):
    def name(self) -> Text:
        return "action_contato_gabinete_relator"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            dispatcher.utter_message(text="As informações de contato do gabinete do Relator Xxxxxxx Xxxxxx são:")
        except:
            dispatcher.utter_message(
                text="Erro")

        return []