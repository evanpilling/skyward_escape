import pygame
import sys
import time
import random

# set up some variables
screen_width, screen_height = 800, 600
play_button_width, play_button_height = 100, 50
white = (255, 255, 255)
green = (0, 255, 0)
bright_green = (0, 255, 0)
red = (255, 0, 0)
bright_red = (255, 0, 0)

# Initialize the mixer module
# pygame.mixer.init()
# Load the music file
# pygame.mixer.music.load('path/to/your/musicfile.mp3')
# Play the music (loops forever)
# pygame.mixer.music.play(-1)

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(WIN, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(WIN, ic, (x, y, w, h))

    smallText = pygame.font.Font(None ,20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x + (w / 2)), (y + (h / 2)) )
    WIN.blit(textSurf, textRect)
    
def text_objects(text, font):
    textSurface = font.render(text, True, "white")
    return textSurface, textSurface.get_rect()

def draw(player, elasped_time, stars):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elasped_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    pygame.draw.rect(WIN, "grey", player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    start_time = time.time()
    elasped_time = 0

    star_add_increment = 2000
    star_count = 0
    STAR_WIDTH = 10
    STAR_HEIGHT = 20
    STAR_VELOCITY = 3

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elasped_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and (player.x - PLAYER_VELOCITY) >= 0:
            player.x -= PLAYER_VELOCITY
        elif keys[pygame.K_RIGHT] and (player.x + PLAYER_VELOCITY + PLAYER_WIDTH) <= WIDTH:
            player.x += PLAYER_VELOCITY
        elif keys[pygame.K_ESCAPE]:
            run = False

        for star in stars[:]:
            star.y += STAR_VELOCITY
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + STAR_HEIGHT >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("FAILURE", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break
        elif elasped_time == 10:
            win_text = FONT.render("YOU WIN!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elasped_time, stars)

    # pygame.quit()

def main_menu():
    while True:
        # Position of the main menu title
        main_menu_y = HEIGHT // 5
        button_width, button_height = 500, 60
        button_x = WIDTH // 2 - button_width // 2
        button_1_y = HEIGHT // 2 - button_height - 20
        button_2_y = HEIGHT // 2 + button_height // 4 + 5
        outline_thickness = 5
        outline_color = 'white'
        mx, my = pygame.mouse.get_pos()
        WIN.blit(MMBG, (0, 0))

        button_1 = pygame.Rect(button_x, button_1_y, button_width, button_height)
        button_2 = pygame.Rect(button_x, button_2_y, button_width, button_height)

        # Create text surfaces and use hover effect
        main_menu_surface = MAIN_MENU_FONT.render('SKYWARD ESCAPE', True, 'white')
        play_text_surface = FONT.render('PLAY', True, 'black' if button_1.collidepoint((mx, my)) else 'white')
        quit_text_surface = FONT.render('QUIT', True, 'black' if button_2.collidepoint((mx, my)) else 'white')

        if button_1.collidepoint((mx, my)):
            if click:
                main()
        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        # Draw the outlines for the buttons
        pygame.draw.rect(WIN, outline_color, (button_1.x - outline_thickness, button_1.y - outline_thickness,
                                      button_1.width + 2 * outline_thickness, button_1.height + 2 * outline_thickness))
        pygame.draw.rect(WIN, outline_color, (button_2.x - outline_thickness, button_2.y - outline_thickness,
                                      button_2.width + 2 * outline_thickness, button_2.height + 2 * outline_thickness))
         
        # Draw buttons
        pygame.draw.rect(WIN, outline_color if button_1.collidepoint((mx, my)) else 'black', button_1)
        pygame.draw.rect(WIN, outline_color if button_2.collidepoint((mx, my)) else 'black', button_2)

        # Place buttons onto screen
        WIN.blit(main_menu_surface, (WIDTH//2 - main_menu_surface.get_width()//2, main_menu_y))

        WIN.blit(play_text_surface, (button_1.x + button_1.width//2 - play_text_surface.get_width()//2,
                               button_1.y + button_1.height//2 - play_text_surface.get_height()//2))
        
        WIN.blit(quit_text_surface, (button_2.x + button_2.width//2 - quit_text_surface.get_width()//2,
                               button_2.y + button_2.height//2 - quit_text_surface.get_height()//2))

        # Event loop
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    pygame.font.init()

    title_screen = True
    WIDTH, HEIGHT = 1000, 800

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Skyward Escape")

    MMBG = pygame.transform.scale(pygame.image.load("images/main_menu2.png"), (WIDTH, HEIGHT))
    BG = pygame.transform.scale(pygame.image.load("images/main_menu2.png"), (WIDTH, HEIGHT))

    PLAYER_WIDTH = 40
    PLAYER_HEIGHT = 60
    PLAYER_VELOCITY = 5

    FONT_PATH = "fonts/Orbitron/static/Orbitron-Black.ttf"
    FONT = pygame.font.Font(FONT_PATH, 30)
    MAIN_MENU_FONT = pygame.font.Font(FONT_PATH, 75)

    clock = pygame.time.Clock()
    keys = pygame.key.get_pressed()
    main_menu()