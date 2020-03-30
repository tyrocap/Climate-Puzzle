import pygame, sys, os, random

class ClimatePuzzle:
    def __init__(self, gs, ts, ms):
        self.gs = gs
        self.ts = ts
        self.ms = ms

        self.tiles_len = gs[0]*gs[1] - 1
        self.tiles = [(x,y) for y in range(gs[1]) for x in range(gs[0])]
        self.tilepos = {(x,y):(x*(ts+ms)+ms, y*(ts+ms)+ms) for y in range(gs[1]) for x in range(gs[0])}
        self.font = pygame.font.Font(None, 50)
        self.prev = None

        w, h = gs[0]*(ts+ms)+ms, gs[1]*(ts+ms)+ms

        pic = pygame.image.load('Ocean-Pollution.jpg')
        pic = pygame.transform.scale(pic, (w, h))

        self.images = []
        for i in range(self.tiles_len):
            x, y = self.tilepos[self.tiles[i]]
            image = pic.subsurface(x, y, ts, ts)
            self.images += [image]

    def getBlank(self):
        return self.tiles[-1]
    
    def setBlank(self, pos):
        self.tiles[-1] = pos
    
    opentile = property(getBlank, setBlank)

    def switch(self, tile): 
        self.tiles[self.tiles.index(tile)] = self.opentile
        self.opentile = tile


    def in_grid(self, tile): 
        return tile[0] >= 0 and tile[0] < self.gs[0] and tile[1] >= 0 and tile[1] < self.gs[1] 

    def adjacent(self):
        x, y = self.opentile
        return (x-1, y), (x+1, y), (x, y-1), (x, y+1)
    
    def random(self):
        adj = self.adjacent()
        self.switch(random.choice([pos for pos in adj if self.in_grid(pos) and pos != self.prev]))

    # Create a mouse vs grid
    def update(self, dt):
        
        mouse = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()

        if mouse[0]:

            x = mpos[0] % (self.ts + self.ms)
            y = mpos[1] % (self.ts + self.ms)
            
            if x > self.ms and y > self.ms:

                tile = mpos[0]//self.ts, mpos[1]//self.ts
                n = self.tiles.index(tile)
                if self.in_grid(tile): 
                    self.switch(tile)
               
    # Draw tiles
    def draw(self, screen):
        for i in range(self.tiles_len):
            x, y = self.tilepos[self.tiles[i]]
            screen.blit(self.images[i], (x,y))
    
    # Assign SPACE to random 
    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for i in range(200):
                    self.random()

def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def button_objects(screen, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                if action == "play": 
                    game_main()
                elif action == "quit": 
                    pygame.quit(); sys.exit()

 
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))

        small_text_font = pygame.font.Font('freesansbold.ttf', 20)
        text_surface, text_rect = text_objects(msg, small_text_font, (255, 255, 255))
        text_rect.center = ((x+(w/2)), (y+(h/2)))
        screen.blit(text_surface, text_rect)

def game_intro():

    pygame.init()
    pygame.display.set_caption('Intro')
    screen = pygame.display.set_mode((860, 690))
    fpsclock = pygame.time.Clock()
    screen.fill((240,240,240))
    
    w, h = 900, 700
    background = pygame.image.load('flags.jpg')
    background = pygame.transform.scale(background, (w, h))
    
    screen.blit(background, (0, 0))

    while True:
        dt = fpsclock.tick()/1000
        
        text_font = pygame.font.Font('freesansbold.ttf', 50)
        text_surface, text_rect = text_objects('Climate Puzzle', text_font, (51, 0, 255))
        text_rect.center = ((900/2), (230))
        screen.blit(text_surface, text_rect)

        text_font = pygame.font.Font('freesansbold.ttf', 20)
        text_surface, text_rect = text_objects('Contributors: (The Zip team) Adam | Bean | Bermet | Dzmitry', text_font, (0, 0, 0))
        text_rect.center = ((900/3), (650))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        screen.blit(text_surface, text_rect)
        
        button_objects(screen,'Enter', 180, 350, 100, 50, (51, 90, 255), (51, 120, 255), "play")
        
        button_objects(screen,'Quit', 570, 350, 100, 50, (51, 90, 255), (51, 120, 255), "quit")
        
        
        pygame.display.update()

def game_main():

    pygame.init()
    pygame.display.set_caption('Climate Puzzle')
    screen = pygame.display.set_mode((860, 690))
    fpsclock = pygame.time.Clock()
    program = ClimatePuzzle((10,8), 80, 5)

    while True:
        try:
            dt = fpsclock.tick()/1000

            screen.fill((0,0,0))
            program.draw(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                program.events(event)
            program.update(dt)
        except:
            continue

game_intro()


