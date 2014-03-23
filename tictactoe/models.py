import os.path
from django.db import models
from django.conf import settings

class PossibleWins():
	
	possible_wins = [
		[1,2,3],
		[4,5,6],
		[7,8,9],
		[1,4,7],
		[2,5,8],
		[3,6,9],
		[1,5,9],
		[3,5,7],
		]

	def __unicode__(self):
		return self.possible_wins

	

