# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 22:42:02 2021

@author: Ali
"""

import random,sys,copy
from optparse import OptionParser
try:
  import psyco
  psyco.full()
except ImportError:
  pass
 
 
class board:
  def __init__(self, list=None,numberOfQueens=8):
    self.n_queens=numberOfQueens  
    if list == None:
      self.board = [[0 for i in range(0,self.n_queens)] for j in range(0,self.n_queens)]
      #Placing queens in random cells in every column
      for i in range(0,self.n_queens):
        #while 1:
          rand_row = random.randint(0,self.n_queens-1)
          rand_col = random.randint(0,self.n_queens-1)
          if self.board[rand_row][i] == 0:
            self.board[rand_row][i] = 1
            #break
  """
  Using this function, we define how to print out the board
  
  """      
  def __repr__(self):
    mstr = ""
    for i in range(0,self.n_queens):
      for j in range(0,self.n_queens):
        mstr = mstr + str(self.board[i][j]) + " "
      mstr = mstr + "\n"
    return (mstr)







 
class queens:
  def __init__(self, numruns, showIntermediateResults, passedboard=None,numberOfQueens=8):
    self.total_n_runs = numruns
    self.all_n_successfull = 0
    self.all_n_steps = 0
    self.showIntermediateResults = showIntermediateResults
    self.n_queens=numberOfQueens
    self.board=passedboard
    self.chessBoard=None
    self.cost=None
    self.all_n_failed=0
    self.StepsToSuccess=0
    self.allSucceedSteps=0
      
  def StartSolvingNQueensProblem(self):
      for i in range(0,self.total_n_runs):
          if self.showIntermediateResults == True:
              print ("_"*50)
              print ("# of Random Board Sample: ",i+1)
              print ("-"*50)
          self.chessBoard = board(None,self.n_queens)
          self.cost = self.CalculateHeuristicCost(self.chessBoard)
          self.SteepestHillClimbing()
 
  def SteepestHillClimbing(self):
    #self.allSucceedSteps=0  
    self.StepsToSuccess=0
    while 1:
      currViolations = self.cost
      self.getBestBoard()
      self.all_n_steps += 1
      #self.succeedSteps+=1
      if currViolations == self.cost: # if current cost is not better than previous cost, exits the loop
        #self.succeedSteps=0
        break
      

      if self.showIntermediateResults == True:
        print ("# of Queens attacking each other: ", self.CalculateHeuristicCost(self.chessBoard))
        print (self.chessBoard)
      
      if self.cost != 0:
          self.StepsToSuccess+=1
         
          
    if self.cost != 0:
      self.all_n_failed+=1
      
      if self.showIntermediateResults == True:
        print ("There is no solution")
    else:
      if self.showIntermediateResults == True:
        print ("Solution found. Number of Steps to reach solution: ",self.StepsToSuccess+1)
      self.allSucceedSteps+= self.StepsToSuccess+1 #we add success by 1 because it starts from 0.
      self.all_n_successfull += 1
    return self.cost

  def getBoard(self):
      return self.chessBoard
 
  def printstats(self):
    print("\n")
    print("-"*20 + "Final Evaluation" +"-"*20)
    print ("Total iterations: ", self.total_n_runs)
    print ("All Steps (in which cost is computed): ", self.all_n_steps)

    print ("-"*10 + "Success Record" +"-"*10)
    print ("Total Successful iterations: ", self.all_n_successfull)
    print ("Total successful Steps: ", self.allSucceedSteps)
    print ("Success Avg on iteration. : ", float(self.all_n_successfull)/float(self.total_n_runs))
    print ("Success Avg on all steps: ", float(self.allSucceedSteps)/float(self.all_n_steps))

    print ("-"*10 + "Fail Record" +"-"*10)    
    print ("Total Fails: ", self.all_n_failed)
    print ("Total Failed Steps: ", self.all_n_steps-self.allSucceedSteps)
    print ("Fail Avg on iteration. : ", self.all_n_failed /float(self.total_n_runs))
    print ("Fail Avg on all steps: ", (self.all_n_steps-self.allSucceedSteps)/float(self.all_n_steps))

  """
  This function calculates the number of attacks happening for each cell 
  once the cell contains a queen. These attacks can be directly or indirectly  
  """
  def CalculateHeuristicCost(self, tboard):

    totalhcost = 0
    totaldcost = 0
    for i in range(0,self.n_queens):
      for j in range(0,self.n_queens):
        
        if tboard.board[i][j] == 1: #if this node is a queen, calculate all dangers
          totalhcost -= 2 #subtract 2 so don't count self sideways and vertical
          for k in range(0,self.n_queens):
            if tboard.board[i][k] == 1:
              totalhcost += 1
            if tboard.board[k][j] == 1:
              totalhcost += 1
          
          k, l = i+1, j+1 #calculate diagonal dangers for down-right moves
          while k < self.n_queens and l < self.n_queens:
            if tboard.board[k][l] == "1":
              totaldcost += 1
            k +=1
            l +=1
          k, l = i+1, j-1
          while k < self.n_queens and l >= 0: #calculate diagonal dangers for up-left moves
            if tboard.board[k][l] == 1:
              totaldcost += 1
            k +=1
            l -=1
          k, l = i-1, j+1
          while k >= 0 and l < self.n_queens: #calculate diagonal dangers for down-left moves
            if tboard.board[k][l] == 1:
              totaldcost += 1
            k -=1
            l +=1
          k, l = i-1, j-1
          while k >= 0 and l >= 0: #calculate diagonal dangers for up-right moves
            if tboard.board[k][l] == 1:
              totaldcost += 1
            k -=1
            l -=1
    return (totaldcost + totalhcost) #According to the textbookfor Heuristic function we need both direct and indirect dangers
 #/2
  """
  This function moves every queen to in its column and recalculate the corresponding cost of the new board.
  Finally returns the lowest cost board as well as its corresponding cost.

  """

  def getBestBoard(self):
    lowestCost = self.CalculateHeuristicCost(self.chessBoard)
    lowestBoard = self.chessBoard
    for queenRow in range(0,self.n_queens): #Move one queen in its column and find the corresponding heuristic cost
      for queenColumn in range(0,self.n_queens):
        if self.chessBoard.board[queenRow][queenColumn] == 1: #get the lowest cost by moving this queen
          for m_row in range(0,self.n_queens):
            for m_col in range(0,self.n_queens):
              if self.chessBoard.board[m_row][m_col] != 1:    # temporary place the queen here and look for better results
                tempBoard = copy.deepcopy(self.chessBoard)
                tempBoard.board[queenRow][queenColumn] = 0
                tempBoard.board[m_row][m_col] = 1
                tempCost = self.CalculateHeuristicCost(tempBoard)
                if tempCost < lowestCost:               # if better result found replace with the current . This is what hill climbing does
                  lowestCost = tempCost
                  lowestBoard = tempBoard
    self.chessBoard = lowestBoard
    self.cost = lowestCost
 
chessBoard = queens(showIntermediateResults=True,numruns=100, numberOfQueens=8)
chessBoard.StartSolvingNQueensProblem()

board=chessBoard.getBoard().board
chessBoard.printstats()
