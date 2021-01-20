#######those case will return a number if the state of the game meet the condition##########
#each case will detect the number of the position on board meet the condition, and the program based on it calculate a score#        
def case_free(player_b):#have chance to go in mancala
    pos_num=0
    for i in range(6):
        if(player_b[i]%13+i==6):
            pos_num+=1
    return pos_num
def case_cap(player_b,oppo_b):#capture opponent(player have chance to cap oppo, return how many available)
    pos_num=0
    for i in range(6):
        if(player_b[i]%13+i<6 and (player_b[player_b[i]%13+i]==0 or player_b[i]%13==0) and oppo_b[5-i]!=0):
            pos_num +=1
    return pos_num
##----------other calculation functions for score calculating (some of them may not be used in final vr)
def diffMancala(player_man,oppo_man):#mancala difference (first-second)
    return player_man-oppo_man# 1 if player_man>oppo_man else -1
def sumBoard(player_b):#on board seeds summerize
    sumPlayerBoard=0
    for i in player_b:
        sumPlayerBoard+=i
    return sumPlayerBoard
def weightSum(player_b):#weight sum for seeds number on board
    return player_b[0]*6 + player_b[1]*5 + player_b[2]*4 + player_b[3]*3 + player_b[4]*2 + player_b[5]*1
def fillNum(player_b):#the number of hole on player side is not empty (control of board)
    numHoleFill=0#player's
    #numHoleFill2=0#opponent's
    for i in player_b:
        if(i!=0):
            numHoleFill+=1
    return numHoleFill
def fillNum123(player_b):#the holes filled in 123 holes
    numHoleFill=0#player's
    for i in range(3):
        if(player_b[i]!=0):
            numHoleFill+=1
    return numHoleFill
def capTargeting(hole, oppo_b): #to determine if cap is possible for this hole hole is mine
    for i in range(6):
        if(oppo_b[i]%13+i==5-hole and oppo_b[5-hole]==0):
            return 1
    return 0
########################################################################
def rule1(pos):
    if(pos==6):                                                 #in mancala
        return 1
    else:
        return 2
    
def rule2(pos,switch, p_board, op_board):
    if(pos!=6 and switch!=2):
        if(p_board[pos]==1 and op_board[5-pos]!=0):
            return True
    return False

def recurProcess(isPlayer,p_board,p_man,op_board,op_man,MAXSTEP,alpha,beta):#because we switch the player's perspective to do the same calculation, isPlayer tracks is the current player is our player or current opponent is our player
#    if(isPlayer): 
#        print(p_board,p_man,op_board,op_man)
#    else:
#        print(op_board,op_man,p_board,p_man)
    global player_id
    global maxSimStep
    global sumBoards
    global player_steps#for debug
