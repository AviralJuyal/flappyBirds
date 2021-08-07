import sys      # we will use this to exit the game
import random   # To create randomness in game
import pygame   
from pygame.locals import *
 
#Global variable for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH , SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPIRITS = {}
GAME_SOUNDS = {}
PIPE = 'gallary/images/pipe.png'
PLAYER = 'gallary/images/flappybird.png'
BACKGROUND = 'gallary/images/background.png'

def welcomeScreen():
    '''
    shows welcome image on the screen
     '''
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPIRITS['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPIRITS['message'].get_height()+80)/2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            #if user clicks on cross then it should close the game 
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #if the user presses space or up key then the game should start
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            
            else:
                SCREEN.blit(GAME_SPIRITS['background'], (0,0))
                # SCREEN.blit(GAME_SPIRITS['player'], (playerx , playery))
                SCREEN.blit(GAME_SPIRITS['message'], (messagex , messagey))
                SCREEN.blit(GAME_SPIRITS['base'], (basex , GROUNDY ))
                pygame.display.update()
                FPSCLOCK.tick(FPS)




def mainGame():
    

    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0 
    
    #creating 2 pipes for bliting on screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    
    #list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200 , 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2) , 'y': newPipe2[0]['y'] }
    ]
 
    #list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200 , 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2) , 'y': newPipe2[1]['y'] }
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccVelY = 1

    playerFlapAccV = -8     # velocity while flapping
    playerFlapped = False   # It is true only when bird is flapping
   
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
             
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccV
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollid(playerx , playery , upperPipes , lowerPipes)  #this will return true if crashed 
        if crashTest:
           
            # GAME_SOUNDS['gameover'].play()
            return       
                
        #check for score
        playerMidPos = playerx + GAME_SPIRITS['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPIRITS['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4 :
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()


        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccVelY   

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPIRITS['player'].get_height()
        playery = playery + min(playerVelY , GROUNDY - playery - playerHeight) #it is used so that the player should not go below the ground
        
        for upperpipe , lowerpipe in zip(upperPipes , lowerPipes):
            upperpipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX

        #add a new pipe when the first pipe about to go to the left out of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        #if the pipe is out of the screen then remove it
        if upperPipes[0]['x'] < -GAME_SPIRITS['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #lets blit splites now
        if score < 15 or (score >30 and score < 45) :
            
            SCREEN.blit(GAME_SPIRITS['background'], ( 0,0 ))
        else :

            SCREEN.blit(GAME_SPIRITS['backgroundnight'], ( 0,0 ))
            
        for upperpipe , lowerpipe in zip(upperPipes , lowerPipes):
            SCREEN.blit(GAME_SPIRITS['pipe'][0], (upperpipe['x'] ,upperpipe['y'] ))
            SCREEN.blit(GAME_SPIRITS['pipe'][1], (lowerpipe['x'] ,lowerpipe['y'] ))            

        SCREEN.blit(GAME_SPIRITS['base'], (basex ,GROUNDY ))
        SCREEN.blit(GAME_SPIRITS['player'], ( playerx,playery ))

        if score % 15 == 0 and score != 0:
            GAME_SOUNDS['level'].play() 
             

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPIRITS['numbers'][digit].get_width()

        xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPIRITS['numbers'][digit] , (xoffset, SCREENHEIGHT*0.12))
            xoffset += GAME_SPIRITS['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)



def isCollid(playerx , playery , upperPipes , lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True    
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPIRITS['pipe'][0].get_height()
        if (playery<pipeHeight + pipe['y'] and abs(playerx - pipe['x'])< GAME_SPIRITS['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
            if (playery + GAME_SPIRITS['player'].get_height()> pipe['y'])and abs(playerx - pipe['x'])< GAME_SPIRITS['pipe'][0].get_width():
                GAME_SOUNDS['hit'].play()
                return True
    

def getRandomPipe():
    '''
    generates random positions of pipes (straight pipe at the bottom and rotated one at the top)
    '''
    pipeHeight = GAME_SPIRITS['pipe'][0].get_height()
    
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0 , int(SCREENHEIGHT - GAME_SPIRITS['base'].get_height() - 1.2*offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x' : pipeX , 'y' : -y1 } , #Upper pipe
        {'x' : pipeX , 'y' : y2 }   #Lower pipe
    ]
    return pipe


if __name__ == '__main__':
    #main game prog starts from here

    pygame.init()  #to initialize the modules of pygame module
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy game by Aviral')
    GAME_SPIRITS ['numbers'] = (
     pygame.image.load('gallary/images/0.png').convert_alpha(), 
     pygame.image.load('gallary/images/1.png').convert_alpha(),  
     pygame.image.load('gallary/images/2.png').convert_alpha(), 
     pygame.image.load('gallary/images/3.png').convert_alpha(),  
     pygame.image.load('gallary/images/4.png').convert_alpha(),
     pygame.image.load('gallary/images/5.png').convert_alpha(),
     pygame.image.load('gallary/images/6.png').convert_alpha(),
     pygame.image.load('gallary/images/7.png').convert_alpha(), 
     pygame.image.load('gallary/images/8.png').convert_alpha(), 
     pygame.image.load('gallary/images/9.png').convert_alpha() 
    )

    GAME_SPIRITS['message'] = (pygame.image.load('gallary/images/welcome.png').convert_alpha())
    GAME_SPIRITS['base'] = ( pygame.image.load('gallary/images/base.png').convert_alpha() )
    GAME_SPIRITS['pipe'] = ( 
       pygame.transform.rotate (pygame.image.load(PIPE).convert_alpha(), 180),
       pygame.image.load(PIPE).convert_alpha()
        )
    GAME_SPIRITS['backgroundnight'] = (pygame.image.load('gallary/images/backgroundnight.png'))
    
    #GAME SOUNDS
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallary/audio/hit.mp3')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallary/audio/swoosh.mp3')
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallary/audio/die.mp3')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallary/audio/wing.mp3')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallary/audio/point.mp3')
    GAME_SOUNDS['level'] = pygame.mixer.Sound('gallary/audio/level.wav')



    GAME_SPIRITS['background'] = ( pygame.image.load(BACKGROUND).convert())
    GAME_SPIRITS['player'] = ( pygame.image.load(PLAYER).convert_alpha())

    while True:
        welcomeScreen()
        mainGame()
    
        