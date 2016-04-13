import sys
import pygame
import random

class States():
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

class Menu(States):


    def __init__(self):
        States.__init__(self)
        self.image = pygame.image.load('menu.png').convert_alpha()
        try:
            pygame.mixer.init()
            pygame.mixer.music.load('menu.ogg')
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play()
        except:
            pass

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if (x>80 and x<290) and (y>300 and y<450):
                self.next = 'game1'
            elif (x>310 and x<520) and (y>300 and y<450):
                self.next = 'game2'
            elif (x>80 and x<290) and (y>500 and y<650):
                self.next = 'info'
            elif (x>310 and x<520) and (y>500 and y<650):              
                self.next = 'menu'
                pygame.quit()
                sys.exit()
            self.done = True

    def update(self,screen,dt):
        self.draw(screen)

    def draw(self,screen):
        screen.blit(self.image,(0,0))

class Info(States):
    def __init__(self):
        States.__init__(self)
        self.image = pygame.image.load('info.png').convert_alpha()

    def get_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.done = True
            self.next = 'menu'
        elif event.type == pygame.KEYDOWN:
            self.done = True
            self.next = 'menu'

    def update(self,screen,dt):
        screen.blit(self.image,(0,0))

class Game(States):
    def __init__(self,choice=0):
        States.__init__(self)
        self.replay = False
        self.choice = choice
        self.caption = pygame.display.set_caption('Boggle')     
        self.letters = Dice(self.choice).roll()
        self.guess_init()
        self.timer = 0
        self.end_time = 180
        self.hint_time = 0
        self.hint_text = None
        self.points = 0
        f = open('words.txt')
        self.word_list = f.read()
        f.close()
        g = open('record.txt')
        self.record =int(g.readline())
        g.close()
        
    def guess_init(self):
        self.guess = []
        self.result = None
        
        self.board_letters =[]
        for i in range(4):
            self.board_letters.append([])
            for j in range(4):
                self.board_letters[i].append(self.letters[i][j])

        self.valid_pos=[x for x in range(16)]

        self.valid_input = []
        for i in self.board_letters:
            for j in i:
                self.valid_input.append(j.lower())

        self.valid_key_input = []
        for i in self.board_letters:
            for j in i:
                self.valid_key_input.append(ord(j.lower()))

        self.confirmed_pos =[]
        self.multi_choice = []
        self.last_pos =[]
        self.draw_cirle_pos =[]

    def draw(self,screen):
        screen.fill((241,142,56))
        Text().print_text(screen,(50,50),Text().text_1,40,(255,255,255))
        Text().print_text(screen,(350,50),Text().text_2,40,(255,255,255))
        Text().print_text(screen,(50,100),Text().text_3,40,(255,255,255))
        self.a = pygame.image.load('letter_A.png').convert()
        self.b = pygame.image.load('letter_B.png').convert()
        self.c = pygame.image.load('letter_C.png').convert()
        self.d = pygame.image.load('letter_D.png').convert()
        self.e = pygame.image.load('letter_E.png').convert()
        self.f = pygame.image.load('letter_F.png').convert()
        self.g = pygame.image.load('letter_G.png').convert()
        self.h = pygame.image.load('letter_H.png').convert()
        self.i = pygame.image.load('letter_I.png').convert()
        self.j = pygame.image.load('letter_J.png').convert()
        self.k = pygame.image.load('letter_K.png').convert()
        self.l = pygame.image.load('letter_L.png').convert()
        self.m = pygame.image.load('letter_M.png').convert()
        self.n = pygame.image.load('letter_N.png').convert()
        self.o = pygame.image.load('letter_O.png').convert()
        self.p = pygame.image.load('letter_P.png').convert()
        self.q = pygame.image.load('letter_Q.png').convert()
        self.r = pygame.image.load('letter_R.png').convert()
        self.s = pygame.image.load('letter_S.png').convert()
        self.t = pygame.image.load('letter_T.png').convert()
        self.u = pygame.image.load('letter_U.png').convert()
        self.v = pygame.image.load('letter_V.png').convert()
        self.w = pygame.image.load('letter_W.png').convert()
        self.x = pygame.image.load('letter_X.png').convert()
        self.y = pygame.image.load('letter_Y.png').convert()
        self.z = pygame.image.load('letter_Z.png').convert()
        self.image_dict = {'A':self.a,'B':self.b,'C':self.c,'D':self.d,
                           'E':self.e,'F':self.f,'G':self.g,'H':self.h,
                           'I':self.i,'J':self.j,'K':self.k,'L':self.l,
                           'M':self.m,'N':self.n,'O':self.o,'P':self.p,
                           'Q':self.q,'R':self.r,'S':self.s,'T':self.t,
                           'U':self.u,'V':self.v,'W':self.w,'X':self.x,
                           'Y':self.y,'Z':self.z}
        
        for row in range(4):
            for column in range(4):
                screen.blit(self.image_dict[self.letters[row][column]],(44+column*128,244+row*128,128,128))
        
    def get_event(self,event):
        '''I really really can not make the following code neat
           by my current level,sometimes i do not know how many space
           i should press...so many for and if, i hate them. And the
           worst is, there are still bugs exit'''
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in self.valid_key_input:                 
                letter = pygame.key.name(event.key)
                self.guess.append(letter)
                if letter == 'q':
                    self.guess.append('u')
                current_pos = []
                for i in range(4):
                    for j in range(4):
                        if self.board_letters[i][j]== letter.upper():
                            x,y=i,j
                            current_pos.append([x,y])
                            
                if len(self.last_pos)!=0:
                    del_pos=[]
                    for i in range(len(current_pos)):
                        k=0
                        for j in range(len(self.last_pos)):
                            if((current_pos[i][0]-self.last_pos[j][0]>1 or current_pos[i][0]-self.last_pos[j][0]<-1) or \
                               (current_pos[i][1]-self.last_pos[j][1]>1 or current_pos[i][1]-self.last_pos[j][1]<-1)):
                                k+=1
                        if current_pos[i] in self.last_pos:
                            k+=1
                        if k==len(self.last_pos):
                            del_pos.append(current_pos[i])
                    for i in del_pos:
                        if i in current_pos:
                            current_pos.remove(i)
                self.last_pos[:]=current_pos[:]
                if len(self.multi_choice)==0:
                    for i in current_pos:
                        self.multi_choice.append(i)
                else:
                    for i in range(len(current_pos)):
                        for j in range(len(self.multi_choice)):
                            if (current_pos[i][0]-self.multi_choice[j][0] <= 1 and current_pos[i][0]-self.multi_choice[j][0] >=-1) and \
                               (current_pos[i][1]-self.multi_choice[j][1] <= 1 and current_pos[i][1]-self.multi_choice[j][1] >=-1):
                                self.multi_choice[j].append(current_pos[i][0])
                                self.multi_choice[j].append(current_pos[i][1])
                self.multi_choice.sort(key =lambda x:len(x),reverse=True)
                if len(self.multi_choice)==1 or len(self.multi_choice[0])>len(self.multi_choice[1]):
                    self.confirmed_pos[:]=self.multi_choice[0][:]
                    self.multi_choice.clear()
                    for i in range(0,len(self.confirmed_pos),2):
                        self.board_letters[self.confirmed_pos[i]][self.confirmed_pos[i+1]]=None
                    self.confirmed_pos.clear()
                for i in range(4):
                    for j in range(4):
                        if self.board_letters[i][j]==None:
                            self.draw_cirle_pos.append([i,j])
                            
                self.valid_input = []
                for i in self.board_letters:
                    for j in i:
                        if j== None:
                            self.valid_input.append(None)
                        else:
                            self.valid_input.append(j.lower())
                youxiao_pos = []
                for i in range(4):
                    for j in range(4):
                        for k in range(len(current_pos)):
                            if (current_pos[k][0]-i <= 1 and current_pos[k][0]-i >=-1) and \
                               (current_pos[k][1]-j <= 1 and current_pos[k][1]-j >=-1) and not\
                               (current_pos[k][0]-i == 0 and current_pos[k][1]-j ==0):
                                youxiao_pos.append(i*4+j)
                                youxiao_pos = list(set(youxiao_pos))
                self.valid_pos[:]=youxiao_pos[:]
                for i in self.valid_pos:
                    if self.valid_input[i]==None:
                        self.valid_pos.remove(i)
                for i in range(len(self.valid_input)):
                    if i not in youxiao_pos:
                        self.valid_input[i]=None
                self.valid_key_input = []
                for i in self.valid_input:
                    if i != None:
                        self.valid_key_input.append(ord(i))
                        self.valid_key_input = list(set(self.valid_key_input))

            elif event.key == pygame.K_SPACE:
                self.replay = True
            elif event.key == pygame.K_RETURN:
                pass
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit
            else:
                self.hint_time = 0.8
                self.hint_text = "PLEASE INPUT A VALID KEY"
                music = pygame.mixer.Sound('wrong.ogg')
                music.play()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if (x>44 and x<556) and (y>244 and y<756):
                y,x = int((x-44)/128),int((y-244)/128)
                letter = self.board_letters[x][y]
            if pygame.mouse.get_pressed()[0]==1 and x*4+y in self.valid_pos:            
                self.guess.append(letter.lower())
                if letter.lower() == 'q':
                    self.guess.append('u')
                current_pos = []
                current_pos.append([x,y])                   
                if len(self.last_pos)!=0:
                    del_pos=[]
                    for i in range(len(current_pos)):
                        k=0
                        for j in range(len(self.last_pos)):
                            if((current_pos[i][0]-self.last_pos[j][0]>1 or current_pos[i][0]-self.last_pos[j][0]<-1) or \
                               (current_pos[i][1]-self.last_pos[j][1]>1 or current_pos[i][1]-self.last_pos[j][1]<-1)):
                                k+=1
                        if current_pos[i] in self.last_pos:
                            k+=1
                        if k==len(self.last_pos):
                            del_pos.append(current_pos[i])
                    for i in del_pos:
                        if i in current_pos:
                            current_pos.remove(i)
                self.last_pos[:]=current_pos[:]
                if len(self.multi_choice)==0:
                    for i in current_pos:
                        self.multi_choice.append(i)
                else:
                    for i in range(len(current_pos)):
                        for j in range(len(self.multi_choice)):
                            if (current_pos[i][0]-self.multi_choice[j][0] <= 1 and current_pos[i][0]-self.multi_choice[j][0] >=-1) and \
                               (current_pos[i][1]-self.multi_choice[j][1] <= 1 and current_pos[i][1]-self.multi_choice[j][1] >=-1):
                                self.multi_choice[j].append(current_pos[i][0])
                                self.multi_choice[j].append(current_pos[i][1])
                self.multi_choice.sort(key =lambda x:len(x),reverse=True)
                if len(self.multi_choice)==1 or len(self.multi_choice[0])>len(self.multi_choice[1]):
                    self.confirmed_pos[:]=self.multi_choice[0][:]
                    self.multi_choice.clear()
                    for i in range(0,len(self.confirmed_pos),2):
                        self.board_letters[self.confirmed_pos[i]][self.confirmed_pos[i+1]]=None
                    self.confirmed_pos.clear()
                for i in range(4):
                    for j in range(4):
                        if self.board_letters[i][j]==None:
                            self.draw_cirle_pos.append([i,j])                                
                self.valid_input = []
                for i in self.board_letters:
                    for j in i:
                        if j== None:
                            self.valid_input.append(None)
                        else:
                            self.valid_input.append(j.lower())
                youxiao_pos = []
                for i in range(4):
                    for j in range(4):
                        for k in range(len(current_pos)):
                            if (current_pos[k][0]-i <= 1 and current_pos[k][0]-i >=-1) and \
                               (current_pos[k][1]-j <= 1 and current_pos[k][1]-j >=-1) and not\
                               (current_pos[k][0]-i == 0 and current_pos[k][1]-j ==0):
                                youxiao_pos.append(i*4+j)
                                youxiao_pos = list(set(youxiao_pos))
                self.valid_pos[:]=youxiao_pos[:]
                for i in self.valid_pos:
                    if self.valid_input[i]==None:
                        self.valid_pos.remove(i)
                for i in range(len(self.valid_input)):
                    if i not in youxiao_pos:
                        self.valid_input[i]=None
                self.valid_key_input = []
                for i in self.valid_input:
                    if i != None:
                        self.valid_key_input.append(ord(i))
                        self.valid_key_input = list(set(self.valid_key_input))
            elif pygame.mouse.get_pressed()[0]==1 and x*4+y not in self.valid_pos:
                self.hint_time = 0.8
                self.hint_text = 'CLICK ADJACENT LETTERS'
                music = pygame.mixer.Sound('wrong.ogg')
                music.play()

            elif pygame.mouse.get_pressed()[2]==1:
                if len(self.guess)>=3:
                    self.result ='\n'+''.join(self.guess)+'\n'
                    if self.word_list.find(self.result)>0:
                        self.hint_time = 0.8
                        self.hint_text = 'YOU GET IT!'
                        music = pygame.mixer.Sound('right.ogg')
                        music.play()
                        if len(self.guess)>=8:
                            self.points += 11
                        elif len(self.guess)>=7:
                            self.points += 5
                        elif len(self.guess)>=6:
                            self.points += 3
                        elif len(self.guess)>=5:
                            self.points += 2
                        elif len(self.guess)>=3:
                            self.points += 1
                        self.word_list = self.word_list.replace(self.result,'\n\n')
                        self.guess_init()
                    else:
                        self.hint_time = 0.8
                        self.hint_text = 'NOT IN THE LIST!'
                        self.guess_init()
                elif len(self.guess)<3:
                    self.hint_time =0.8
                    self.hint_text = 'LESS THAN 3 LETTERS!'
                    self.guess_init()
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_F1:
                pass
            elif event.key == pygame.K_RETURN:
                if len(self.guess)>=3:
                    self.result ='\n'+''.join(self.guess)+'\n'

                    if self.word_list.find(self.result)>0:
                        self.hint_time = 0.8
                        self.hint_text = 'YOU GET IT!'
                        music = pygame.mixer.Sound('right.ogg')
                        music.play()
                        if len(self.guess)>=8:
                            self.points += 11
                        elif len(self.guess)>=7:
                            self.points += 5
                        elif len(self.guess)>=6:
                            self.points += 3
                        elif len(self.guess)>=5:
                            self.points += 2
                        elif len(self.guess)>=3:
                            self.points += 1
                        self.word_list = self.word_list.replace(self.result,'\n\n')
                        self.guess_init()
                    else:
                        self.hint_time = 0.8
                        self.hint_text = 'NOT IN THE LIST!'
                        self.guess_init()
                elif len(self.guess)<3:
                    self.hint_time =0.8
                    self.hint_text = 'LESS THAN 3 LETTERS!'
                    self.guess_init()
    
    def update(self,screen,dt):
        self.draw(screen)
        while self.replay == True:
            self.letters = Dice(self.choice).roll()
            self.guess_init()
            self.timer = 0
            self.end_time = 180
            self.hint_time = 0
            self.hint_text = None
            self.points = 0
            f = open('words.txt')
            self.word_list = f.read()
            f.close()
            g = open('record.txt')
            self.record =int(g.readline())
            g.close()
            self.replay = False

        if self.hint_time > 0:
            Text().print_text(screen,(150,200),self.hint_text,30,(255,255,255))
            self.hint_time -= dt
            if self.hint_time <0:
                self.hint_time =0
                
        self.timer += dt
        self.left_time = int(self.end_time - self.timer +1)
        if self.timer >= self.end_time:
            point = open('points.txt','w')
            point.write(str(self.points))
            point.close()
            if self.points > self.record:
                self.record = self.points
                new = open('record.txt','w')
                new.write(str(self.record))
                new.close()
            pygame.time.delay(500)
            self.done = True
            self.next ='end'
            self.letters = Dice(self.choice).roll()
            self.guess_init()
            self.timer = 0
            self.end_time = 180
            self.hint_time = 0
            self.hint_text = None
            self.points = 0
            f = open('words.txt')
            self.word_list = f.read()
            f.close()
            g = open('record.txt')
            self.record =int(g.readline())
            g.close()


        Text().print_text(screen,(160,50),str(self.left_time),40,(255,255,255))
        Text().print_text(screen,(500,50),str(self.points),40,(255,255,255))

        self.guess_string = ''.join(self.guess)
        self.guess_string = self.guess_string.upper()
        Text().print_text(screen,(200,100),self.guess_string,40,(255,255,255))

        for i in self.draw_cirle_pos:
            pygame.draw.circle(screen,(241,142,56),(108+i[1]*128,308+i[0]*128),50,3)


