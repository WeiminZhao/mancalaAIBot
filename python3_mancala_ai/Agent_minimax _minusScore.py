def case_1(player_b,player_man,oppo_b,oppo_man):#will be capture, will return possible opponent next step to happen
    op_pos=-1
    for i in range(6):
        if(oppo_b[oppo_b[i+1]%13+i+1]==0 and player_b[5-i+1]!=0):
            op_pos = i
    return op_pos
def case_2(player_b,player_man,oppo_b,oppo_man):#opponent will have a chance to go in mancala, will return possible opponent next step to make it happen
    op_pos=-1
    for i in range(6):
        if(oppo_b[i+1]%13+i+1==7):
            op_pos = i
    return op_pos
        
def case_3(player_b,player_man,oppo_b,oppo_man):#self have chance to go in mancala
    pos=-1
    for i in range(6):
        if(player_b[i+1]%13+i+1==7):
            pos = i
    return pos
def case_4(player_b,player_man,oppo_b,oppo_man):#capture enemy's
    pos=-1
    for i in range(6):
        if(player_b[player_b[i+1]%13+i+1]==0 and oppo_b[5-i+1]!=0):
            pos = i
    return pos

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
    #print(MAXSTEP)
    global maxSimStep
    global player_steps#for debug
    detect_end=0
    detect_end2=0
    for i in p_board:                                                          #game end when player's board is empty
        detect_end+=i
    for i in op_board:
        detect_end2+=i
    if(detect_end==0 or detect_end2==0):                                        #when game end
        sumPlayerBoard=0
        sumOppoBoard=0
        for i in p_board:
            sumPlayerBoard+=i
        for i in op_board:
            sumOppoBoard+=i
        if(isPlayer):                                     #return the difference of score the bigger the better for us
            return (p_man+sumPlayerBoard)-(op_man+sumOppoBoard)
        else:
            return (op_man+sumOppoBoard)-(p_man+sumPlayerBoard) 

    if(MAXSTEP==0):                                           #when we reach the end of the prediction 
        sumPlayerBoard=0
        sumOppoBoard=0
        for i in p_board:
            sumPlayerBoard+=i
        for i in op_board:
            sumOppoBoard+=i
        if(isPlayer):                                     #return the difference of score the bigger the better for us
            return (p_man+sumPlayerBoard/3)-(op_man+sumOppoBoard/3)

        else:
            return (op_man+sumOppoBoard/3)-(p_man+sumPlayerBoard/3) 

    pick=0
    maxPredict=-5000
    minPredict=5000
    for i in range(6):                                          #6 cases for 6 slots
        copy_p_board=p_board.copy()
        copy_op_board=op_board.copy()
        copy_p_man=p_man
        copy_op_man=op_man
        if(copy_p_board[i]==0):
            continue
        player_steps.append(i)                              #record the step (might not needed)
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
            elif(switch==1 and pos>=7):                 #switch to other player's board
                switch=2
                pos=0
            elif(switch==1):                            #regular +1 case
                copy_p_board[pos]+=1
            elif(switch==2 and pos>=6):                 #switch to other player's board
                switch=1
                pos=0
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
        ###alph-beta###
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
            
        ###############
    
    if(MAXSTEP==maxSimStep):                                    #if the function reach the end and we are in the first level, we should return a final pic
        return pick#here we return a best max case
    else:
        if(isPlayer):
            return maxPredict
        else:
            return minPredict

################main###################
maxSimStep=11#how many step prediction

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

player_steps=[]

go=0                                                                #the result
if(player_id==1):
    go=recurProcess(True,player1_b,player1_man,player2_b,player2_man,maxSimStep,-5000,5000)
    while(player1_b[go]==0):
        go+=1
        if(go>=6):
            go=0
else:
    go=recurProcess(True,player2_b,player2_man,player1_b,player1_man,maxSimStep,-5000,5000)
    while(player2_b[go]==0):
        go+=1
        if(go>=6):
            go=0

print(go+1)
#print(player_steps," ")
#input()