import pygame
import time
from functools import partial
import datetime
import math
import random
import sys
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
from pygame.locals import *
from sys import stdin, exit
from os import environ

environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

pygame.font.init()


#Background Music
pygame.mixer.music.load('background.wav')
#You got caught lying!
#caught = pygame.mixer.Sound("caught.wav")
#Peanut Butter
#pbj = pygame.mixer.Sound("pbj.wav")

iconcard = pygame.image.load('app.png')
pygame.display.set_icon(iconcard)
#pygame.mixer.music.play(-1)


class Listener(ConnectionListener):
	# init the player
	def __init__(self, host, port):
		self.Connect((host, port))
		
		# set the window
		#3 pixel space between each number
		self.width=1120
		self.height=650
		self.screen = pygame.display.set_mode((self.width, self.height))#,HWSURFACE|DOUBLEBUF|RESIZABLE)
		self.bg = pygame.image.load("images/table.jpg")
		self.checkmark = pygame.image.load("images/check.png")

		self.backcardside = pygame.image.load("images/back.jpg")
		self.titlefnt = pygame.font.SysFont("Copperplate", 145)
		self.title = self.titlefnt.render("Cheat!", 1, (255,255,0))

		self.exitfnt = pygame.font.SysFont("Copperplate", 75)
		self.exit = self.exitfnt.render("Exit", 1, (0,0,0))
		

		self.clock = pygame.time.Clock()
		self.caption = pygame.display.set_caption("Online Game")
		
		# player number. this can be 0 (left player) or 1 (right player)
		#self.num = None

		#Number of players
		self.playeramount = 2
		self.deck1 = []
		self.deck2 = []
		self.deck3 = []
		self.deck4 = []
		self.deck5 = []
		self.playedcards=[]

		#Rank Menus Buttons
		self.one = []
		self.two = []
		self.three = []
		self.four = []
		self.five = []
		self.six = []
		self.seven = []
		self.eight = []
		self.nine = []
		self.ten = []
		self.eleven = []
		self.twelve = []
		self.thirteen = []


		# True if the server sended the ready message
		self.ready = False
		# True if the game is working
		self.start = False

		# font for writing the scores
		self.font = pygame.font.SysFont('sans,freesans,courier,arial', 18, True)
		self.red = [255, 0, 0]
		self.black=[0,0,0]
		# points of the first and second players
		self.points = [0, 0]

		#Empty Deck
		self.deck = []
		self.dicdeck ={}
		self.suiteranks = []
		#rank
		self.rank = []
		self.redrank = []

		self.in_number_menu = False

		self.pressed=False

		self.cardpick = False

		self.cardshow11=self.cardshow21=self.cardshow22=self.cardshow31=self.cardshow32=self.cardshow33=self.cardshow41=self.cardshow42=self.cardshow43=self.cardshow44 = False
		self.pick = {'pick1': [0,0,0,0,0],'pick2': [0,0,0,0,0], 'pick3': [0,0,0,0,0],'pick4': [0,0,0,0,0],'pick5': [0,0,0,0,0],'pick6': [0,0,0,0,0],'pick7': [0,0,0,0,0],'pick8': [0,0,0,0,0],'pick9': [0,0,0,0,0],'pick10': [0,0,0,0,0],'pick11': [0,0,0,0,0],'pick12': [0,0,0,0,0],'pick13': [0,0,0,0,0]}

		self.nums = {'num14':False, 'num24':False, 'num34':False, 'num44':False, 'num54':False, 'num64':False, 'num74':False, 'num84':False, 'num94':False, 'num104':False, 'num114':False, 'num124':False, 'num134':False, 
		'num11':False, 'num21':False, 'num31':False, 'num41':False, 'num51':False, 'num61':False, 'num71':False, 'num81':False, 'num91':False, 'num101':False, 'num111':False, 'num121':False, 'num131':False, 
		'num12':False, 'num22':False, 'num32':False, 'num42':False, 'num52':False, 'num62':False, 'num72':False, 'num82':False, 'num92':False, 'num102':False, 'num112':False, 'num122':False, 'num132':False, 'num13':False, 
		'num23':False, 'num33':False, 'num43':False, 'num53':False, 'num63':False, 'num73':False, 'num83':False, 'num93':False, 'num103':False, 'num113':False, 'num123':False, 'num133':False}

	# funtion to manage bars movement
	def Network_move(self, data):
		if data['player'] != self.num:
			self.players[data['player']].top = data['top']
	
	# get the player number
	def Network_number(self, data):
		self.num = data['num']

	# get ballpos
	def Network_ballpos(self, data):
		self.ballrect = pygame.Rect(data['pos'], data['size'])
	
	# if the game is ready
	def Network_ready(self, data):
		self.ready = not self.ready
	
	# change players' score
	def Network_points(self, data):
		self.points[0] = data[0]
		self.points[1] = data[1]
	
	# start the game
	def Network_start(self, data):
		self.ready = False
		self.start = True

	def cards(self):
		self.shuffle()
		self.deal_out()

	def Loop(self):
		
		while self.pressed==False:
			self.clock.tick(60)
			# update connection
			connection.Pump()
			# update the listener
			self.Pump()
			# control user input
			for event in pygame.event.get():
				# end the game in necessary
				if event.type == pygame.QUIT:
					exit(0)

				# if the game is started
				else:

					self.screen.blit(self.bg,(0,0)) #Background
					self.screen.blit(self.backcardside,((self.width/2)-160,105)) #Facedown card
					self.screen.blit(self.title, (400, 0)) #Title on top
					self.show_ranks() #Shows ranks numbers on main screen 
					self.button(event)

					pygame.display.update()

					

	def normal_screen(self):
		self.screen.blit(self.bg,(0,0)) #Background
		self.screen.blit(self.backcardside,((self.width/2)-160,105)) #Facedown card
		self.screen.blit(self.title, (100, 0)) #Title on top
		self.show_ranks() #Shows ranks numbers on main screen 
		self.button()

	def shuffle(self): #Creates deck
	#Imports cards and create a shuffled deck
		for x in range(1, 14):
			clubs = "clubs"+str(x)
			self.dicdeck[clubs] = pygame.image.load("images/cards/clubs/"+str(x)+"_of_clubs.png")

			spades = "spades"+str(x)
			self.dicdeck[spades] = pygame.image.load("images/cards/spades/"+str(x)+"_of_spades.png")

			hearts = "hearts"+str(x)
			self.dicdeck[hearts] = pygame.image.load("images/cards/hearts/"+str(x)+"_of_hearts.png")

			diamonds = "diamonds"+str(x)
			self.dicdeck[diamonds] = pygame.image.load("images/cards/diamonds/"+str(x)+"_of_diamonds.png")

		self.suiteranks =  list(self.dicdeck.keys())
		random.shuffle(self.suiteranks)
		pygame.display.update()

	def deal_out(self): #Sorts deck into 13 numbers

		#for x in range(1,(52/(self.playeramount)+1)):
		for x in range(1,27):
			y = random.choice(self.suiteranks)
			self.deck1.append(y)
			self.suiteranks.remove(y)
		hell = 0
		for x in range(len(self.deck1)):
			if self.deck1[x] in ("clubs1", "spades1", "hearts1", "diamonds1"):
				self.one.append(self.deck1[x])
			elif self.deck1[x] in ("clubs2", "spades2", "hearts2", "diamonds2"):
				self.two.append(self.deck1[x])
			elif self.deck1[x] in ("clubs3", "spades3", "hearts3", "diamonds3"):
				self.three.append(self.deck1[x])
			elif self.deck1[x] in ("clubs4", "spades4", "hearts4", "diamonds4"):
				self.four.append(self.deck1[x])
			elif self.deck1[x] in ("clubs5", "spades5", "hearts5", "diamonds5"):
				self.five.append(self.deck1[x])
			elif self.deck1[x] in ("clubs6", "spades6", "hearts6", "diamonds6"):
				self.six.append(self.deck1[x])
			elif self.deck1[x] in ("clubs7", "spades7", "hearts7", "diamonds7"):
				self.seven.append(self.deck1[x])
			elif self.deck1[x] in ("clubs8", "spades8", "hearts8", "diamonds8"):
				self.eight.append(self.deck1[x])
			elif self.deck1[x] in ("clubs9", "spades9", "hearts9", "diamonds9"):
				self.nine.append(self.deck1[x])
			elif self.deck1[x] in ("clubs10", "spades10", "hearts10", "diamonds10"):
				self.ten.append(self.deck1[x])
			elif self.deck1[x] in ("clubs11", "spades11", "hearts11", "diamonds11"):
				self.eleven.append(self.deck1[x])
			elif self.deck1[x] in ("clubs12", "spades12", "hearts12", "diamonds12"):
				self.twelve.append(self.deck1[x])
			elif self.deck1[x] in ("clubs13", "spades13", "hearts13", "diamonds13"):
				self.thirteen.append(self.deck1[x])
			
			
	'''
	#Sorts into different number for vieiwng during game
	def sort():

	'''
	def show_ranks(self): #Shows rank numbers
		#import rank photos
		for x in range(1, 14):
			self.rank.append(pygame.image.load("images/numbers/"+str(x)+".png"))
			self.redrank.append(pygame.image.load("images/numbers/"+str(x)+"red.png"))

		#Top 7 seven ranks
		top_length = 5
		for x in range(1,8): #+10
			self.screen.blit(self.rank[x-1], (top_length,(self.height-300)))				
			if top_length < self.width:
				top_length+=160
		#Bottom 6 ranks
		top_length = 80
		for x in range(8,14): #+10
			self.screen.blit(self.rank[x-1], (top_length,(self.height-150)))
			if top_length < self.width:
				top_length+=160

		pygame.draw.line(self.screen, self.black, (0,335), (self.width,335), 5) #where, color, start, end, thickness in pixels

	

	def button(self, event): #message, x location, y location, width, height, inactive color, active color, action
		pressed = False
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed() #Gets data from mouse press (left right click)
		top_length = 5
		for x in range(1,8):
			if (top_length+150) > mouse[0] > top_length and (self.height-300)+150 > mouse[1] > (self.height-300): #if mouse coord is in range of x value and y value of the created box, do what follows
				self.screen.blit(self.redrank[x-1], (top_length,(self.height-300)))
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.pressed=True
					self.show_rankcard(x)
			top_length+=160

		top_length = 80
		for x in range(8,14):
			if (top_length+150) > mouse[0] > top_length and (self.height-150)+150 > mouse[1] > (self.height-150): #if mouse coord is in range of x value and y value of the created box, do what follows
				self.screen.blit(self.redrank[x-1], (top_length,(self.height-150)))
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.pressed=True
					self.show_rankcard(x)
			top_length+=160


	def show_rankcard(self, number): #Displays card when you click number, new game loop
		while self.pressed==True:
			self.clock.tick(100)
			# update connection
			connection.Pump()
			# update the listener
			self.Pump()
			# control user input
			for event in pygame.event.get():
				# end the game in necessary
				if event.type == pygame.QUIT:
					exit(0)

				# if the game is started
				else:
					mouse = pygame.mouse.get_pos()
					click = pygame.mouse.get_pressed()
					self.screen.fill(self.red)
					self.screen.blit(self.bg,(0,0))
					pygame.draw.rect(self.screen, [255,100,100], (920,575,200,75))  #start, wide, height
					self.screen.blit(self.exit, (965, 590))
					wide = 50
					high = 50

					#165x240
					#85 pillow
					#self.num["num"+str(number)]=True
					self.pick["pick"+str(number)][4]=1
					if number==1:
						
						for card in self.one:
							self.screen.blit(self.dicdeck[card], (wide, high))
							wide+=250
						number_of_cardsinitial = len(self.one)
						self.mousecheck(number_of_cardsinitial, number)
			
					if number==2:
						
						for card in self.two:
							self.screen.blit(self.dicdeck[card], (wide, high))
							wide+=250
						number_of_cards = len(self.two)
						number_of_cardsinitial = len(self.two)
						self.mousecheck(number_of_cardsinitial, number)
					if number==3:
						for card in self.three:
							self.screen.blit(self.dicdeck[card], (wide, high))
							wide+=250
						number_of_cards = len(self.three)
						number_of_cardsinitial = len(self.three)
						self.mousecheck(number_of_cardsinitial, number)
					if number==4:
						for card in self.four:
							self.screen.blit(self.dicdeck[card], (wide, high))
							wide+=250
						number_of_cards = len(self.four)
						number_of_cardsinitial = len(self.four)
						self.mousecheck(number_of_cardsinitial, number)
					if number==5:
						for card in self.five:
							self.screen.blit(self.dicdeck[card], (wide, high))
							wide+=250
						number_of_cards = len(self.five)
						number_of_cardsinitial = len(self.five)
						self.mousecheck(number_of_cardsinitial, number)
					if number==6:
						for card in self.six:
							self.screen.blit(self.dicdeck[card], (wide, high))
							wide+=250
						number_of_cards = len(self.six)
						number_of_cardsinitial = len(self.six)
						self.mousecheck(number_of_cardsinitial, number)
					if number==7:
						for card in self.seven:
							self.screen.blit(self.dicdeck[card], (wide, high))
							wide+=250
						number_of_cards = len(self.seven)
						number_of_cardsinitial = len(self.seven)
						self.mousecheck(number_of_cardsinitial, number)
					if number==8:
						for card in self.eight:
							self.screen.blit(self.dicdeck[card], (wide, high))
							wide+=250
						number_of_cards = len(self.eight)
						number_of_cardsinitial = len(self.eight)
						self.mousecheck(number_of_cardsinitial, number)
					if number==9:
						for card in self.nine:
							self.screen.blit(self.dicdeck[card], (wide, high))
							wide+=250
						number_of_cards = len(self.nine)
						number_of_cardsinitial = len(self.nine)
						self.mousecheck(number_of_cardsinitial, number)
					if number==10:
						for card in self.ten:
							self.screen.blit(self.dicdeck[card], (wide, high))
							wide+=250
						number_of_cards = len(self.ten)
						number_of_cardsinitial = len(self.ten)
						self.mousecheck(number_of_cardsinitial, number)
					if number==11:
						for card in self.eleven:
							self.screen.blit(self.dicdeck[card], (wide, high))
							wide+=250
						number_of_cards = len(self.eleven)
						number_of_cardsinitial = len(self.eleven)
						self.mousecheck(number_of_cardsinitial, number)
					if number==12:
						self.nums["num121"]=self.nums["num121"]=self.nums["num121"]=self.nums["num121"]=True
						for card in self.twelve:
							self.screen.blit(self.dicdeck[card], (wide, high))
							wide+=250
						number_of_cards = len(self.twelve)
						number_of_cardsinitial = len(self.twelve)
						self.mousecheck(number_of_cardsinitial, number)
						if self.exit()==True:
							self.nums["num121"]=self.nums["num121"]=self.nums["num121"]=self.nums["num121"]=False
							self.Loop() 
					if number==13:
						for card in self.thirteen:
							self.screen.blit(self.dicdeck[card], (wide, high))
							wide+=250
						number_of_cards = len(self.thirteen)
						number_of_cardsinitial = len(self.thirteen)
						self.mousecheck(number_of_cardsinitial, number)
						


				#First Card display
					if (self.cardshow11==True or self.pick['pick1'][0]==1) and self.nums["num11"]==True:
						self.screen.blit(self.checkmark,(50,300))
					if (self.cardshow21==True or self.pick['pick2'][0]==1) and self.pick["pick"+str(number)][4]==1:
						self.screen.blit(self.checkmark,(50,300))
					if (self.cardshow31==True or self.pick['pick3'][0]==1) and self.pick["pick"+str(number)][4]==1:
						self.screen.blit(self.checkmark,(50,300))
					if (self.cardshow41==True or self.pick['pick4'][0]==1)and self.pick["pick"+str(number)][4]==1:
						self.screen.blit(self.checkmark,(50,300))
				#SECOND CARD Display
					if (self.cardshow22==True or self.pick['pick2'][1]==1) and self.pick["pick"+str(number)][4]==1:
						self.screen.blit(self.checkmark,(300,300))
					if (self.cardshow32==True or self.pick['pick3'][1]==1) and self.pick["pick"+str(number)][4]==1:
						self.screen.blit(self.checkmark,(300,300))
					if (self.cardshow42==True or self.pick['pick4'][1]==1) and self.pick["pick"+str(number)][4]==1:
						self.screen.blit(self.checkmark,(300,300))
				#Third card display
					if (self.cardshow33==True or self.pick['pick3'][2]==1) and self.pick["pick"+str(number)][4]==1:
						self.screen.blit(self.checkmark,(550,300))
					if (self.cardshow43==True or self.pick['pick4'][2]==1) and self.pick["pick"+str(number)][4]==1:
						self.screen.blit(self.checkmark,(550,300))
				#Fourth card display
					if (self.cardshow44==True or self.pick['pick4'][3]==1) and self.pick["pick"+str(number)][4]==1:
						self.screen.blit(self.checkmark,(800,300))
	def exit(self):
		#Exit button
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if 965 < mouse[0] and 590 < mouse[1]:
			pygame.draw.rect(self.screen, self.red, (920,575,200,75))  #start, wide, height
			self.screen.blit(self.exit, (965, 590))
			if event.type == pygame.MOUSEBUTTONDOWN:
				return True
				#self.pressed=False
				#self.nums["num"+str(number)]=False
				#self.pick["pick"+str(number)][4]=0
				#self.Loop() 

					pygame.display.update()

	def mousecheck(self, number_of_cards, number):
