import sys, pygame, random, time

                                                ###################################################################################################
                                                #           Game Creator - Vsevolod (Folgo) Prostyakov                                            #
                                                #           GitHub - https://github.com/Fo1Go                                                     #
                                                #           Vk - https://vk.com/seva229                                                           #
                                                ###################################################################################################

                                                # Initialization game variables
SIZE = WIDTH, HEIGHT = 800, 600
FPS = 200
RUNNING = True
LEVEL = 1
SCORE = 0
DEAD = 0
MAX_DEAD = 5
MAX_SCORE = 20
MAX_CANDY = 8
CANDY_NOW = 0
                                                # Initialization game
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Happy 2021")        # Initialization game caption 
screen = pygame.display.set_mode(SIZE)          # Initialization game window
clock = pygame.time.Clock()                     # Initialization game fps

background = pygame.image.load("images/bg.png") # Initialization background
bg = background.get_rect()
font_name = pygame.font.match_font('arial')     # Initialization font

class Game:
    """
    Class Game: Contains functions to be called in the game
    """
    def draw_text_center(self,surf, text, size, x, y):
        """
        Game.draw_text_center - draw text
        surf - the screen on which the text will be displayed
        text - the text to be displayed
        size - text size
        x - coordinate x (relative to the center) where the text will be located
        y - coordinate y (relative to the center) where the text will be located
        """
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, (0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    """
    Class Player: Creates a character for which we will play
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("images/lcanta.png").convert(), (120, 180))
        self.image.set_colorkey((71,112,76))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT-80)
        self.speedx = 0

    def update(self):
        """
        Player.update() - updated once per fps/1000
        """
        keystate = pygame.key.get_pressed()
        if LEVEL == 1 or LEVEL == 2:
            if keystate[97]:
                self.speedx = -1
            if keystate[100]:
                self.speedx = 1
        if LEVEL == 3:
            if keystate[97]:
                self.speedx = -2
            if keystate[100]:
                self.speedx = 2
        if keystate[115]:
            self.speedx = 0
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class candy(pygame.sprite.Sprite):
    """
    Class candy: Creates a candy for which we will catch
    """
    def __init__(self):
        global CANDY_NOW
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("images/candy"+ str(random.randint(1,2)) +".png").convert(), (50, 50))
        self.image.set_colorkey((71,112,76))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(WIDTH/40,WIDTH-(WIDTH/40)),random.randint(25,50))
        CANDY_NOW += 1

    def update(self):
        """
        candy.update() - updated once per fps/1000
        """
        global DEAD, CANDY_NOW
        if LEVEL == 1:
            self.rect.center = (self.rect.center[0],self.rect.center[1]+random.randint(1,1))
        if LEVEL == 2:
            self.rect.center = (self.rect.center[0],self.rect.center[1]+random.randint(1,2))
        if LEVEL == 3:
            self.rect.center = (self.rect.center[0],self.rect.center[1]+random.randint(1,3))
        if self.rect.center[1] > 601:
            self.kill()
            CANDY_NOW -= 1
            c = candy()
            all_sprites.add(c)
            cands.add(c)
            DEAD = DEAD + 1

if LEVEL == 1:
    all_sprites = pygame.sprite.Group()
    cands = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    for i in range(4):
        c = candy()
        all_sprites.add(c)
        cands.add(c)
    
# Beginning of the game     
while RUNNING:
    game = Game()
    clock.tick(FPS)
    for event in pygame.event.get(): 
        # If game be closed, we do sys.exit()
        if event.type == 256: # can be like     if event.type == pygame.QUIT: 
            sys.exit()
        # If button is down
        if event.type == 768: # can be like     if event.type == pygame.KEYDOWN: 
            if event.key == 32: # ID32 == K_SPACE
                if DEAD >= MAX_DEAD and LEVEL >= 1:
                    LEVEL = 1
                    SCORE = 0
                    DEAD = 0
                    MAX_CANDY = 8
                    CANDY_NOW = 0
                    MAX_DEAD = 5
                    MAX_SCORE = 20

                    player = Player()
                    all_sprites.add(player)

                    for i in range(4):
                        c = candy()
                        all_sprites.add(c)
                        cands.add(c)

                if SCORE >= MAX_SCORE and LEVEL == 1:
                    LEVEL = 2
                    SCORE = 0
                    DEAD = 0
                    MAX_CANDY = 12
                    CANDY_NOW = 0
                    MAX_DEAD = 12
                    MAX_SCORE = 30

                    player = Player()
                    all_sprites.add(player)

                    for i in range(5):
                        c = candy()
                        all_sprites.add(c)
                        cands.add(c)

                if SCORE >= MAX_SCORE and LEVEL == 2:
                    LEVEL = 3
                    SCORE = 0
                    DEAD = 0
                    MAX_CANDY = 18
                    CANDY_NOW = 0
                    MAX_DEAD = 15
                    MAX_SCORE = 60

                    player = Player()
                    all_sprites.add(player)

                    for i in range(6):
                        c = candy()
                        all_sprites.add(c)
                        cands.add(c)

                if SCORE >= MAX_SCORE and LEVEL == 3:
                    player.kill()
                    for deadly in cands:
                        deadly.kill()
                    RUNNING = False

    hits = pygame.sprite.spritecollide(player, cands, False)
    for hit in hits:
        hit.kill()
        CANDY_NOW -= 1
        if not (CANDY_NOW > MAX_CANDY):
            c = candy()
            all_sprites.add(c)
            cands.add(c)
        SCORE+=1

    all_sprites.update()
    player.update()
    screen.fill((0,0,0))
    screen.blit(background, bg)
    all_sprites.draw(screen)
    game.draw_text_center(screen, f"У вас {SCORE} конфет | Нужно поймать {MAX_SCORE} конфет | Вы потеряли {DEAD} конфет(ы) | Можно потерять конфет - {MAX_DEAD} | Вы на {LEVEL} уровне", 17, WIDTH/2, 20)

    # There is nothing further.

    if DEAD >= MAX_DEAD:
        player.kill()
        for deadly in cands:
            deadly.kill()
        game.draw_text_center(screen, f"Ты проиграл с {SCORE} конфетами!", 48, WIDTH/2, 200)
        game.draw_text_center(screen, f"Что бы начать заного нажмите Space.", 48, WIDTH/2, 250)
        
    if SCORE >= MAX_SCORE and LEVEL == 1:
        player.kill()
        for deadly in cands:
            deadly.kill()
        game.draw_text_center(screen, f"Ты победил с {DEAD} потеряннымы конфетами!", 48, WIDTH/2, 200)
        game.draw_text_center(screen, f"Что бы продолжить нажмите Space.", 48, WIDTH/2, 250)
    
    if SCORE >= MAX_SCORE and LEVEL == 2:
        player.kill()
        for deadly in cands:
            deadly.kill()
        game.draw_text_center(screen, f"Ты победил с {DEAD} потеряннымы конфетами!", 48, WIDTH/2, 200)
        game.draw_text_center(screen, f"Что бы продолжить нажмите Space.", 48, WIDTH/2, 250)

    if SCORE >= MAX_SCORE and LEVEL == 3:
        player.kill()
        for deadly in cands:
            deadly.kill()
        game.draw_text_center(screen, f"Ты победил с {DEAD} потеряннымы конфетами!", 48, WIDTH/2, 200)
        game.draw_text_center(screen, f"Что бы продолжить нажмите Space.", 48, WIDTH/2, 250)

    pygame.display.flip()

while True: # Victory screen
    screen.fill((0,0,0))
    screen.blit(background, bg)
    game.draw_text_center(screen, f"Вы прошли игру. Поздравляю!", 48, WIDTH/2, 200)
    for event in pygame.event.get(): 
        if event.type == 256:
            sys.exit()
    pygame.display.flip()

pygame.quit()