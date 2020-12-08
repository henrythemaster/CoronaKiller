#Importação de módulos.
import pygame
import random

#Iniciar módulos do pygame.
pygame.init()

#Frames por segundo.
FPS = pygame.time.Clock()

#Parâmetros da janela principal.
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
mainwindowWIDTH = 1000
mainwindowHEIGHT = 700
mainwindow = pygame.display.set_mode((mainwindowWIDTH, mainwindowHEIGHT))
pygame.display.set_caption("CORONA")

#Iniciar os módulos do pygame.
pygame.init()

#Imagens/Sons/Fonte.
player1image = pygame.image.load("jogador.png")
proteinimage = pygame.image.load("proteina.png")
virusimage = pygame.image.load("virus.png")
shieldimage = pygame.image.load("escudo.png")
bombimage = pygame.image.load("bomba.png")
shielddropimage = pygame.image.load("shielddrop.png")
slowdropimage = pygame.image.load("slowdrop.png")
bombdropimage = pygame.image.load("bombdrop.png")
eatsound = pygame.mixer.Sound("eat.wav")
spawnsound = pygame.mixer.Sound("spawn.wav")
gameoversound = pygame.mixer.Sound("gameover.wav")
slowsound = pygame.mixer.Sound("slow.wav")
bipsound = pygame.mixer.Sound("bip.wav")
popsound = pygame.mixer.Sound("pop.wav")
bombsound = pygame.mixer.Sound("bomb.wav")
font_name = pygame.font.match_font('arial')

#Definir o volume do som do jogo.
pygame.mixer.Sound.set_volume(eatsound, 0.3)
pygame.mixer.Sound.set_volume(bipsound, 0.3)

#Definir icone.
pygame.display.set_icon(player1image)

#Vars Globais.
proteinlist = []
poweruplist = []
viruslist = []
timeeventlist = []
score = 0
running = True
fps = 160

#Jogador1 classe.
class player1(object):
    def __init__(self, player1X, player1Y, player1WIDTH, player1HEIGHT, player1state):
        self.player1X = player1X
        self.player1Y = player1Y
        self.player1WIDTH = player1WIDTH
        self.player1HEIGHT = player1HEIGHT
        self.player1speed = 3
        self.player1state = player1state
        self.player1shield = False
        self.player1bomb = False
        self.player1bombcount = 0
    def draw(self, mainwindow):
        if self.player1state:
            mainwindow.blit(player1image, (self.player1X, self.player1Y))
            if self.player1shield:
                mainwindow.blit(shieldimage, (self.player1X - 4, self.player1Y - 4))
            if self.player1bomb:
                mainwindow.blit(bombimage, (self.player1X - 48, self.player1Y - 48))

#Proteina classe.
class protein(object):
    def __init__(self, proteinX, proteinY, proteinstate):
        self.proteinX = proteinX
        self.proteinY = proteinY
        self.proteinstate = proteinstate
    def draw(self, mainwindow):
        global score
        if self.proteinstate:
            mainwindow.blit(proteinimage, (self.proteinX, self.proteinY))
            if player1instance.player1X < self.proteinX + 25 and player1instance.player1X + 25 > self.proteinX and player1instance.player1Y < self.proteinY + 25 and player1instance.player1Y + 25 > self.proteinY:
                    self.proteinstate = False
                    eatsound.play()
                    score = score + 1
                    #Spawn power up every x.
                    if score % 25 == 0:
                        spawnpowerup(1)
        else:
            proteinlist.remove(self)

#Poderes classes.
class powerup(object):
    def __init__(self, x, y, item, state):
        self.x = x
        self.y = y
        self.item = item
        self.state = state
    def draw(self, mainwindow):
        global fps
        if self.state:
            if player1instance.player1X < self.x + 25 and player1instance.player1X + 25 > self.x and player1instance.player1Y < self.y + 25 and player1instance.player1Y + 25 > self.y:
                if self.item == "shield":
                    self.state = False
                    eatsound.play()
                    player1instance.player1shield = True
                elif self.item == "slow":
                    self.state = False
                    eatsound.play()
                    slowtime(True)
                elif self.item == "bomb":
                    self.state = False
                    eatsound.play()
                    bipsound.play()
                    if player1instance.player1bombcount == 0:
                        timeeventlist.append(timeevent(1000, "bip"))
                        timeeventlist.append(timeevent(2000, "bombon"))
                    player1instance.player1bombcount += 1
            if self.item == "shield":
                mainwindow.blit(shielddropimage, (self.x, self.y))
            elif self.item == "slow":
                mainwindow.blit(slowdropimage, (self.x, self.y))
            elif self.item == "bomb":
                mainwindow.blit(bombdropimage, (self.x, self.y))

