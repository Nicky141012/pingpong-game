from pygame import *
import pygame
import random

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
        if self.reverse_controls:
            if keys[K_UP]:
                self.rect.y += self.speed
                if self.rect.y >= win_height - 145:
                    self.rect.y = win_height - 145
            if keys[K_DOWN]:
                self.rect.y -= self.speed
                if self.rect.y <= 0:
                    self.rect.y = 0
        else:
            if keys[K_UP]:
                self.rect.y -= self.speed
                if self.rect.y <= 0:
                    self.rect.y = 0
            if keys[K_DOWN]:
                self.rect.y += self.speed
                if self.rect.y >= win_height - 145:
                    self.rect.y = win_height - 145

    def update_rightplayer(self):
        keys = key.get_pressed()
        if self.reverse_controls:
            if keys[K_w]:
                self.rect.y += self.speed
                if self.rect.y >= win_height - 145:
                    self.rect.y = win_height - 145
            if keys[K_s]:
                self.rect.y -= self.speed
                if self.rect.y <= 0:
                    self.rect.y = 0
        else:
            if keys[K_w]:
                self.rect.y -= self.speed
                if self.rect.y <= 0:
                    self.rect.y = 0
            if keys[K_s]:
                self.rect.y += self.speed
                if self.rect.y >= win_height - 145:
                    self.rect.y = win_height - 145
window = display.set_mode((win_width, win_height))
display.set_caption("Ping Pong Game")
background = transform.scale(image.load(img_background), (win_width, win_height))

player_1 = Player("./assets/racket.png", 30, 200, 4, 50, 150)
player_2 = Player("./assets/racket.png", win_width - 80, 200, 4, 50, 150)
ball = GameSprite("./assets/tenis_ball.png", 200, 200, 4, 50, 50)

# Mystery Box properties
mystery_box_width, mystery_box_height = 50, 50
mystery_box_x = random.randint(100, win_width - 100)
mystery_box_y = random.randint(100, win_height - 200)
mystery_box_active = True
mystery_box_triggered = False
mystery_box_effect = None
effect_timer = 0
effect_duration = 5 * 60  # 5 seconds in frames
original_ball_speed_x = ball_speedx
original_ball_speed_y = ball_speedy

# Meme picture (replace with your image file path)
try:
    meme_image = pygame.image.load("./assets/meme.png")
    meme_image = transform.scale(meme_image, (300, 300))
except pygame.error:
    meme_image = None
    print("Meme image not found!")

# Mystery Box Image
try:
    mystery_box_image = pygame.image.load("./assets/mystery_box.png")
    mystery_box_image = transform.scale(mystery_box_image, (mystery_box_width, mystery_box_height))
except pygame.error:
    mystery_box_image = None
    print("Mystery box image not found!")

game = True
finish = False
clock = time.Clock()
FPS = 60

def draw_ui(x, y, score):
    my_font = font.Font(None, 36)
    text = my_font.render("Score:" + str(score), 1, (255, 255, 255))
    window.blit(text, (x, y))

