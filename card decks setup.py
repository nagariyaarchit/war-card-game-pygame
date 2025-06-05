import pygame
import random 
from game_engine_war import Game
from game_engine_war import Room
from game_engine_war import TextRectangle
from game_engine_war import GameObject 

#Create a new game
g = Game(800,600)

#Color
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#load resources 
gameFont = g.makeFont("Arial",34)
simpleBackground = g.makeBackground(BLACK)
diamondPics = []
for i in range (2,15):
        diamondPics.append(g.makeSpriteImage("cards/DIAMONDS" + str(i) + ".jpg"))
heartPics = []
for i in range(2,15):
        heartPics.append(g.makeSpriteImage("cards/HEARTS" + str(i) + ".jpg"))
spadePics = []
for i in range(2,15):
        spadePics.append(g.makeSpriteImage("cards/SPADES" + str(i) + ".jpg"))
clubPics = []
for i in range(2,15):
        clubPics.append(g.makeSpriteImage("cards/CLUBS" + str(i) + ".jpg"))

topCard = g.makeSpriteImage("cards/TOP.jpg")
returnbutton = g.makeSpriteImage("Returnbutton.jpg")


#Create Rooms
r1 = Room("Game", simpleBackground)
g.addRoom(r1)

#Classes for game objects
class Card(GameObject):

        def __init__(self, picture, value, suit):
                GameObject.__init__(self, picture)

                #attributes
                self.value = value# 2 - 14
                self.suit = suit #h,d,c,s

        def update(self):

                self.checkMousePressedOnMe(event)

                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:

                        p.playCard(self)
                        played.addCard(self)

                        print(d)
                        print(p)
                        print(played)
                        self.mouseHasPressedOnMe = False

        def __str__(self):
                return str(self.value) + self.suit

class CardDeck(GameObject):

        def __init__(self, picture, xPos, yPos):
                GameObject.__init__(self, picture)

                self.rect.x = xPos
                self.rect.y = yPos

                self.deck = []

                for i in range(0,len(diamondPics)):
                        c = Card(diamondPics[i], (i + 2), "D")
                        self.deck.append(c)
                        
                for i in range(0,len(heartPics)):
                        c = Card(heartPics[i], (i + 2), "H")
                        self.deck.append(c)
                        
                for i in range(0,len(spadePics)):
                        c = Card(spadePics[i], (i + 2), "S")
                        self.deck.append(c)
                        
                for i in range(0,len(clubPics)):
                        c = Card(clubPics[i], (i + 2), "C")
                        self.deck.append(c)

                random.shuffle(self.deck)


        def update(self):

                self.checkMousePressedOnMe(event)

                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:
                        
                        if p.hasFreeSpot():
                                card = self.deal()
                                p.takeCard(card)
                        print(d)
                        print(p)
                        self.mouseHasPressedOnMe = False 

        def deal(self):

                if len(self.deck) > 0:

                        c = self.deck[0]
                        del self.deck[0]
                        if len(self.deck) == 0:
                                self.kill()
                                restock = AddtoDeckButton(returnbutton, 300, 400)
                                r1.addObject(restock)
                return c

        def add(self, card):
                self.deck.append(card)
        
        def __str__(self):

                s = ""
                for card in self.deck:
                        s = s + str(card) + " "       
                s = "Deck:\n" + s + "\n"
                return s

class Player(GameObject):

        def __init__(self, handsize, xPos, yPos):
                GameObject.__init__(self)

                self.startingX = xPos
                self.startingY = yPos

                #attributes
                self.maxCards = handsize
                self.hand = []
                self.cardsInHand = 0

        def hasFreeSpot(self):

                if self.cardsInHand < self.maxCards:
                        return True
                else:
                        return False

        def takeCard(self, card):

                self.hand.append(card)

                card.rect.x = self.startingX + (4 + card.rect.width) * self.cardsInHand
                card.rect.y = self.startingY
                r1.addObject(card)
                
                self.cardsInHand = self.cardsInHand + 1

        def playCard(self, card):

                for c in self.hand:
                        c.kill()

                self.hand.remove(card)
                self.cardsInHand = self.cardsInHand - 1

                for i in range (0, self.cardsInHand):
                        self.hand[i].rect.x = self.startingX + (i * (card.rect.width + 4))
                        self.hand[i].rect.y = self.startingY
                        r1.addObject(self.hand[i])

        def __str__(self):

                s = ""
                for card in self.hand:
                        s = s + str(card) + " "       
                s = "Player:\n" + s + "\n"
                return s

class PlayedPile(GameObject):

        def __init__(self, xPos, yPos):
                GameObject.__init__(self)

                self.playedCards = []

                self.rect.x = xPos
                self.rect.y = yPos

        def addCard(self, card):
                self.playedCards.append(card)

                self.image = card.image

        def removeCards(self):

                keep = self.playedCards[len(self.playedCards)-1]
                self.playedCards.remove(keep)

                for card in self.playedCards:
                        d.add(card)

                random.shuffle(d.deck)

                self.playedCards.clear()

                self.playedCards.append(keep)

        def __str__(self):

                s = ""
                for card in self.playedCards:
                        s = s + str(card) + " "       
                s = "Played:\n" + s + "\n"
                return s

class AddtoDeckButton(GameObject):

        def __init__(self, picture, xPos, yPos):
                GameObject.__init__(self, picture)

                self.rect.x = xPos
                self.rect.y = yPos

        def update(self):

                self.checkMousePressedOnMe(event)

                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:

                        played.removeCards()
                        r1.addObject(d)
                        print(d)
                        print(played)
                        self.kill()

#Initialize the game objects
playerHandLabe1 = TextRectangle("Players hand - Click Card to play", 8, 0, gameFont, RED)
deckLabe1 = TextRectangle("Deck - Click Card To Deal", 8, 200, gameFont, RED)
playedLabe1 = TextRectangle("Played cards", 8, 400, gameFont, RED)


r1.addObject(playerHandLabe1)
r1.addObject(deckLabe1)
r1.addObject(playedLabe1)

d = CardDeck(topCard, 8, 250)
r1.addObject(d)

p = Player(5, 8, 50)

played = PlayedPile(8,450)
r1.addObject(played)

print(d)

#Initialize the game
g.start()

#Game Loop
while g.running:

	#Limit the game execution framerate
	dt = g.clock.tick(60)

	#Check for Events
	for event in  pygame.event.get():

		#Quit if user clicks[x]
		if event.type == pygame.QUIT:
			g.stop()

	#Update the gamestate of all the objects
	g.currentRoom().updateObjects()

	#Render the background to the window surface
	g.currentRoom().renderBackground(g)

	#Render the object images to the background
	g.currentRoom().renderObjects(g)

	#Draw everything on the screen
	pygame.display.flip()

pygame.quit()