class Dice():
    def __init__(self,cube_faces = 0):
        self.dice1 = list("AACIOT")
        self.dice2 = list("AHMORS")
        self.dice3 = list("EGKLUY")
        self.dice4 = list("ABILTY")
        self.dice5 = list("ACDEMP")
        self.dice6 = list("EGINTV")
        self.dice7 = list("GILRUW")
        self.dice8 = list("ELPSTU")
        self.dice9 = list("DENOSW")
        self.dice10 = list("ACELRS")
        self.dice11 = list("ABJMOQ")
        self.dice12 = list("EEFHIY")
        self.dice13 = list("EHINPS")
        self.dice14 = list("DKNOTU")
        self.dice15 = list("ADENVZ")
        self.dice16 = list("BIFORX")
        if cube_faces == 1:
            self.dice1 = list("AAEEGN")
            self.dice2 = list("ELRTTY")
            self.dice3 = list("AOOTTW")
            self.dice4 = list("ABBJOO")
            self.dice5 = list("EHRTVW")
            self.dice6 = list("CIMOTU")
            self.dice7 = list("DISTTY")
            self.dice8 = list("EIOSST")
            self.dice9 = list("DELRVY")
            self.dice10 = list("ACHOPS")
            self.dice11 = list("HIMNQU")
            self.dice12 = list("EEINSU")
            self.dice13 = list("EEGHNW")
            self.dice14 = list("AFFKPS")
            self.dice15 = list("HLNNRZ")
            self.dice16 = list("DEILRX")

    def roll(self):
        self.dice_result = []
        self.dice_group = [self.dice1,self.dice2,self.dice3,self.dice4,
                           self.dice5,self.dice6,self.dice7,self.dice8,
                           self.dice9,self.dice10,self.dice11,self.dice12,
                           self.dice13,self.dice14,self.dice15,self.dice16]
        for i in range(16):
            random.shuffle(self.dice_group[i])
        random.shuffle(self.dice_group)
        for row in range(4):
            self.dice_result.append([])
            for column in range(4):
                self.dice_result[row].append(self.dice_group[row*4+column][0])
        return self.dice_result

