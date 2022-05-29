class JogoDaVelha():

    def __init__(self, partidaID, jogador1 = None, jogador2 = None):
        self.casa1 = ''
        self.casa2 = ''
        self.casa3 = ''
        self.casa4 = ''
        self.casa5 = ''
        self.casa6 = ''
        self.casa7 = ''
        self.casa8 = ''
        self.casa9 = ''
        self.qtdjogada = 0
        self.jogador1 = jogador1
        self.jogador2 = jogador2
        self.Pecajogador1 = 'x'
        self.Pecajogador2 = 'o'
        self.vez = 'x'
        self.partidaID = partidaID
        self.pontosjogador1 = 0
        self.pontosjogador2 = 0

    def resetaTabuleiro(self):
        self.casa1 = ''
        self.casa2 = ''
        self.casa3 = ''
        self.casa4 = ''
        self.casa5 = ''
        self.casa6 = ''
        self.casa7 = ''
        self.casa8 = ''
        self.casa9 = ''
        self.qtdjogada = 0
        self.vez = 'x'

    def verificarTabuleiro(self):
      # Verificações das 3 verticais
        if self.casa7 == self.casa4 == self.casa1 != '':
          return self.casa7
        elif self.casa8 == self.casa5 == self.casa2 != '':
            return self.casa8
        elif self.casa9 == self.casa6 == self.casa3 != '':
            return self.casa9


        # Verificações das 3 horizontais
        elif self.casa7 == self.casa8 == self.casa9 != '':
            return self.casa7
        elif self.casa4 == self.casa5 == self.casa6 != '':
            return self.casa8
        elif self.casa1 == self.casa2 == self.casa3 != '':
            return self.casa1

        # Verificações das 2 diagonais
        elif self.casa7 == self.casa5 == self.casa3 != '':
            return self.casa7
        elif self.casa1 == self.casa5 == self.casa9 != '':
            return self.casa1

        # Verificando empate
        if self.qtdjogada == 9:
            return "empate"
        else:
            return "continua"