player_1.reverse_controls = False
player_2.reverse_controls = False
reverse_timer_1 = 0
reverse_timer_2 = 0
player_1_speed_timer = 0
player_2_speed_timer = 0
ball_size_timer = 0
ball_original_size = 50
ball_new_size = 50

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background, (0, 0))
        player_1.update_rightplayer()
        player_2.update_leftplayer()

        draw_ui(0, 5, player_1.score)
        draw_ui(win_width - 100, 5, player_2.score)

        ball.rect.x += ball_speedx
        ball.rect.y += ball_speedy

        # Limit ball speed
        max_speed = 10  # Adjust as needed
        if abs(ball_speedx) > max_speed:
            ball_speedx = max_speed * (ball_speedx / abs(ball_speedx))
        if abs(ball_speedy) > max_speed:
            ball_speedy = max_speed * (ball_speedy / abs(ball_speedy))

        # Check for out of range and reset
        if ball.rect.x < -1000 or ball.rect.x > 3000:
            ball.rect.x = win_width // 2
            ball.rect.y = win_height // 2

        # Clamping ball position
        if ball.rect.x < 0:
            ball.rect.x = 0
            ball_speedx *= -1
        elif ball.rect.x > win_width - ball.rect.width:
            ball.rect.x = win_width - ball.rect.width
            ball_speedx *= -1

        # Corrected ball collision
        if ball.rect.y >= win_height - 50:
            ball.rect.y = win_height - 50
            ball_speedy *= -1
        elif ball.rect.y <= 0:
            ball.rect.y = 0
            ball_speedy *= -1

        # Racket bounce
        if sprite.collide_rect(ball, player_1) or sprite.collide_rect(ball, player_2):
            ball_speedx *= -1

        # Pass through score
        if ball.rect.x > player_2.rect.x + player_2.rect.width: # pass right player
            player_1.score += 1
            ball.rect.x = 200
            ball.rect.y = 200
            ball_speedx *= -1
            print("Player 1 score 1 point:", player_1.score)
        elif ball.rect.x < player_1.rect.x: # pass left player
            player_2.score += 1
            ball.rect.x = 200
            ball.rect.y = 200
            ball_speedx *= -1
            print("Player 2 score 1 point:", player_2.score)

        # Ball collision with mystery box (using ball center collision)
        ball_center = ball.rect.center
        mystery_box_rect = Rect(mystery_box_x, mystery_box_y, mystery_box_width, mystery_box_height)
        if mystery_box_active and mystery_box_rect.collidepoint(ball_center):
            mystery_box_active = False
            mystery_box_triggered = True
            mystery_box_effect = random.choice(["speed", "disappear", "meme", "reverse_controls_1", "reverse_controls_2", "speed_up_1","speed_up_2", "ball_size"])
            effect_timer = effect_duration
            original_ball_speed_x = ball_speedx
            original_ball_speed_y = ball_speedy

        # Apply mystery box effect
        if mystery_box_triggered and effect_timer > 0:
            if mystery_box_effect == "speed":
                ball_speedx *= 1.5
                ball_speedy *= 1.5
            elif mystery_box_effect == "disappear":
                player_1.rect.width = 0
                player_2.rect.width = 0
            elif mystery_box_effect == "reverse_controls_1":
                player_1.reverse_controls = True
                reverse_timer_1 = effect_timer
            elif mystery_box_effect == "reverse_controls_2":
                player_2.reverse_controls = True
                reverse_timer_2 = effect_timer
            elif mystery_box_effect == "speed_up_1":
                player_1.speed *= 2
                player_1_speed_timer = effect_timer
            elif mystery_box_effect == "speed_up_2":
                player_2.speed *= 2
                player_2_speed_timer = effect_timer
            elif mystery_box_effect == "ball_size":
                ball_new_size = 100
                ball_size_timer = effect_timer
                ball.image = transform.scale(image.load("./assets/tenis_ball.png"), (ball_new_size, ball_new_size))
                ball.rect = ball.image.get_rect(center=ball.rect.center)
            effect_timer -= 1
        elif mystery_box_triggered and effect_timer <= 0:
            if mystery_box_effect == "speed":
                ball_speedx = original_ball_speed_x
                ball_speedy = original_ball_speed_y
            elif mystery_box_effect == "disappear":
                player_1.rect.width = 50
                player_2.rect.width = 50
            elif mystery_box_effect == "reverse_controls_1":
                player_1.reverse_controls = False
            elif mystery_box_effect == "reverse_controls_2":
                player_2.reverse_controls = False
            elif mystery_box_effect == "speed_up_1":
                player_1.speed /= 2
            elif mystery_box_effect == "speed_up_2":
                player_2.speed /= 2
            elif mystery_box_effect == "ball_size":
                ball_new_size = 50
                ball.image = transform.scale(image.load("./assets/tenis_ball.png"), (ball_new_size, ball_new_size))
                ball.rect = ball.image.get_rect(center=ball.rect.center)
            mystery_box_triggered = False
            mystery_box_effect = None
            mystery_box_x = random.randint(100, win_width - 100)
            mystery_box_y = random.randint(100, win_height - 200)
            mystery_box_active = True

        # Draw Mystery box
        if mystery_box_active:
            if mystery_box_image:
                window.blit(mystery_box_image, (mystery_box_x, mystery_box_y))
            else:
                draw.rect(window, (255, 255, 0), (mystery_box_x, mystery_box_y, mystery_box_width, mystery_box_height))

        # Draw meme
        if mystery_box_triggered and mystery_box_effect == "meme" and meme_image:
            window.blit(meme_image, (win_width // 2 - 150, win_height // 2 - 150))

        ball.reset()
        player_1.reset()
        player_2.reset()
        display.update()
        clock.tick(FPS)