from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from django.conf import settings

from tictactoe.models import Wins,BlockWins 

# Create your views here.

def available_moves(request):

	request.session['available_moves'] = [1,2,3,4,5,6,7,8,9]

	request.session['current_board'] = [1,2,3,4,5,6,7,8,9]

	request.session['currentMove'] = 0
	request.session['currentPlayer'] = 0 

	request.session['player'] = ['X','O']

	request.session['player_moves'] = []
	request.session['computer_moves'] = []

	request.session['block'] = None
	request.session['win'] = None

	return True

def initialize_game(request):

	possible_wins = Wins()

	available_moves(request)

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

def block_a_win(request):

	block_wins = BlockWins()

	wins = Wins()

	request.session['block'] = None

	if len(request.session['player_moves']) > 1:

		for win in request.session['available_moves']:

			copy_player_moves = list(request.session['player_moves'])

			if len(copy_player_moves) > 2:

				copy_player_moves = [request.session['player_moves'][-1],request.session['player_moves'][-2]]
			
			copy_player_moves.append(int(win))

			for this_win in wins.wins:

				if set(this_win) == set(copy_player_moves):

					request.session['block'] = win 

	return request 
		 
def is_a_win(request,player):

	wins = Wins()

	if len(request.session[player]) > 2:

		copy_list = [request.session[player][-1],request.session[player][-2],request.session[player][-3]]

	else:
		copy_list = list(request.session[player])

	for win in wins.wins:

		if set(win) == set(copy_list):

			return True

	return False
	
def record_move(request,move):

	movePosition = int(move) - 1

	request.session['available_moves'].remove(int(move))

	request.session['player_moves'].append(int(move))

	if is_a_win(request,'player_moves'):

		request.session['win'] = 'Player' 

		return request

	request.session['moveStrength'] = judge_move(int(move))

	request.session['current_board'][movePosition] = request.session['player'][0] 

	request = block_a_win(request) 

	"""
	this is the computer player
	"""
	if request.session['block'] is not None:

		move = int(request.session['block'])
	else:

		if 1 in request.session['available_moves']:
			
			move = 1

		elif 3 in request.session['available_moves']:

			move = 3

		elif 7 in request.session['available_moves']:

			move = 7

		elif 9 in request.session['available_moves']:

			move = 9

		elif 5 in request.session['available_moves']:

			move = 5

		elif 2 in request.session['available_moves']:

			move = 2

		elif 4 in request.session['available_moves']:
	
			move = 4

		elif 6 in request.session['available_moves']:

			move = 6

		elif 8 in request.session['available_moves']:
		
			move = 8

	movePosition = int(move) - 1

	request.session['computer_moves'].append(int(move))

	if is_a_win(request,'computer_moves'):

		request.session['win'] = 'Computer' 

		return request

	request.session['available_moves'].remove(int(move))

	request.session['current_board'][movePosition] = request.session['player'][1] 

	return request 

def game_board(request,move):

	message = '' 

	gameStatus = ''

	isComputerMove = 0

	computerMove = 0

	if int(move) == 0:

		request.session.flush()

	elif int(move) > 0 and int(move) < 10:

		request = record_move(request,move)

	message = 'Make a move'

	if request.session.get('available_moves') is None:

		initialize_game(request)

		message = 'You are Xs, Please make the first move'


	"""
	if request.session.get('currentPlayer') is 1:

		message = 'The computer will move next, please wait...'
		isComputerMove = 1
	else:
		isComputerMove = 0
	"""

	gameObj = {'name':'Tic-Tac-Toe',
		'description':''}

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
		'win':request.session['win'],
		'isComputerMove':isComputerMove,
		'computerMove':computerMove},
		context_instance=RequestContext(request))

