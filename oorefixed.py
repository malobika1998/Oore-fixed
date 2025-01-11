import pygame, os

# Initialize pygame
pygame.init()

# Pygame setup (screen)
display_surface = pygame.display.set_mode((900, 500))
pygame.display.set_caption('Space Fight')

# Loading and setting the image sizes and rotations
bckgrnd_img = pygame.image.load("images/space.png")
bckgrnd = pygame.transform.scale(bckgrnd_img, (900, 500))

y_spcshp_img = pygame.image.load("images/spaceship_yellow.png")
y_spcshp = pygame.transform.rotate(pygame.transform.scale(y_spcshp_img, (50, 50)), 90)

r_spcshp_img = pygame.image.load("images/spaceship_red.png")
r_spcshp = pygame.transform.rotate(pygame.transform.scale(r_spcshp_img, (50, 50)), 270)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 60)

# Setting up the image classes
class Spaceship:
    def __init__(self, loc_x, loc_y, clr, keys):
        self.rect = pygame.Rect(loc_x, loc_y, 50, 50)
        self.hp = 10
        self.clr = clr
        self.keys = keys
        self.bullets = []
        
    def draw(self):
        if self.clr == 'yellow':
            display_surface.blit(y_spcshp, (self.rect.x, self.rect.y))
        else:
            display_surface.blit(r_spcshp, (self.rect.x, self.rect.y))

    def move(self):
        key_pressed = pygame.key.get_pressed()
        if self.clr == 'yellow':
            if key_pressed[self.keys['left']] and self.rect.x > 0:
                self.rect.x -= 5
            if key_pressed[self.keys['right']] and self.rect.x < (900 // 2) - 60:
                self.rect.x += 5
            if key_pressed[self.keys['up']] and self.rect.y > 0:
                self.rect.y -= 5
            if key_pressed[self.keys['down']] and self.rect.y < 450:
                self.rect.y += 5
        else:
            if key_pressed[self.keys['left']] and self.rect.x > (900 // 2) + 10:
                self.rect.x -= 5
            if key_pressed[self.keys['right']] and self.rect.x < 900:
                self.rect.x += 5
            if key_pressed[self.keys['up']] and self.rect.y > 0:
                self.rect.y -= 5
            if key_pressed[self.keys['down']] and self.rect.y < 500:
                self.rect.y += 5

    def shoot(self):
        if self.clr == 'yellow':
            bullet = Bullet(self.rect.x + 50, self.rect.y + 20, 'right')  # Shoot right
        else:
            bullet = Bullet(self.rect.x - 20, self.rect.y + 20, 'left')  # Shoot left
        self.bullets.append(bullet)


class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 20, 10)
        self.direction = direction

    def bullet_move(self):
        if self.direction == 'left':
            self.rect.x -= 10
        elif self.direction == 'right':
            self.rect.x += 10

    def bullet_draw(self):
        pygame.draw.rect(display_surface, (255, 255, 0), self.rect)

        if self.direction == 'right':
            semi_circle_rect = pygame.Rect(self.rect.x + 15, self.rect.y, 10, 10)
            pygame.draw.arc(display_surface, (128, 128, 128), semi_circle_rect, 1.57, 4.71, 5)
        elif self.direction == 'left':
            semi_circle_rect = pygame.Rect(self.rect.x - 5, self.rect.y, 10, 10)
            pygame.draw.arc(display_surface, (128, 128, 128), semi_circle_rect, -1.57, 1.57, 5)


class Game:
    def __init__(self):
        self.y_spcshp = Spaceship(200, 250, 'yellow', {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s})
        self.r_spcshp = Spaceship(700, 250, 'red', {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN})
        
    def draw_window(self):
        display_surface.blit(bckgrnd, (0, 0))
        y_hptxt = HEALTH_FONT.render(f'Health:{self.y_spcshp.hp}', 1, 'White')
        r_hptxt = HEALTH_FONT.render(f'Health:{self.r_spcshp.hp}', 1, 'White')
        display_surface.blit(y_hptxt, (10, 10))
        display_surface.blit(r_hptxt, (700, 10))

        self.y_spcshp.draw()
        self.r_spcshp.draw()
        rect_width = 15
        rect_height = 500
        rect_x = (900 - rect_width) // 2
        rect_y = (500 - rect_height) // 2
        pygame.draw.rect(display_surface, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height))
        
        for bullet in self.y_spcshp.bullets:
            bullet.bullet_move()
            bullet.bullet_draw()
        for bullet in self.r_spcshp.bullets:
            bullet.bullet_move()
            bullet.bullet_draw()
        
        pygame.display.update()

    def handle_bullets(self):
        # Handle yellow spaceship's bullets
        for bullet in self.y_spcshp.bullets:
            bullet.bullet_move()
            if self.r_spcshp.rect.colliderect(bullet.rect):  # Collision detection for red spaceship
                self.r_spcshp.hp -= 1  # Decrease red spaceship's health
                self.y_spcshp.bullets.remove(bullet)  # Remove the bullet

        # Handle red spaceship's bullets
        for bullet in self.r_spcshp.bullets:
            bullet.bullet_move()
            if self.y_spcshp.rect.colliderect(bullet.rect):  # Collision detection for yellow spaceship
                self.y_spcshp.hp -= 1  # Decrease yellow spaceship's health
                self.r_spcshp.bullets.remove(bullet)  # Remove the bullet

    def main(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Yellow spaceship shoots
                        self.y_spcshp.shoot()
                    if event.key == pygame.K_RETURN:  # Red spaceship shoots
                        self.r_spcshp.shoot()

            self.y_spcshp.move()
            self.r_spcshp.move()
            self.draw_window()
            self.handle_bullets()

            # Check for game over condition
            if self.y_spcshp.hp <= 0:
                winner_text = WINNER_FONT.render('Red Wins!', 1, (255, 0, 0))
                display_surface.blit(winner_text, (350, 200))
                pygame.display.update()
                pygame.time.wait(2000)
                running = False
            elif self.r_spcshp.hp <= 0:
                winner_text = WINNER_FONT.render('Yellow Wins!', 1, (255, 255, 0))
                display_surface.blit(winner_text, (300, 200))
                pygame.display.update()
                pygame.time.wait(2000)
                running = False

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.main()
