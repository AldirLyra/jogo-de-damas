from enum import Flag,auto
import enum
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
class Status(enum):
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
	def jogar(self,TABOLEIRO,Pecas):
		pass

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
								[Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO],
								[Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO,Peca.ESPAÇO_VAZIO],
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
	def movimento_obrigatorio_celula(self, localizacao_cedula):
		obrigatorios = []
		posicao_cedula_pulada = []

		linha,coluna = localizacao_cedula
		
		jogador = self.jogadores[self.turno % 2]
		self.rotacionarTabuleiro(jogador.peca)
		array = [Peca.ESPAÇO_VAZIO,jogador.peca]
		# logica para quando a posicao selecionada e uma peça do jogador e nao e uma dama 
		if self.matrizTaboleiro[linha][coluna] == jogador.peca and self.matrizTaboleiro[linha][coluna] != Peca.DAMA:
				if linha > 0:
					if coluna < self.matrizTaboleiro[0].__len__():
						if self.matrizTaboleiro[linha - 1][coluna + 1] not in array :
							linhaPulada = linha - 1
							colunaPulada = coluna + 1

							if linhaPulada - 1 >= 0 and colunaPulada + 1 <= self.matrizTaboleiro[0].__len__():
								if self.matrizTaboleiro[linhaPulada - 1][colunaPulada + 1] == Peca.ESPAÇO_VAZIO:
									obrigatorios.append([linhaPulada - 1, colunaPulada + 1])
									posicao_cedula_pulada.append([linhaPulada, colunaPulada])
					if coluna > 0:
						if self.matrizTaboleiro[linha - 1][coluna - 1] not in array:
							linhaPulada = linha - 1
							colunaPulada = coluna - 1

							if linhaPulada - 1 >= 0 and colunaPulada - 1 >= 0:
								if self.matrizTaboleiro[linhaPulada - 1][colunaPulada - 1] == Peca.ESPAÇO_VAZIO:
									obrigatorios.append([linhaPulada - 1, colunaPulada - 1])
									posicao_cedula_pulada.append([linhaPulada, colunaPulada])
				if linha < self.matrizTaboleiro.__len__():
					if coluna < self.matrizTaboleiro[0].__len__():
						if self.matrizTaboleiro[linha + 1][coluna + 1] not in array:
							linhaPulada = linha + 1
							colunaPulada = coluna + 1

							if linhaPulada + 1 <= self.matrizTaboleiro.__len__() and colunaPulada + 1 <= self.matrizTaboleiro[0].__len__():
								if self.matrizTaboleiro[linhaPulada + 1][colunaPulada + 1] == Peca.ESPAÇO_VAZIO:
									obrigatorios.append([linhaPulada + 1, colunaPulada + 1])
									posicao_cedula_pulada.append((linhaPulada, colunaPulada))
					if coluna > 0:
						if self.matrizTaboleiro[linha + 1][coluna - 1] not in array:
							linhaPulada = linha + 1
							colunaPulada = coluna - 1

							if linhaPulada + 1 <= self.matrizTaboleiro.__len__() and colunaPulada - 1 >= 0:
								if self.matrizTaboleiro[linhaPulada + 1][colunaPulada - 1] == Peca.ESPAÇO_VAZIO:
									obrigatorios.append([linhaPulada + 1, colunaPulada - 1])
									posicao_cedula_pulada.append((linhaPulada, colunaPulada))

		return obrigatorios, posicao_cedula_pulada

	# RETORNA TODOS OS MOVIMENTOS OBRIGATÓRIOS DE UM TURNO
	def todos_obrigatorios(self):
		todos = (()())

		for r in range(len(self.matrizTaboleiro)):
			for c in range(len(self.matrizTaboleiro[r])):
				ob, pulos = self.movimento_obrigatorio((r, c))
				if  ob != []:
					todos[(r, c)] = ob

		return todos
		
	# RETORNA SE EXISTE UM MOVIMENTO POSSIVEL A SE FAZER COM A PEÇA
	def existe_possivel(self):
		for l in range(len(self.matrizTaboleiro)):
			for c in range(len(self.matrizTaboleiro[l])):
				if self.movimentos_possiveis((l, c))[0]:
					return True
		return False


	# MOSTRA OS MOVIMENTOS POSSÍVEIS DE UMA PEÇA 
	def movimentos_possiveis(self, localizacao_cedula):
		movimentos, pulos = self.movimento_obrigatorio(localizacao_cedula)

		if movimentos == []:
			linha_atual = localizacao_cedula[0]
			coluna_atual = localizacao_cedula[1]

			if self.matrizTaboleiro[linha_atual][coluna_atual].islower():
				if self.matrizTaboleiro[linha_atual][coluna_atual] == Peca.BRANCA:
					if linha_atual > 0:
						if coluna_atual < 7:
							if self.matrizTaboleiro[linha_atual - 1][coluna_atual + 1] == Peca.ESPAÇO_VAZIO:
								movimentos.append([linha_atual - 1, coluna_atual + 1])
						if coluna_atual > 0:
							if self.matrizTaboleiro[linha_atual - 1][coluna_atual - 1] == Peca.ESPAÇO_VAZIO:
								movimentos.append([linha_atual - 1, coluna_atual - 1])
				
				elif self.matrizTaboleiro[linha_atual][coluna_atual] == Peca.PRETA:
					if linha_atual < 7:
						if coluna_atual < 7:
							if self.matrizTaboleiro[linha_atual + 1][coluna_atual + 1] == Peca.ESPAÇO_VAZIO:
								movimentos.append([linha_atual + 1, coluna_atual + 1])
						if coluna_atual > 0:
							if self.matrizTaboleiro[linha_atual + 1][coluna_atual - 1] == Peca.ESPAÇO_VAZIO:
								movimentos.append([linha_atual + 1, coluna_atual - 1])
			elif self.matrizTaboleiro[linha_atual][coluna_atual].isupper():
				conta_linha = linha_atual
				conta_coluna = coluna_atual
				while True:
					if conta_linha - 1 < 0 or conta_coluna - 1 < 0: break
					else:
						if self.matrizTaboleiro[conta_linha - 1][conta_coluna - 1] == Peca.ESPAÇO_VAZIO:
							movimentos.append([conta_linha - 1, conta_coluna - 1])
						else: break
					conta_linha -= 1
					conta_coluna -= 1

				conta_linha = linha_atual
				conta_coluna = coluna_atual
				while True:
					if conta_linha - 1 < 0 or conta_coluna + 1 > 7: break
					else:
						if self.matrizTaboleiro[conta_linha - 1][conta_coluna + 1] == Peca.ESPAÇO_VAZIO:
							movimentos.append([conta_linha - 1, conta_coluna + 1])
						else: break
					conta_linha -= 1
					conta_coluna += 1

				conta_linha = linha_atual
				conta_coluna = coluna_atual
				while True:
					if conta_linha + 1 > 7 or conta_coluna + 1 > 7: break
					else:
						if self.matrizTaboleiro[conta_linha + 1][conta_coluna + 1] == Peca.ESPAÇO_VAZIO:
							movimentos.append([conta_linha + 1, conta_coluna + 1])
						else: break
					conta_linha += 1
					conta_coluna += 1

				conta_linha = linha_atual
				conta_coluna = coluna_atual
				while True:
					if conta_linha + 1 > 7 or conta_coluna - 1 < 0: break
					else:
						if self.matrizTaboleiro[conta_linha + 1][conta_coluna - 1] == Peca.ESPAÇO_VAZIO:
							movimentos.append([conta_linha + 1, conta_coluna - 1])
						else: break
					conta_linha += 1
					conta_coluna -= 1
				
		return movimentos, pulos



	# PRÓXIMO TURNO
	def proximo_turno(self):
		self.turno += 1

	# VERIFICA O VENCEDOR
	def verifica_vencedor(self):

		x = sum([contador.count(Peca.PRETA) + contador.count(Peca.PRETA) for contador in self.matrizTaboleiro])
		o = sum([contador.count(Peca.BRANCA) + contador.count(Peca.BRANCA) for contador in self.matrizTaboleiro])

		if x == 0:
			return Peca.BRANCA

		if o == 0:
			return Peca.PRETA

		if x == 1 and o == 1:
			return 'Empate'

		if self.cedula_selecionada:
			if not self.movimentos_possiveis(self.cedula_selecionada)[0]:
				if x == 1 and self.turno % 2 == 0:
					return  Status.br
				if o == 1 and self.turno % 2 == 1:
					return Peca.PRETA

		if not self.existe_possivel():
			return 'Empate'


		return None