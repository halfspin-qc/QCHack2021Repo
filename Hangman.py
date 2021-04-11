import pygame
import sys
import random
import time
import re
from circuit import *
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

GREY = (200,200,200)

LEFT_CLICK = (1,0,0)
RIGHT_CLICK = (0,0,1)

pygame.init()

pygame.display.set_caption("Hangman")

bg = 'logo.png'
bg = pygame.image.load(bg)
bg = pygame.transform.scale(bg, (500, 500))
gates = ['X0', 'Y0', 'Z0', 'H0', 'C01', 'X1', 'Y1', 'Z1', 'H1', 'C10']
gateslist=[]
#32 bit display
Display = pygame.display.set_mode((500,500),0,32)

Easy = ["BELL","STAR","PICNIC", "PIE","HAT","HEART","FLAG"]
Medium = ["CARPET","POPCORN","SEAFOOD","DOORBELL","COWBOY",\
          "INSIDE","OUTSIDE","RAINBOW","POSTMAN","WATERMELON",\
          "FOOTBALL","STRAWBERRY"]
Hard = ["BACKGROUND","BOOKWORM","FIREFIGHTER","SOUNDPROOF","THUNDERSTORM",\
        "CAMPGROUND","FRIENDSHIP","SKYSCRAPER","SUPERHUMAN","FINGERPRINT",\
        "MASTERPIECE", "LOUDSPEAKER"]
Color = ["BLACK","WHITE","RED","GREEN","BLUE","GREY"]

Font = pygame.font.Font("freesansbold.ttf",33)
Font2 = pygame.font.Font("freesansbold.ttf",20)
font = pygame.font.Font("freesansbold.ttf", 36)

Display.fill(WHITE)
display_width = 500
display_height = 500


def randomNum(choice):
    RandomNum = 0
    if choice == 1:
        RandomNum == random.randint(0,len(Easy)-1)

    elif choice == 2:
        RandomNum = random.randint(0,len(Medium)-1)

    elif choice == 3:
        RandomNum = random.randint(0,len(Hard)-1)

    elif choice == 4:
        RandomNum =  random.randint(0,len(Color)-1)# as elements of color is 0,1,2,3,4
        
    return RandomNum

def List(number,choice):
    if (choice == 1):
        Word = Easy[number]

    elif (choice == 2):
        Word = Medium[number]

    elif (choice == 3):
        Word = Hard[number]

    elif (choice == 4):
        Word = Color[number]
        
    return Word

def Hangman(condition):
    if (condition == 0):
        img = pygame.image.load('initial.png')
        img = pygame.transform.scale(img, (350, 150))
        Display.blit(img, (50,280))
    else:
        img = pygame.image.load('current.png')
        img = pygame.transform.scale(img, (350, 150))
        Display.blit(img, (50,280))#baseline


def PreHangMan():
    qc=ansatz([])
    qc.draw('mpl').savefig('initial.png')
    qc.draw('mpl').savefig('current.png')
    img = pygame.image.load('initial.png')
    img = pygame.transform.scale(img, (150, 150))
    Display.blit(img, (50,180))

		
def StartScreen():
    Display.blit(pygame.font.Font("freesansbold.ttf",40).render("QHANGMAN",True,BLACK), (20,20))
    Display.blit(Font2.render("For the QcHACK2021",True,BLACK), (60,60))
    Display.blit(Font.render("Level Difficulty",True,BLACK), (200,150))
    Display.blit(Font2.render("1- Easy",True,BLACK), (200,200))
    Display.blit(Font2.render("2- Medium",True,BLACK), (200,250))
    Display.blit(Font2.render("3- Hard",True,BLACK), (200,300))

class Button(object):
    def __init__(self, text, color, x=None, y=None, **kwargs):
        self.surface = font.render(text, True, color)

        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()

        if 'centered_x' in kwargs and kwargs['centered_x']:
            self.x = display_width // 2 - self.WIDTH // 2
        else:
            self.x = x

        if 'centered_y' in kwargs and kwargs['cenntered_y']:
            self.y = display_height // 2 - self.HEIGHT // 2
        else:
            self.y = y

    def display(self):
        Display.blit(self.surface, (self.x, self.y))

    def check_click(self, position):
        x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
        y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT

        if x_match and y_match:
            return True
        else:
            return False

