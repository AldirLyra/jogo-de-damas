
#realizando inports nessesarios
#%% 
from enum import Flag,auto,Enum
from copy import copy
# import enum
from abc import ABC, abstractmethod
from IPython.display import display
import rotate_matrix 
from infixpy import Seq
#%%

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
class Player():
	def __init__(self,taboleiro,peca):
		self.taboleiro = taboleiro
		self.peca = peca
	
class Humano(Player):
	# overriding abstract method
	def jogar(self):
		self.efetuarJogada()
	
	def efetuarJogada(self):
		movimentos = Movimento.filtraPorObrigatorio(movimentos)
		
		print("escolha algum dos seguintes movimentos :\n")
		for i in range(movimentos.__len__()):
			movimento = movimentos[i]
			print("======="+str(i)+"=======")
			print(movimento.imprimir())
		indice = int(input("digite o indice do movimento:"))
		movimentos[indice].moverPeca(self.taboleiro,self.peca)		
	
# class RedeNeural(Player):
#     def jogar(self,TABOLEIRO):
#         pass
class MiniMax(Player):
	def jogar(self):
		# taboleiro = Taboleiro()
		_,movimento = MiniMax.simulacao(self.taboleiro,self.peca,self.peca)
		movimento.moverPeca(self.taboleiro,self.peca)
	def simulacao(taboleiro,pecaTurno,peca):
		#taboleiro = Taboleiro()
		taboleiro.verificaVencedor()
		if taboleiro.status == Status.BRANCA_VENCERAN :
			if peca == Peca.BRANCA:
				return 30
			else:
				return -15
		elif taboleiro.status == Status.PRETAS_VENCERAN :
			if peca == Peca.BRANCA:
				return -15
			else:
				return 30
		elif taboleiro.status == Status.EMPATE:
			return 0 
		
		pontuacao = 0
		maiorPt = 0 
		melhorMov = None
		movimentos = movimentos = Movimento.filtraPorObrigatorio(taboleiro.movimentosTaboleiro(pecaTurno))
		for movimento in movimentos:
			taboleiroSimu = copy(taboleiro)
			movimento.moverPeca(taboleiroSimu,pecaTurno)
			if movimento.isObrigatorio:
				pontuacao +=10	
			
			pecaTurno = Peca.PRETA if pecaTurno == Peca.BRANCA else Peca.BRANCA
			pontuacaoMov,_ = MiniMax.simulacao(taboleiroSimu,pecaTurno,peca)
			if pontuacaoMov > maiorPt:
				melhorMov = movimento
			elif maiorPt == 0:
				melhorMov = movimento

			pontuacao += pontuacaoMov
			if pontuacao >= 40:
				return pontuacao, melhorMov	
			# break
		return pontuacao, melhorMov	
#%%	
class Movimento():
	def __init__(self,posicaoInicial,posicaoFinal,posicaoCedulaPulada=None,isObrigatorio=False):
		self.posicaoInicial = posicaoInicial
		self.posicaoFinal = posicaoFinal
		self.posicaoCedulaPulada = posicaoCedulaPulada
		self.isObrigatorio = isObrigatorio
	def imprimir(self):
		movimentostr = "\n"
		movimentostr += "posicaoInicial:"+ str(self.posicaoInicial) +"\n"
		movimentostr += "posicaoCedulaPulada:"+ str(self.posicaoCedulaPulada )+"\n"
		movimentostr += "posicaoFinal:"+ str(self.posicaoFinal) +"\n"
		return movimentostr
	def moverPeca(self,taboleiro, peca):

		lilhaI,colunaI = self.posicaoInicial
		taboleiro.rotacionarTabuleiro(peca)
		taboleiro.matrizTaboleiro[lilhaI][colunaI] = Peca.ESPAÇO_VAZIO
		if self.posicaoCedulaPulada != None:
			lilhaP,colunaP = self.posicaoCedulaPulada
			taboleiro.matrizTaboleiro[lilhaP][colunaP] = Peca.ESPAÇO_VAZIO
		lilhaF,colunaF = self.posicaoFinal
		taboleiro.matrizTaboleiro[lilhaF][colunaF] = peca

	def filtraPorObrigatorio(movimentos):
		movimentosObrigatorios = Seq(movimentos).filter(lambda x: x.isObrigatorio == True).tolist()
		if movimentosObrigatorios.__len__() != 0:
			return movimentosObrigatorios
		else :
			return movimentos
		
