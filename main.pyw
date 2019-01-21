import pygame, math, random, os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)

pygame.init()

balltexture = pygame.image.load('textures/Ball.png')
rocktexture = pygame.image.load('textures/rock.png')

screensize = pygame.display.Info()
win = pygame.display.set_mode( (screensize.current_w, screensize.current_h-30))
clock = pygame.time.Clock()
pygame.display.set_caption('Bouncy Ball')

def redrawGameWindow():
    win.fill((240,240,240))

    Player.draw()

    for i in rocks:
        i.draw(win)
    
    pygame.display.update()
    

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = balltexture.get_rect()
        self.rect.x=225
        self.rect.y=400
        self.radius = 100
        self.velx=0
        self.vely=0
        self.action=False
        self.switchx=0
        self.switchy=0
        
        self.mask = pygame.mask.from_surface(balltexture)
    def draw(self):
        win.blit(balltexture, self.rect)
    

class rock(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rocktexture.get_rect()
        self.rect.x = screensize.current_w
        self.rect.y = y
        self.width = 120
        self.mask = pygame.mask.from_surface(rocktexture)

        
    def draw(self, win):
        win.blit(rocktexture, self.rect)
        
def vsub(x,y):
    return [x[0]-y[0],x[1]-y[1]]

Player = Ball()
score = 0
run = True
switchcooldown = 0

global rocks

deltay = random.randrange(100)+320
y = random.randrange(screensize.current_h-30-deltay)
rocks = [rock(y-862), rock(y+deltay)]


while run:
    clock.tick(144)
    deltay = 0
    for i in rocks:
        i.rect.x -= 1
        if i.rect.x == -i.width:
            rocks.pop(0)
            rocks.pop(0)
            break
        if screensize.current_w-i.rect.x==1000 and len(rocks)<4:
            deltay = random.randrange(100)+320
            y = random.randrange(screensize.current_h-30-deltay)
            rocks.append(rock(y-862))            
            rocks.append(rock(y+deltay))
            break
        

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            deltax = (mouse[0] - Player.rect.x-Player.radius)
            deltay = (mouse[1] - Player.rect.y-Player.radius)
            if math.sqrt(deltax **2 + deltay**2) < Player.radius:
                Player.vely = int((deltay+Player.vely/10)/5)
                Player.action = True
                Player.velx = int((deltax+Player.velx/10)/5)
                score += 1
                Player.switchx = 0
                Player.switchy = 0
    try:
        Player.vely -= 0.05
    except:
        pass

    
    if switchcooldown == 0:
        Player.switchx,Player.switchy = 0,0
    else:
        switchcooldown -= 1




    if Player.rect.x<0 and Player.switchx != -1:
        if Player.velx*2/3 > 1:
            Player.velx = -Player.velx*2/3
        else:
            Player.velx = - Player.velx
        Player.witchx = -1
        switchcooldown = 20
        
    elif Player.rect.x>screensize.current_w-Player.radius*2 and Player.switchx != 1:
        if Player.velx*2/3 < 1:
            Player.velx = -Player.velx*2/3
        else:
            Player.velx = - Player.velx
        Player.switchx = 1
        switchcooldown = 20
    if Player.rect.y>screensize.current_h-30-Player.radius*2 and Player.switchy != -1:
        Player.switchy  = -1
        Player.vely = - Player.vely*2/3
        switchcooldown = 20
    elif Player.rect.y<0 and Player.switchy != 1:
        Player.switchy  = 1
        Player.vely = - Player.vely*2/3
        switchcooldown = 20
    if Player.rect.x >screensize.current_w-Player.radius*2 and Player.switchx != 1:
        if Player.velx*2/3 < 1:
            Player.velx = -Player.velx*2/3
        else:
            Player.velx = - Player.velx
        Player.switchx = 1
        switchcooldown = 20        
    if Player.rect.y>screensize.current_h-30-Player.radius*2 and Player.switchy != -1:
        Player.switchy  = -1
        Player.vely = - Player.vely*2/3
        switchcooldown = 20
    elif Player.rect.y<0 and Player.switchy != 1:
        Player.switchy  = 1
        Player.vely = - Player.vely*2/3
        switchcooldown = 20


    for i in rocks:
##        if pygame.sprite.collide_mask(i, Player) is not None:
##            print(2)
##        offset = (Player.rect.x-i.rect.x, Player.rect.y-i.rect.y)
##        offset = list(map(int,vsub(Player.rect,i.rect)))
##        overlap = Player.mask.overlap_area(i.mask,offset)
##        if overlap != 0:
##            print(3218304231802374658923406)
##        if Player.mask.overlap_area(i.mask, offset):
##            print(1)
##        if pygame.sprite.collide_mask(i, Player):
##            print(2)
        if pygame.sprite.collide_rect(i, Player):
            if i.rect.y<0:
                if Player.rect.y+Player.radius<i.rect.y+862:
                    if Player.rect.x<i.rect.x:
                        if Player.velx > 0:
                            Player.velx = -Player.velx
                        else:
                            Player.velx -= 1
                    else:
                        if Player.velx < 0:
                            Player.velx = -Player.velx
                        else:
                            Player.velx += 1
            else:
                if Player.rect.y+Player.radius>i.rect.y:
                    Player.velx = -Player.velx
        
    Player.rect.x = int(Player.rect.x-Player.velx)
    Player.rect.y = int(Player.rect.y-Player.vely)

                    
    redrawGameWindow()
    
pygame.quit()
quit()
