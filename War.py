import pygame
import random 
from game_engine_war import Game
from game_engine_war import Room
from game_engine_war import TextRectangle
from game_engine_war import GameObject
from game_engine_war import Alarm
#making the list of the players cards global 
global player1Deck
global player2Deck
global topCard

#Create a new game
g = Game(800,600)

#Color
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#load resources 
gameFont = g.makeFont("Arial",30)
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
Joker = g.makeSpriteImage("cards/JOKER.jpg")
playbutton = g.makeSpriteImage("cards/PLAY.jpg")

#Create Rooms
r1 = Room("Game", simpleBackground)
g.addRoom(r1)

r2 = Room("Conclusion", simpleBackground)
g.addRoom(r2)

#classes for game objects
class Card(GameObject):

        def __init__(self, picture, value, suit):
                GameObject.__init__(self, picture)

                #attributes
                self.value = value# 2 - 15
                self.suit = suit #h,d,c,s,j

        def __str__(self):
                return str(self.value) + self.suit


class playerDeck1(GameObject):

        def __init__(self, picture, xPos, yPos):
                GameObject.__init__(self, picture)

                self.rect.x = xPos
                self.rect.y = yPos
                global player1deck

        def __str__(self):

                 s = ""
                 for card in player1Deck:
                         s = s + str(card) + " "
                 s = "player 1 deck:\n" + s + "\n"
                 return s

class playerDeck2(GameObject):

         def __init__(self, picture, xPos, yPos):
                GameObject.__init__(self, picture)

                self.rect.x = xPos
                self.rect.y = yPos
                global player2Deck

         def __str__(self):

                 s = ""
                 for card in player2Deck:
                         s = s + str(card) + " "
                 s = "player 2 deck:\n" + s + "\n"
                 return s

