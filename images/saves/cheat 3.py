#import GOD
import pygame
import time
import datetime
import random
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
from pygame.locals import *
from sys import stdin, exit
from os import environ
from pickle import dumps, loads
from pprint import pprint
import socket
HOST, PORT = "", 9999  # defined for now

BUFFSIZE = 1024				 # for socket.send & recv commands
BACKLOG = 2					 # number of clients supported by
#server  
SECONDS = 3					 # seconds until socket.timeout (not

environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

pygame.font.init()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Background Music
pygame.mixer.music.load('background.wav')
#You got caught lying!
#caught = pygame.mixer.Sound("caught.wav")
#Peanut Butter
#pbj = pygame.mixer.Sound("pbj.wav")

iconcard = pygame.image.load('app.png')
pygame.display.set_icon(iconcard)
pygame.mixer.music.play(-1)

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
		self.instructionsimg = pygame.image.load("images/instructions.png")

		self.backcardside = pygame.image.load("images/back.jpg")
		self.titlefnt = pygame.font.SysFont("Copperplate", 145)
		self.title = self.titlefnt.render("Cheat!", 1, (255,255,0))

		self.maintitlefnt = pygame.font.SysFont("Copperplate", 300)
		self.maintitle = self.maintitlefnt.render("Cheat!", 1, (255,255,0))

		self.exitfnt = pygame.font.SysFont("Copperplate", 75)
		self.exit = self.exitfnt.render("Exit", 1, (0,0,0))

		self.playcardfnt = pygame.font.SysFont("Copperplate", 30)
		self.playcardtxt = self.playcardfnt.render("Play cards!", 1, (0,0,0))

		self.otherplayerturnfnt = pygame.font.SysFont("Copperplate", 80)
		self.otherplayerturntxt = self.otherplayerturnfnt.render("Waiting for other players!", 1, (0,0,0))

		self.playgamefnt = pygame.font.SysFont("Copperplate", 90)
		self.playgametxt = self.playgamefnt.render("Play!", 1, (0,0,0))
		
		self.instructionsfnt = pygame.font.SysFont("Copperplate", 35)
		self.instructionstxt = self.instructionsfnt.render("Instructions", 1, (0,0,0))

		self.clock = pygame.time.Clock()
		self.caption = pygame.display.set_caption("Online Game")
		
		# player number. this can be 0 (left player) or 1 (right player)
		#self.num = None

		#Number of players
		self.playeramount = 2
		self.deck1, self.deck2, self.deck3, self.deck4, self.deck5 = [], [], [], [], []

		self.playedcards=[]

		self.card={'cardrank1':[], 'cardrank2':[], 'cardrank3':[], 'cardrank4':[], 'cardrank5':[], 'cardrank6':[], 'cardrank7':[], 'cardrank8':[], 'cardrank9':[], 'cardrank10':[], 'cardrank11':[], 'cardrank12':[], 'cardrank13':[]}
		self.card2={'cardrank1':[], 'cardrank2':[], 'cardrank3':[], 'cardrank4':[], 'cardrank5':[], 'cardrank6':[], 'cardrank7':[], 'cardrank8':[], 'cardrank9':[], 'cardrank10':[], 'cardrank11':[], 'cardrank12':[], 'cardrank13':[]}


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
		self.dicdeck ={}
		self.suiteranks = []
		self.shuffleddeck = []

		#rank
		self.rank = []
		self.redrank = []

		self.in_number_menu = False

		self.pressed=False


		self.cardshow11, self.cardshow21, self.cardshow22, self.cardshow31, self.cardshow32, self.cardshow33, self.cardshow41, self.cardshow42, self.cardshow43, self.cardshow44 = False, False, False, False, False, False, False, False, False, False
		#a=dict.fromkeys(['cardshow11', 'b', 'f', 'h', 'p'], True)
		self.cardshow = dict.fromkeys(['cardshow11', 'cardshow21', 'cardshow22', 'cardshow31', 'cardshow32', 'cardshow33', 'cardshow41', 'cardshow42', 'cardshow43', 'cardshow44'], False)
		self.pick = {'pick1': [0,0,0,0],'pick2': [0,0,0,0], 'pick3': [0,0,0,0],'pick4': [0,0,0,0],'pick5': [0,0,0,0],'pick6': [0,0,0,0],'pick7': [0,0,0,0],'pick8': [0,0,0,0],'pick9': [0,0,0,0],'pick10': [0,0,0,0],'pick11': [0,0,0,0],'pick12': [0,0,0,0],'pick13': [0,0,0,0]}
		self.nums = dict.fromkeys(['num14', 'num24', 'num34', 'num44', 'num54', 'num64', 'num74', 'num84', 'num94', 'num104', 'num114', 'num124', 'num134', 
		'num11', 'num21', 'num31', 'num41', 'num51', 'num61', 'num71', 'num81', 'num91', 'num101', 'num111', 'num121', 'num131', 
		'num12', 'num22', 'num32', 'num42', 'num52', 'num62', 'num72', 'num82', 'num92', 'num102', 'num112', 'num122', 'num132', 'num13', 
		'num23', 'num33', 'num43', 'num53', 'num63', 'num73', 'num83', 'num93', 'num103', 'num113', 'num123', 'num133'], False)
		# self.nums = {'num14':False, 'num24':False, 'num34':False, 'num44':False, 'num54':False, 'num64':False, 'num74':False, 'num84':False, 'num94':False, 'num104':False, 'num114':False, 'num124':False, 'num134':False, 
		# 'num11':False, 'num21':False, 'num31':False, 'num41':False, 'num51':False, 'num61':False, 'num71':False, 'num81':False, 'num91':False, 'num101':False, 'num111':False, 'num121':False, 'num131':False, 
		# 'num12':False, 'num22':False, 'num32':False, 'num42':False, 'num52':False, 'num62':False, 'num72':False, 'num82':False, 'num92':False, 'num102':False, 'num112':False, 'num122':False, 'num132':False, 'num13':False, 
		# 'num23':False, 'num33':False, 'num43':False, 'num53':False, 'num63':False, 'num73':False, 'num83':False, 'num93':False, 'num103':False, 'num113':False, 'num123':False, 'num133':False}

		self.wid = 0

		self.my_turn = True

		self.intro=True
		self.instructionrunning=False

		self.turnin=[]
		self.initialdealout=True

		self.currentpile=0

		self.currentplayingrank = 1 #What needs to be played

		self.delete1, self.delete2, self.delete3, self.delete4 = False, False, False, False

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

	def intro_screen(self):
		while self.intro:
			for event in pygame.event.get():
				# end the game in necessary
				if event.type == pygame.QUIT:
					exit(0)
				mouse = pygame.mouse.get_pos()
				click = pygame.mouse.get_pressed()
				self.screen.blit(self.bg,(0,0))
				self.screen.blit(self.maintitle, (220,50))
				pygame.draw.rect(self.screen, [255,100,100], (485,325,150,100))
				pygame.draw.rect(self.screen, [255,100,100], (485,500,150,100))
				self.screen.blit(self.playgametxt, (485, 345))
				self.screen.blit(self.instructionstxt, (486, 535))
				if 485 < mouse[0]<635 and 325 < mouse[1] <425:
					pygame.draw.rect(self.screen, [255,50,50], (485,325,150,100))
					self.screen.blit(self.playgametxt, (485, 345))
					if click[0]:
						self.Loop()
				if 485 < mouse[0]<635 and 500 < mouse[1] <600:
					pygame.draw.rect(self.screen, [255,50,50], (485,500,150,100))
					self.screen.blit(self.instructionstxt, (486, 535))
					if click[0]:
						self.instructionrunning=True
						self.instructions()

			pygame.display.update()

	def instructions(self):
		while self.instructionrunning:
			self.clock.tick(60)
			# update connection
			connection.Pump()
			# update the listener
			self.Pump()
			for event in pygame.event.get():
				# end the game in necessary
				if event.type == pygame.QUIT:
					exit(0)
				mouse = pygame.mouse.get_pos()
				click = pygame.mouse.get_pressed()
				self.screen.blit(self.bg,(0,0))
				self.screen.blit(self.instructionsimg,(0,0))
				pygame.draw.rect(self.screen, [255,100,100], (920,575,200,75))
				self.screen.blit(self.exit, (965, 590))
				if 965 < mouse[0] and 590 < mouse[1]:
					pygame.draw.rect(self.screen, self.red, (920,575,200,75))  #start, wide, height
					self.screen.blit(self.exit, (965, 590))
					if event.type == pygame.MOUSEBUTTONDOWN:
							self.instructionrunning=False
							self.intro_screen()
			pygame.display.update()
				
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
					mouse = pygame.mouse.get_pos()
					click = pygame.mouse.get_pressed()

					self.screen.blit(self.bg,(0,0)) #Background
					self.screen.blit(self.backcardside,((self.width/2)-160,105)) #Facedown card
					self.screen.blit(self.title, (400, 0)) #Title on top

					pygame.draw.rect(self.screen, [255,100,100], (850,0,150,100))
					self.screen.blit(self.playcardtxt,(875,40)) #Play cards button
					if 850 < mouse[0] <1000 and 0 < mouse[1] <100:
						if click[0]:
							if self.my_turn==True:
								for x in range(1,14):
									for y in range(4):
										if self.pick["pick"+str(x)][y]==1:
											#try:
											print('Card deck initial')
											print(self.card["cardrank"+str(x)])
											#problem below
											
											self.turnin.append(self.card["cardrank"+str(x)][y])
											#del self.card["cardrank"+str(x)][y]
											#Problem above
											if y==0:
												self.delete1 = True
											if y==1:
												self.delete2 = True
											if y==2:
												self.delete3 = True
											if y==3:
												self.delete4 = True
												
											print('Card deck after')
											print(self.card["cardrank"+str(x)])
											self.currentpile+=1
											
										#self.pick["pick"+str(x)][y]=0

									print(self.card["cardrank"+str(x)])
									if self.delete1==True:
										self.pick["pick"+str(x)][0]=0
										self.deck1.remove(self.card["cardrank"+str(x)][0])
										del self.card["cardrank"+str(x)][0]
									if self.delete2==True:
										print(self.pick["pick"+str(x)][1])
										self.pick["pick"+str(x)][1]=0
										self.deck1.remove(self.card["cardrank"+str(x)][1])
										del self.card["cardrank"+str(x)][1]
									if self.delete3==True:
										self.pick["pick"+str(x)][2]=0
										self.deck1.remove(self.card["cardrank"+str(x)][2])
										del self.card["cardrank"+str(x)][2]
									if self.delete4==True:
										self.pick["pick"+str(x)][3]=0
										self.deck1.remove(self.card["cardrank"+str(x)][3])
										del self.card["cardrank"+str(x)][3]
									print(self.card["cardrank"+str(x)])

									self.delete1, self.delete2, self.delete3, self.delete4 = False, False, False, False
									
									self.cardshow11, self.cardshow21, self.cardshow22,self.cardshow31, self.cardshow32 = False, False, False, False, False
									self.cardshow33, self.cardshow41, self.cardshow42, self.cardshow43, self.cardshow44 = False, False, False, False, False
									self.card={'cardrank1':[], 'cardrank2':[], 'cardrank3':[], 'cardrank4':[], 'cardrank5':[], 'cardrank6':[], 'cardrank7':[], 'cardrank8':[], 'cardrank9':[], 'cardrank10':[], 'cardrank11':[], 'cardrank12':[], 'cardrank13':[]}
									self.deal_out()
						
					self.show_ranks() #Shows ranks numbers on main screen 
					self.button(event)

					pygame.display.update()

					

	def normal_screen(self):
		self.screen.blit(self.bg,(0,0)) #Background
		self.screen.blit(self.backcardside,((self.width/2)-160,105)) #Facedown card
		self.screen.blit(self.title, (100, 0)) #Title on top
		self.show_ranks() #Shows ranks numbers on main screen 
		self.button()
	def safe_input(prompt, values='abcdefghijklmnopqrstuvwxyz'):
		#gives prompt, checks first char of input, assures it meets
		#given values #default is anything goes """
		while True:
			i = input(prompt)
			try:
				c = i[0].lower()
			except IndexError:  # the only possible error?!
				if c=='':
					print("Try again.")
			else:
				if c not in values: # some other character
					print("Try again.")
				else:   # looks good. continue.
					break
		return i

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
		self.shuffleddeck = list(self.dicdeck.keys())
		random.shuffle(self.suiteranks)
		pygame.display.update()

	def deal_out(self): #Sorts deck into 13 numbers, server side code

		#Get two decks for two playerss
		if self.initialdealout==True:

			for x in range(1,27):
				y = random.choice(self.suiteranks)
				self.deck1.append(y)
				self.suiteranks.remove(y)
			#send deck 1 out

			for x in range(1,27):
				y = random.choice(self.suiteranks)
				self.deck2.append(y)
				self.suiteranks.remove(y)
			#send this out deck2

			# for x in range(1,(52/self.playeramount)+1):
			# 	y = random.choice(self.suiteranks)
			# 	self.deck2.append(y)
			# 	self.suiteranks.remove(y)


			if self.playeramount==3:
				y = random.choice(self.suiteranks)
				self.deck3.append(y)
				self.suiteranks.remove(y)
			if self.playeramount==4:
				y = random.choice(self.suiteranks)
				self.deck4.append(4)
				self.suiteranks.remove(y)
			if self.playeramount==5:
				y = random.choice(self.suiteranks)
				self.deck5.append(y)
				self.suiteranks.remove(y)

		self.initialdealout=False
		for x in range(len(self.deck1)): #length 26
			for y in range(1,14): #13 ranks clubs1
				if self.deck1[x] in ("clubs"+str(y), "spades"+str(y), "hearts"+str(y), "diamonds"+str(y)):
					self.card["cardrank"+str(y)].append(self.deck1[x])

	def show_ranks(self): #Shows rank numbers
		#import rank photos
		if self.my_turn==True:
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
		else:
			self.screen.blit(self.otherplayerturntxt,(200,450))

		pygame.draw.line(self.screen, self.black, (0,335), (self.width,335), 5) #where, color, start, end, thickness in pixels

	def button(self, event): #message, x location, y location, width, height, inactive color, active color, action
		if self.my_turn==True:
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

					for x in range(1,14):
						if number==x:
							cardnumber=1
							for card in self.card["cardrank"+str(x)]:
								
								self.nums["num"+str(x)+str(cardnumber)]=True
								if self.nums["num"+str(x)+str(cardnumber)]==True:
									self.screen.blit(self.dicdeck[card], (wide, high))
									wide+=250

								cardnumber+=1

							number_of_cardsinitial = len(self.card["cardrank"+str(x)])
							self.mousecheck(number_of_cardsinitial, number)

				
					for x in range(1,14):
						for y in range(4):
							if self.pick['pick'+str(x)][y]==1 and number==x:
								if y==0:
									self.wid = 50
								if y==1:
									self.wid = 300
								if y==2:
									self.wid = 550
								if y==3:
									self.wid = 800
								self.screen.blit(self.checkmark,(self.wid,300))
				
					if 965 < mouse[0] and 590 < mouse[1]:
						pygame.draw.rect(self.screen, self.red, (920,575,200,75))  #start, wide, height
						self.screen.blit(self.exit, (965, 590))
						if event.type == pygame.MOUSEBUTTONDOWN:
							
							self.pressed=False
							self.Loop() 
							pygame.display.update()

					pygame.display.update()

	def mousecheck(self, number_of_cards, number):		
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		'''		
		if number_of_cards==1 or number_of_cards==2 or number_of_cards==3 or number_of_cards==4: #cardshow22
			if 50<mouse[0]<215 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow["cardshow"+str(number_of_cards)+"1"]==False:
						self.cardshow["cardshow"+str(number_of_cards)+"1"] = True					
						self.pick["pick"+str(number)][0]=1
						print(self.pick["pick"+str(number)])
					#elif self.cardshow["cardshow"+str(number_of_cards)+"1"]==True:
					else:
						self.cardshow["cardshow"+str(number_of_cards)+"1"] = False
						self.pick["pick"+str(number_of_cards)][0]=0
						print(self.pick["pick"+str(number)])

		if number_of_cards==2 or number_of_cards==3 or number_of_cards==4:
			if 300<mouse[0]<465 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow["cardshow"+str(number_of_cards)+"2"]==False:
						self.cardshow["cardshow"+str(number_of_cards)+"2"] = True
						self.pick["pick"+str(number)][1]=1
						print(self.pick["pick"+str(number)])
					# elif self.cardshow["cardshow"+str(number_of_cards)+"2"]==True:
					else:
						self.cardshow["cardshow"+str(number_of_cards)+"2"] = False
						self.pick["pick"+str(number)][1]=0
						print(self.pick["pick"+str(number)])
		if number_of_cards==3 or number_of_cards==4:
			if 550<mouse[0]<715 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow["cardshow"+str(number_of_cards)+"3"]==False:
						self.cardshow["cardshow"+str(number_of_cards)+"3"] = True
						self.pick["pick"+str(number)][2]=1
						print(self.pick["pick"+str(number)])
					#elif self.cardshow["cardshow"+str(number_of_cards)+"3"]==True:
					else:
						self.cardshow["cardshow"+str(number_of_cards)+"3"] = False
						self.pick["pick"+str(number_of_cards)][2]=0
						print(self.pick["pick"+str(number)])
		if number_of_cards==4: 
			if 800<mouse[0]<965 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow["cardshow"+str(number_of_cards)+"4"]==False:
						self.cardshow["cardshow"+str(number_of_cards)+"4"] = True
						self.pick["pick"+str(number)][3]=1
						print(self.pick["pick"+str(number)])
					#elif self.cardshow["cardshow"+str(number_of_cards)+"4"]==True:
					else:
						self.cardshow["cardshow"+str(number_of_cards)+"4"] = False
						self.pick["pick"+str(number_of_cards)][3]=0
						print(self.pick["pick"+str(number)])
		'''
		if number_of_cards==1:	
			if 50<mouse[0]<215 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow11==False:
						self.cardshow11 = True					
						self.pick["pick"+str(number)][0]=1
					elif self.cardshow11==True:
						self.pick["pick"+str(number)][0]=0
						self.cardshow11 = False

		elif number_of_cards==2:
			if 50<mouse[0]<215 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow21==False:
						self.cardshow21 = True
						self.pick["pick"+str(number)][0]=1

					elif self.cardshow21==True:
						self.cardshow21 = False
						self.pick["pick"+str(number)][0]=0
			if 300<mouse[0]<465 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow22==False:
						self.cardshow22 = True
						self.pick["pick"+str(number)][1]=1
					elif self.cardshow22==True:
						self.cardshow22 = False
						self.pick["pick"+str(number)][1]=0

		elif number_of_cards==3:
			if 50<mouse[0]<215 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow31==False:
						self.cardshow31 = True
						self.pick["pick"+str(number)][0]=1
					elif self.cardshow31==True:
						self.cardshow31 = False
						self.pick["pick"+str(number)][0]=0
			if 300<mouse[0]<465 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow32==False:
						self.cardshow32 = True
						self.pick["pick"+str(number)][1]=1
					elif self.cardshow32==True:
						self.cardshow32 = False
						self.pick["pick"+str(number)][1]=0
			if 550<mouse[0]<715 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow33==False:
						self.cardshow33 = True
						self.pick["pick"+str(number)][2]=1
					elif self.cardshow33==True:
						self.cardshow33 = False
						self.pick["pick"+str(number)][2]=0

		elif number_of_cards==4:
			if 50<mouse[0]<215 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow41==False:
						self.cardshow41 = True
						self.pick["pick"+str(number)][0]=1
					elif self.cardshow41==True:
						self.cardshow41 = False
						self.pick["pick"+str(number)][0]=0
			if 300<mouse[0]<465 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow42==False:
						self.cardshow42 = True
						self.pick["pick"+str(number)][1]=1
					elif self.cardshow42==True:
						self.cardshow42 = False
						self.pick["pick"+str(number)][1]=0
			if 550<mouse[0]<715 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow43==False:
						self.cardshow43 = True
						self.pick["pick"+str(number)][2]=1
					elif self.cardshow43==True:
						self.cardshow43 = False
						self.pick["pick"+str(number)][2]=0
			if 800<mouse[0]<965 and 50<mouse[1]<290:
				if click[0]:
					if self.cardshow44==False:
						self.cardshow44 = True
						self.pick["pick"+str(number)][3]=1
					elif self.cardshow44==True:
						self.cardshow44 = False
						self.pick["pick"+str(number)][3]=0

		# def multiplayerhost(self):
		# 	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #  			sock.bind((HOST, PORT))
  #  			sock.listen(BACKLOG)
  #  			serverip, serverport = sock.getsockname()
  #  			print("Running at %s, %s" % (serverip, serverport))
  #  			client, address = sock.accept()
  #  			clientip, clientport = address

  #  		def multiplayerjoin(self):
  #  			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #  			sock.connect((HOST, PORT))
  #  			while True:
  #      			sock.send(dumps(game))
  #      			try:
  #          			P1game = loads(sock.recv(BUFFSIZE))
  #      			except EOFError:
  #          			print(P1game['name'], "left the game.")
  #          			break
  #      			if P1game['start']:
  #          			print("You're connected to "+P1game['name']+"'s game.")
  #          			game['start'] = False
  #      			if P1game['message']!='' and P1game['message']!=game['sentmessage']:
  #          			print(P1game['name']+': '+P1game['message'])
  #          			game['sentmessage'] = P1game['message']
  #          			game['move'] = ''
  #      			if game['move']=='':
  #          			game['move'] = safe_input('1, 2, 3, GO! ')
  #          		if game['move']=='q':
  #              		break
  #          		elif game['move'] not in 'rps':
  #              		game['message'] = game['move']
  #              		game['move'] = ''
  #      			if P1game['move']!='':
  #          			# check game outcome dict
  #          			game=get_result(game, P1game)
  #          			game['move']=''
  #  			# exit loop
  #  			sock.close()
  #  print('\nYou won %s, lost %s, drew %s (%s total)\n' % (game['won'],game['lost'],game['drew'],game['total']))
  #  main_menu(game)

	#def select_card(self):

		#Number on top of screen
		#Exit button
		#Show four cards 
		
	# def win(self):
	# 	if len(self.deck1)==0 and if it's not my turn:
	# 		You win
	# 		wait 5 seconds
	# 	exit()
	
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
listener.intro_screen()
#listener.Loop()

