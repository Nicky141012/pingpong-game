from pygame import *
import pygame
pygame.init()
win_width = 700
win_height = 500
img_background = "./assets/background.jpg" 


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_leftplayer(self):
        keys = key.get_pressed()
        if keys[K_UP] :
            if self.rect.y <= 0:
                self.rect.y == 0
            else:
                self.rect.y -= self.speed
        if keys[K_DOWN]:
            if self.rect.y >= win_height -145:
                self.rect.y == 0
            else:
                self.rect.y += self.speed

    def update_rightplayer(self):
        keys = key.get_pressed()
        if keys[K_w]:
            if self.rect.y <= 0:
                self.rect.y == 0
            else:
                self.rect.y -= self.speed
        if keys[K_s]:
            if self.rect.y >= win_height -145:
                self.rect.y == 0
            else:
                self.rect.y += self.speed

        
window = display.set_mode((win_width, win_height))
display.set_caption("Ping Pong Game")
background = transform.scale(image.load(img_background), (win_width, win_height))


player_1 = Player("./assets/racket.png",  30, 200, 4, 50, 150)
player_2 = Player("./assets/racket.png",  win_width -80, 200, 4, 50, 150)
ball = GameSprite("./assets/tenis_ball.png", 200, 200, 4, 50, 50)

game = True
finish =  False
clock = time.Clock()
FPS = 60

while game:
        for e in event.get():
            if e.type == QUIT:
                game = False
        if finish != True:
            window.blit(background,(0,0))
            player_1.update_rightplayer()
            player_2.update_leftplayer()
            ball.update()
            
            ball.reset()
            player_1.reset()
            player_2.reset()
        display.update()
        clock.tick(FPS)