#%%	
class Taboleiro:

	# Classe para tomar conta do status do jogo
	def __init__(self):
		self.status = Status.JOGANDO
		self.turno = 1
		self.jogadores = [Player(self,Peca.PRETA), Player(self,Peca.BRANCA)]
		
		self.matrizTaboleiro = [
								[Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO],
								[Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA],
				  				[Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO,Peca.PRETA,Peca.ESPAÇO_VAZIO],
								[Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO],
								[Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO],
								[Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA],
								[Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO],
								[Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA,Peca.ESPAÇO_VAZIO,Peca.BRANCA]
								]
		self.sentidoTaboleiro = Peca.BRANCA
	def jogo(self):
		while True:
			jogador = self.jogadorTurno()
			print(jogador.__class__)
			print(jogador.peca.name)

			print(self.toString())
			jogador.jogar()
			self.proximoTurno()
			self.verificaVencedor()
			if self.status != Status.JOGANDO:
				return None
	# RETORNA OS MOVIMENTOS OBRIGATÓRIOS DE UMA PEÇA QUE PODE SER JOGADA EM DETERMINADO TURNO
	# rotacionando tabuleiro 
	def rotacionarTabuleiro(self,sentido):
		if self.sentidoTaboleiro != sentido:
			self.matrizTaboleiro = rotate_matrix.clockwise(rotate_matrix.clockwise(self.matrizTaboleiro))
			# self.sentidoTaboleiro = self.sentidoTaboleiro == Peca.BRANCA if Peca.PRETA else Peca.BRANCA
			self.sentidoTaboleiro = sentido
			for linha in range(self.matrizTaboleiro.__len__()):
				self.matrizTaboleiro[linha] =  list(self.matrizTaboleiro[linha])
	
	def jogadorTurno(self):
		return self.jogadores[self.turno % 2]
	
	# RETORNA TODOS OS MOVIMENTOS OBRIGATÓRIOS DE UM TURNO
	def movimentosTaboleiro2(self):
		return self.movimentosTaboleiro(self.jogadorTurno().peca)
	
	def movimentosTaboleiro(self,peca):
		retorno = []
		for i in range(self.matrizTaboleiro.__len__()-1):
			for e in range(self.matrizTaboleiro[0].__len__()-1):
				if i+e % 2 == 1:
					aux = self.movimentoCelula((i,e),peca)
					if aux != None:
						retorno.extend(aux)
		return retorno
	# RETORNA TODOS OS MOVIMENTOS OBRIGATÓRIOS DE UMa celula
	def movimentoCelula(self, localizacao_cedula,peca):
		movimentos =[]
		linha,coluna = localizacao_cedula
		

		self.rotacionarTabuleiro(peca)
		array = [Peca.ESPAÇO_VAZIO,peca]
		# logica para quando a posicao selecionada e uma peça do jogador e nao e uma dama 
		if self.matrizTaboleiro[linha][coluna] == peca :
				if linha > 0:
					if coluna < self.matrizTaboleiro[0].__len__() - 1:
						# logica da peça comun
						if self.matrizTaboleiro[linha - 1][coluna + 1] not in array :
							linhaPulada = linha - 1
							colunaPulada = coluna + 1

							if linhaPulada - 1 >= 0 and colunaPulada + 1 <= self.matrizTaboleiro[0].__len__()-1:
								if self.matrizTaboleiro[linhaPulada - 1][colunaPulada + 1] == Peca.ESPAÇO_VAZIO:
									movimento = Movimento(
										posicaoInicial = [linha,coluna],
										posicaoFinal = [linhaPulada - 1, colunaPulada + 1],
										posicaoCedulaPulada = [linhaPulada, colunaPulada],
										isObrigatorio = True
										)
									movimentos.append(movimento)
						if self.matrizTaboleiro[linha - 1][coluna + 1] == Peca.ESPAÇO_VAZIO:
							movimento = Movimento(
								posicaoInicial = [linha,coluna],
								posicaoFinal = [linha - 1,coluna + 1],
								posicaoCedulaPulada = None,
								isObrigatorio = False
							)
							movimentos.append(movimento)
						# logica da dama 
						if self.matrizTaboleiro[linha][coluna] == peca|Peca.DAMA:
							if self.matrizTaboleiro[linha + 1][coluna + 1] not in array :
								linhaPulada = linha + 1
								colunaPulada = coluna + 1

								if linhaPulada + 1 >= self.matrizTaboleiro.__len__()-1 and colunaPulada + 1 <= self.matrizTaboleiro[0].__len__()-1:
									if self.matrizTaboleiro[linhaPulada + 1][colunaPulada + 1] == Peca.ESPAÇO_VAZIO:
										movimento = Movimento(
											posicaoInicial = [linha,coluna],
											posicaoFinal = [linhaPulada + 1, colunaPulada + 1],
											posicaoCedulaPulada = [linhaPulada, colunaPulada],
											isObrigatorio = True
											)
										movimentos.append(movimento)
							if self.matrizTaboleiro[linha + 1][coluna + 1] == Peca.ESPAÇO_VAZIO:
								movimento = Movimento(
									posicaoInicial = [linha,coluna],
									posicaoFinal = [linha + 1,coluna + 1],
									posicaoCedulaPulada = None,
									isObrigatorio = False
								)
								movimentos.append(movimento)
							
					if coluna > 0:
						# logica da peça comun
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
						if self.matrizTaboleiro[linha - 1][coluna - 1] == Peca.ESPAÇO_VAZIO:
							movimento = Movimento(
								posicaoInicial = [linha,coluna],
								posicaoFinal = [linha - 1,coluna - 1],
								posicaoCedulaPulada = None,
								isObrigatorio = False
							)
							movimentos.append(movimento)
						# logica da dama 
						if self.matrizTaboleiro[linha][coluna] == peca|Peca.DAMA:
							if self.matrizTaboleiro[linha + 1][coluna - 1] not in array:
								linhaPulada = linha + 1
								colunaPulada = coluna - 1

								if linhaPulada + 1 >= self.matrizTaboleiro.__len__()-1 and colunaPulada - 1 >= 0:
									if self.matrizTaboleiro[linhaPulada + 1][colunaPulada - 1] == Peca.ESPAÇO_VAZIO:
										movimento = Movimento(
											posicaoInicial = [linha,coluna],
											posicaoFinal = [linhaPulada + 1, colunaPulada - 1],
											posicaoCedulaPulada = [linhaPulada, colunaPulada],
											isObrigatorio = False
										)
										movimentos.append(movimento)
							if self.matrizTaboleiro[linha + 1][coluna - 1] == Peca.ESPAÇO_VAZIO:
								movimento = Movimento(
									posicaoInicial = [linha,coluna],
									posicaoFinal = [linha + 1,coluna - 1],
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

	# retorna uma string do taboleiro
	def toString(self):
		tabstr = "  | 0 || 1 || 2 || 3 || 4 || 5 || 6 || 7 |\n"
		
		for linhaI in range(self.matrizTaboleiro.__len__()):
			linha = self.matrizTaboleiro[linhaI]
			tabstr += str(linhaI)+" " 
			for e in linha:
				if e == Peca.BRANCA :
					tabstr += "| ○ |"
				elif e == Peca.PRETA :
					tabstr += "| ● |"
				elif e == Peca.ESPAÇO_VAZIO:
					tabstr += "|   |"
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
			self.status = Status.BRANCA_VENCERAN
		if pecasBrancas == 0:
			self.status =Status.PRETAS_VENCERAN
		if self.existeMovimentoPossivel(Peca.BRANCA) and not self.existeMovimentoPossivel(Peca.PRETA):
			self.status =Status.BRANCA_VENCERAN
		if not self.existeMovimentoPossivel(Peca.BRANCA) and  self.existeMovimentoPossivel(Peca.PRETA):
			self.status =Status.PRETAS_VENCERAN
		if not self.existeMovimentoPossivel(Peca.BRANCA) and not self.existeMovimentoPossivel(Peca.BRANCA):
			self.status =Status.EMPATE
		if PecasPreta == 1 and pecasBrancas == 1:
			self.status =Status.EMPATE
		self.status = Status.JOGANDO
		return self.status
#%%
tab = Taboleiro()
tab.jogadores[0] = Humano(tab,tab.jogadores[0].peca)
tab.jogadores[1] = MiniMax(tab,tab.jogadores[1].peca)

tab.jogo()


