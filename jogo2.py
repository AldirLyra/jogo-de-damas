#%%
from enum import Flag,auto,Enum
# import enum
from abc import ABC, abstractmethod
import rotate_matrix 

class Peca(Flag):
	ESPAÇO_VAZIO = 0
	BRANCA = 1
	PRETA = 2
	DAMA = 4
	FORA_MOVIMAENTACAO = 8 
	DAMA_BRANCA = BRANCA|DAMA 
	DAMA_PRETA = PRETA|DAMA 
class Status(Enum):
	JOGANDO = 0
	BRANCA_VENCERAN = 1
	PRETAS_VENCERAN = 2
	EMPATE = 3
class Player(ABC):
	def __init__(self,taboleiro,peca):
		self.taboleiro = taboleiro
		self.peca = peca
	def jogar(self,TABOLEIRO,Pecas):
		pass
# class Humano(Player):
#     def jogar(self,TABOLEIRO):
#         pass
# class RedeNeural(Player):
#     def jogar(self,TABOLEIRO):
#         pass
class MiniMax(Player):
	def jogar(self):
		taboleiro = Taboleiro()
		taboleiro.movimentosTaboleiro(self.peca)
	def simulacao():
		return -1

class Movimento():
	def __init__(self,posicaoInicial,posicaoFinal,posicaoCedulaPulada=None,isObrigatorio=False):
		self.posicaoInicial = posicaoInicial
		self.posicaoFinal = posicaoFinal
		self.posicaoCedulaPulada = posicaoCedulaPulada
		self.isObrigatorio = isObrigatorio
