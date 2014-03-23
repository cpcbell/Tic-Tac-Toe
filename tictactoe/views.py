from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from django.conf import settings

from tictactoe.models import PossibleWins 

# Create your views here.

def available_moves(request):

	if request.session.get('available_moves') is undefined:

		request.session['available_moves'] = [1,2,3,4,5,6,7,8,9]

		return True

def initialize_game(request):

	possible_wins = PossibleWins()

	available_moves = AvailableMoves(request.session)
	
def record_move(request,move):

	return True		

def game_board(request,move):

	message = None

	gameObj = {'name':'Tic-Tac-Toe',
		'description':''}

	return render_to_response('tictactoe.html', 
		{
		'gameObj':gameObj,
		'foundationUri':settings.FOUNDATION_URI,
		'otherStaticUri':'http://localhost/tictactoe/',
		'url':'/tictactoe/',
		'message':message,},
		context_instance=RequestContext(request))

