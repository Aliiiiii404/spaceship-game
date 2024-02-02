import pygame
import os
pygame.font.init()
pygame.mixer.init()

# the main window
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE WAR")

# the border and the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

#the games sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(
    'assets', 'get-hit.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(
    'assets', 'hit.ogg'))
GAME_OVER = pygame.mixer.Sound(os.path.join(
    'assets', 'game_over.ogg'))

# the text font
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 144
VEL = 5
BULLETS_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIGHT, SPACESHIP_HEIGHT = 55, 40
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
#the keybinds on the screen
# the font
KEYBINDS_FONT = pygame.font.SysFont('sans', 20)
# red
UP_RED = "z"
DOWN_RED = "s"
LEFT_RED = "q"
RIGHT_RED = "d"
HIT_RED = "e"
# blue
UP_BLUE = "↑"
DOWN_BLUE = "↓"
LEFT_BLUE = "←"
RIGHT_BLUE = "→"
HIT_BLUE ="m"

# the first player
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'rocket.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIGHT, SPACESHIP_HEIGHT)), 270)

# the seceond player
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'spaceship.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIGHT, SPACESHIP_HEIGHT)), 90)

# the background
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'space.jpg')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, WIDTH, HEIGHT):
    # draw the window
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    # to show the health of the players
    red_health_text = HEALTH_FONT.render(
        "Blue's health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Red's health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
   
    # to show the keybinds on the screen : RED
    red_keybinds_movment = KEYBINDS_FONT.render(
        "movment : " + str(UP_RED) + "-" + str(DOWN_RED) +  "-" + str(RIGHT_RED) + "-" + str(LEFT_RED), 1, WHITE)
    red_keybinds_shooting = KEYBINDS_FONT.render(
        "shooting : " + str(HIT_RED), 1, WHITE)
    WIN.blit(red_keybinds_movment, (10, 35))
    WIN.blit(red_keybinds_shooting, (10, 55))

   # to show the keybinds on the screen : BLUE
    blue_keybinds_movment = KEYBINDS_FONT.render(
        "movment : " + str(UP_BLUE) + "-" + str(DOWN_BLUE) +  "-" + str(RIGHT_BLUE) + "-" + str(LEFT_BLUE), 1, WHITE)
    blue_keybinds_shooting = KEYBINDS_FONT.render(
        "shooting : " + str(HIT_BLUE), 1, WHITE)
    WIN.blit(blue_keybinds_movment, (WIDTH - blue_keybinds_movment.get_width() - 10, 35))
    WIN.blit(blue_keybinds_shooting, (WIDTH - blue_keybinds_shooting.get_width() - 10, 55))
    
    #show the players on the screen
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movment(keys_pressed, yellow):
    if keys_pressed[pygame.K_q] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pygame.K_z] and yellow.y -VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 10:
        yellow.y += VEL

def red_handle_movment(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 10:
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2
                         , HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIGHT, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIGHT, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_m and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Winner : RED!!"
            GAME_OVER.play()

        if yellow_health <= 0:
            winner_text = "Winner : BLUE!!"
            GAME_OVER.play()

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movment(keys_pressed, yellow)
        red_handle_movment(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,red_health, yellow_health, WIDTH, HEIGHT)

    main()

if __name__ == "__main__":
    main()
