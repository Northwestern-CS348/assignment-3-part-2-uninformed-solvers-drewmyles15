from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg1_tuple = ()
        peg1_list = []
        ask1 = parse_input("fact: (on ?X peg1)")
        answer = self.kb.kb_ask(ask1)
        if answer != False:
            for ans in answer.list_of_bindings:
                disk = ans[0].bindings[0].constant.element.split('disk',1)[1]
                peg1_list.append(disk)
            peg1_list.sort()
            for disk in peg1_list:
                peg1_tuple = peg1_tuple + (int(disk),)


        peg2_tuple = ()
        peg2_list = []
        ask2 = parse_input("fact: (on ?X peg2)")
        answer2 = self.kb.kb_ask(ask2)
        if answer2 != False:
            for ans in answer2.list_of_bindings:
                disk = ans[0].bindings[0].constant.element.split('disk',1)[1]
                peg2_list.append(disk)
            peg2_list.sort()
            for disk in peg2_list:
                peg2_tuple = peg2_tuple + (int(disk),)
            #peg2_tuple = peg2_tuple.sort()


        peg3_tuple = ()
        peg3_list = []
        ask3 = parse_input("fact: (on ?X peg3)")
        answer3 = self.kb.kb_ask(ask3)
        if answer3 != False:
            for ans in answer3.list_of_bindings:
                disk = ans[0].bindings[0].constant.element.split('disk',1)[1]
                peg3_list.append(disk)
            peg3_list.sort()
            for disk in peg3_list:
                peg3_tuple = peg3_tuple + (int(disk),)
            #peg3_tuple = peg3_tuple.sort()

        state_tuple = (peg1_tuple,peg2_tuple,peg3_tuple)
        return state_tuple

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        disk = movable_statement.terms[0].term.element
        initial = movable_statement.terms[1].term.element
        goal = movable_statement.terms[2].term.element
        #### Add the disk to the new stack and remove the facts of it being on the old one
        r1 = parse_input("fact: (on " + disk + " " + initial + ")")
        self.kb.kb_retract(r1)
        r2 = parse_input("fact: (isTopofStack " + disk + " " + initial + ")")
        self.kb.kb_retract(r2)
        stat1 = parse_input("fact: (on " + disk +  " " + goal + ")")
        self.kb.kb_assert(stat1)
        stat2 = parse_input("fact: (isTopofStack " + disk +  " " + goal + ")")
        self.kb.kb_assert(stat2)

        ## Determine if any disks are on the initial peg
        ask1 = parse_input("fact: (on ?X " + initial + ")")
        answer = self.kb.kb_ask(ask1)
        if answer == False:     #If no disks are on the initial peg
            empty_stat = parse_input("fact: (isempty " + initial + ")")
            self.kb.kb_assert(empty_stat)
        else:
            disks_on_initial = []
            for ans in answer.list_of_bindings:
                disks_on_initial.append(int(ans[0].bindings[0].constant.element.split('disk',1)[1]))
            ask_top = parse_input("fact: (isTopofStack ?X " + initial + ")")
            top_ans = self.kb.kb_ask(ask_top)
            disks_on_initial.sort()
            if top_ans:
                for ans in top_ans.list_of_bindings:
                    if int(ans[0].bindings[0].constant.element.split('disk',1)[1]) != disks_on_initial[0]:
                        retract = parse_input("fact: (isTopofStack " + ans[0].bindings[0].constant.element + " " + initial + ")")
                        self.kb.kb_retract(retract)
            assert1 = parse_input("fact: (isTopofStack disk" + str(disks_on_initial[0]) + " " + initial + ")")
            self.kb.kb_assert(assert1)

        goal_ask = parse_input("fact: (on ?X " + goal + ")")
        goal_answer = self.kb.kb_ask(goal_ask)
        disks_on_goal = []
        for ans in goal_answer.list_of_bindings:
            disks_on_goal.append(int(ans[0].bindings[0].constant.element.split('disk',1)[1]))
        ask_topg = parse_input("fact: (isTopofStack ?X " + goal + ")")
        top_ansg = self.kb.kb_ask(ask_topg)
        disks_on_goal.sort()
        if top_ansg:
            for ans in top_ansg.list_of_bindings:
                if int(ans[0].bindings[0].constant.element.split('disk',1)[1]) != disks_on_goal[0]:
                    retract = parse_input("fact: (isTopofStack " + ans[0].bindings[0].constant.element + " " + goal + ")")
                    self.kb.kb_retract(retract)

        ask2 = parse_input("fact: (isempty " + goal + ")")
        answer2 = self.kb.kb_ask(ask2)
        if answer2:
            self.kb.kb_retract(ask2)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        #print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        row1_tuple = ()
        row1_list = {}
        ask1 = parse_input("fact: (on ?X ?Y pos1)")
        answer1 = self.kb.kb_ask(ask1)
        if answer1 != False:
            for ans in answer1.list_of_bindings:
                tile = ans[0].bindings[0].constant.element
                if len(tile.split('tile',1)) > 1:
                    tile = int(tile.split('tile',1)[1])
                else:
                    tile = -1
                pos = (ans[0].bindings[1].constant.element).split('pos',1)[1]
                row1_list[int(pos)] = tile
            #print("ROW1: ", len(row1_list))
            for i in range(len(row1_list)):
                val = row1_list[i+1]
                #print(val)
                row1_tuple = row1_tuple + (val,)

        row2_tuple = ()
        row2_list = {}
        ask2 = parse_input("fact: (on ?X ?Y pos2)")
        answer2 = self.kb.kb_ask(ask2)
        if answer2 != False:
            for ans in answer2.list_of_bindings:
                tile = ans[0].bindings[0].constant.element
                if len(tile.split('tile',1)) > 1:
                    tile = int(tile.split('tile',1)[1])
                else:
                    tile = -1
                pos = (ans[0].bindings[1].constant.element).split('pos',1)[1]
                row2_list[int(pos)] = tile
            #print("ROW2: ", len(row2_list))
            for i in range(len(row2_list)):
                val = row2_list[i+1]
                row2_tuple = row2_tuple + (val,)

        row3_tuple = ()
        row3_list = {}
        ask3 = parse_input("fact: (on ?X ?Y pos3)")
        answer3 = self.kb.kb_ask(ask3)
        if answer3 != False:
            for ans in answer3.list_of_bindings:
                tile = ans[0].bindings[0].constant.element
                if len(tile.split('tile',1)) > 1:
                    tile = int(tile.split('tile',1)[1])
                else:
                    tile = -1
                pos = (ans[0].bindings[1].constant.element).split('pos',1)[1]
                row3_list[int(pos)] = tile
            #print("ROW3: ", len(row3_list))
            for i in range(len(row3_list)):
                val = row3_list[i+1]
                row3_tuple = row3_tuple + (val,)
        #print("-----------------------------------------------------------------------------------------------")


        state_tuple = (row1_tuple,row2_tuple,row3_tuple)
        #print(state_tuple)
        return state_tuple



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        tile = movable_statement.terms[0].term.element
        initialX = movable_statement.terms[1].term.element
        initialY = movable_statement.terms[2].term.element
        goalX = movable_statement.terms[3].term.element
        goalY = movable_statement.terms[4].term.element
        r1 = parse_input("fact: (on " + tile + " " + initialX + " " + initialY + ")")
        self.kb.kb_retract(r1)
        stat1 = parse_input("fact: (on " + tile + " " + goalX + " " + goalY + ")")
        self.kb.kb_assert(stat1)
        r2 = parse_input("fact: (on empty " + goalX + " " + goalY + ")")
        self.kb.kb_retract(r2)
        stat2 = parse_input("fact: (on empty " + initialX + " " + initialY + ")")
        self.kb.kb_assert(stat2)


        #for facts in self.kb.facts:
        #    print(facts.statement)

        #print("\n\n")
        ##Need to handle adjacentTo
        '''ask = parse_input("fact: (adjacentTo empty ?tile)")
        answer = self.kb.kb_ask(ask)
        empty_adj = []
        if answer:
            for ans in answer.list_of_bindings:
                adjTile = ans[0].bindings[0].constant.element
                if adjTile != tile:
                    rt = parse_input("fact: (adjacentTo empty " + adjTile + ")")
                    self.kb.kb_retract(rt)
                    #print("RMOVINGGGG")
                    #print(rt)
                    rt1 = parse_input("fact: (adjacentTo " + adjTile + " empty)")
                    self.kb.kb_retract(rt1)
                    empty_adj.append(adjTile)       #All of empty's adjacent tiles'''

        #for facts in self.kb.facts:
        #    print(facts.statement)

        #print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        '''ask1 = parse_input("fact: (adjacentTo " + tile + " ?tile)")
        answer1 = self.kb.kb_ask(ask1)
        if answer1:
            for ans in answer1.list_of_bindings:
                adjTile = ans[0].bindings[0].constant.element
                if adjTile != "empty":
                    stat = parse_input("fact: (adjacentTo empty " + adjTile + ")")
                    self.kb.kb_assert(stat)
                    radj1 = parse_input("fact: (adjacentTo " + tile + " " + adjTile + ")")
                    self.kb.kb_retract(radj1)
                    radj2 = parse_input("fact: (adjacentTo " + adjTile + " " + tile + ")")
                    self.kb.kb_retract(radj2)
        for tiles in empty_adj:
            stat = parse_input("fact: (adjacentTo " + tile + " " + tiles + ")")
            self.kb.kb_assert(stat)'''



    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
