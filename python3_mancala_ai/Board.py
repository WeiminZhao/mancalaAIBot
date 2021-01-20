class Board:
    turn=1                                          #to indicate which player's turn
    player1=[4,4,4,4,4,4,0]                         #print left to right (buttonplayer)
    player2=[4,4,4,4,4,4,0]                         #print right to left (topplayer)
    #def _init_():
    #       x=0
    def showBoard(self):
        print(self.turn)
        print(self.player1[6])
        for i in range(6):
            print(self.player1[i]," ",end="")
        print()
        print(self.player2[6])
        for i in range(6):
            print(self.player2[i]," ",end="")
        print()
    def play(self):
        if(self.turn==1):
            self.play1()
        else:
            self.play2()
    def play1(self):
        switch=1                                    #use to indicate the pos is in which player's board
        pos=int(input())-1
        movStep=self.player1[pos]
        self.player1[pos]=0
        pos+=1
        for i in range(movStep):
            if(switch==1 and pos>=7):
                switch=2
                pos=0
            if(switch==2 and pos>=6):
                switch=1
                pos=0
            if(switch==1):
                self.player1[pos]+=1
            else:
                self.player2[pos]+=1
            pos+=1
        self.rule(pos,switch)
        self.rule2(pos,switch,self.player1,self.player2)
            
    def play2(self):
        switch=2                                    #use to indicate the pos is in which player's board
        pos=int(input())-1
        movStep=self.player2[pos]
        self.player2[pos]=0
        pos+=1
        for i in range(movStep):
            if(switch==2 and pos>=7):
                switch=1
                pos=0
            if(switch==1 and pos>=6):
                switch=2
                pos=0
            if(switch==1):
                self.player1[pos]+=1
            else:
                self.player2[pos]+=1
            pos+=1
        self.rule(pos,switch)
        self.rule2(pos,switch,self.player2,self.player1)

    def rule(self,pos,switch):
        if(pos==7):
            return

        if(self.turn==1):
            self.turn=2
            return
        if(self.turn==2):
            self.turn=1
            return
            
    def rule2(self,pos,switch,pb,pboppo):           #pb stands for current player board, pboppo stands for current player's opponent's board
        pos=pos-1                                   #as pos enter here will be the actual stop pos + 1
        if(self.turn==switch and pos!=6):
            if(self.turn==1 and self.player1[pos]==1 and self.player2[5-pos]!=0):
                self.player1[6]=self.player1[pos]+self.player2[5-pos]
                self.player1[pos]==0
                self.player2[pos]==0
            if(self.turn==2 and self.player2[pos]==1 and self.player1[5-pos]!=0):
                self.player2[6]=self.player2[pos]+self.player1[5-pos]
                self.player2[pos]==0
                self.player1[pos]==0
                
                
