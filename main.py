from pygame import *
import pygame
import random
import time as timeModule

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
        self.visible = True  # Add visibility attribute

    def reset(self):
        if self.visible:  # Only draw if visible
            window.blit(self.image, (self.rect.x, self.rect.y))

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

class Area():
    '''
    Making a rect area in the screen with some functionality
    1. Function.color: => change the self.fill_color of the class
    2. Function.fill: => do fill the area with the color property
    3. Function.outline: => Creat the border for the area
    4. Function.collidepoint => Check the position is inside the area yes or no
    '''
    
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color # changing the color

    def fill(self):
        pygame.draw.rect(window, self.fill_color, self.rect)

    def outline(self, frame_color, thickness):
        pygame.draw.rect(window, frame_color, self.rect, thickness)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

class Label(Area): # Lable class is inherited the Area class.
    '''
    1. Function set_text: => Set the text inside the area wich percific position
    2. Function draw: => Make it appear in the screen on percific position

    '''
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('Verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

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
effect_run_one = False

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

def show__waiting_screen():
    window.blit(background, (0,0))
    title_font = pygame.font.Font(None, 72)
    text_font = pygame.font.Font(None, 36)
    title_text = title_font.render("Ping Pong Game", True, (0,0,0))

    promt_text = text_font.render("Press space start to play the game now!", True, (0,0,0))
    window.blit(title_text, (150,200))
    window.blit(promt_text, (130, 300))

    while True:
        for e in event.get():
            if e.type == QUIT:
                global game
                game = False
                break
        keys =key.get_pressed()
        if keys[K_SPACE]:
            break
        display.update()
def show_winner(player):
        window.blit(background, (0,0))
        title_font = pygame.font.Font(None, 72)
        text_font = pygame.font.Font(None, 36)
        title_text = title_font.render(player + ' is the winer!!!!!' , True, (0,0,0))

        promt_text = text_font.render("Press space to restart a game!", True, (0,0,0))
        window.blit(title_text, (100,200))
        window.blit(promt_text, (170, 300))

        while True:
            for e in event.get():
                if e.type == QUIT:
                    global game
                    game = False
                    break
            keys =key.get_pressed()
            if keys[K_SPACE]:
                global player_1
                global player_2
                global fresh_start
                fresh_start = True
                player_1.score = 0
                player_2.score = 0
                break 
            display.update()

def draw_round(round):
        round_text = Label(0,0,700,500,(0,0,0))
        round_text.set_text("Round"  + str(round) , 20, (255,255,255))
        round_text.draw(10,10)
        round_text.fill()



       
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
fresh_start = True
pause_time = 3
round = 1


show__waiting_screen()
start_time = timeModule.time()
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
        if timeModule.time() - start_time > 3:
            fresh_start = False
        
        if not  fresh_start:
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
        if ball.rect.x >= win_width - ball.rect.width: # pass right player
            player_1.score += 1
            ball.rect.x = 200
            ball.rect.y = 200
            ball_speedx *= -1
            fresh_start =True
            pause_time = 2
            start_time = timeModule.time()
            print("Player 1 score 1 point:", player_1.score)
            round += 1
        elif ball.rect.x < player_1.rect.x: # pass left player
            player_2.score += 1
            ball.rect.x = 200
            ball.rect.y = 200
            ball_speedx *= -1
            fresh_start =True
            pause_time = 2
            start_time = timeModule.time()
            print("Player 2 score 1 point:", player_2.score)
            round += 1            
        if player_1.score >= 5:
            show_winner("Player 1")
        elif player_2.score >= 5:
            show_winner("Player 2")

        # Ball collision with mystery box (using ball center collision)
        ball_center = ball.rect.center
        mystery_box_rect = Rect(mystery_box_x, mystery_box_y, mystery_box_width, mystery_box_height)
        if mystery_box_active and mystery_box_rect.collidepoint(ball_center):
            mystery_box_active = False
            mystery_box_triggered = True
            mystery_box_effect = random.choice(["speed", "disappear", "meme", "reverse_controls_1", "reverse_controls_2", "speed_up_1","speed_up_2", "ball_size"])
            print(mystery_box_effect)
            effect_timer = effect_duration
            original_ball_speed_x = ball_speedx
            original_ball_speed_y = ball_speedy
            effect_run_one = True

        # Apply mystery box effect
        if mystery_box_triggered and effect_timer > 0:
            if mystery_box_effect == "speed":
                if effect_run_one:
                    ball_speedx *= 2
                    ball_speedy *= 2
                    effect_run_one = False
            elif mystery_box_effect == "disappear":
                player_1.visible = False
                player_2.visible = False
            elif mystery_box_effect == "reverse_controls_1":
                player_1.reverse_controls = True
                reverse_timer_1 = effect_timer
            elif mystery_box_effect == "reverse_controls_2":
                player_2.reverse_controls = True
                reverse_timer_2 = effect_timer
            elif mystery_box_effect == "speed_up_1":
                if effect_run_one:
                    player_1.speed *= 3
                    player_1_speed_timer = effect_timer
                    effect_run_one = False
            elif mystery_box_effect == "speed_up_2":
                if effect_run_one:
                    player_2.speed *= 3
                    player_2_speed_timer = effect_timer
                    effect_run_one = False
            elif mystery_box_effect == "ball_size":
                ball_new_size = 100
                ball_size_timer = effect_timer
                ball.image = transform.scale(image.load("./assets/tenis_ball.png"), (ball_new_size, ball_new_size))
                ball.rect = ball.image.get_rect(center=ball.rect.center)
            elif mystery_box_effect == "meme" and meme_image:
                meme_scaled = transform.scale(meme_image, (win_width, win_height))
                window.blit(meme_scaled, (0, 0))
            effect_timer -= 1
        elif mystery_box_triggered and effect_timer <= 0:
            if mystery_box_effect == "speed":
                ball_speedx = original_ball_speed_x
                ball_speedy = original_ball_speed_y
            elif mystery_box_effect == "disappear":
                player_1.visible = True
                player_2.visible = True
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
            effect_run_one = False

        # Draw Mystery box
        if mystery_box_active:
            if mystery_box_image:
                window.blit(mystery_box_image, (mystery_box_x, mystery_box_y))
            else:
                draw.rect(window, (255, 255, 0), (mystery_box_x, mystery_box_y, mystery_box_width, mystery_box_height))

        # Don't draw normal game elements if meme is active
        if not (mystery_box_triggered and mystery_box_effect == "meme"):
            ball.reset()
            player_1.reset()
            player_2.reset()
        if  fresh_start:
            draw_round(round)




        display.update()
        clock.tick(FPS)