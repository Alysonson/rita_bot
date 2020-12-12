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
        ret_ultimo_evento = processo['resumo'].values[-1]
        ret_ultimo_setor = processo['setor'].values[-1]
        ret_ultimo_arquivo = processo['NomeArquivo'].values[-1]
        ret_contato_setor = processo['ContatoSetor'].values[-1]
        ret_contato_relator = processo['ContatoRelator'].values[-1]
        ret_identificador_setor = processo['IdentificadorSetor'].values[-1]
        
        return ret_numero, ret_ano, ret_assunto, ret_relator, ret_maior_evento, ret_ultimo_evento, ret_ultimo_setor, ret_ultimo_arquivo, ret_contato_setor, ret_contato_relator, ret_identificador_setor

    def get_informacoes_corpo_tecnico(self, numero, ano):
        return self.get_informacoes(numero, ano, 'UT')

    def get_informacao_corpo_tecnico(self, numero, ano, evento):
        return self.get_informacao(numero, ano, evento, 'UT')

    def get_informacoes_mp(self, numero, ano):
        return self.get_informacoes(numero, ano, 'MP')

    def get_informacao_mp(self, numero, ano, evento):
        return self.get_informacao(numero, ano, evento, 'MP')

    def get_informacoes(self, numero, ano, tipo):
        informacoes = self.df_processos[(self.df_processos['numero_processo'] == int(
            numero)) & (self.df_processos['ano_processo'] == int(ano)) & (self.df_processos['IdentificadorSetor'] == tipo)][['resumo','setor','evento']]
        return informacoes

    def get_informacao(self, numero, ano, evento, tipo):
        arquivo = self.df_processos[(self.df_processos['numero_processo'] == int(
            numero)) & (self.df_processos['ano_processo'] == int(ano)) 
            & (self.df_processos['IdentificadorSetor'] == tipo)
            & (self.df_processos['evento'] == int(evento))].iloc[0]['NomeArquivo']
        return arquivo


    def get_decisoes(self, numero, ano):
        decisoes = self.df_processos[(self.df_processos['numero_processo'] == int(
            numero)) & (self.df_processos['ano_processo'] == int(ano)) & (self.df_processos['Decisao'] == 'S')][['resumo','setor','evento']]
        return decisoes

    def get_decisao(self, numero, ano, evento):
        arquivo = self.df_processos[(self.df_processos['numero_processo'] == int(
            numero)) & (self.df_processos['ano_processo'] == int(ano)) 
            & (self.df_processos['Decisao'] == 'S')
            & (self.df_processos['evento'] == int(evento))].iloc[0]['NomeArquivo']
        return arquivo
