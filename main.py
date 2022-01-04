import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chashi Besh")

BEGO_HIT = pygame.USEREVENT + 1
ORJO_HIT = pygame.USEREVENT + 2

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255,0,0)
GREEN = (10, 255, 120)
BLACK = (0, 0, 0)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Gun+Silencer.mp3'))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))
BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
BULLET_VEL = 7
VEL = 5
MAX_BULLETS = 3
FPS = 60


BEGO_IMAGE = pygame.image.load(os.path.join('Assets','bego.png'))
BEGO = pygame.transform.scale(BEGO_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
ORJO_IMAGE = pygame.image.load(os.path.join('Assets','orjo.png'))
ORJO = pygame.transform.scale(ORJO_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)
def handle_bullets(bego_bullets, orjo_bullets, bego, orjo):
    for bullet in bego_bullets:
        bullet.x+= BULLET_VEL
        if orjo.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ORJO_HIT))
            bego_bullets.remove(bullet)
        elif bullet.x > 900 : bego_bullets.remove(bullet)
    for bullet in orjo_bullets:
        bullet.x-= BULLET_VEL
        if bego.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BEGO_HIT))
            orjo_bullets.remove(bullet)
        elif bullet.x < 0: orjo_bullets.remove(bullet)        
        


def bego_handle_movement(key_pressed, bego):
    if key_pressed[pygame.K_w] and (bego.y - VEL > 0): #UP
        bego.y -= VEL
    if key_pressed[pygame.K_s] and (bego.y + VEL + SPACESHIP_WIDTH < 500): #DOWN
        bego.y += VEL
    if key_pressed[pygame.K_a] and (bego.x - VEL > 0): #LEFT
        bego.x -= VEL
    if key_pressed[pygame.K_d] and (bego.x - VEL + SPACESHIP_WIDTH + 5< BORDER.x): #RIGHT
        bego.x += VEL

def orjo_handle_movement(key_pressed, orjo):
    if key_pressed[pygame.K_UP] and (orjo.y - VEL > 0): #UP
        orjo.y -= VEL
    if key_pressed[pygame.K_DOWN] and (orjo.y + VEL + SPACESHIP_WIDTH < 500) : #DOWN
        orjo.y += VEL
    if key_pressed[pygame.K_LEFT] and (orjo.x - VEL > BORDER.x + BORDER.width): #LEFT
        orjo.x -= VEL
    if key_pressed[pygame.K_RIGHT] and (orjo.x + VEL + SPACESHIP_WIDTH + 7 < 910): #RIGHT
        orjo.x += VEL


def draw_window(orjo, bego, orjo_bullets, bego_bullets, orjo_health, bego_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    orjo_health_text = HEALTH_FONT.render("Health: " + str(orjo_health), 1, WHITE)
    bego_health_text = HEALTH_FONT.render("Health: " + str(bego_health), 1, WHITE)
    WIN.blit(orjo_health_text, ((WIDTH - orjo_health_text.get_width() - 10), 10))
    WIN.blit(bego_health_text, (10, 10))
    
    WIN.blit(BEGO,(bego.x, bego.y))
    WIN.blit(ORJO,(orjo.x, orjo.y))
    
    for bullet in orjo_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in bego_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def main() :
    orjo = pygame.Rect(800 - SPACESHIP_WIDTH, 250 - SPACESHIP_HEIGHT, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    bego = pygame.Rect(100, 250 - SPACESHIP_HEIGHT, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    orjo_health = 3
    bego_health = 3
    clock = pygame.time.Clock()
    orjo_bullets = []
    bego_bullets = []
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(bego_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(bego.x + bego.width,bego.y + bego.height//2 - 2, 8 , 4)
                    bego_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(orjo_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(orjo.x,orjo.y + orjo.height//2 - 2, 8, 4)
                    orjo_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == ORJO_HIT:
                orjo_health-=1
                BULLET_HIT_SOUND.play()
            if event.type == BEGO_HIT: 
                bego_health-=1
                BULLET_HIT_SOUND.play()
        winner_text = ""
        
        if orjo_health <= 0:
            winner_text = "Bego Wins!"
        if bego_health <= 0:
            winner_text = "Orjo Wins!"
        if winner_text != "" :
            draw_winner(winner_text)
            break
            
            
        key_pressed = pygame.key.get_pressed()
        bego_handle_movement(key_pressed, bego)
        orjo_handle_movement(key_pressed, orjo)
        handle_bullets(bego_bullets, orjo_bullets, bego, orjo)
        draw_window(orjo, bego, orjo_bullets, bego_bullets, orjo_health, bego_health)

    main()

if __name__ == "__main__":
    main()