#menu 2 with 2 cards		
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		#finley      = {'a':0, 'b':2, 'c':[41, 51 ,61]}
		#crazy_sauce = {'d':3}
		#finley['c'].append(crazy_sauce['d'])

		if number_of_cards==1:	
			if 50<mouse[0]<215 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow11==False:
						self.cardshow11 = True					
						self.pick["pick"+str(number)][0]=1
						print(self.pick["pick"+str(number)])
					elif self.cardshow11==True:
						self.pick["pick"+str(number)][0]=0
						print(self.pick["pick"+str(number)])
						self.cardshow11 = False

		elif number_of_cards==2:
			if 50<mouse[0]<215 and 50<mouse[1]<290:
				print('2')
				if click[0]:
					if self.cardshow21==False:
						self.cardshow21 = True
						self.pick["pick"+str(number)][0]=1
						#self.screen.blit(self.checkmark,(50,300))
					elif self.cardshow21==True:
						self.cardshow21 = False
						self.pick["pick"+str(number)][0]=0
			if 300<mouse[0]<465 and 50<mouse[1]<290:
				print('2b')
				if click[0]:
					if self.cardshow22==False:
						self.cardshow22 = True
						self.pick["pick"+str(number)][1]=1
						#self.screen.blit(self.checkmark,(300,300))
					elif self.cardshow22==True:
						self.cardshow22 = False
						self.pick["pick"+str(number)][1]=0

		elif number_of_cards==3:
			if 50<mouse[0]<215 and 50<mouse[1]<290:
				print('3')
				if click[0]:
					if self.cardshow31==False:
						self.cardshow31 = True
						self.pick["pick"+str(number)][0]=1
						#self.screen.blit(self.checkmark,(50,300))
					elif self.cardshow31==True:
						self.cardshow31 = False
						self.pick["pick"+str(number)][0]=0
			if 300<mouse[0]<465 and 50<mouse[1]<290:
				print('3b')
				if click[0]:
					if self.cardshow32==False:
						self.cardshow32 = True
						self.pick["pick"+str(number)][1]=1
						#self.screen.blit(self.checkmark,(300,300))
					elif self.cardshow32==True:
						self.cardshow32 = False
						self.pick["pick"+str(number)][1]=0
			if 550<mouse[0]<715 and 50<mouse[1]<290:
				print('3c')
				if click[0]:
					if self.cardshow33==False:
						self.cardshow33 = True
						self.pick["pick"+str(number)][2]=1
						#self.screen.blit(self.checkmark,(550,300))
					elif self.cardshow33==True:
						self.cardshow33 = False
						self.pick["pick"+str(number)][2]=0

		elif number_of_cards==4:
			if 50<mouse[0]<215 and 50<mouse[1]<290:
				print('4')
				if click[0]:
					if self.cardshow41==False:
						self.cardshow41 = True
						self.pick["pick"+str(number)][0]=1
						#self.screen.blit(self.checkmark,(50,300))
					elif self.cardshow41==True:
						self.cardshow41 = False
						self.pick["pick"+str(number)][0]=0
			if 300<mouse[0]<465 and 50<mouse[1]<290:
				print('4a')
				if click[0]:
					if self.cardshow42==False:
						self.cardshow42 = True
						self.pick["pick"+str(number)][1]=1
						#self.screen.blit(self.checkmark,(300,300))
					elif self.cardshow42==True:
						self.cardshow42 = False
						self.pick["pick"+str(number)][1]=0
			if 550<mouse[0]<715 and 50<mouse[1]<290:
				print('4b')
				if click[0]:
					if self.cardshow43==False:
						self.cardshow43 = True
						self.pick["pick"+str(number)][2]=1
						#self.screen.blit(self.checkmark,(550,300))
					elif self.cardshow43==True:
						self.cardshow43 = False
						self.pick["pick"+str(number)][2]=0
			if 800<mouse[0]<965 and 50<mouse[1]<290:
				print('4c')
				if click[0]:
					if self.cardshow44==False:
						self.cardshow44 = True
						self.pick["pick"+str(number)][3]=1
						#self.screen.blit(self.checkmark,(800,300))
					elif self.cardshow44==True:
						self.cardshow44 = False
						self.pick["pick"+str(number)][3]=0

	#def select_card(self):

		#Number on top of screen
		#Exit button
		#Show four cards 
		
'''
print ('Enter the server ip adresse (pleaviously enter on the server script).')
print ('Empty for localhost')
# ask the server ip adresse
server = input('server ip: ')
# control if server is empty
if server == '':
	server = 'localhost'
'''

server = 'localhost'
# init the listener
listener = Listener(server, 31500)
# start the mainloop
listener.cards()
listener.Loop()

