import re
import sys

class UH(object):
    def __init__(self, rmw):
        self.rmw = rmw
        self.w = ""
        self.fita = {}
        self.head = {}
        self.alfabeto_fita = []
        self.estados = []
        self.numero_transicoes = 0
        self.transicao_anterior = None


        self.flag_max = False

        for i in range(1, 5):
            self.fita.update({i: []})
            self.head.update({i: 0})

        self.escreveNaFita(1, rmw, "1", cabecaInicio=True)

        formaRegex = r"(000((1+)0(1+)0(1+)0(1+)0(1+)00)*((1+)0(1+)0(1+)0(1+)0(1+))000((1+)0)*(1+)000)"
        if not re.match(formaRegex, self.rmw):
            exit()
            # TODO imprimir fitas
        else:
            self.w = self.rmw.split("000")[2]

            trans = self.rmw.split("000")[1]
            trans = trans.split("00")
            for t in trans:
                args = t.split("0")

                q0 = (args[0])
                if q0 not in self.estados:
                    self.estados.append(q0)

                x = int(args[1])
                if x not in self.alfabeto_fita:
                    self.alfabeto_fita.append(x)

                y = int(args[3])
                if y not in self.alfabeto_fita:
                    self.alfabeto_fita.append(y)

            self.escreveNaFita(3, self.w, cabecaInicio=True)  # Escreve a palavra w na fita 3
            self.escreveNaFita(2, "1", cabecaInicio=True)  # Estado inicial q0

    '''
    ------------------------------------------------------------------------------------------------------------------
    MÉTODO PARA ESCREVER UMA STRING EM UMA FITA
    ------------------------------------------------------------------------------------------------------------------
      | fita (int) -> número da fita
      | escrita (str) -> o que será escrito
      | direcao (str) -> "1" para direita ou "11" para esquerda
      | cabecaInicio (bool) -> True para a cabeça voltar ao inicio da fita após a escrita, False para manter onde parou
    ------------------------------------------------------------------------------------------------------------------
    '''  # DOCUMENTAÇÃO
    def escreveNaFita(self, fita, escrita, direcao="1", cabecaInicio=False):
        for e in escrita:
            e = int(e)
            if len(self.fita[fita]) >= 0 or self.head[fita] == len(self.fita[fita]):
                self.fita[fita].append(e)
            elif self.head[fita] < len(self.fita[fita]):
                self.fita[fita][self.head[fita]] = e

            if direcao == "1":
                self.head[fita] += 1
            elif direcao == "11":
                self.head[fita] -= 1

        if cabecaInicio:
            self.moverCabecaParaInicio(fita)

    '''
    ------------------------------------------------------------------------------------------------------------------
     MÉTODO PARA MOVER PARA O INICIO A CABEÇA DE L/E DE UMA DETERMINADA FITA
    ------------------------------------------------------------------------------------------------------------------
      | fita (int) -> número da fita
    ------------------------------------------------------------------------------------------------------------------
    '''  # DOCUMENTAÇÃO
    def moverCabecaParaInicio(self, fita):
        self.head[fita] = 0

    '''
    ------------------------------------------------------------------------------------------------------------------
    MÉTODO PARA APAGAR CONTEÚDO DE UMA FITA
    ------------------------------------------------------------------------------------------------------------------
      | fita (int) -> número da fita
    ------------------------------------------------------------------------------------------------------------------
    '''  # DOCUMENTAÇÃO
    def apagarFita(self, fita):
        self.fita[fita] = []
        self.head[fita] = 0


    '''
    ------------------------------------------------------------------------------------------------------------------
    MÉTODO PARA OBTER O SÍMBOLO QUE A MÁQUINA SIMULADA ESTÁ LENDO NO MOMENTO
    ------------------------------------------------------------------------------------------------------------------
    '''  # DOCUMENTAÇÃO
    def simboloAtual(self):
        pos = self.head[3]
        fim = False
        simbolo = ""
        while pos < len(self.fita[3]) and not fim:
            if self.fita[3][pos] == 1:
                simbolo += "1"
            else:
                fim = True

            pos += 1

        return simbolo

    '''
    ------------------------------------------------------------------------------------------------------------------
    MÉTODO PARA OBTER O ESTADO ATUAL QUE A MÁQUINA SIMULADA ESTÁ
    ------------------------------------------------------------------------------------------------------------------
    '''  # DOCUMENTAÇÃO
    def estadoAtual(self):
        estado = ""
        for i in self.fita[2]:
            estado += str(i)

        return estado

    '''
    ------------------------------------------------------------------------------------------------------------------
    MÉTODO RECURSIVO PARA SIMULAR A EXECUÇÃO DA MÁQUINA
    ------------------------------------------------------------------------------------------------------------------
    '''  # DOCUMENTAÇÃO
    def executaMaquinaSimulada(self):
        trans = self.rmw.split("000")[1]
        trans = "000"+trans+"000"

        pos = trans.find(f'00{self.estadoAtual()}0{self.simboloAtual()}0')

        if pos != -1:

            self.numero_transicoes += 1

            if not self.flag_max and ((len(self.estados)* (len(self.alfabeto_fita) ** (len(self.w) - 3)) * (len(self.w) - 3)) < self.numero_transicoes):
                self.numero_transicoes = 0
                self.flag_max = True
                print ("Caso essa MT seja um ALL, ela está em loop.")
            elif self.flag_max:
                print ("Loop.")
                exit();


            pos += 2
            self.head[1] = pos

            argumento = 0  # 0: estado atual, 1: simbolo atual, 2: novo estado, 3: novo simbolo, 4: direcao
            novoEstado = ""
            novoSimbolo = ""
            direcao = ""
            while pos < len(self.fita[1]) and argumento < 5:
                if self.fita[1][pos] == 1:
                    if argumento == 2:
                        novoEstado += "1"
                    elif argumento == 3:
                        novoSimbolo += "1"
                    elif argumento == 4:
                        direcao += "1"
                else:
                    argumento += 1
                pos += 1

            if self.flag_max and ((self.estadoAtual(), self.simboloAtual(), novoEstado, novoSimbolo, direcao) == self.transicao_anterior):
                self.numero_transicoes += 1
            elif self.flag_max:
                self.numero_transicoes = 0


            self.transicao_anterior = (self.estadoAtual(), self.simboloAtual(), novoEstado, novoSimbolo, direcao)
            print (self.fita[3])
            self.executaTransicao(novoEstado, novoSimbolo, direcao)
            self.executaMaquinaSimulada()

    '''
    ------------------------------------------------------------------------------------------------------------------
    MÉTODO PARA EXECUTAR UMA TRANSICAO NA MÁQUINA SIMULADA
    ------------------------------------------------------------------------------------------------------------------
      | novoEstado (str) -> estado atingido após a transição
      | novoSimbolo (str) -> simbolo a ser escrito na fita após a transição
      | direcao (str) -> "1" para movimentar a direita, "11" para a esquerda
    ------------------------------------------------------------------------------------------------------------------
    '''  # DOCUMENTAÇÃO
    def executaTransicao(self, novoEstado, novoSimbolo, direcao):
        # <INICIO> Altera o estado atual
        self.apagarFita(2)
        self.escreveNaFita(2, novoEstado, cabecaInicio=True)

        # <INICIO> Substitui o simbolo
        pos = self.head[3]

        while pos < len(self.fita[3]) and self.fita[3][pos] == 1:
            self.fita[3].pop(pos)

        if pos == len(self.fita[3]):
            self.fita[3].append(0)
            self.fita[3].append(1)
            self.fita[3].append(1)
            self.fita[3].append(1)

        for e in novoSimbolo:
            self.fita[3].insert(pos, int(e))

        # <INICIO> Move cabeça de R/W da fita 3
        if direcao == "1":
            while pos < len(self.fita[3]) and self.fita[3][pos] == 1:
                pos += 1

            if pos == len(self.fita[3]):
                self.fita[3].append(0)
                self.fita[3].append(1)
                self.fita[3].append(1)
                self.fita[3].append(1)

            pos += 1  # Para sair do simbolo 0

        elif direcao == "11":
            if pos >= 2:
                pos -= 2  # Volta para o ultimo 1 do símbolo anterior

            while self.fita[3][pos] == 1 and pos > 0:
                pos -= 1

            if pos > 0:
                pos += 1  # Para sair do simbolo 0

        self.head[3] = pos

    '''
    ------------------------------------------------------------------------------------------------------------------
    MÉTODO RETORNAR VARIÁVEIS COMPOSTAS CONVERTIDAS EM CADEIA DE CARACTERES
    ------------------------------------------------------------------------------------------------------------------
      | item (tuple, list, dict) -> item a ser convertidos
    ------------------------------------------------------------------------------------------------------------------
    '''  # DOCUMENTAÇÃO
    def stringify(self, item):
            r = ""
            if (type(item) is list) or (type(item) is tuple):
                for x in item:
                    r += str(x)
            elif type(item) is dict:
                for k in item.keys():
                    r += str(item[k])

            return r




if sys.argv[1] != None:
    arquivo = open(sys.argv[1], "r")
    aux = arquivo.readline();
    rmw = aux.split("\n")[0]

    mtu = UH(rmw)
    mtu.executaMaquinaSimulada()
