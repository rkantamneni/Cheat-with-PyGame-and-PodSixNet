#Cheat by Revant Kantamneni
'''
I spent a lot of time manipulating variables in this project. That's what took a lot of time.
Learning the servide side was brutal. I had to contact several people but I pulled it off.
This game is right now for two players. I tried to run more than two pygame windows but the
windows kept lagging and crashing because my computer couldn't handle. This game can easily be
adapted for more players with a few code changes.

You might want to read the README because they is quite a bit you need to install to get this to work
Search youtube for 'Cheat Cardgame with PodSix and Pygame' for my explanation
'''
import pygame
import datetime
import random
from PodSixNet.Connection import connection, ConnectionListener
from time import sleep
from sys import stdin, exit
from os import environ

HOST, PORT = "", 9999  # defined for now

BUFFSIZE = 1024				 # for socket.send & recv commands
BACKLOG = 2					 # number of clients supported by
#server  
SECONDS = 3					 # seconds until socket.timeout (not

environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

pygame.font.init()


#Background Music
pygame.mixer.music.load('background.wav')

iconcard = pygame.image.load('app.png')
pygame.display.set_icon(iconcard)
#pygame.mixer.music.play(-1)
class Listener(ConnectionListener):
	# init the player
	def __init__(self, host, port):
		self.Connect((host, port))
		print('Client has started')

		# set the window
		#3 pixel space between each number
		self.width=1120
		self.height=650
		self.screen = pygame.display.set_mode((self.width, self.height))#,HWSURFACE|DOUBLEBUF|RESIZABLE)
		self.bg = pygame.image.load("images/table.jpg")
		self.winnerbg = pygame.image.load("images/winner.jpg")
		self.checkmark = pygame.image.load("images/check.png")
		self.instructionsimg = pygame.image.load("images/instructions.png")

		self.backcardside = pygame.image.load("images/back.jpg")#Card in main menu
		self.titlefnt = pygame.font.SysFont("Copperplate", 145)#Font for titel
		self.title = self.titlefnt.render("Cheat!", 1, (255,0,0))#Title Attributes
		#Self explanatory vairables
		self.maintitlefnt = pygame.font.SysFont("Copperplate", 300)
		self.maintitle = self.maintitlefnt.render("Cheat!", 1, (255,0,0))

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

		self.waitingfnt = pygame.font.SysFont("Copperplate", 60)
		self.waitingtxt = self.waitingfnt.render("Waiting for other players.", 1, (0,0,0))
		#One person has to start game
		self.waitingforstarttxt = self.waitingfnt.render("Other player must press play.", 1, (0,0,0))
		#Displays whose turn it is first
		self.yourtunrfirsttxt = self.waitingfnt.render("You have first turn. Play 1 Spades.", 1, (0,0,0))
		self.waitingforturntxt = self.waitingfnt.render("Waiting for turn.", 1, (0,0,0))

		self.callblufftxt = self.waitingfnt.render("Call Bluff!", 1, (0,0,0))
		self.proceedtxt = self.waitingfnt.render("Proceed", 1, (0,0,0))

		#Place Holder
		self.cardnumpickedtxt = self.waitingfnt.render("Call Bluff!", 1, (0,0,0)) 
		self.currentranktxt = self.waitingfnt.render("Call Bluff!", 1, (0,0,0)) 
		self.currentpiletxt=self.waitingfnt.render("Call Bluff!", 1, (0,0,0)) 
		self.numofcardsplayedblufftxt=self.waitingfnt.render("Call Bluff!", 1, (0,0,0)) 
		self.bluffcalltxt=self.waitingfnt.render("Call Bluff!", 1, (0,0,0)) 
		#Dertermines FPS
		self.clock = pygame.time.Clock()
		self.caption = pygame.display.set_caption("Online Game")
		
		# player number. this can be 0 (left player) or 1 (right player)
		#self.num = None

		#Number of players
		self.playeramount = 2
		#Main deck with everythins
		self.deck1= []
		#Gets card which have been played
		self.playedcards=[]

		#Know whether there is certain card or not.
		self.card={'cardrank1':[[],[],[],[]], 'cardrank2':[[],[],[],[]], 'cardrank3':[[],[],[],[]], 'cardrank4':[[],[],[],[]], 'cardrank5':[[],[],[],[]], 'cardrank6':[[],[],[],[]], 'cardrank7':[[],[],[],[]], 'cardrank8':[[],[],[],[]], 'cardrank9':[[],[],[],[]], 'cardrank10':[[],[],[],[]], 'cardrank11':[[],[],[],[]], 'cardrank12':[[],[],[],[]], 'cardrank13':[[],[],[],[]]}
		

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

		#Empty Deck for backup purposes
		self.fulldeck ={} #Use this as refeference to load in images
		self.suiteranks = []
		self.shuffleddeck = []

		#rank images get appended to these lists
		self.rank = []
		self.redrank = []

		self.playernumber = 0 #Gives you a number, 1 or 2

		self.in_number_menu = False #Once you click a number circle in the menus, it turns True

		self.pressedrankbutton=False

		#Helps determine whether to show checks under cards or not
		self.cardshow11, self.cardshow21, self.cardshow22, self.cardshow31, self.cardshow32, self.cardshow33, self.cardshow41, self.cardshow42, self.cardshow43, self.cardshow44 = False, False, False, False, False, False, False, False, False, False 
		self.cardshow = dict.fromkeys(['cardshow11', 'cardshow21', 'cardshow22', 'cardshow31', 'cardshow32', 'cardshow33', 'cardshow41', 'cardshow42', 'cardshow43', 'cardshow44'], False)
		#Keeps track of what cards you picked. Dealed with recusion errors here so I put lists inside lists
		self.pick = {'pick1': [0,0,0,0],'pick2': [0,0,0,0], 'pick3': [0,0,0,0],'pick4': [0,0,0,0],'pick5': [0,0,0,0],'pick6': [0,0,0,0],'pick7': [0,0,0,0],'pick8': [0,0,0,0],'pick9': [0,0,0,0],'pick10': [0,0,0,0],'pick11': [0,0,0,0],'pick12': [0,0,0,0],'pick13': [0,0,0,0]}
		self.nums = dict.fromkeys(['num14', 'num24', 'num34', 'num44', 'num54', 'num64', 'num74', 'num84', 'num94', 'num104', 'num114', 'num124', 'num134', 
		'num11', 'num21', 'num31', 'num41', 'num51', 'num61', 'num71', 'num81', 'num91', 'num101', 'num111', 'num121', 'num131', 
		'num12', 'num22', 'num32', 'num42', 'num52', 'num62', 'num72', 'num82', 'num92', 'num102', 'num112', 'num122', 'num132', 'num13', 
		'num23', 'num33', 'num43', 'num53', 'num63', 'num73', 'num83', 'num93', 'num103', 'num113', 'num123', 'num133'], False)

		self.wid = 0

		self.my_turn = False #Tells you whether it is your turn or not
		self.gamestart=False

		self.intro=True #Switch for intro screen
		self.instructionrunning=False

		self.turnin=[] #Keeps track of what cards have been turned in
		self.initialdealout=True

		self.currentpile=0 #At the bginning, no cards have been played

		self.delete1, self.delete2, self.delete3, self.delete4 = False, False, False, False

		self.countmake = dict.fromkeys(['count1', 'count2', 'count3', 'count4', 'count5', 'count6', 'count7', 'count8', 'count9', 'count10', 'count11', 'count12', 'count13'], 0)

		self.access=False

		self.otherstart = False

		self.callbluff=False

		self.currentrank = 1 #Represents ace of spades

		self.pickbluff={}

		self.dealout2=False

		self.firstbluff=False

		self.bluffcall=False


	def Network_createplayerdeck(self,data): #Sets player deck from server command
		self.suiteranks=data['keylist']
		print('Part 1')

		#player.Send({"action": "initial", "lines": dict([(p.id, {"color": p.color, "lines": p.lines}) for p in self.players])})

	def Network_playernumber(self, data): #Player gets assinged number by server
		self.playernumber=int(data['playernum'])
		self.caption = pygame.display.set_caption("Cheat: Player"+str(self.playernumber))

	def Network_initialplayerturn(self, data): #Server detemrines who goes first
		if data['playernum']==self.playernumber:
			self.my_turn=True
			self.access=True
			
		self.gamestart=True
		print('This is my playernumber: '+str(self.playernumber))

	def Network_otherplayerscanstartnow(self, data): #Gives other players to start once the first person has started
		self.access=data['startothers']

	def Network_updatenumplayedcards(self,data):
		self.currentpile=data['num'] #Number of cards in pile

	def Network_updateplayedcards(self,data):
		self.turnin=data['turnincards'] #List of strings ranks in list

	def Network_turnchangeclient(self, data): #Change whose turn it is
		if self.my_turn==True:
			self.my_turn=False
			self.callbluff=False

		elif self.my_turn==False:
			#self.my_turn=True
			self.callbluff=True
	def Network_decreaseplayernum(self, data): #Experimental function
		#{'action': 'decreaseplayernum', 'playernum': data['num']}
		print('Player '+str(data['num']+'disconnected.'))

	def Network_numofcardsplayedinturn(self, data): #How many cards the prior player played
		self.numofcardsplayedbluff = data['numplayedcards']#How many cards the other person picked in their turn, call their bluff

	def Network_currentrank(self, data): #Current rank card which needs to be played
		if self.my_turn==False:
			self.currentrank=data['rank']
		

	def Network_checkbluff(self, data): #Sees if person is bluffing
		self.pickbluff=data['pickarray']
		print(self.pickbluff)

	def Network_lostbluff(self, data): #What happens when you lose the bluff
		self.turnin=data['bluff']
		self.dealout2=True
		self.deal_out()

	def Network_wonbluff(self, data): #What happens when you win the bluff
		self.turnin=data['bluff']
		for x in self.turnin:
			self.suiteranks.append(x)
			self.turnin.remove(x)
		#self.initialdealout=True
		self.dealout2=True
		self.deal_out()

	def Network_blufftext(self,data):
		self.bluffcall=data['bluff']
		self.firstbluff=data['onebluff']

	##built in##
	def Network_connected(self, data):
		print ("You are now connected to the server")
	
	def Network_error(self, data):
		print ('error:', data['error'][1])
		connection.Close()
	
	def Network_disconnected(self, data):
		print ('Server disconnected')
		exit()
	##built in##


	def Pumping(self): #Constant connection to server
		connection.Pump()
		self.Pump()

	def cards(self): #Initial card dealing
		self.shuffle()
		self.deal_out()

	def intro_screen(self): #Intro screen with play and instructions button
		while self.intro:
			connection.Pump()
			self.Pump()
			for event in pygame.event.get():
				connection.Pump()
				self.Pump()
				# end the game in necessary
				if event.type == pygame.QUIT:
					connection.Pump()
					self.Pump()
					connection.Send({"action": 'playerdisconnect', "num": self.playernumber})
					connection.Pump()
					self.Pump()
					exit(0)
				mouse = pygame.mouse.get_pos()
				click = pygame.mouse.get_pressed()
				#Adds objects to screen
				self.screen.blit(self.bg,(0,0))# Background
				self.screen.blit(self.maintitle, (220,50))#title
				pygame.draw.rect(self.screen, [255,100,100], (485,325,150,100))
				pygame.draw.rect(self.screen, [255,100,100], (485,500,150,100))
				self.screen.blit(self.playgametxt, (485, 345))
				self.screen.blit(self.instructionstxt, (486, 535))
				#gives you acces to view certain things
				if self.my_turn==True and self.access==True:
					self.screen.blit(self.yourtunrfirsttxt, (250,250))
				if self.my_turn==False and self.gamestart==False:
					self.screen.blit(self.waitingtxt, (325,250))
				if self.my_turn==False and self.gamestart==True:
					self.screen.blit(self.waitingforstarttxt, (275,250))
				#Starts main menu loop when click play
				if 485 < mouse[0]<635 and 325 < mouse[1] <425:
					pygame.draw.rect(self.screen, [255,50,50], (485,325,150,100))
					self.screen.blit(self.playgametxt, (485, 345))
					#if click[0] and self.gamestart==True and self.my_turn==True or self.otherstart==True and self.access==True:
					if click[0] and self.access==True:
						connection.Pump()
						self.Pump()
						connection.Send({"action": "otherplayercanstart", "access": True})
						self.deckcreate()
						self.deal_out()
						self.Loop()
				#Starts instruction when clicked
				if 485 < mouse[0]<635 and 500 < mouse[1] <600:
					pygame.draw.rect(self.screen, [255,50,50], (485,500,150,100))
					self.screen.blit(self.instructionstxt, (486, 535))
					if click[0]:
						self.instructionrunning=True
						self.instructions()

			pygame.display.update() #Update display

	def instructions(self):
		while self.instructionrunning:
			self.clock.tick(60)
			# update connection
			connection.Pump()
			# update the listener
			self.Pump()
			sleep(0.001)
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
							self.intro_screen() #Return back to intor screen
			pygame.display.update()
				
	def Loop(self):
		#Runs when it's your turn
		while self.pressedrankbutton==False:
			self.clock.tick(60)
			# update connection
			connection.Pump()
			# update the listener
			self.Pump()
			sleep(0.0001)
			man=False
			# control user input
			for event in pygame.event.get():
				# end the game in necessary
				if event.type == pygame.QUIT:
					exit(0)

				# if the game is started
				else:
					mouse = pygame.mouse.get_pos() #Get what the mouse is doing
					click = pygame.mouse.get_pressed() #Gives click numbers

					self.screen.blit(self.bg,(0,0)) #Background
					self.screen.blit(self.backcardside,((self.width/2)-160,105)) #Facedown card
					self.screen.blit(self.title, (400, 0)) #Title on top
					pygame.draw.line(self.screen, self.black, (0,335), (self.width,335), 5) #where, color, start, end, thickness in pixels
					#Current Rank
					self.currentranktxt = self.waitingfnt.render('Current Rank: '+ str(self.currentrank), 1, (0,0,0))
					self.screen.blit(self.currentranktxt, (0, 0))
					#Current pile stack
					self.currentpiletxt = self.waitingfnt.render('Played Cards:'+ str(self.currentpile), 1, (0,0,0))
					self.screen.blit(self.currentpiletxt, (0, 100))

					if self.my_turn==True: #If it is your turn
						self.numberofcardspicked=0
						for x in range(1,14):
							for y in range(4):
								if self.pick["pick"+str(x)][y]==1:
									self.numberofcardspicked+=1
						self.cardnumpickedtxt = self.waitingfnt.render('Cards Picked: '+ str(self.numberofcardspicked), 1, (0,0,0))
						self.screen.blit(self.cardnumpickedtxt,(0,200))
						if self.bluffcall==True and self.firstbluff==True:
							self.bluffcalltxt = self.waitingfnt.render('Bluff: Correct!', 1, (34,139,34))
							self.screen.blit(self.bluffcalltxt,(0,280))

						elif self.bluffcall==False and self.firstbluff==True:
							self.bluffcalltxt = self.waitingfnt.render('Bluff: Wrong!', 1, (255,0,0))
							self.screen.blit(self.bluffcalltxt,(0,280))
						

						pygame.draw.rect(self.screen, [255,100,100], (850,0,150,100))

						self.screen.blit(self.playcardtxt,(875,40)) #Play cards button
										
						self.show_ranks() #Shows ranks numbers on main screen 
						self.button(event)
						if 850 < mouse[0] <1000 and 0 < mouse[1] <100 and self.numberofcardspicked>0:
							self.submit()#Submits the cards you've picked

					elif self.callbluff==True: #If it is not your turn
						#Tells person how many cards the other person played in their turn
						self.numofcardsplayedblufftxt = self.waitingfnt.render(str(self.numofcardsplayedbluff)+' card played prior', 1, (0,0,0))
						self.screen.blit(self.numofcardsplayedblufftxt,(0,200))
						self.bluffcall=False
						self.firstbluff=False

						pygame.draw.rect(self.screen, [255,100,100], (0,340,(self.width/2), 310))
						pygame.draw.rect(self.screen, [125,255,0], ((self.width/2), 340, (self.width/2), 310))

						if 0 < mouse[0] < (self.width/2) and 340 < mouse[1] <650:
							pygame.draw.rect(self.screen, [255,0,0], (0,340,(self.width/2), 310))

							if click[0]: #Call Bluff
								#Send number of cards you sent, need rank.
								correct=0
								for x in range(4):
									if self.pickbluff["pick"+str(self.currentrank)][x]==1:
										correct+=1

								if correct==self.numofcardsplayedbluff: #Lost bluff, add cards to your deck, other stats the same
									for x in self.turnin:
										self.suiteranks.append(x)
										self.turnin.remove(x)
									self.dealout2=True
									self.deal_out()
									self.bluffcall=False
									self.firstbluff=True
									#bluff=False
									#Sends an empty list to everybody
									connection.Send({"action": "lostbluff", "bluff": self.turnin, "player": self.playernumber})

								elif correct!=self.numofcardsplayedbluff: #Won Bluff: Add list to other person, keep yous
									connection.Send({"action": "wonbluff", "bluff": self.turnin, "player": self.playernumber})
									self.turnin=[]
									self.bluffcall=True
									self.firstbluff=True

								self.currentpile=0
								connection.Send({"action": "updatenumplayedcards", "num": self.currentpile})
								#Makes it your turn and increase rank by one
								if self.currentrank<13:
									self.currentrank+=1
								elif self.currentrank==13:
									self.currentrank=1
								
								#connection.Send({"action": "blufftext", "bluff": self.bluffcall, "onebluff": self.firstbluff})
								connection.Send({"action": "currentrank", "rank": self.currentrank})
								self.my_turn=True
								self.callbluff=False
								
						#No bluff, proceed, increase rank
						elif (self.width/2) < mouse[0] <self.width and 340 < mouse[1] < 650:
							pygame.draw.rect(self.screen, [173,255,47], ((self.width/2), 340, (self.width/2), 310))
							if click[0]: #Becomes your turn if you proceed
								self.my_turn=True
								self.callbluff=False
								if self.currentrank<13:
									self.currentrank+=1
								elif self.currentrank==13:
									self.currentrank=1
								connection.Send({"action": "currentrank", "rank": self.currentrank})
						self.screen.blit(self.callblufftxt, (165,475))
						self.screen.blit(self.proceedtxt, (770, 475))


					else:
						self.screen.blit(self.waitingforturntxt,(400,400))

				pygame.display.update()


	def submit(self):
		#Submit the cards you selected
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if click[0]:
			if self.my_turn==True:
				#Below line helps determines if the person is bluffing
				connection.Send({"action": "checkbluff", "pickarray": self.pick, "player": self.playernumber})
				for x in range(1,14):
					for y in range(4):
						if self.pick["pick"+str(x)][y]==1:
							self.turnin.append(self.card["cardrank"+str(x)][y][0])
							self.pick["pick"+str(x)][y]=0
							self.deck1.remove(self.card["cardrank"+str(x)][y][0])
							del self.card["cardrank"+str(x)][y][0]
							self.currentpile+=1
					self.deal_out()
					self.cardshow11, self.cardshow21, self.cardshow22,self.cardshow31, self.cardshow32 = False, False, False, False, False
					self.cardshow33, self.cardshow41, self.cardshow42, self.cardshow43, self.cardshow44 = False, False, False, False, False
			#Sends number of cards played in a turn
			connection.Send({"action": "numofcardsplayedinturn", "numplayedcards": self.numberofcardspicked})#I picked and played this many

			connection.Send({"action": "numplayedcards", "numplayedcards": self.currentpile})#Number of cards in pil
			connection.Send({"action": "playedcardspile", "playedcards": self.turnin})#Strings in list
			connection.Send({"action": "turnchange", "turn": True})#Changes Turn


	def deckcreate(self): #Creates deck
	#Imports cards and create a shuffled deck
		for x in range(1, 14):
			clubs = "clubs"+str(x)
			self.fulldeck[clubs] = pygame.image.load("images/cards/clubs/"+str(x)+"_of_clubs.png")

			spades = "spades"+str(x)
			self.fulldeck[spades] = pygame.image.load("images/cards/spades/"+str(x)+"_of_spades.png")

			hearts = "hearts"+str(x)
			self.fulldeck[hearts] = pygame.image.load("images/cards/hearts/"+str(x)+"_of_hearts.png")

			diamonds = "diamonds"+str(x)
			self.fulldeck[diamonds] = pygame.image.load("images/cards/diamonds/"+str(x)+"_of_diamonds.png")

	def deal_out(self): #Sorts deck into 13 numbers, server side code

		if self.initialdealout==True:
			for x in range(1,27):
				y = random.choice(self.suiteranks)
				self.deck1.append(y)
				self.suiteranks.remove(y)
		#After every bluff call, this happens
		if self.dealout2==True:
			print(self.suiteranks)
			for x in self.suiteranks:
				y = random.choice(self.suiteranks)
				self.deck1.append(y)
				self.suiteranks.remove(y)
		#got a new deck called deck 1 with a bunch of keys
		self.dealout2=False
		self.initialdealout=False
		self.countmake = dict.fromkeys(['count1', 'count2', 'count3', 'count4', 'count5', 'count6', 'count7', 'count8', 'count9', 'count10', 'count11', 'count12', 'count13'], 0)
		self.card={'cardrank1':[[],[],[],[]], 'cardrank2':[[],[],[],[]], 'cardrank3':[[],[],[],[]], 'cardrank4':[[],[],[],[]], 'cardrank5':[[],[],[],[]], 'cardrank6':[[],[],[],[]], 'cardrank7':[[],[],[],[]], 'cardrank8':[[],[],[],[]], 'cardrank9':[[],[],[],[]], 'cardrank10':[[],[],[],[]], 'cardrank11':[[],[],[],[]], 'cardrank12':[[],[],[],[]], 'cardrank13':[[],[],[],[]]}
		for x in range(len(self.deck1)): #length 26
			for y in range(1,14): #13 ranks clubs
				if self.deck1[x] in ("clubs"+str(y), "spades"+str(y), "hearts"+str(y), "diamonds"+str(y)):
					#self.card["cardrank"+str(y)].append(self.deck1[x])#orig

					if len(self.card["cardrank"+str(y)][0])==0:#new
						self.card["cardrank"+str(y)][0].append(self.deck1[x])
						self.countmake['count'+str(y)]=0

					elif len(self.card["cardrank"+str(y)][1])==0:
						self.card["cardrank"+str(y)][1].append(self.deck1[x])
						self.countmake['count'+str(y)]=1

					elif len(self.card["cardrank"+str(y)][2])==0:
						self.card["cardrank"+str(y)][2].append(self.deck1[x])
						self.countmake['count'+str(y)]=2

					elif len(self.card["cardrank"+str(y)][3])==0:
						self.card["cardrank"+str(y)][3].append(self.deck1[x])
						self.countmake['count'+str(y)]=3

		
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
		pygame.display.update()

		

	def button(self, event): #message, x location, y location, width, height, inactive color, active color, action
		#What happens when you're in the menu, draw circle number button
		if self.my_turn==True:
			pressed = False
			mouse = pygame.mouse.get_pos()
			click = pygame.mouse.get_pressed() #Gets data from mouse press (left right click)
			top_length = 5
			for x in range(1,8):
				if (top_length+150) > mouse[0] > top_length and (self.height-300)+150 > mouse[1] > (self.height-300): #if mouse coord is in range of x value and y value of the created box, do what follows
					self.screen.blit(self.redrank[x-1], (top_length,(self.height-300)))
					if event.type == pygame.MOUSEBUTTONDOWN:
						self.pressedrankbutton=True
						self.show_rankcard(x)
				top_length+=160

			top_length = 80
			for x in range(8,14):
				if (top_length+150) > mouse[0] > top_length and (self.height-150)+150 > mouse[1] > (self.height-150): #if mouse coord is in range of x value and y value of the created box, do what follows
					self.screen.blit(self.redrank[x-1], (top_length,(self.height-150)))
					if event.type == pygame.MOUSEBUTTONDOWN:
						self.pressedrankbutton=True
						self.show_rankcard(x)
				top_length+=160

	def show_rankcard(self, number): 
	#Displays card when you click number, new game loop
		while self.pressedrankbutton==True:
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
							for y in range(4):
								for card in self.card["cardrank"+str(x)][y]:
									
									self.nums["num"+str(x)+str(cardnumber)]=True
									if self.nums["num"+str(x)+str(cardnumber)]==True:
										self.screen.blit(self.fulldeck[card], (wide, high))
										wide+=250

									cardnumber+=1
								#print(self.countmake['count'+x])
							number_of_cardsinitial = int(self.countmake['count'+str(x)])+1 
								#number_of_cardsinitial = len(self.card["cardrank"+str(x)][y])
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
								pygame.display.update()
				
					if 965 < mouse[0] and 590 < mouse[1]:
						pygame.draw.rect(self.screen, self.red, (920,575,200,75))  #start, wide, height
						self.screen.blit(self.exit, (965, 590))
						if event.type == pygame.MOUSEBUTTONDOWN:
							
							self.pressedrankbutton=False
							self.Loop() 
							pygame.display.update()

					pygame.display.update()

	def mousecheck(self, number_of_cards, number):		
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		#Check to see if you click a card or not. Number of cards got passed through
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

		
	def win(self):
		if len(self.deck1)==0 and self.my_turn==False:
			self.blit(self.winner,(0,0))
			sleep(5)
		exit()
	
	def serverstuff(self): #Experimental
		connection.Pump()
		self.Pump()
		connection.Send({"action": "myaction", "blah": 123, "things": [3, 4, 3, 4, 7]})
	


server = 'localhost'
port = 31425
# init the listener
listener = Listener('10.24.10.137', 9999)

listener.intro_screen()



