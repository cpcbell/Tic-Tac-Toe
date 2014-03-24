from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from django.conf import settings

from tictactoe.models import PossibleWins 

# Create your views here.

def available_moves(request):

	request.session['available_moves'] = [1,2,3,4,5,6,7,8,9]

	request.session['current_board'] = [1,2,3,4,5,6,7,8,9]

	request.session['currentMove'] = 0
	request.session['currentPlayer'] = 0 

	request.session['player'] = ['X','O']

	return True

def initialize_game(request):

	possible_wins = PossibleWins()

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
	
def record_move(request,move):

	request.session['currentMove'] += 1

	if request.session['currentPlayer'] is 0:
		request.session['currentPlayer'] = 1

		"""
		This is their first move, lets see if they are expert, moderate or beginner
		request.session['currentPlayer'] = 1

		request.session['moveStrength'] = judge_move(move)

		movePosition = int(move) - 1;

		request.session['current_board'][movePosition] = request.session['player'][0] 
	else:
		"""
		"""
		this is the human player
		"""

	request.session['moveStrength'] = judge_move(move)

	movePosition = int(move) - 1;

	request.session['current_board'][movePosition] = request.session['player'][0] 

	"""
	when done set player to next
	"""
	request.session['currentPlayer'] = 2
		
	#else:
	request.session['currentMove'] += 1
	"""
	this is the computer player
	"""
	if 1 in request.session['current_board']:
			
		movePosition = 0
	elif 3 in request.session['current_board']:
		movePosition = 2
	elif 7 in request.session['current_board']:
		movePosition = 6
	elif 9 in request.session['current_board']:
		movePosition = 8
	elif 5 in request.session['current_board']:
		movePosition = 4
	elif 2 in request.session['current_board']:
		movePosition = 1
	elif 4 in request.session['current_board']:
		movePosition = 3
	elif 6 in request.session['current_board']:
		movePosition = 5
	elif 8 in request.session['current_board']:
		movePosition = 7

	request.session['current_board'][movePosition] = request.session['player'][1] 
	"""
	when done set player to next
	"""
	request.session['currentPlayer'] = 1

	return move		

def game_board(request,move):

	message = '' 

	gameStatus = ''

	isComputerMove = 0

	computerMove = 0

	if int(move) == 0:

		request.session.flush()

	elif int(move) > 0 and int(move) < 10:

		computerMove = record_move(request,move)

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
		'gameStatus':gameStatus,
		'isComputerMove':isComputerMove,
		'computerMove':computerMove},
		context_instance=RequestContext(request))