def gate_choose():
    Display.fill(WHITE)
    img = pygame.image.load('current.png')
    img = pygame.transform.scale(img, (400, 200))
    Display.blit(img, (50, 20))

    img = pygame.image.load('histogram.png')
    img = pygame.transform.scale(img, (500, 200))
    Display.blit(img, (500, 20))

    pygame.display.update()  # update the display
    game_title = font.render('Which gate would you like to choose?', True, RED)

    Display.blit(game_title, (display_width // 2 - game_title.get_width() // 2, 250))
    left = 200
    H_button = Button('H', WHITE, left, 50)
    X_button = Button('X', WHITE, left, 400)
    Y_button = Button('Y', WHITE, left, 450)
    Z_button = Button('Z', WHITE, None, 350, centered_x=True)
    CNOT1_button = Button('CX10', WHITE, None, 400, centered_x=True)
    CNOT_button = Button('CX01', WHITE, None, 450, centered_x=True)
    DONE_button = Button('DONE', WHITE, None, 500, centered_x=True)

    H_button.display()
    X_button.display()
    Z_button.display()
    Y_button.display()
    CNOT1_button.display()
    CNOT_button.display()
    DONE_button.display()

    pygame.display.update()
    while True:

        if H_button.check_click(pygame.mouse.get_pos()):
            H_button = Button('H', RED, left, 350)
        else:
            H_button = Button('H', WHITE, left, 350)

        if X_button.check_click(pygame.mouse.get_pos()):
            X_button = Button('X', RED, left, 400)
        else:
            X_button = Button('X', WHITE, left, 400)

        if Y_button.check_click(pygame.mouse.get_pos()):
            Y_button = Button('Y', RED, left, 450)
        else:
            Y_button = Button('Y', WHITE, left, 450)

        if Z_button.check_click(pygame.mouse.get_pos()):
            Z_button = Button('Z', RED, None, 350, centered_x=True)
        else:
            Z_button = Button('Z', WHITE, None, 350, centered_x=True)

        if CNOT1_button.check_click(pygame.mouse.get_pos()):
            CNOT1_button = Button('CX10', RED, None, 400, centered_x=True)
        else:
            CNOT1_button = Button('CX10', WHITE, None, 400, centered_x=True)
        if CNOT_button.check_click(pygame.mouse.get_pos()):
            CNOT_button = Button('CX01', RED, None, 450, centered_x=True)
        else:
            CNOT_button = Button('CX01', WHITE, None, 450, centered_x=True)

        if DONE_button.check_click(pygame.mouse.get_pos()):
            DONE_button = Button('DONE', RED, None, 500, centered_x=True)
        else:
            DONE_button = Button('DONE', WHITE, None, 500, centered_x=True)

        H_button.display()
        X_button.display()
        Y_button.display()
        Z_button.display()
        CNOT1_button.display()
        CNOT_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        if pygame.mouse.get_pressed()[0]:
            if H_button.check_click(pygame.mouse.get_pos()):
                return 'H'
                break
            if X_button.check_click(pygame.mouse.get_pos()):
                return "X"
                break
            if Y_button.check_click(pygame.mouse.get_pos()):
                return "Y"
                break
            if Z_button.check_click(pygame.mouse.get_pos()):
                return "Z"
                break
            if CNOT1_button.check_click(pygame.mouse.get_pos()):
                return "C10"
                break
            if CNOT_button.check_click(pygame.mouse.get_pos()):
                return "C01"
                break
         

def qubit_choose():
    Display.fill(WHITE)
    game_title = font.render('Which qubit would you like to apply that gate on?', True, RED)

    Display.blit(game_title, (display_width // 2 - game_title.get_width() // 2, 250))
    zero_button = Button('0', WHITE, None, 350, centered_x=True)
    one_button = Button('1', WHITE, None, 400, centered_x=True)

    zero_button.display()
    one_button.display()

    pygame.display.update()
    while True:

        if zero_button.check_click(pygame.mouse.get_pos()):
            zero_button = Button('0', RED, None, 350, centered_x=True)
        else:
            zero_button = Button('0', WHITE, None, 350, centered_x=True)

        if one_button.check_click(pygame.mouse.get_pos()):
            one_button = Button('1', RED, None, 400, centered_x=True)
        else:
            one_button = Button('1', WHITE, None, 400, centered_x=True)

        zero_button.display()
        one_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        if pygame.mouse.get_pressed()[0]:
            if zero_button.check_click(pygame.mouse.get_pos()):
                return '0'
                break
            if one_button.check_click(pygame.mouse.get_pos()):
                return '1'
                break

          
def main():
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)

    GREY = (200,200,200)

    TheChoice = 0
		
    StartScreen()
		
    PreHangMan()

    #background music
    pygame.mixer.music.load('Music\KM\Two Finger Johnny.mp3')
    pygame.mixer.music.play(-1,0)
    FirstCondi = True
    while FirstCondi:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                #print(FirstCondi)
                if (event.key == K_1) or (event.key == 257):#257 is 1 in numpad
                    TheChoice = 1
                    FirstCondi = False
                    break
                elif event.key == K_2 or event.key == 258:#258 is 2 in numpad
                    TheChoice = 2
                    FirstCondi = False
                    break
                elif event.key == K_3 or event.key == 259:#259 is 3 in numpad
                    TheChoice = 3
                    FirstCondi = False
                    break
                elif event.key == K_4 or event.key == 260:#260 is 4 in numpad
                    TheChoice = 4
                    FirstCondi = False
                    break

            elif event.type == MOUSEBUTTONDOWN:
                #print(pygame.mouse.get_pressed())
                if (pygame.mouse.get_pressed() != (0,0,0)):#Scroller of mouse
                    pygame.mixer.Sound('Music\Mouse Click Fast.wav').play()
                    
                #Easy
                if (pygame.mouse.get_pos()[0] > 200 and\
                    pygame.mouse.get_pos()[1] > 200 and\
                    pygame.mouse.get_pos()[0] < 265 and\
                    pygame.mouse.get_pos()[1] < 215):
                    TheChoice = 1
                    FirstCondi = False
                    break
                #Medium
                elif (pygame.mouse.get_pos()[0] > 200 and\
                      pygame.mouse.get_pos()[1] > 250 and\
                      pygame.mouse.get_pos()[0] < 295 and\
                      pygame.mouse.get_pos()[1] < 265):
                    TheChoice = 2
                    FirstCondi = False
                    break
                #Hard
                elif (pygame.mouse.get_pos()[0] > 200 and\
                      pygame.mouse.get_pos()[1] > 300 and\
                      pygame.mouse.get_pos()[0] < 265 and\
                      pygame.mouse.get_pos()[1] < 315):
                    TheChoice = 3
                    FirstCondi = False
                    break
                #Color
                elif (pygame.mouse.get_pos()[0] > 200 and\
                      pygame.mouse.get_pos()[1] > 350 and\
                      pygame.mouse.get_pos()[0] < 270 and\
                      pygame.mouse.get_pos()[1] < 365):
                    TheChoice = 4
                    FirstCondi = False
                    break
                
        if (TheChoice!= 0):
            Display.fill(WHITE)
            
        pygame.display.update()
        pygame.time.Clock().tick(30) #30fps        
    
    #This is to make sure the word and random number is constant
    TheNum = randomNum(TheChoice)
    TheWord = List(TheNum, TheChoice)
    #TheWord = "wew"

    #This is to check if it got the word from the list
    #print(TheWord)

    EmptyList = []

    for i in range(len(TheWord)):
        EmptyList.append('-')

    #print(EmptyList)
    #print("".join(EmptyList))

    Hidden = Font.render("".join(EmptyList),True,BLACK)
    HiddenRect = Hidden.get_rect()
    HiddenRect.center = (250,250)
    Display.blit(Hidden,HiddenRect)

    Condition = 0;#if condition is 10, then end game

    Off = 0 #quit game at game over and congrats

    TheTime = 0
    Start = time.time() #current time

    Display.blit(Font2.render("Time(s):",True,BLACK),(300,10))

    LastKeyPressed = ""

    Display.blit(pygame.font.Font("freesansbold.ttf",15).render("Press 0 to quit game",True,BLACK),(20,10))
    
    while True:
        Hangman(Condition)
        End = time.time() #end time
        if (int(End) - int(Start) == 1):
            pygame.draw.rect(Display,WHITE,(385,0,100,50)) #hide time
            TheTime = TheTime + 1 
            #print(TheTime, 'seconds has passed')
            Timer = Font2.render(str(TheTime),True,BLACK)
            Display.blit(Timer, (400,10))
            Start = time.time()
            
        for event in pygame.event.get():

            #mouse
            #print(pygame.mouse.get_pos())
            #print(pygame.mouse.get_pressed())

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == KEYDOWN:
                pygame.mixer.Sound('Music\Keyboard.wav').play()
                
                #if exit key is pressed
                LastKeyPressed = event.key
                pygame.draw.rect(Display,WHITE,(220,200,280,100)) #hide word
                pygame.draw.rect(Display,WHITE,(260,50,200,100)) # hide invalid input
                UserInput = event.key
                #print(chr(event.key))
                #This is use to check if it changes the ASCII int value to the char
                if re.search("[a-z]",chr(event.key)):
                    if ((chr(event.key).upper() in TheWord) or (chr(event.key).lower() in TheWord)):
                        for i in range(len(TheWord)):
                            if ((TheWord[i] == (chr(event.key)).upper()) or (TheWord[i] == (chr(event.key)).lower())):
                                EmptyList[i] = TheWord[i]

                    else:

                         Condition = Condition + 1
                         gate_selected=gate_choose()
                         qubit_selected=qubit_choose()
                         gateslist.append(gate_selected+qubit_selected)
                         qc=ansatz(gateslist)
                         qc.draw('mpl').savefig('current.png')
                         Display.fill(WHITE)

                    Hidden = Font.render("".join(EmptyList),True,BLACK)
                    HiddenRect = Hidden.get_rect()
                    HiddenRect.center = (350,250)
                    Display.blit(Hidden,HiddenRect)
                    
                else:
                    if (event.key == K_0 or event.key == 256):#256 is 0 in numpad
                        Display.blit(Font.render("EXIT?",True,RED),(340,220))
                        Display.blit(Font2.render("Yes",True,BLUE),(340,270))
                        Display.blit(Font2.render("No",True,BLUE),(415,270))
                    else:
                        Input = Font2.render("INVALID INPUT!!!",True,RED)
                        InputRect = Input.get_rect()
                        InputRect.center = (350,100)
                        Display.blit(Input, InputRect)
                        Display.blit(Hidden,HiddenRect)
                        
            elif event.type == KEYUP:
                pygame.draw.rect(Display,WHITE,(260,50,200,100)) # hide invalid input
                        
            elif event.type == MOUSEBUTTONDOWN:
                #print("mouse pressed")
                #print(pygame.mouse.get_pressed())
                if (pygame.mouse.get_pressed() != (0,0,0)):#Scroller of mouse
                    pygame.mixer.Sound('Music\Mouse Click Fast.wav').play()
                    
                if (LastKeyPressed == K_0 or LastKeyPressed == 256):#256 is 0 in numpad
                    if (pygame.mouse.get_pressed() == LEFT_CLICK):
                        #Yes
                        if (pygame.mouse.get_pos()[0] > 340 and\
                            pygame.mouse.get_pos()[1] > 270 and\
                            pygame.mouse.get_pos()[0] < 385 and\
                            pygame.mouse.get_pos()[1] < 285):
                            pygame.draw.rect(Display,WHITE,(340,270,35,25)) #hide yes
                            Display.blit(Font2.render("Yes",True,GREEN),(340,270))
                            #print(pygame.mouse.get_pos())
                            #print("YES")
                            
                        #NO
                        elif (pygame.mouse.get_pos()[0] > 415 and\
                              pygame.mouse.get_pos()[1] > 270 and\
                              pygame.mouse.get_pos()[0] < 450 and\
                              pygame.mouse.get_pos()[1] < 285):
                            pygame.draw.rect(Display,WHITE,(415,270,35,25)) #hide no
                            Display.blit(Font2.render("No",True,GREEN),(415,270))
                            #print(pygame.mouse.get_pos())
                            #print("NO")

                            
            elif event.type == MOUSEBUTTONUP:#Yes
                if (LastKeyPressed == K_0 or LastKeyPressed == 256):#256 is 0 in numpad
                    #Yes
                    if (pygame.mouse.get_pos()[0] > 340 and\
                       pygame.mouse.get_pos()[1] > 270 and\
                       pygame.mouse.get_pos()[0] < 385 and\
                       pygame.mouse.get_pos()[1] < 285):
                        
                        #quit game
                        pygame.quit()
                        sys.exit()

                    #No
                    elif (pygame.mouse.get_pos()[0] > 415 and\
                          pygame.mouse.get_pos()[1] > 270 and\
                          pygame.mouse.get_pos()[0] < 450 and\
                          pygame.mouse.get_pos()[1] < 285):
                        pygame.draw.rect(Display,WHITE,(415,270,35,25)) #hide no
                        Display.blit(Font2.render("No",True,GREEN),(415,270))
                        pygame.draw.rect(Display,WHITE,(300,200,200,100)) #hide exit, yes,no

                        Hidden = Font.render("".join(EmptyList),True,BLACK)
                        HiddenRect = Hidden.get_rect()
                        HiddenRect.center = (400,250)
                        Display.blit(Hidden,HiddenRect)

                        LastKeyPressed = ""
                    
                        
                    else:
                        pygame.draw.rect(Display,WHITE,(340,270,35,25)) #hide yes
                        Display.blit(Font2.render("Yes",True,BLUE),(340,270))
                        pygame.draw.rect(Display,WHITE,(415,270,35,25)) #hide no
                        Display.blit(Font2.render("No",True,BLUE),(415,270))

        #Check if the word is word and the condition
        if (Condition == 10):
            Display.fill(WHITE)
            Hangman(Condition+1)
            Over = Font2.render("GAME OVER!!!",True,RED)
            OverRect = Over.get_rect()
            OverRect.center = (400,250)
            Display.blit(Over,OverRect)
            Off = 1

            #stop the BGM
            pygame.mixer.music.stop()

            pygame.mixer.music.load('Music\KM\Loping Sting.mp3')
            pygame.mixer.music.play(0,0)

        elif (TheWord == "".join(EmptyList)):
            Display.fill(WHITE)
            Cong = Font.render("CONGRATS!!!",True,GREEN)
            CongRect = Cong.get_rect()
            CongRect.center = (250,220)
            Display.blit(Cong,CongRect)
            
            Word = Font2.render("The word is:",True,BLACK)
            WordRect = Word.get_rect()
            WordRect.center = (250,250)
            Display.blit(Word,WordRect)

            Word2 = Font.render(TheWord,True,BLACK)
            Word2Rect = Word2.get_rect()
            Word2Rect.center = (250,285)
            Display.blit(Word2,Word2Rect)
            
            Off = 1

            #stop the BGM
            pygame.mixer.music.stop()

            pygame.mixer.music.load('Music\KM\Loping Sting.mp3')
            pygame.mixer.music.play(0,0)            

        pygame.display.update()
        pygame.time.Clock().tick(30) #30fps
        
        if (Off == 1):
            #wait 5 seconds
            time.sleep(5)
            #quit game
            pygame.quit()
            sys.exit()

main()
        
