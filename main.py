from pygame import *
import pygame
pygame.init()
win_width = 700
win_height = 500
img_background = "./assets/background.jpg" 
ball_speedx = -3
ball_speedy = -3

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
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__(player_image, player_x, player_y, player_speed, size_x, size_y)
        self.score = 0



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

def draw_ui(x, y, score):
    my_font = font.Font(None, 36)
    text = my_font.render("Score:" + str(score) , 1 ,(255, 255, 255))
    window.blit(text, (x, y))

while game:
        for e in event.get():
            if e.type == QUIT:
                game = False
        if finish != True:
            window.blit(background,(0,0))
            player_1.update_rightplayer()
            player_2.update_leftplayer()

            draw_ui(0,5,player_1.score)
            draw_ui(win_width - 100, 5, player_2.score)

            ball.rect.x += ball_speedx
            ball.rect.y += ball_speedy

            if (ball.rect.y >= win_height - 50):
                ball_speedy *= -1
            
            if (ball.rect.y <= 0 ):
                ball_speedy *= -1
            
            if(sprite.collide_rect(ball, player_1) or sprite.collide_rect(ball, player_2)):
                ball_speedx *= -1
            
            if ball.rect.x > win_width:
                player_1.score += 1
                ball.rect.x = 200
                ball.rect.y = 200
                ball_speedx *= -1
                print("Player 1 score 1 point:", player_1.score)
            if ball.rect.x < 0:
                player_2.score += 1
                ball.rect.x = 200
                ball.rect.y = 200
                ball_speedx *= -1
                print("Player 2 score 1 point:", player_2.score)

            ball.update()
            
            ball.reset()
            player_1.reset()
            player_2.reset()
        display.update()
        clock.tick(FPS)