class PlayButton(GameObject):

        def __init__(self, picture, xPos, yPos):
                GameObject.__init__(self, picture)

                self.rect.x = xPos
                self.rect.y = yPos
                #Importing the player2Deck and making it a self
                global player2Deck
                global player1Deck
                global topCard
                self.topCard = topCard
                # Creating the list of discard piles to store the values
                self.player1DiscardPile = []
                self.player2DiscardPile = []
                #Create an Alarm
                self.timer1 = Alarm()
                self.timer2 = Alarm()
                #create a list to kill the cards
                self.cards_to_kill = []
                #create a list to append war cards
                self.war_cards = []

        def update(self):
                 global player1Deck
                 global player2Deck

                 if self.timer1.finished():
                         r1.addObject(d)

                 if self.timer2.finished():
                         r1.addObject(f)
                         

                 self.checkMousePressedOnMe(event)
                 if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:
                         for cards in self.cards_to_kill:
                                        cards.kill()
                                 
                         card1, card2 = player1Deck[0], player2Deck[0]
                         print("")
                         print("card1 is:",card1)
                         print("card2 is:",card2)
                         diplay = self.displayTheCards(card1, card2)
                         compare = self.comparison(card1, card2)
                         
                         
                         # Print discard piles after the round
                         self.print_discard_pile()
                         self.print_discard_pile2()
                         
                         
                         if len(player1Deck) == 0:
                                 if len(self.player1DiscardPile) == 0:
                                         g.nextRoom()
                                         Conclusion = TextRectangle("Player 2 has won the game", 200, 350, gameFont, RED)
                                         r2.addObject(Conclusion)
                                 else:
                                         d.kill()
                                         player1Deck = self.player1DiscardPile.copy()
                                         self.player1DiscardPile = []
                                         random.shuffle(player1Deck)
                                         dp1.kill()
                                         self.timer1.setAlarm(1000)

                         if len(player2Deck) == 0:
                                 if len(self.player2DiscardPile) == 0:
                                         g.nextRoom()
                                         Conclusion = TextRectangle("Player 1 has won the game", 200, 350, gameFont, RED)
                                         r2.addObject(Conclusion)
                                 else:
                                         f.kill()
                                         player2Deck = self.player2DiscardPile.copy()
                                         self.player2DiscardPile = []
                                         random.shuffle(player2Deck)
                                         dp2.kill()
                                         self.timer2.setAlarm(1000)  
                                 

                         self.mouseHasPressedOnMe = False

                

        def comparison(self, card1, card2):

                if card1.value > card2.value:
                        self.player1DiscardPile.append(card1)
                        self.player1DiscardPile.append(card2)
                        r1.addObject(dp1)
                        roundResult.setText("Player 1 wins round")

                if card2.value > card1.value: 
                        self.player2DiscardPile.append(card1)
                        self.player2DiscardPile.append(card2)
                        r1.addObject(dp2)
                        roundResult.setText("Player 2 wins round")

                if card1.value == card2.value or card2.value == card1.value:
                        roundResult.setText("WAR!")
                        war = self.War()
                        displayTop = self.displayTopCard()
                        diplaying = self.displayWar(card1, card2)


        def displayTheCards(self, card1, card2):
            # Remove the old cards from the display
            card1.kill()
            card2.kill()
            # Check if the decks are not empty before accessing the first element
            if player1Deck:
                card1 = player1Deck[0]
                del player1Deck[0]
                print(d)
                card1.rect.x = 500
                card1.rect.y = 100
                r1.addObject(card1)

            if player2Deck:
                card2 = player2Deck[0]
                del player2Deck[0]
                print(f)
                card2.rect.x = 500
                card2.rect.y = 400
                r1.addObject(card2)


        def War(self):

                # confirming to have enough cards for war
                if len(player1Deck) <= 4:
                        d.kill()
                        random.shuffle(self.player1DiscardPile)
                        #making it so the oringinal cards in the deck stay
                        player1Deck.extend(self.player1DiscardPile.copy())
                        self.player1DiscardPile = []
                        dp1.kill()
                        self.timer1.setAlarm(1000)
                        print(d)

                if len(player2Deck) <= 4:
                        f.kill()
                        random.shuffle(self.player2DiscardPile)
                        #making it so the oringinal cards in the deck stay
                        player2Deck.extend(self.player2DiscardPile.copy())
                        self.player2DiscardPile = []
                        dp2.kill()
                        self.timer2.setAlarm(1000)
                        print(f)

        def displayTopCard(self):
                #displaying the top cards for war
                # Create instances of the Card class for war cards
                for i in range(1,4):
                        fcard = Card(topCard, 0, 0)
                        fcard.rect.x = 500
                        fcard.rect.y = 100 + (i*20)
                        r1.addObject(fcard)
                        self.cards_to_kill.append(fcard)

                for i in range(1,4):
                        fcard2 = Card(topCard, 0, 0)
                        fcard2.rect.x = 500
                        fcard2.rect.y = 400 + (i*20)
                        r1.addObject(fcard2)
                        self.cards_to_kill.append(fcard2)
                
        def print_discard_pile(self):
                print("Discard Pile 1:")
                for card in self.player1DiscardPile:
                        print(str(card))
                        
        def print_discard_pile2(self):
                print("Discard Pile 2:")
                for card in self.player2DiscardPile:
                        print(str(card))


        def displayWar(self, card1, card2):

                if len(player1Deck) < 4:
                        g.nextRoom()
                        Conclusion = TextRectangle("Player 2 has won the game (Player 1 couldn't continue war)", 100, 300, gameFont, RED)
                        r2.addObject(Conclusion)
                        return

                if len(player2Deck) < 4:
                        g.nextRoom()
                        Conclusion = TextRectangle("Player 1 has won the game (Player 2 couldn't continue war)", 100, 300, gameFont, RED)
                        r2.addObject(Conclusion)
                        return

    # naming the 4 cards for each decks and displaying and appending into list
                self.war_cards.append(card1)
                self.war_cards.append(card2)

                tcard1 = player1Deck[0]
                self.war_cards.append(tcard1)
                tcard2 = player1Deck[1]
                self.war_cards.append(tcard2)
                tcard3 = player1Deck[2]
                self.war_cards.append(tcard3)
                dcard1 = player1Deck[3]
                self.war_cards.append(dcard1)
                dcard1.rect.x = 500
                dcard1.rect.y = 180

                bcard1 = player2Deck[0]
                self.war_cards.append(bcard1)
                bcard2 = player2Deck[1]
                self.war_cards.append(bcard2)
                bcard3 = player2Deck[2]
                self.war_cards.append(bcard3)
                dcard2 = player2Deck[3]
                self.war_cards.append(dcard2)
                dcard2.rect.x = 500
                dcard2.rect.y = 480

    # Remove war cards from decks
                for _ in range(4):
                        del player1Deck[0]
                        del player2Deck[0]

    # Display final battle cards
                r1.addObject(dcard1)
                self.cards_to_kill.append(dcard1)
                r1.addObject(dcard2)
                self.cards_to_kill.append(dcard2)

    # Compare final cards
                if dcard1.value > dcard2.value:
                        self.player1DiscardPile.extend(self.war_cards)
                        self.war_cards = []
                        r1.addObject(dp1)
                        roundResult.setText("Player 1 wins WAR")

                elif dcard2.value > dcard1.value:
                        self.player2DiscardPile.extend(self.war_cards)
                        self.war_cards = []
                        r1.addObject(dp2)
                        roundResult.setText("Player 2 wins WAR")
                else:
                        for cards in self.cards_to_kill:
                                cards.kill()
                        roundResult.setText("WAR continues!")
                        self.anotherWar(dcard1, dcard2)

        def anotherWar(self, gcard1, gcard2):
                #checking for enough cards
                self.War()
                #relocating the cards
                gcard1.rect.x = 500
                gcard1.rect.y = 100
                r1.addObject(gcard1)
                
                
                gcard2.rect.x = 500
                gcard2.rect.y = 400
                r1.addObject(gcard2)
                #display the top cards
                self.displayTopCard()
                diplaying = self.displayWar(gcard1, gcard2)             
                         
                        
                                           
