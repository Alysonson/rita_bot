import pandas as pd

class DBCarregador():
    def __init__(self):
        self.df_processos = pd.read_csv("teste.csv", sep=",", encoding="latin9")
        #self.df_informacoes = pd.read_csv("data/informacoes.csv", sep=";")
        #self.df_contatos_setor = pd.read_csv("data/contatos_setor.csv", sep=";")

    def get_processo(self, numero, ano):
        processo = self.df_processos[(self.df_processos['NumeroProcesso'] == int(
            numero)) & (self.df_processos['AnoProcesso'] == int(ano))]

        ret_numero = processo['NumeroProcesso'].values[0]
        ret_ano = processo['AnoProcesso'].values[0]
        ret_assunto = processo['Assunto'].values[0]

        return ret_numero, ret_ano, ret_assunto

    def get_informacao(self, numero, ano):
        pass

    def get_contato_setor(self, id_setor):
        pass
