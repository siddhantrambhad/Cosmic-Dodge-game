import pygame
import random
pygame.init()
WIDTH, HEIGHT = 800, 600
UFO_SPEED = 5
COMET_SPEED = 3
SPAWN_INTERVAL = 1000  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UFO Dodge")
clock = pygame.time.Clock()


background_img = pygame.image.load("background.jpg") 
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
ufo_img = pygame.image.load("ufo2.jpg")  
ufo_img = pygame.transform.scale(ufo_img, (60, 60))
comet_img = pygame.image.load("comet2.jpg")  
comet_img = pygame.transform.scale(comet_img, (50, 50))


class UFO:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 80
        self.width = 60
        self.height = 60
        self.speed = UFO_SPEED
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.height:
            self.y += self.speed
    
    def draw(self):
        screen.blit(ufo_img, (self.x, self.y))


class Comet:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 50)
        self.y = -50
        self.speed = COMET_SPEED
    
    def move(self):
        self.y += self.speed
    
    def draw(self):
        screen.blit(comet_img, (self.x, self.y))
    
    def off_screen(self):
        return self.y > HEIGHT
    
    def collides_with(self, ufo):
        return pygame.Rect(self.x, self.y, 50, 50).colliderect(pygame.Rect(ufo.x, ufo.y, ufo.width, ufo.height))


def show_menu():
    menu_font = pygame.font.Font(None, 50)
    title = menu_font.render("UFO Dodge", True, WHITE)
    start_button = menu_font.render("Press ENTER to Start", True, WHITE)
    quit_button = menu_font.render("Press ESC to Quit", True, WHITE)
    
    while True:
        screen.fill(BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        screen.blit(start_button, (WIDTH//2 - start_button.get_width()//2, 250))
        screen.blit(quit_button, (WIDTH//2 - quit_button.get_width()//2, 300))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False


def show_game_over(score):
    game_over_font = pygame.font.Font(None, 60)
    text = game_over_font.render(f"Game Over! Score: {score}", True, RED)
    restart_text = game_over_font.render("Press ENTER to Restart", True, WHITE)
    screen.fill(BLACK)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 200))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 300))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False


def game_loop():
    ufo = UFO()
    comets = []
    running = True
    score = 0
    last_spawn_time = pygame.time.get_ticks()
    font = pygame.font.Font(None, 40)
    
    while running:
        screen.blit(background_img, (0, 0))
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
        
        
        if pygame.time.get_ticks() - last_spawn_time > SPAWN_INTERVAL:
            comets.append(Comet())
            last_spawn_time = pygame.time.get_ticks()
        
       
        ufo.move(keys)
        ufo.draw()
        
        
        for comet in comets[:]:
            comet.move()
            comet.draw()
            if comet.collides_with(ufo):
                show_game_over(score)
                return
            if comet.off_screen():
                comets.remove(comet)
        
        
        score = pygame.time.get_ticks() // 1000
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)


if show_menu():
    while True:
        game_loop()
