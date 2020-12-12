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
                ret_numero, ret_ano, ret_assunto, ret_relator, ret_maior_evento, ret_ultimo_evento, ret_ultimo_setor, ret_ultimo_arquivo, ret_contato_setor, ret_contato_relator, ret_identificador_setor = db.get_processo(self.numero, self.ano)

                dados_usuarios[tracker.sender_id]['assunto'] = ret_assunto
                dados_usuarios[tracker.sender_id]['relator'] = ret_relator
                dados_usuarios[tracker.sender_id]['maior_evento'] = ret_maior_evento
                dados_usuarios[tracker.sender_id]['ultimo_evento'] = ret_ultimo_evento
                dados_usuarios[tracker.sender_id]['ultimo_setor'] = ret_ultimo_setor
                dados_usuarios[tracker.sender_id]['ultimo_arquivo'] = ret_ultimo_arquivo
                dados_usuarios[tracker.sender_id]['contato_setor'] = ret_contato_setor
                dados_usuarios[tracker.sender_id]['contato_relator'] = ret_contato_relator
                dados_usuarios[tracker.sender_id]['identificador_setor'] = ret_identificador_setor

                dispatcher.utter_message(text="O processo de número {}, ano {}, assunto {}, encontra-se atualmente no Gabinete do(a) Conselheiro(a) {}. Seu último evento é o de número {}. Sua última informação é: {}. O setor atual é {}, contato {}. ".format(
                    ret_numero, ret_ano, ret_assunto, ret_relator, ret_maior_evento, ret_ultimo_evento, ret_ultimo_setor, ret_contato_setor))
                dispatcher.utter_message(template='utter_quais_opcoes')
                #dispatcher.utter_template('utter_quais_opcoes', tracker)
            except:
                dispatcher.utter_message(text="Não encontrei o seu processo, procurei pelo processo ({}).".format(processo_id))
                dispatcher.utter_message(template='utter_numero_processo')
        else:
            dispatcher.utter_message(text="Não encontrei processo com os termos selecionados.")
        return []


class ActionUltimaInformacao(Action):
    def name(self) -> Text:
        return "action_ultima_informacao"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            link_arquivo = "http://localhost/{}".format(dados_usuarios[tracker.sender_id]['ultimo_arquivo'])
        
            dispatcher.utter_message(text="A última peça juntada ao processo {}/{} foi {} pelo setor {}.".format(
                dados_usuarios[tracker.sender_id]['numero_processo'],
                dados_usuarios[tracker.sender_id]['ano_processo'],
                dados_usuarios[tracker.sender_id]['ultimo_evento'],
            dados_usuarios[tracker.sender_id]['ultimo_setor']))
            dispatcher.utter_message(text="Encontrei o arquivo {}".format(link_arquivo))
        except:
            dispatcher.utter_message(text="Erro")
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
            dispatcher.utter_message(template="utter_numero_processo")

        return []

class ActionInformacaoCorpoTecnico(Action):
    def name(self) -> Text:
        return "action_informacao_corpo_tecnico"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        evento = tracker.latest_message['text']
        arquivo = db.get_informacao_corpo_tecnico(dados_usuarios[tracker.sender_id]['numero_processo'], dados_usuarios[tracker.sender_id]['ano_processo'], evento)
        link_arquivo = "http://localhost/{}".format(arquivo)

        try:
            dispatcher.utter_message(text="Encontrei o arquivo {}".format(link_arquivo))
            dispatcher.utter_message(template="utter_numero_processo")
        except:
            dispatcher.utter_message(
                text="Erro")
            dispatcher.utter_message(template="utter_numero_processo")

        return []

class ActionInformacoesMP(Action):
    def name(self) -> Text:
        return "action_informacoes_mp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        informacoes = db.get_informacoes_mp(dados_usuarios[tracker.sender_id]['numero_processo'], dados_usuarios[tracker.sender_id]['ano_processo'])
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
            dispatcher.utter_message(template="utter_numero_processo")

        return []

class ActionInformacaoMP(Action):
    def name(self) -> Text:
        return "action_informacao_mp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        evento = tracker.latest_message['text']
        arquivo = db.get_informacao_mp(dados_usuarios[tracker.sender_id]['numero_processo'], dados_usuarios[tracker.sender_id]['ano_processo'], evento)
        link_arquivo = "http://localhost/{}".format(arquivo)

        try:
            dispatcher.utter_message(text="Encontrei o arquivo {}".format(link_arquivo))
            dispatcher.utter_message(template="utter_numero_processo")
        except:
            dispatcher.utter_message(text="Erro")
            dispatcher.utter_message(template="utter_numero_processo")

        return []



class ActionDecisoes(Action):
    def name(self) -> Text:
        return "action_decisoes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        decisoes = db.get_decisoes(dados_usuarios[tracker.sender_id]['numero_processo'], dados_usuarios[tracker.sender_id]['ano_processo'])

        if len(decisoes):
            texto_resposta = "As decisões encontrados são os seguintes:\n\n"
            for _,r in decisoes.iterrows():
                texto_resposta += "Decisão {} - {}\n\n".format(r['evento'], r['resumo'])
            try:
                dispatcher.utter_message(text=texto_resposta)
                dispatcher.utter_message(template="utter_opcoes_eventos")
            except:
                dispatcher.utter_message(text="Erro")
        else:
            dispatcher.utter_message(template="utter_nenhum_evento")
            dispatcher.utter_message(template="utter_numero_processo")
            

        return []


class ActionDecisao(Action):
    def name(self) -> Text:
        return "action_decisao"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        evento = tracker.latest_message['text']
        arquivo = db.get_decisao(dados_usuarios[tracker.sender_id]['numero_processo'], dados_usuarios[tracker.sender_id]['ano_processo'], evento)
        link_arquivo = "http://localhost/{}".format(arquivo)

        try:
            dispatcher.utter_message(text="Encontrei o arquivo {}".format(link_arquivo))
            dispatcher.utter_message(template="utter_numero_processo")
        except:
            dispatcher.utter_message(text="Erro")
            dispatcher.utter_message(template="utter_numero_processo")

        return []
 

class ActionContatoSetorAtual(Action):
    def name(self) -> Text:
        return "action_contato_setor_atual"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            dispatcher.utter_message(text="O contato do setor onde o processo se encontra é: {}".format(dados_usuarios[tracker.sender_id]['contato_setor']))
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
            dispatcher.utter_message(text="O contato do gabinete do Relator é: {}".format(dados_usuarios[tracker.sender_id]['contato_relator']))
        except:
            dispatcher.utter_message(text="Erro")

        return []