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
	
def record_move(request,move):

	request.session['currentMove'] += 1

	if request.session['currentPlayer'] is 0:
		"""
		This is their first move, lets see if they are expert, moderate or beginner
		"""
		request.session['currentPlayer'] = 1

		movePosition = int(move) - 1;

		request.session['current_board'][movePosition] = request.session['player'][0] 

	return True		

def game_board(request,move):

	message = '' 

	gameStatus = ''

	if int(move) == 0:

		request.session.flush()

	elif int(move) > 0 and int(move) < 10:

		record_move(request,move)

	if request.session.get('available_moves') is None:

		initialize_game(request)

		message = 'You are Xs, Please make the first move'

	if request.session.get('currentPlayer') is 1:

		message = 'The computer will move next, please wait...'

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
		'computersMove':computersMove},
		context_instance=RequestContext(request))

