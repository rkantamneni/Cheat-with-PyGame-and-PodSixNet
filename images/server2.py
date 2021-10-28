#Cheat Card Game by Revant Kantamneni

#Variable assingnments
import pygame
# import network modules
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
# random module to randomize the initial ball direction
from random import randint
import random
from time import sleep
import sys
pygame.init()

# class representing a sigle connection with a client
# this can also represent a player

#Gets called whenever client sends message to server
class ClientChannel(Channel):
	def __init__(self, *args, **kwargs):
		Channel.__init__(self, *args, **kwargs)

#Will always be called
	def Network(self, data): #Whenever the client does connection.Send(mydata), the Network() method will be called. 
		print('It works man')
#Reflection of what is called in the client
	def Network_otherplayercanstart(self, data):
		self._server.SendToAll({'action': 'otherplayerscanstartnow', 'startothers': True})

	def Network_turnchange(self,data):
		change = data['turn']
		self._server.SendToAll({'action': 'turnchangeclient', 'turnclient': change})

	def Network_numplayedcards(self, data):
		number=data['numplayedcards']
		self._server.SendToAll({'action': 'updatenumplayedcards', 'num': number})

	def Network_playedcardspile(self,data):
		pile=data['playedcards']
		self._server.SendToAll({'action': 'updateplayedcards', 'turnincards': pile})

	def Network_playerdisconnect(self, data):
		self._server.SendToAll({'action': 'decreaseplayernum', 'playernum': data['num']})
	def Network_numofcardsplayedinturn(self, data):
		self._server.SendToAll(data)
	def Network_currentrank(self, data):
		self._server.SendToAll(data)
	def Network_checkbluff(self,data):
		self._server.SendToSpecificPerson(data)

	def Network_lostbluff(self, data):
		self._server.SendToSpecificPerson(data)

	def Network_wonbluff(self, data):
		self._server.SendToSpecificPerson(data)
	def Network_blufftext(self, data):
		self._server.SendToSpecificPerson(data)

# class representing the server
class MyServer(Server):
	channelClass = ClientChannel
	
	# Start the server, runs code once in init
	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		
		self.playernumber=0
		self.players=[]

		#Deck with imported pictures, 52 cards
		self.dicdeck ={} #Dictionary of image directory
		self.suiteranks=[] #List of keys of all cards
		
		# adresse and port at which server is started
		adresse, port = kwargs['localaddr']
		self.player1keylist=[]
		self.player2keylist=[]

		self.shuffle()
		
		print ('Server started at', adresse, 'at port', str(port))
		print ('Now you can start the clients')

	# function called on every new client connection
	def SendToAll(self, data):
		[p.Send(data) for p in self.players]

	def SendToSpecificPerson(self, data):
		if data['player']==1:
			self.players[1].Send(data)

		if data['player']==2:
			self.players[0].Send(data)


	def SendToAllDisconnect(self,data):#Disconnect everybody
		num = int(data['num'])
		self.playernumber-=1
		del self.players[num-1]
		[p.Send(data) for p in self.players]

	def Connected(self, player, addr): #Called an every new client connection
		self.players.append(player)
		print('Length of players: '+str(len(self.players)))
		self.playernumber+=1
		print(self.playernumber)
		#Player.send only sends it to certain people
		player.Send({'action': 'playernumber', 'playernum': self.playernumber})
		print ('Player'+str(self.playernumber)+'connected at', addr[0], 'at port', addr[1])


		# if there are two player we can start the game
		if len(self.players) == 2:
		 	self.dealout()

	def dealout(self): #Creates two lists with cards sends them to the clients
	#Deterines who has the ace of spades and they go first

		self.players[0].Send({"action": "createplayerdeck", "keylist": self.player1keylist})
		self.players[1].Send({"action": "createplayerdeck", "keylist": self.player2keylist})

		if "spades1" in self.player1keylist:
			self.players[0].Send({'action': 'initialplayerturn', 'playernum': 1})
			self.players[1].Send({'action': 'initialplayerturn', 'playernum': 1})
			print('Spades 1 in 1')

		if "spades1" in self.player2keylist:
			self.players[1].Send({'action': 'initialplayerturn', 'playernum': 2})
			self.players[0].Send({'action': 'initialplayerturn', 'playernum': 2})
			print('Spades 1 in 2')


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


		self.suiteranks =  list(self.dicdeck.keys())#Takes all names and creates a list
		random.shuffle(self.suiteranks)

		for x in range(26):
			self.player1keylist.append(self.suiteranks[x])

		for x in range(26, 52):
			self.player2keylist.append(self.suiteranks[x])
	

	def launch(self):
		while True:
			self.Pump()
			sleep(0.0001)

		


#playercount = input('How many players are playing? Max 2 or 4')
adresse = 'localhost'
#ask for player numbers as input

# inizialize the server


# if len(sys.argv) != 2:
# 	print ("Usage:", sys.argv[0], "host:port")
# 	print ("e.g.", sys.argv[0], "localhost:31425")
# else:
#host, port = sys.argv[1].split(":")
s = MyServer(localaddr=('localhost', int(9999)))
s.launch()

