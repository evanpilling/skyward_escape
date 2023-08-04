import pygame
import random
import sys
import time

def draw(player, elasped_time, stars):
    # Set background
    WIN.blit(BG, (0, 0))

    # Elasped time on screen
    time_text = FONT.render(f"Time: {round(elasped_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # Draw playe to screen
    pygame.draw.rect(WIN, "grey", player)

    # Place star(s)
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    # Keep display updating at 60FPS
    pygame.display.update()

def main():
    #Player creation
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    # Time variables
    start_time = time.time()
    elasped_time = 0

    # Star variables
    star_add_increment = 2000
    star_count = 0
    star_width = 10
    star_height = 20
    star_velocity = 3
    stars = []

    # Miscellaneous initializations
    hit = False
    run = True

    while run:
        # Key pressed event initialization
        keys = pygame.key.get_pressed()

        # Time and star count variables
        star_count += clock.tick(60)
        elasped_time = time.time() - start_time

        # Star spawning
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - star_width)
                star = pygame.Rect(star_x, -star_height, star_width, star_height)
                stars.append(star)
            
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Player controls
        if keys[pygame.K_LEFT] and (player.x - PLAYER_VELOCITY) >= 0:
            player.x -= PLAYER_VELOCITY
        elif keys[pygame.K_RIGHT] and (player.x + PLAYER_VELOCITY + PLAYER_WIDTH) <= WIDTH:
            player.x += PLAYER_VELOCITY
        elif keys[pygame.K_ESCAPE]:
            run = False

        # Star spawning
        for star in stars[:]:
            star.y += star_velocity
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star_height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        # Collision events
        if hit:
            lost_text = FONT.render("FAILURE", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        # Draw player to screen
        draw(player, elasped_time, stars)

def main_menu():
    while True:
        # Screen variables
        WIN.blit(MMBG, (0, 0))
        outline_thickness = 5
        outline_color = 'white'
        main_menu_y = HEIGHT // 5
        main_menu_surface = MAIN_MENU_FONT.render('SKYWARD ESCAPE', True, 'white')

        # Mouse and button variables
        mx, my = pygame.mouse.get_pos()
        button_width, button_height = 500, 60
        button_x = WIDTH // 2 - button_width // 2
        button_1_y = HEIGHT // 2 - button_height - 20
        button_2_y = HEIGHT // 2 + button_height // 4 + 5

        # Button creation
        button_1 = pygame.Rect(button_x, button_1_y, button_width, button_height)
        button_2 = pygame.Rect(button_x, button_2_y, button_width, button_height)

        # Create text surfaces and use hover effect
        play_text_surface = FONT.render('PLAY', True, 'black' if button_1.collidepoint((mx, my)) else 'white')
        quit_text_surface = FONT.render('QUIT', True, 'black' if button_2.collidepoint((mx, my)) else 'white')

        # Button click events
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

        # Quit and key click events
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

        # Frame rate control (60FPS)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":

    # Screen variables
    WIDTH, HEIGHT = 1000, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Skyward Escape")
    MMBG = pygame.transform.scale(pygame.image.load("images/main_menu2.png"), (WIDTH, HEIGHT))
    BG = pygame.transform.scale(pygame.image.load("images/main_menu2.png"), (WIDTH, HEIGHT))

    # Player variables
    PLAYER_WIDTH = 40
    PLAYER_HEIGHT = 60
    PLAYER_VELOCITY = 5
    
    # Font variables
    pygame.font.init()
    FONT_PATH = "fonts/Orbitron/static/Orbitron-Black.ttf"
    FONT = pygame.font.Font(FONT_PATH, 30)
    MAIN_MENU_FONT = pygame.font.Font(FONT_PATH, 75)

    # Clock variables
    clock = pygame.time.Clock()
    keys = pygame.key.get_pressed()

    # Initialize the mixer module
    # pygame.mixer.init()
    # Load the music file
    # pygame.mixer.music.load('path/to/your/musicfile.mp3')
    # Play the music (loops forever)
    # pygame.mixer.music.play(-1)

    main_menu()