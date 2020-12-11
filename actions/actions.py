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

import re

import pandas as pd

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .database import DBCarregador


db = DBCarregador()
dados_usuarios = {}
ano = ""
numero = ""

class ActionLocalizarProcesso(Action):
    def name(self) -> Text:
        return "action_localizar_processo"

    def separar_numero_ano(self, id_processo):
        numero, ano = re.search(r"(\d+)[^0-9]+(\d+)",id_processo).groups()
        return numero, ano

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        processo_id = tracker.latest_message['text']
        print(processo_id)

        self.numero, self.ano = self.separar_numero_ano(processo_id)
        print(self.numero)
        
        if self.numero and self.ano:
            dados_usuarios[tracker.sender_id] = {"numero_processo":self.numero, "ano_processo":self.ano}
            try:
                ret_numero, ret_ano, ret_assunto, ret_relator, ret_maior_evento, ret_ultimo_evento, ret_ultimo_setor, ret_contato_setor, ret_contato_relator, ret_identificador_setor = db.get_processo(self.numero, self.ano)

                dados_usuarios[tracker.sender_id]['assunto'] = ret_assunto
                dados_usuarios[tracker.sender_id]['relator'] = ret_relator
                dados_usuarios[tracker.sender_id]['maior_evento'] = ret_maior_evento
                dados_usuarios[tracker.sender_id]['ultimo_evento'] = ret_ultimo_evento
                dados_usuarios[tracker.sender_id]['ultimo_setor'] = ret_ultimo_setor
                dados_usuarios[tracker.sender_id]['contato_setor'] = ret_contato_setor
                dados_usuarios[tracker.sender_id]['contato_relator'] = ret_contato_relator
                dados_usuarios[tracker.sender_id]['identificador_setor'] = ret_identificador_setor

                dispatcher.utter_message(text="O processo de número {}, ano {}, assunto {}, encontra-se atualmente no Gabinete do(a) Conselheiro(a) {}. Seu último evento é o de número {}. Sua última informação é: {}. O setor atual é {}, contato {}. ".format(
                    ret_numero, ret_ano, ret_assunto, ret_relator, ret_maior_evento, ret_ultimo_evento, ret_ultimo_setor, ret_contato_setor))
                #dispatcher.utter_template('utter_quais_opcoes', tracker)
            except:
                dispatcher.utter_message(
                    text="Não encontrei o seu processo, procurei pelo processo ({}) {}/{}. Por favor, informe um processo existente.".format(processo_id, numero, ano))
        else:
            dispatcher.utter_message(text="Não encontrei processo com os termos selecionados.")
        return []


class ActionUltimaInformacao(Action):
    def name(self) -> Text:
        return "action_ultima_informacao"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #dispatcher.utter_message(text='Ultima informacao é {}'.format(dados_usuarios[tracker.sender_id]['ultimo_evento']))

        try:
            dispatcher.utter_message(text="A última peça juntada ao processo XXXXXX/XXXX foi publicada no dia XX/XX/XXXX pelo setor XXX (Evento 9). Para visualizar a peça processual acesse o link www.tce.rn.gov.br/processo/xxxxx.pdf")
        except:
            dispatcher.utter_message(
                text="Erro")
            print("Aqui erro")

        return []


class ActionInformacoesCorpoTecnico(Action):
    def name(self) -> Text:
        return "action_informacoes_corpo_tecnico"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        informacoes = db.get_informacoes_corpo_tecnico(dados_usuarios[tracker.sender_id]['numero_processo'], dados_usuarios[tracker.sender_id]['ano_processo'])
        print(informacoes)

        if len(informacoes):
            texto_resposta = "Os eventos encontrados são os seguintes:\n\n"
            for _,r in informacoes.iterrows():
                texto_resposta += "Evento {} - {}\n\n".format(r['evento'], r['resumo'])
            try:
                dispatcher.utter_message(text=texto_resposta)
                dispatcher.utter_message(template="utter_opcoes_eventos")
            except:
                dispatcher.utter_message(text="Erro")
        else:
            dispatcher.utter_message(template="utter_nenhum_evento")

        return []

class ActionInformacaoCorpoTecnico(Action):
    def name(self) -> Text:
        return "action_informacao_corpo_tecnico"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        evento = tracker.latest_message['text']
        arquivo = db.get_informacao_corpo_tecnico(dados_usuarios[tracker.sender_id]['numero_processo'], dados_usuarios[tracker.sender_id]['ano_processo'], evento)

        try:
            dispatcher.utter_message(text="Encontrei o arquivo {}".format(arquivo))
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