class End(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'
        self.image = pygame.image.load('gameover.png').convert()
        self.score = 0
        self.record = 0

    def get_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.done = True
            self.next = 'menu'
        elif event.type == pygame.KEYDOWN:
            self.done = True
            self.next = 'menu'

    def update(self,screen,dt):
        score = open('points.txt')
        self.score = score.read()
        score.close()
        records = open('record.txt')
        self.record = records.read()
        records.close()
        screen.blit(self.image,(0,0))
        Text().print_text(screen,(250,500),self.score,100,(255,255,255))
        Text().print_text(screen,(400,699),self.record,26,(255,255,255))


class Text():
    def __init__(self):
        self.text_1 = "TIME:"
        self.text_2 = "POINTS:"
        self.text_3 = "WORD:"
            
    def print_text(self,surface,position,text,size,colour,bg_colour=None):
        font_layer = pygame.font.SysFont('calibri',size,True)
        font_surface = font_layer.render(text,True,colour,bg_colour)
        surface.blit(font_surface,position)

class Control:
    def __init__(self):
        self.done = False
        self.fps = 60
        self.screen = pygame.display.set_mode((600,800))
        self.clock = pygame.time.Clock()

    def setup_states(self,state_dict,start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def flip_state(self):
        self.state.done =False
        previous,self.state_name = self.state_name,self.state.next
        self.state = self.state_dict[self.state_name]
        self.state.previous = previous

    def update(self,dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen,dt)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)

    def main_game_loop(self):
        while not self.done:
            dt = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(dt)
            pygame.display.update()

if __name__=='__main__':
    pygame.init()
    app = Control()
    state_dict ={'menu':Menu(),
                 'game1':Game(0),
                 'game2':Game(2),
                 'info':Info(),
                 'end':End()
                 }
    app.setup_states(state_dict,'menu')
    app.main_game_loop()
    pygame.quit()
    sys.exit()
