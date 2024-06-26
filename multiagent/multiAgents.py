# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        pacman_position = list(successorGameState.getPacmanPosition())                             #Retrieve Pacman's current position as a list
        minimum_distance = float('inf')                                                            #Initialize the minimum distance to an extremely high value
        food_positions = currentGameState.getFood().asList()                                       #Get the current state of the food and convert it to a list of food positions
        for food_pos in food_positions:                                                            #Iterate over each food position to find the closest one to Pacman
          distance = manhattanDistance(food_pos, pacman_position)
          if distance < minimum_distance:
            minimum_distance = distance
        minimum_distance = -minimum_distance                                                       #Negate the minimum distance
        for ghost_state in newGhostStates:                                                         #Iterate over each ghost state
          if ghost_state.scaredTimer == 0 and ghost_state.getPosition() == tuple(pacman_position): #Check if the ghost is not scared and is at Pacman's position
            return -float('inf')                                                                   #Return a very low value if the ghost is at Pacman's position
        if action == 'Stop':                                                                       #Check if the action is to stop
          return -float('inf')                                                                     #Return a very low value if the action is to stop
        return minimum_distance                                                                    #Return the negated minimum distance


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def minimax(agent, depth, gameState):
          if gameState.isLose() or gameState.isWin() or depth == self.depth:                            #Check if the game is over or the maximum depth is reached
            return self.evaluationFunction(gameState)
          
          if agent == 0:                                                                                #maximize for pacman                                                             
            max_utility = float("-inf")                                                                 #Find the maximum utility by recursively calling minimax for each legal action
            for new_state in gameState.getLegalActions(agent):                                          #Iterate over all legal actions for Pacman
              utility = minimax(1, depth, gameState.generateSuccessor(agent, new_state))                #Find the utility for the next agent       
              max_utility = max(max_utility, utility)                                                   #Update the maximum utility
            return max_utility                                                                          #Return the maximum utility
          
          else:                                                                                         #minimize for ghosts
            next_agent = agent + 1
            if gameState.getNumAgents() == next_agent:                                                  #Check if all agents have played          
              next_agent = 0                                                                            #Reset the agent to Pacman        
              depth += 1                                                                                #Increment the depth        
            min_utility = float("inf")                                                                  #Find the minimum utility by recursively calling minimax for each legal action
            for new_state in gameState.getLegalActions(agent):                                          #Iterate over all legal actions for the ghost
              utility = minimax(next_agent, depth, gameState.generateSuccessor(agent, new_state))       #Find the utility for the next agent
              min_utility = min(min_utility, utility)                                                   #Update the minimum utility
            return min_utility                                                                          #Return the minimum utility
        maximum = float("-inf")                                                                         #Initialize the maximum utility to an extremely low value
        action = Directions.WEST                                                                        #Initialize the action to a random direction
        for agent_state in gameState.getLegalActions(0):                                               
          utility = minimax(1, 0, gameState.generateSuccessor(0, agent_state))                          #Find the utility for each legal action
          if utility > maximum or maximum == float("-inf"):                                             #Update the maximum utility and action
            maximum = utility 
            action = agent_state 

        return action                                                                                   #Return the action with the maximum utility
    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