#Initialize the game objects
mainDeck1 = TextRectangle("Player 1 deck", 8, 10, gameFont, RED)
r1.addObject(mainDeck1)

mainDeck2 = TextRectangle("Player 2 deck", 8, 300, gameFont, RED)
r1.addObject(mainDeck2)

displayCard1 = TextRectangle("Player 1's card drawn", 480, 50, gameFont, RED)
r1.addObject(displayCard1)

displayCard2 = TextRectangle("Player 2's card drawn", 480, 350, gameFont, RED)
r1.addObject(displayCard2)

discardpile1 = TextRectangle("Discard Pile", 200, 50, gameFont, RED)
r1.addObject(discardpile1)

discardpile2 = TextRectangle("Discard Pile", 200, 350, gameFont, RED)
r1.addObject(discardpile2)

# Declare who won the round
roundResult = TextRectangle("", 480, 275, gameFont, RED)
r1.addObject(roundResult)

#appending cards in the deck
deck = []
for i in range(0,len(diamondPics)):
        c = Card(diamondPics[i], (i + 2), "D")
        deck.append(c)
                        
for i in range(0,len(heartPics)):
        c = Card(heartPics[i], (i + 2), "H")
        deck.append(c)
                        
for i in range(0,len(spadePics)):
        c = Card(spadePics[i], (i + 2), "S")
        deck.append(c)
                        
for i in range(0,len(clubPics)):
        c = Card(clubPics[i], (i + 2), "C")
        deck.append(c)

for i in range(0,2):
        c = Card(Joker, 15, "J")
        deck.append(c)

random.shuffle(deck)
player1Deck = []
player2Deck = []
j = (len(deck))/2

# distributing the cards
for i in range(0,len(deck)):
        if i < j:
                player1Deck.append(deck[i])
        else:
                player2Deck.append(deck[i])

                
d = playerDeck1(topCard, 8, 50)
r1.addObject(d)

f = playerDeck2(topCard, 8, 350)
r1.addObject(f)

play = PlayButton(playbutton, 250, 240)
r1.addObject(play)

dp1 = playerDeck1(topCard, 200, 100)


dp2 = playerDeck2(topCard, 200, 400)


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
