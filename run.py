import pygame
import random
import os
import math
import time
WIDTH = 1000
HEIGHT = 800
FPS = 30

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mr.Woof : the game")
clock = pygame.time.Clock()

#player variables

playerHEALTH = 5

playerMax = 1

p_INVIS = 0

p_rot = 0

#assets

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

#colors
colBlack = (0, 0, 0)
colWhite = (255, 255, 255)
colRed = (155, 0, 0)
colRedB = (255, 0, 0)
colGreen = (0, 155, 0)
colBlue = (0, 0, 155)
colBACK = (50, 127, 230)
colYellow = (255, 255, 0)


class Player(pygame.sprite.Sprite):
    global playerHEALTH
    global playerMax
    global p_INVIS
    global p_rot
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if playerHEALTH > 1:
            self.image = pygame.image.load(os.path.join(img_folder, "woof.png")).convert_alpha()
        else:
            self.image = pygame.image.load(os.path.join(img_folder, "oof.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2 , HEIGHT / 2)
        self.p_rot = 0
        self.shootDelay = 0
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -10
        if keystate[pygame.K_d]:
            self.speedx = 10
        self.rect.x += self.speedx
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.speedy = -10
        if keystate[pygame.K_s]:
            self.speedy = 10
        self.rect.y += self.speedy
        if keystate[pygame.K_LEFT]:
            self.p_rot += 0.05
        if keystate[pygame.K_RIGHT]:
            self.p_rot -= 0.05
        if keystate[pygame.K_SPACE] and self.shootDelay < 1:
            self.shootDelay = 5
            self.shoot()
        self.shootDelay -= 1
        if self.rect.y > HEIGHT:
            self.rect.y = -50
        if self.rect.y < -50:
            self.rect.y = HEIGHT
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.x < 0:
            self.rect.x = 0
        if playerHEALTH < 1.5:
            self.image = pygame.image.load(os.path.join(img_folder, "oof.png")).convert_alpha()
        if playerHEALTH > 1:
            self.image = pygame.image.load(os.path.join(img_folder, "woof.png")).convert_alpha()
        if p_INVIS > 0:
            self.image = pygame.image.load(os.path.join(img_folder, "p_INVIS.png")).convert_alpha()
        if math.floor(p_INVIS) % 2 == 0 and p_INVIS > 0:
            if playerHEALTH == 1:
                self.image = pygame.image.load(os.path.join(img_folder, "oof.png")).convert_alpha()
            if playerHEALTH == 0.5:
                self.image = pygame.image.load(os.path.join(img_folder, "oof.png")).convert_alpha()
            if playerHEALTH > 1:
                self.image = pygame.image.load(os.path.join(img_folder, "woof.png")).convert_alpha()
        self.aiming()
    def shoot(self):
        bullet = Bullet(self.rect.centerx + 55*math.sin(self.p_rot), self.rect.centery + 55*math.cos(self.p_rot), 21*math.cos(self.p_rot), 21*math.sin(self.p_rot))
        bullet.add(blocks)
        bullet.add(all_sprites)
    def aiming(self):
        aim = AimCursor(self.rect.centerx + 55*math.sin(self.p_rot), self.rect.centery + 55*math.cos(self.p_rot))
        
        aim.add(all_sprites)
        aim = AimCursor(self.rect.centerx + 45*math.sin(self.p_rot), self.rect.centery + 45*math.cos(self.p_rot))
        
        aim.add(all_sprites)
        

        

            
class Mob(pygame.sprite.Sprite):
    def __init__(self, type_):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        if type_ == 0:
            self.image.fill(colRed)
        elif type_ == 1:
            self.image.fill(colRedB)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = 50
        if type_ == 0:
            self.speedBASE = random.randint(5, 8)
        elif type_ == 1:
            self.speedBASE = random.randint(13, 16)
        self.speedBASE_h = random.randint(-1, 1)
        self.speedy = self.speedBASE
        self.speedx = self.speedBASE_h
        self.p_rot = 0
        self.type = type_
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.y > HEIGHT:
            self.rect.y = -50
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.speedy = self.speedBASE
        if self.rect.y < -50:
            self.rect.y = HEIGHT
            self.rect.x = random.randrange(WIDTH - self.rect.width)
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.x < 0:
            self.rect.x = 0
    def explode(self):
        for i in range(0,8):
            rot = random.randint(1,360)
            spark = Spark(self.rect.centerx, self.rect.centery, 3*math.cos(rot), 3*math.sin(rot))
            spark.add(all_sprites)
            spark.add(sparks)
        self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, XVEL, YVEL):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(colYellow)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.speedy = XVEL
        self.speedx = YVEL
        self.solidCount = 8000
    def update(self):
        if self.solidCount > 0:
            self.rect.y += self.speedy
            self.rect.x += self.speedx
        self.solidCount -= 1
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > HEIGHT:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > WIDTH:
            self.kill()
class Spark(pygame.sprite.Sprite):
    def __init__(self, x, y, XVEL, YVEL):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.speedy = YVEL
        self.speedx = XVEL
        
        self.life = 250
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.life < 1:
            self.kill()
        else:
            self.life -= 1
        self.image.fill((255-self.life/2, self.life, 0))
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > HEIGHT:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > WIDTH:
            self.kill()
class AimCursor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        if player.shootDelay > 1:
            self.image.fill(colRed)
        else:
            self.image.fill(colGreen)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.potato = 1
    def update(self):
        self.potato -= 1
        if self.potato == 0:
            self.kill()
        
        
        
all_sprites = pygame.sprite.Group()

mobs = pygame.sprite.Group()
player = Player()
blocks = pygame.sprite.Group()
sparks = pygame.sprite.Group()
all_sprites.add(player)
running = True

for i in range(8):
    m = Mob(0)
    all_sprites.add(m)
    mobs.add(m)

#loop

while running:
    clock.tick(FPS)
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update
    all_sprites.update()
    hits = pygame.sprite.groupcollide(mobs, blocks, False, False)
    for hit in hits:
        hit.explode()
        m = Mob(random.randint(0,1))
        all_sprites.add(m)
        mobs.add(m)
        
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits and p_INVIS < 1:
        playerHEALTH -= 1
        p_INVIS = 10
    if playerHEALTH < 0.5:
        running = False
    hits = pygame.sprite.spritecollide(player, sparks, False)
    if hits and p_INVIS < 1:
        playerHEALTH -= 0.5
        p_INVIS = 10
    if playerHEALTH < 0.5:
        running = False
    p_INVIS -= 0.1
    #render
    screen.fill(colBACK)
    all_sprites.draw(screen)
    
    pygame.display.flip()

pygame.quit()
