from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from django.conf import settings

from tictactoe.models import Wins,BlockWins 

# Create your views here.

def available_moves(request):

	request.session['available_moves'] = [1,2,3,4,5,6,7,8,9]

	request.session['available_wins'] = list() 

	request.session['current_board'] = [1,2,3,4,5,6,7,8,9]

	request.session['currentMove'] = 0
	request.session['currentPlayer'] = 0 

	request.session['player'] = ['X','O']

	request.session['player_moves'] = list() 
	request.session['computer_moves'] = list() 

	request.session['winner_moves'] = list() 
	request.session['player_winner_moves'] = list() 

	request.session['error'] = None 

	request.session['block'] = None
	request.session['winner'] = None
	request.session['win'] = None

	return True

def initialize_game(request):

	possible_wins = Wins()

	request.session['possible_wins'] = list(possible_wins.wins)

	available_moves(request)

	for some_wins in possible_wins.wins:
		
		request.session['available_wins'].append(some_wins)	


def expert_move(move):

	if int(move) in [1,3,7,9]:

		return True

	return False

def ok_move(move):

	if int(move) is 5:

		return True

	return False

def novice_move(move):

	if int(move) in [2,4,6,8]:

		return True

	return False

def judge_move(move):

	if expert_move(move):
		return 3
	elif ok_move(move):
		return 2
	else:
		return 1

def even_number(move):

	if move % 2 == 0:
		return True
	return False

"""
"""
def is_a_win(request,player):

	wins = Wins()
		
	for winners in wins.wins:

		if winners in request.session['available_wins']:

			if set(winners) == set(request.session[player]):

				#request.session['winner_moves'].append(list(winners))

				request.session['available_wins'].remove(list(winners))

				return True

	return False

def get_a_win(request,player):

	if len(request.session[player]) >= 2:

		for win in request.session['available_moves']:

			copy_list = list(request.session[player])

			if len(request.session[player]) == 2:

				copy_list.append(int(win))

				copy_list.sort()

				request.session['player_winner_moves'] = list(copy_list)

				if is_a_win(request,'player_winner_moves') is True:

					request.session['win'] = win

					del copy_list

					return True

			elif len(request.session[player]) >= 3:

				for thisPosition in range(0,len(request.session[player])):

					copy_list.sort()

					copy_list.pop(thisPosition)

					copy_list.append(int(win))

					copy_list.sort()

					try:
						del request.session['player_winner_moves']
					except:
						None	

					request.session['player_winner_moves'] = [copy_list[0],copy_list[1],copy_list[2]]

					if is_a_win(request,'player_winner_moves') is True:

						request.session['win'] = win

						del copy_list

						return True

					copy_list = list(request.session[player])

			del request.session['player_winner_moves']
			request.session['player_winner_moves'] = list()

			del copy_list

	return False

def best_move(request):

	move = None

	if 5 in request.session['available_moves']:

		move = 5

	elif 1 in request.session['available_moves']:
			
		move = 1

	elif 3 in request.session['available_moves']:

		move = 3

	elif 7 in request.session['available_moves']:

		move = 7

	elif 9 in request.session['available_moves']:

		move = 9

	elif 2 in request.session['available_moves']:

		move = 2

	elif 4 in request.session['available_moves']:
	
		move = 4

	elif 6 in request.session['available_moves']:

		move = 6

	elif 8 in request.session['available_moves']:
		
		move = 8

	return move
	
def record_move(request,move):

	if int(move) not in request.session['available_moves']:

		request.session['error'] = 'Illegal Move'
		
		return request

	movePosition = int(move) - 1

	request.session['available_moves'].remove(int(move))

	request.session['player_moves'].append(int(move))

	if is_a_win(request,'player_moves'):

		request.session['winner'] = 'Player' 

		request.session['current_board'][movePosition] = request.session['player'][0] 

		return request

	if len(request.session['available_moves']) == 1:
		
		request.session['winner'] = 'No one wins, except the Cat.' 
		
		return request

	request.session['moveStrength'] = judge_move(int(move))

	request.session['current_board'][movePosition] = request.session['player'][0] 

	if len(request.session['available_moves']) == 1:

		return request
	"""
	block the player win
	"""
	#request = get_a_win(request,'player_moves') 

	"""
	get the computer win
	"""
	#request = get_a_win(request,'computer_moves') 

	if get_a_win(request,'player_moves'):

		move = int(request.session['win'])

	elif get_a_win(request,'computer_moves'):

		move = int(request.session['win'])
	
	else:
		move = best_move(request)

	if move is None:

		request.session['winner'] = 'No one wins, except the Cat.' 
		
		return request

	movePosition = int(move) - 1

	request.session['computer_moves'].append(int(move))

	if is_a_win(request,'computer_moves'):

		request.session['winner'] = 'Computer' 

		request.session['current_board'][movePosition] = request.session['player'][1] 

		return request

	try:
		request.session['available_moves'].remove(int(move))

		request.session['current_board'][movePosition] = request.session['player'][1] 
	except:
		None

	return request 

def game_board(request,move):

	message = '' 

	gameStatus = ''

	isComputerMove = 0

	computerMove = 0

	request.session['error'] = None

	if int(move) == 0:

		request.session.flush()

		if request.session.get('available_moves') is None:

			initialize_game(request)

			message = 'You are Xs, Please make the first move'

	elif int(move) > 0 and int(move) < 10:

		request = record_move(request,move)

		message = 'Make a move'


	"""
	if request.session.get('currentPlayer') is 1:

		message = 'The computer will move next, please wait...'
		isComputerMove = 1
	else:
		isComputerMove = 0
	"""

	if request.session['error'] is not None:

		message = request.session['error']

	gameObj = {'name':'Tic-Tac-Toe',
		'description':''}

	"""
		'winnerMoves':request.session['winner_moves'],
		'playerWinnerMoves':request.session['player_winner_moves'],
	"""

	return render_to_response('tictactoe.html', 
		{
		'currentBoard':request.session['current_board'],
		'gameObj':gameObj,
		'foundationUri':settings.FOUNDATION_URI,
		'otherStaticUri':'http://localhost/tictactoe/',
		'url':'/tictactoe/',
		'message':message,
		'gameStatus':request.session['available_moves'],
		'playerMoves':request.session['player_moves'],
		'computerMoves':request.session['computer_moves'],
		'winner':request.session['winner'],
		'possibleWins':request.session['possible_wins'],
		'availableWins':request.session['available_wins'],
		'isComputerMove':isComputerMove,
		'computerMove':computerMove},
		context_instance=RequestContext(request))