#Virus classes.
class virus(object):
    def __init__(self, virusX, virusY, virusstate):
        self.virusX = virusX
        self.virusY = virusY
        self.virusstate = virusstate
        self.virusdirectionX = randomint()
        self.virusdirectionY = randomint()
    def draw(self, mainwindow):
        if self.virusstate:
            if player1instance.player1bomb:
                if player1instance.player1X - 60 < self.virusX + 16 and player1instance.player1X + 92 > self.virusX and player1instance.player1Y - 60 < self.virusY + 16 and player1instance.player1Y + 92 > self.virusY:
                    self.virusstate = False
            if player1instance.player1X < self.virusX + 16 and player1instance.player1X + 16 > self.virusX and player1instance.player1Y < self.virusY + 16 and player1instance.player1Y + 16 > self.virusY:
                if not player1instance.player1shield:
                    player1instance.player1state = False
                else:
                    popsound.play()
                    self.virusstate = False
                    player1instance.player1shield = False
            mainwindow.blit(virusimage, (self.virusX, self.virusY))
            self.virusX = self.virusX + self.virusdirectionX
            self.virusY = self.virusY + self.virusdirectionY
            virus.move(self)
        else:
            viruslist.remove(self)
    def move(self):
        if self.virusX >= 990:
            self.virusdirectionX = -1 + randomint()
            self.virusdirectionY = +1 + randomint()
        if self.virusX <= 0:
            self.virusdirectionX = +1 + randomint()
            self.virusdirectionY = -1 + randomint()
        if self.virusY >= 790:
            self.virusdirectionY = -1 + randomint()
            self.virusdirectionX = +1 + randomint()
        if self.virusY <= 0:
            self.virusdirectionY = +1 + randomint()
            self.virusdirectionX = -1 + randomint()

#Tela de game over.
def mainmenu():
    global proteinlist, poweruplist, viruslist, score, running
    gameover = True
    pygame.time.set_timer(28, 100)
    #input_box
    replay_box = pygame.Rect(500, 500, 140, 32)
    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = False
                running = False
            if event.type == 28:
                mainwindow.fill((0, 0, 0))
                draw_text(mainwindow, "CORONAKILLER", 80, 500, 300)
                draw_text(mainwindow, "APERTE ENTER PARA COMEÇAR", 30, 500, 600)
                mainwindow.blit(virusimage, (500, 400))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameover = False
                    running = True
                    player1instance.player1X = 500
                    player1instance.player1Y = 400
                    player1instance.player1state = True
                    proteinlist = []
                    poweruplist = []
                    viruslist = []
                    score = 0
                    start()
        pygame.display.update()

#Tela de game over2.
def gameover():
    global proteinlist, poweruplist, viruslist, timeeventlist, score, running, fps
    gameover = True
    pygame.time.set_timer(28, 1800)
    pygame.mixer.music.stop()
    gameoversound.play()
    #input_box
    replay_box = pygame.Rect(500, 500, 140, 32)
    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = False
                running = False
            if event.type == 28:
                mainwindow.fill((0, 0, 0))
                draw_text(mainwindow, "FIM DE JOGO !", 80, 500, 300)
                draw_text(mainwindow, "Seu placar: {}".format(str(score)), 30, 500, 400)
                draw_text(mainwindow, "Aperte enter para tentar denovo", 30, 500, 500)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameover = False
                    running = True
                    player1instance.player1X = 500
                    player1instance.player1Y = 400
                    player1instance.player1state = True
                    player1instance.player1bomb = False
                    player1instance.player1bombcount = 0
                    proteinlist = []
                    poweruplist = []
                    viruslist = []
                    timeeventlist = []
                    score = 0
                    fps = 160
                    start()
        pygame.display.update()

#Função do display.
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#Evento temporizador x.
class timeevent(object):
    def __init__(self, x, reason):
        self.start = pygame.time.get_ticks()
        self.x = x
        self.reason = reason
    def timer(self):
        passedtime = pygame.time.get_ticks() - self.start
        if passedtime >= self.x:
            return True
        else:
            return False

