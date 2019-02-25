
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here


        #for fact in self.gm.kb.facts:
        #    print(fact.statement)

        if self.currentState.state == self.victoryCondition:
            return True

        if self.gm.getMovables() != False:
            if self.currentState.children == []:
                self.get_children()
            while self.currentState.nextChildToVisit < len(self.currentState.children):
                if self.currentState.children[self.currentState.nextChildToVisit] not in self.visited:
                    break
                else:
                    self.currentState.nextChildToVisit += 1
            while self.currentState.children == [] or self.currentState.nextChildToVisit > len(self.currentState.children):
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
            if self.currentState.nextChildToVisit < len(self.currentState.children) and self.currentState.children[self.currentState.nextChildToVisit] not in self.visited:
                moveState = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1
                self.gm.makeMove(moveState.requiredMovable)
                self.currentState = moveState
                self.visited[self.currentState] = True


        if self.gm.getGameState() == self.victoryCondition:
            return True
        #print('\n')
        return False
        #return True

    def get_children(self):
        if self.gm.getMovables() != False:
            for moves in self.gm.getMovables():
                self.gm.makeMove(moves)
                state = self.gm.getGameState()
                self.gm.reverseMove(moves)
                childstate = GameState(state, self.currentState.depth + 1, moves)
                childstate.parent = self.currentState
                if childstate in self.currentState.children:
                    continue
                else:
                    self.currentState.children.append(childstate)


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.statelist = []

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        #print('\n\n')
        #print(self.gm.getGameState())
        #print(self.victoryCondition)
        if self.gm.getGameState() == self.victoryCondition:
            return True
        #print(self.statelist)
        if self.statelist == []:
            self.initialization()

        #print('-----begin-------')
        #print(self.statelist[0])
        self.gm.makeMove(self.statelist[0])
        del self.statelist[0]
        #print(self.gm.getGameState())
        #for stats in self.statelist:
            #print(stats)
        #print('------end-------')

        #self.currentState = self.gm.getGameState()




        if self.gm.getGameState() == self.victoryCondition:
            return True
        #print('\n')
        return False

    def get_children(self):
        if self.gm.getMovables() != False:
            for moves in self.gm.getMovables():
                self.gm.makeMove(moves)
                state = self.gm.getGameState()
                self.gm.reverseMove(moves)
                childstate = GameState(state, self.currentState.depth + 1, moves)
                childstate.parent = self.currentState
                if childstate in self.currentState.children:
                    continue
                else:
                    self.currentState.children.append(childstate)

    def initialization(self):
        while self.gm.getMovables() != False and self.currentState.state != self.victoryCondition:
            if self.currentState.children == []:
                self.get_children()
            while self.currentState.nextChildToVisit < len(self.currentState.children):
                if self.currentState.children[self.currentState.nextChildToVisit] not in self.visited:
                    break
                else:
                    self.currentState.nextChildToVisit += 1
            while self.currentState.children == [] or self.currentState.nextChildToVisit > len(self.currentState.children):
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
            if self.currentState.nextChildToVisit < len(self.currentState.children) and self.currentState.children[self.currentState.nextChildToVisit] not in self.visited:
                moveState = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1
                self.gm.makeMove(moveState.requiredMovable)
                self.currentState = moveState
                self.visited[self.currentState] = True

        while self.currentState.parent:
            self.statelist.insert(0, self.currentState.requiredMovable)
            #print("requiredMovable")
            #print(self.currentState.requiredMovable)
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
        #print(self.currentState.state)


                #print(moveState.requiredMovable)
