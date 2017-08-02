import pygame,sys,random,time,os
pygame.init()
class flappy():
    def __init__(self,x,y):
     self.movex=0
     self.movey=1
     self.rect=pygame.Rect((x, y, 36, 26))
     self.flapsound = pygame.mixer.Sound(os.path.relpath("flap.wav"))
     self.crashsound = pygame.mixer.Sound(os.path.relpath("hurt.wav"))
     self.scoresound = pygame.mixer.Sound(os.path.relpath("score.wav"))
     self.birdimg = pygame.image.load(os.path.relpath("bird_sing.png"))

    def move(self, y):
        self.rect=self.rect.move(0,y)
    def render(self,screen):
        screen.blit(self.birdimg, self.rect)
    def collide(self,firstwallpair):
        return self.rect.colliderect(firstwallpair.upperwall) or self.rect.colliderect(firstwallpair.lowerwall)
    def experimental(self,y):
        self.rect.y=self.rect.y+y




class pillarpair():
    def __init__(self, width,height,xcord,screen):
        self.screen=screen
        self.width = width
        self.height = height
        self.xcord=xcord
        self.widthofwall = 20
        self.newwall(xcord)
        self.assetloader(width,height)


    def assetloader(self,width, height):

        self.pillar1 = pygame.image.load(os.path.relpath("tube1.png"))
        self.pillar2 = pygame.image.load(os.path.relpath("tube2.png"))
        self.pillar1dest = pygame.transform.scale(self.pillar1, (self.widthofwall, self.upperwall.height))
        self.pillar2dest = pygame.transform.scale(self.pillar2, (self.widthofwall, self.lowerwall.height))

    def newwall(self,xcord):
        self.firstrectlength = random.randint(50, 300)
        self.secondrectlength = self.height - 200 - self.firstrectlength
        self.upperwall = pygame.Rect(xcord, 0, self.widthofwall, self.firstrectlength)
        self.lowerwall = pygame.Rect(xcord, self.height - self.secondrectlength, self.widthofwall, self.secondrectlength)

    def renderpillars(self):
        self.screen.blit(self.pillar1dest, self.upperwall)
        self.screen.blit(self.pillar2dest, self.lowerwall)
    def move(self,x):
        self.upperwall=self.upperwall.move(x,0)
        self.lowerwall=self.lowerwall.move(x,0)

    def copy(self,obj2):
        self.upperwall=obj2.upperwall
        self.lowerwall=obj2.lowerwall



def getgoing():
    size = width, height = 300, 510
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("GK Flappy bird")
    x, y = 10, height / 2
    movey = 4
    bird=flappy(x,y)
    clock = pygame.time.Clock()

    score = 0
    frame = 0
    accel=0
    upaccel=0
    moveyes=0
    qa = 1
    setyes=1
    firstwallx = 200
    secondwallx = 350
    thirdwallx = 500
    totaltimesinceevent=0
    initializer=0

    background = pygame.image.load(os.path.relpath("bg.png"))
    background = pygame.transform.scale(background, (width, height))
    firstwallpair = pillarpair(width, height, firstwallx,screen)
    secondwallpair = pillarpair(width, height, secondwallx,screen)
    thirdwallpair = pillarpair(width, height, thirdwallx,screen)
    while True:

        a=clock.tick_busy_loop(120)
        totaltimesinceevent+=a
        if initializer==0:
            totaltimesinceevent=8
            initializer=1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    movey=1
                    #bird.move(movey)
                    moveyes=1

                    #movey = -90

                    bird.flapsound.play()
                    #movey = 4
                    totaltimesinceevent=0
                    frame=0

        if bird.collide(firstwallpair):
            scorecarddisp = collided(score, width, height)
            bird.crashsound.play()
            anotherdraw(scorecarddisp, width, height,firstwallpair,secondwallpair, bird, background)
            break
        elif bird.rect.left > firstwallpair.upperwall.right and qa == 1:
            score += 1
            bird.scoresound.play()
            qa = 0

        frame += 1



        firstwallpair.move(-1)
        secondwallpair.move(-1)
        thirdwallpair.move(-1)
        if firstwallpair.upperwall.left == -firstwallpair.widthofwall:
            firstwallpair.copy(secondwallpair)
            secondwallpair.copy(thirdwallpair)
            var=thirdwallpair.upperwall.x
            thirdwallpair.newwall(var+150)
            firstwallpair.assetloader(width,height)
            secondwallpair.assetloader(width,height)
            thirdwallpair.assetloader(width,height)
            qa = 1

        if bird.rect.bottom >= height:
            bird.rect.bottom = height
        if bird.rect.top <= 0:
            bird.rect.top = 0

        if moveyes==0:
            if frame <= 15:

                movey = 1
                bird.experimental(movey)
                if frame == 15:
                    movey = 4
                    bird.experimental(movey)
                    movey = 1
                    accel = 0
            else:
                accel += 1
                if accel == 46:
                    if movey < 10:
                        movey += 1
                    accel = 0
                bird.experimental(movey)


        else:

            upaccel += 1
            if upaccel == 1:

                if movey > -6:
                    movey -= 0.5
                    print movey
                    if movey <= -6:
                        moveyes = 0

                bird.experimental(movey)
                upaccel = 0











        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        firstwallpair.renderpillars()
        secondwallpair.renderpillars()
        thirdwallpair.renderpillars()
        bird.render(screen)

        pygame.display.flip()


def collided(score, width, height):
    scorefont = pygame.font.get_default_font()
    scorecard = pygame.font.Font(scorefont, 50)
    scorecarddisp = scorecard.render(str(score), 0, (0, 0, 0))
    return scorecarddisp


def anotherdraw(scorecarddisp, width, height,firstwallpair,secondwallpair , bird, background):
    screen = pygame.display.set_mode()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    getgoing()

        screen.blit(background, (0, 0))

        firstwallpair.renderpillars()
        secondwallpair.renderpillars()

        bird.render(screen)
        screen.blit(scorecarddisp, (width / 2, height / 2))
        pygame.display.flip()


getgoing()

"""

""""""

    def exp(self,y,tick,totaltimesinceevent,acceleration,moveyes,movey):


        if moveyes==0:
            if totaltimesinceevent <= 15 * tick:

                movey = 0.1
                self.experimental(movey)
                if totaltimesinceevent == 15 * tick:

                    movey = 4
                    self.experimental(movey)
                    movey = 1
            elif totaltimesinceevent == 43 * tick:

                if movey < 10:
                    movey += 1
                self.experimental(movey)
                totaltimesinceevent=0

        elif moveyes==1:


            if self.movey > -6:
                print self.movey
                self.movey =self.movey- 1
                if self.movey <= -6:
                    moveyes = 0

            self.move(movey)

        #if self.movey != y:
         #   self.movey = (self.movey + acceleration)
          #  self.experimental(self.movey)


            #if totaltimesinceevent <= 135:

#            if moveyes == 0:
 #               if setyes == 1:
  #                  tempy = 0.1
   #                 self.experimental(tempy)
    #                setyes = 0
     #       return 12




"""

"""
    else:
            bird.exp(-6,a,totaltimesinceevent,-0.5,moveyes,setyes)
            if bird.movey<-6:
                moveyes=0
                setyes=1



"""