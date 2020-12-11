import pandas as pd

class DBCarregador():
    def __init__(self):
        #self.df_processos = pd.read_csv("teste.csv", sep=",", encoding="latin9")
        self.df_processos = pd.read_csv("data/processos_eventos.csv", sep=";", encoding="utf-8")
        #self.df_contatos_setor = pd.read_csv("data/contatos_setor.csv", sep=";")

    def get_processo(self, numero, ano):
        print(numero)
        print(ano)
        processo = self.df_processos[(self.df_processos['numero_processo'] == int(
            numero)) & (self.df_processos['ano_processo'] == int(ano))]

        ret_numero = processo['numero_processo'].values[0]
        ret_ano = processo['ano_processo'].values[0]
        ret_assunto = processo['assunto'].values[0]
        ret_relator = processo['relator'].values[0]
        ret_maior_evento = max(processo['evento'].values)
        ret_ultimo_evento = processo['resumo'].values[-1:]
        ret_ultimo_setor = processo['setor'].values[-1:]
        ret_contato_setor = processo['ContatoSetor'].values[-1:]
        ret_contato_relator = processo['ContatoRelator'].values[-1:]
        ret_identificador_setor = processo['IdentificadorSetor'].values[-1:]
        
        return ret_numero, ret_ano, ret_assunto, ret_relator, ret_maior_evento, ret_ultimo_evento, ret_ultimo_setor, ret_contato_setor, ret_contato_relator, ret_identificador_setor

    def get_informacao(self, numero, ano):
        pass

    def get_contato_setor(self, id_setor):
        pass