#    global counter
#    counter+=1
    #####################terminate states####################################
    sumPB=sumBoard(p_board)#for current player
    sumOB=sumBoard(op_board)#for current opponent
    #---------game end------------------------------------------------
    if(sumPB==0 or sumOB==0):                                        #when game end
        score=0
        if(isPlayer):                                     #return the difference of score the bigger the better for us
            score += diffMancala(p_man,op_man)#*100#mancala
            score += sumPB-sumOB#*100#board
            return (score+2000) if score>0 else (score-2000)#when score>0 our player win so return a big num otherwise a small num
        else:
            score += diffMancala(op_man,p_man)#*-100#mancala
            score += sumOB-sumPB#*-100#board
            return (score+2000) if score>0 else (score-2000)
    #---------when one of the player's mancala reach 25 there is no need to wait till game done
    if(p_man>24):                                                #if a mancala > 24, that mean this player win, no need game end
        if(isPlayer):
            if(MAXSTEP==maxSimStep):                       #if this terminate is on first level
                for i in range(6):
                    if(p_board[i]!=0):
                        return i
            return 2020
        else:
            if(MAXSTEP==maxSimStep):
                for i in range(6):
                    if(op_board[i]!=0):
                        return i
            return -2020
    elif(op_man>24):
        if(isPlayer):
            if(MAXSTEP==maxSimStep):                       #if this terminate is on first level
                for i in range(6):
                    if(p_board[i]!=0):
                        return i
            return -2020
        else: 
            if(MAXSTEP==maxSimStep):
                for i in range(6):
                    if(op_board[i]!=0):
                        return i
            return 2020
    #--------end of prediction----------------------------------------
    if(MAXSTEP==0):                                           #when we reach the end of the prediction 
        score=0
        if(isPlayer):                                     #return the difference of score the bigger the better for us
            score += fillNum123(p_board)*3
            score += p_man
            score += p_board[3]+p_board[4]+p_board[5]#sumPB
            score -= capTargeting(0,oppo_b)+capTargeting(1,oppo_b)+capTargeting(2,oppo_b)+capTargeting(3,oppo_b)+capTargeting(4,oppo_b)+capTargeting(5,oppo_b) 
            
            score -= fillNum123(op_board)*3
            score -= op_man
            score -= op_board[3]+op_board[4]+op_board[5]#sumOB
            
            return score

        else:#since in this area the opponent is our player, we reverse the flavor
            score += fillNum123(op_board)*3
            score += op_man
            score += op_board[3]+op_board[4]+op_board[5]#sumOB
            
            score -= fillNum123(p_board)*3
            score -= p_man
            score -= p_board[3]+p_board[4]+p_board[5]#sumPB
            
            return score
    ##########################################################################
    ####evaluation############################################################
    pick=0
    maxPredict=-5000.0
    minPredict=5000.0
    for i in range(5,-1,-1):                                          #6 cases for 6 slots: range(6)
        copy_p_board=p_board.copy()
        copy_op_board=op_board.copy()
        copy_p_man=p_man
        copy_op_man=op_man
        if(copy_p_board[i]==0):
            continue
        #player_steps.append(i)                              #record the step (for debug)
        ######################################################################
        #start proceed game rules
        switch=1                                            #switch==1 -> currently working on player's board ==2-> currently on opponent's board
        pos=i                                               #pos is the current working board position for current player's board(0-5 6 is for mancala)
        movStep=copy_p_board[pos]                                #how many moving in this step
        copy_p_board[pos]=0                                      #since the first pos is the decision for current step, this slot need to be clear, the seed s will be moved to other slots
        pos+=1
        for j in range(movStep):
            if(switch==1 and pos == 6):                 #mancala
                copy_p_man+=1
            elif(switch==1 and pos>=7):                 #switch to other player's board, and place one in the hole
                switch=2
                pos=0
                copy_op_board[pos]+=1
            elif(switch==1):                            #regular +1 case
                copy_p_board[pos]+=1
                
            elif(switch==2 and pos>=6):                 #switch to other player's board, and place one in the hole
                switch=1
                pos=0
                copy_p_board[pos]+=1
            else:                                       #regular +1 case
                copy_op_board[pos]+=1
            pos+=1                                      #increment position for current player board
        pos-=1
        nextPlayer=rule1(pos)                               #implement rule of free run
        if(rule2(pos, switch, copy_p_board,copy_op_board)): #implement rule of capture, however, the rule on the website is different, we need to put the seed in the opposite hole instead of mancala
            #copy_p_man+=copy_op_board[5-pos] #sinve this is the old rule
            copy_p_board[pos]+=copy_op_board[5-pos]
            copy_op_board[5-pos]=0
            
        #end proceed game rules
        #########################################################################
        ###alph-beta calculation and evaluate the best pick###
        if(isPlayer):
            if(nextPlayer==1):                                  #1 -> still current player go, 2-> other player's turn
                this_prediction=recurProcess(isPlayer,copy_p_board,copy_p_man,copy_op_board,copy_op_man,MAXSTEP-1,alpha,beta)
            else: 
                this_prediction=recurProcess(not isPlayer,copy_op_board,copy_op_man,copy_p_board,copy_p_man,MAXSTEP-1,alpha,beta)
            if (maxPredict<this_prediction):
                pick=i
            maxPredict=max(maxPredict,this_prediction)
            alpha=max(alpha,maxPredict)
            if (beta<=alpha):
                break
            #return maxPredict
        else:
            if(nextPlayer==1):                                  #1 -> still current player go, 2-> other player's turn
                this_prediction=recurProcess(isPlayer,copy_p_board,copy_p_man,copy_op_board,copy_op_man,MAXSTEP-1,alpha,beta)
            else: 
                this_prediction=recurProcess(not isPlayer,copy_op_board,copy_op_man,copy_p_board,copy_p_man,MAXSTEP-1,alpha,beta)
            if(minPredict>this_prediction):
                pick=i
            minPredict=min(minPredict,this_prediction)
            beta=min(beta,minPredict)
            if(beta<=alpha):
                break
            #return minPredict
            
        #######################################################
    ###########return the minmax######################################
    if(MAXSTEP==maxSimStep):                                    #if the function reach the end and we are in the first level, we should return a final pic
        return pick#here we return a best max case
    else:
        if(isPlayer):
            return maxPredict
        else:
            return minPredict
    ##################################################################
################main###################
maxSimStep=11#how many step prediction(try 12)

player_id=int(input())
player1_man=int(input())
player1_b=[]
inp=[]
inp=input().split(' ')
for i in range(6):
    player1_b.append(int(inp[i]))
player2_man=int(input())
player2_b=[]
inp=''
inp=input().split(' ')
for i in range(6):
    player2_b.append(int(inp[i]))
#for debug
player_steps=[]
#counter=0
#---dynamic depth---
sumBoards=0
for i in player1_b:
    sumBoards+=i
for i in player2_b:
    sumBoards+=i
if(sumBoards<=42 and sumBoards>25):
    maxSimStep+=1
elif(sumBoards<=25 and sumBoards>20):
    maxSimStep+=2
elif(sumBoards<=20 and sumBoards>15):
    maxSimStep+=3
elif(sumBoards<=15 and sumBoards>10):
    maxSimStep+=4
elif(sumBoards<=10):
    maxSimStep+=5
#--------------------
go=0                                                                #the result
if(player_id==1):
    go=recurProcess(True,player1_b,player1_man,player2_b,player2_man,maxSimStep,-5000.0,5000.0)
    while(player1_b[go]==0):
        go+=1
        if(go>=6):
            go=0
else:
    go=recurProcess(True,player2_b,player2_man,player1_b,player1_man,maxSimStep,-5000.0,5000.0)
    while(player2_b[go]==0):
        go+=1
        if(go>=6):
            go=0

print(go+1)
#print(player_steps," ")
#print(counter)
#input("check")