#Tempo lento / não lento, verifica se o evento lento já está em andamento.
def slowtime(state):
    global fps
    dupcheck = False
    if state:
        for events in timeeventlist:
            if events.reason == "slow":
                dupcheck = True
                events.x += 10000
                slowsound.play()
        if not dupcheck:
            fps = 60
            timeeventlist.append(timeevent(10000, "slow"))
            pygame.mixer.music.set_volume(0.0)
            slowsound.play()
    else:
        for events in timeeventlist:
            if events.reason == "slow":
                timeeventlist.remove(events)
        fps = 160
        pygame.mixer.music.set_volume(0.5)

# Gera um rand int -1 ou 1.
def randomint(x = 1):
    rand = random.randint(0, x)
    if rand == 0:
        return -1
    else:
        return 1

#Spawn das proteinas.
def spawnprotein(amount):
    for x in range(amount):
        proteinlist.append(protein(random.randint(0, mainwindowWIDTH-50), random.randint(0, mainwindowHEIGHT-50), True))

#Spawn dos virus.
def spawnvirus(amount):
    spawnsound.play()
    for x in range(amount):
        viruslist.append(virus(random.randint(0, 1000), random.randint(0, 800), True))

#Spawn dos poderes.
def spawnpowerup(amount):
    item = ""
    for x in range(amount):
        rand = random.randint(0, 2)
        if rand == 0:
            item = "shield"
        elif rand == 1:
            item = "slow"
        elif rand == 2:
            item = "bomb"
        poweruplist.append(powerup(random.randint(0, mainwindowWIDTH-50), random.randint(0, mainwindowHEIGHT-50), item, True))

#Display update, every frame is updated here.
def mainwindowdraw():
    global running
    mainwindow.fill((0, 0, 0))
    player1instance.draw(mainwindow)
    for viruses in viruslist:
        virus.draw(viruses, mainwindow)
    for proteins in proteinlist:
        protein.draw(proteins, mainwindow)
    for powerups in poweruplist:
        powerup.draw(powerups, mainwindow)
    draw_text(mainwindow, str(score), 50, mainwindowWIDTH / 2, 10)
    if player1instance.player1state == False:
        gameover()
    pygame.display.update()


#Instance player1 ().
player1instance = player1(500, 400, 32, 32, True)

#Começar jogo.
def start():
    global running
    global fps
    #Começar prot/virus spawn.
    spawnprotein(25)
    spawnvirus(1)
    #Começar musica.
    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    #Loop principal.
    pygame.time.set_timer(25, 450)
    pygame.time.set_timer(26, 8000)
    while running:
        #Refresh rate.
        FPS.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == 25:
                spawnprotein(1)
            if event.type == 26:
                spawnvirus(1)
        #Player input.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player1instance.player1X > player1instance.player1speed and player1instance.player1state:
            player1instance.player1X -= player1instance.player1speed
        elif keys[pygame.K_RIGHT] and player1instance.player1X < mainwindowWIDTH - player1instance.player1WIDTH - player1instance.player1speed and player1instance.player1state:
            player1instance.player1X += player1instance.player1speed
        if keys[pygame.K_UP] and player1instance.player1Y > player1instance.player1speed and player1instance.player1state:
            player1instance.player1Y -= player1instance.player1speed
        elif keys[pygame.K_DOWN] and player1instance.player1Y < mainwindowHEIGHT - player1instance.player1HEIGHT - player1instance.player1speed and player1instance.player1state:
            player1instance.player1Y += player1instance.player1speed

        # Eventos cronometrados.
        if timeeventlist:
            for events in timeeventlist:
                if timeevent.timer(events):

            # Se o evento lento terminar, verifique outros eventos lentos na lista.
                    if events.reason == "slow":
                        slowtime(False)
                    if events.reason == "bombon":
                        bombsound.play()
                        player1instance.player1bomb = True
                        timeeventlist.remove(events)
                        timeeventlist.append(timeevent(1000, "bomboff"))
                    if events.reason == "bomboff":
                        player1instance.player1bomb = False
                        timeeventlist.remove(events)
                        player1instance.player1bombcount -= 1
                        if player1instance.player1bombcount > 0:
                            timeeventlist.append(timeevent(2000, "bombon"))
                    if events.reason == "bip":
                        bipsound.play()
                        timeeventlist.remove(events)
        #Draw.
        mainwindowdraw()

#Start.
mainmenu()
pygame.quit()
