import random
import sys
import argparse

# Declare Class to represent a Player
class Player:

    # Initialize the player
    def __init__(self, playerName):        
        self.turnTotal = 0
        self.gameTotal = 0
        self.playerName = playerName

    # Get the players Name
    def getPlayerName(self):
        return str(self.playerName)

    #Gets the players Game Total
    def getGameTotal(self):
        return self.gameTotal

    # Returns the players turn total
    def getTurnTotal(self):
        return self.turnTotal

    # Updates the players turn total
    def updateTurnTotal(self, rollAmount):
        self.turnTotal += rollAmount

    #Ends the players turn. Accepts Boolean indicating whether the turn points shold be added to the players game total. Used when rolling a one
    def endTurn(self, keepPoints):
        if keepPoints == True:
            self.gameTotal += self.turnTotal
        self.turnTotal = 0
        if self.gameTotal >= 100:
            return True

    # Get the users Decision to roll or hold
    def getDecision(self, roll):        

        # Get users choince
        userInput = raw_input('You rolled a ' + str(roll)+ '. Your turn total is ' + str(self.turnTotal) + ', and your game total is ' + str(self.gameTotal) + '. Type r to roll again or h to hold -->')

        #Keep requesting a decision until a valid one is entered
        while userInput != 'h' and userInput != 'r':
           userInput = raw_input('Sorry, that was an invalid entry. Your game total is ' + str(self.gameTotal) + ', your turn total is ' + str(self.turnTotal) + ', and you rolled a ' + str(roll) + '. Type r to roll again or h to hold -->')

        return userInput

# Declare Class to represent the game Die
class Die:

    #Initialize the die to seed the random
    def __init__(self):
        random.seed(0)
    
    # Rolls the die
    def rollDie(self):
        roll = random.randint(1,6)        
        return roll

class Game:

    # Initialize Game and objects. Accepts player count
    def __init__(self, playerCount):
        self.PlayerCount = playerCount
        self.die = Die()
        self.players = []
        self.playerIndex = 0        

    # Creates the game players based on player count
    def createPlayers(self):
        for x in range(0, self.PlayerCount):
            self.players.append(Player('Player #' + str(x + 1)))

    # Returns the game die
    def getGameDie(self):
        return self.die

    # Returns the active player
    def getActivePlayer(self):
        return self.players[self.playerIndex]

    # Iterates to the next player. 
    def iteratePlayer(self):
        if self.playerIndex == len(self.players) - 1:
            self.playerIndex = 0
        else:
            self.playerIndex += 1

    # Iitializes players and prints startup message
    def startGame(self):
        self.createPlayers()
        print 'Game starting...'
        print 'Player #1 is up:'
        
    # Method with game logic
    def playGame(self):
        while True :

            # Roll the die
            roll = self.getGameDie().rollDie()

            # If player rolled a 1
            if roll == 1:
                # End the players turn with out adding turn points
                self.getActivePlayer().endTurn(False)
                # Move to the next player
                self.iteratePlayer()
                # Print message
                print '\nUh Oh!! You rolled a 1 and lost all your turns points. \n\n'+ self.getActivePlayer().getPlayerName() + ' is up!\n'        

            # Else player rolled a valid number
            else:
                # Update the active players turn total
                self.getActivePlayer().updateTurnTotal(roll)
                # Get a decision from the active player
                decision = self.getActivePlayer().getDecision(roll)

                # If player decided to hold
                if decision == 'h':

                    #print points earned this turn
                    print '\nSmart choice!! You scored '+ str(self.getActivePlayer().getTurnTotal())+' points this turn. Your points have been added to your game total!'

                    # End Players Turn and check if they won
                    if self.getActivePlayer().endTurn(True) == True:
                        # Print game won message
                        print '\n\nGame Over!! ' + self.getActivePlayer().getPlayerName() +' won with a score of ' + str(self.getActivePlayer().getGameTotal())
                        # Exit Program
                        sys.exit()
                
                    # Print new game total
                    print 'Your new game total is ' + str(self.getActivePlayer().getGameTotal()) + '.\n'

                    #Switch the player
                    self.iteratePlayer()
                    # Print next players name
                    print self.getActivePlayer().getPlayerName() + ' is up!\n'
            

def main():

    # Add Num Players argument
    parser = argparse.ArgumentParser()
    parser.add_argument("--numPlayers", help="The number of players playing.")
    args = parser.parse_args()

    # Start Game
    game = Game(int(args.numPlayers))
    game.startGame()
    game.playGame()

main()