class Taboleiro:

	# Classe para tomar conta do status do jogo
	def __init__(self):
		self.status = Status.JOGANDO
		self.turno = 1
		self.jogadores = (Player(self,Peca.PRETA), Player(self,Peca.BRANCA))
		
		self.matrizTaboleiro = [
								[Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO],
								[Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA],
				  				[Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO],
								[Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO],
								[Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO],
								[Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA],
								[Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO],
								[Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA]
								]
		self.sentidoTaboleiro = Peca.BRANCA

	# RETORNA OS MOVIMENTOS OBRIGATÓRIOS DE UMA PEÇA QUE PODE SER JOGADA EM DETERMINADO TURNO
	# rotacionando tabuleiro 
	def rotacionarTabuleiro(self,sentidoTaboleiro):
		if self.sentidoTaboleiro == sentidoTaboleiro:
			self.matrizTaboleiro = rotate_matrix.clockwise(rotate_matrix.clockwise(self.matrizTaboleiro))
			self.sentidoTaboleiro = self.sentidoTaboleiro == Peca.BRANCA if Peca.PRETA else Peca.BRANCA
	
	def jogadorTurno(self):
		return self.jogadores[self.turno % 2]
	
	# RETORNA TODOS OS MOVIMENTOS OBRIGATÓRIOS DE UM TURNO
	def movimentosTaboleiro(self):
		return self.movimentosTaboleiro(self.jogadorTurno())
	def movimentosTaboleiro(self,peca):
		retorno = []
		for i in range(self.matrizTaboleiro.__len__()-1):
			for e in range(self.matrizTaboleiro[0].__len__()-1):
				aux = self.movimentoObrigatorioCelula((i,e),peca)
				if aux != None:
					retorno.append(aux)
		return retorno
	# RETORNA TODOS OS MOVIMENTOS OBRIGATÓRIOS DE UMa celula
	def movimentoCelula(self, localizacao_cedula,peca):
		movimentos =[]
		linha,coluna = localizacao_cedula
		

		self.rotacionarTabuleiro(peca)
		array = [Peca.ESPAÇO_VAZIO,peca]
		# logica para quando a posicao selecionada e uma peça do jogador e nao e uma dama 
		if self.matrizTaboleiro[linha][coluna] == peca and self.matrizTaboleiro[linha][coluna] != Peca.DAMA:
				if linha > 0:
					if coluna < self.matrizTaboleiro[0].__len__():
						if self.matrizTaboleiro[linha - 1][coluna + 1] not in array :
							linhaPulada = linha - 1
							colunaPulada = coluna + 1

							if linhaPulada - 1 >= 0 and colunaPulada + 1 <= self.matrizTaboleiro[0].__len__():
								if self.matrizTaboleiro[linhaPulada - 1][colunaPulada + 1] == Peca.ESPAÇO_VAZIO:
									movimento = Movimento(
										posicaoInicial = [linha,coluna],
										posicaoFinal = [linhaPulada - 1, colunaPulada + 1],
										posicaoCedulaPulada = [linhaPulada, colunaPulada],
										isObrigatorio = True
										)
									movimentos.append(movimento)
						elif self.matrizTaboleiro[linha - 1][coluna + 1] == Peca.ESPAÇO_VAZIO:
							movimento = Movimento(
								posicaoInicial = [linha,coluna],
								posicaoFinal = [linha - 1,coluna + 1],
								posicaoCedulaPulada = None,
								isObrigatorio = False
							)
							movimentos.append(movimento)
					if coluna > 0:
						if self.matrizTaboleiro[linha - 1][coluna - 1] not in array:
							linhaPulada = linha - 1
							colunaPulada = coluna - 1

							if linhaPulada - 1 >= 0 and colunaPulada - 1 >= 0:
								if self.matrizTaboleiro[linhaPulada - 1][colunaPulada - 1] == Peca.ESPAÇO_VAZIO:
									movimento = Movimento(
										posicaoInicial = [linha,coluna],
										posicaoFinal = [linhaPulada - 1, colunaPulada - 1],
										posicaoCedulaPulada = [linhaPulada, colunaPulada],
										isObrigatorio = False
									)
									movimentos.append(movimento)
						elif self.matrizTaboleiro[linha - 1][coluna - 1] == Peca.ESPAÇO_VAZIO:
							movimento = Movimento(
								posicaoInicial = [linha,coluna],
								posicaoFinal = [linha - 1,coluna - 1],
								posicaoCedulaPulada = None,
								isObrigatorio = False
							)
							movimentos.append(movimento)
		if movimentos != []:
			return movimentos
		else:
			return None

	# RETORNA SE EXISTE UM MOVIMENTO POSSIVEL A SE FAZER COM A PEÇA
	def existeMovimentoPossivel(self,peca):
		if self.movimentosTaboleiro(peca).__len__() == 0 :
			return False
		else:
			return True
	# def execultarMovimento(self,movimento):

	# 
	def ImprimirTaboleiro(self):
		tabstr = ""
		for i in self.matrizTaboleiro:
			for e in i:
				if e == Peca.BRANCA :
					tabstr += "|◎|"
				elif e == Peca.PRETA :
					tabstr += "|◉|"
				elif e == Peca.ESPAÇO_VAZIO:
					tabstr += "| |"
			tabstr += "\n"
		return tabstr

	# PRÓXIMO TURNO
	def proximoTurno(self):
		self.turno += 1

	# VERIFICA O VENCEDOR
	def verificaVencedor(self):

		PecasPreta = sum([contador.count(Peca.PRETA) for contador in self.matrizTaboleiro])
		pecasBrancas = sum([contador.count(Peca.BRANCA) for contador in self.matrizTaboleiro])

		if PecasPreta == 0:
			return Status.BRANCA_VENCERAN
		if pecasBrancas == 0:
			return Status.PRETAS_VENCERAN
		if self.existeMovimentoPossivel(Peca.BRANCA) and not self.existeMovimentoPossivel(Peca.BRANCA):
			return Status.BRANCA_VENCERAN
		if not self.existeMovimentoPossivel(Peca.BRANCA) and  self.existeMovimentoPossivel(Peca.BRANCA):
			return Status.PRETAS_VENCERAN
		if not self.existeMovimentoPossivel(Peca.BRANCA) and not self.existeMovimentoPossivel(Peca.BRANCA):
			return Status.EMPATE
		if PecasPreta == 1 and pecasBrancas == 1:
			return Status.EMPATE
		return Status.JOGANDO

#%%
tab = Taboleiro()
#%%
print(tab.ImprimirTaboleiro())

