import random, pygame, sys

def animate_ball():
    """We have to make the variables ball_speed_X and ball_speed_Y global variables so that,
    we can use it in any functions other than where it was declared and initialized"""
    global ball_speed_X, ball_speed_Y, score_time, player_score, opponent_score, score_time
    ball.x += ball_speed_X
    ball.y += ball_speed_Y

    if ball.top <= 0 or ball.bottom >= SCREEN_HEI:
        ball_speed_Y*= -1

    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= SCREEN_WID:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_X *= -1

def animate_player():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEI:
        player.bottom = SCREEN_HEI

def animate_opponent():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= SCREEN_HEI:
        opponent.bottom = SCREEN_HEI

def ball_restart():
    global ball_speed_X, ball_speed_Y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (400.5, 300 - 12.5)

    if current_time - score_time < 2100:
        ball_speed_X, ball_speed_Y = 0, 0
    else:
        ball_speed_Y = 7 * random.choice((1, -1))
        ball_speed_X = 7 * random.choice((1, -1))
        score_time = None


#General Setup
pygame.init()
clock=pygame.time.Clock()

#Main Window Setup
SCREEN_WID = 800
SCREEN_HEI = 600
screen = pygame.display.set_mode((SCREEN_WID, SCREEN_HEI))
pygame.display.set_caption("PONG")

#Game Rectangles
#To create a rectangle we need its x and y cooedinates followed by the width and height of the rectangle
#rectangle = pygame.Rect(Xcoordinate, Ycoordinate, Width, Height)
ball = pygame.Rect(SCREEN_WID/2 - 15,SCREEN_HEI/2 - 15, 20, 20)
player = pygame.Rect(SCREEN_WID - 20,SCREEN_HEI/2 - 70, 10, 140)
opponent = pygame.Rect(10, SCREEN_HEI/2 - 70, 10, 140)

#Colors
bg_color = pygame.Color("grey12")
light_grey = (200, 200, 200)

#Game Variables
ball_speed_X = 7 * random.choice((1, -1))
ball_speed_Y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

#Text Variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font('freesansbold.ttf', 24)

#Score Timer
score_time = None


while True:
    #Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed +=7
            if event.key == pygame.K_UP:
                player_speed -=7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -=7
            if event.key == pygame.K_UP:
                player_speed +=7


    #Animations
    animate_ball()  # Ball Collision detections
    animate_player() # Input based Paddle Control
    animate_opponent() # Automated paddle control


    #Visuals
    screen.fill(bg_color)

    #To draw the rectangle we need a surface to draw it on, followed by its color, followed by the rectangle's info
    #pygame.draw.rect(Display Surface, Color, Xcoordinate, Ycoordinate, Width, Height)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (SCREEN_WID/2,0), (SCREEN_WID/2,SCREEN_HEI))

    #Ball animation
    if score_time:
        ball_restart()

    #Game text
    player_text = game_font.render(f'{player_score}', False, light_grey)
    screen.blit(player_text, (415, SCREEN_HEI/2 - 24))
    
    opponent_text = game_font.render(f'{opponent_score}', False, light_grey)
    screen.blit(opponent_text, (375, SCREEN_HEI/2 - 24))


    #Updating the window
    pygame.display.flip()
    clock.tick(60)