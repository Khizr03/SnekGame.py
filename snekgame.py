import pygame
import random
pygame.init()

#board dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20

#rgb colors
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)

#movement
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

class Snek:
    def __init__(self):
        self.body = [(5, 5),(4, 5),(3, 5)]#(head),(body),(tail)
        self.direction = right#starts in the right direction
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        newdir_x, newdir_y = self.direction
        new_head = ((head_x + newdir_x) % (SCREEN_WIDTH // CELL_SIZE),
                    (head_y + newdir_y) % (SCREEN_HEIGHT // CELL_SIZE))
        
        if new_head in self.body[1:]:
            return False
        
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

        return True
    
    def grow_snek(self):
        self.grow = True

    def change_direction(self, new_direction):
        if (new_direction[0] + self.direction[0] == 0) and (new_direction[1] + self.direction[1] == 0):
            return
        self.direction = new_direction

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(
                screen, green, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

class Apple:
    def __init__(self):
        self.position = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1),
                          random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1))

    def random_position(self):
        self.position = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1),
                          random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1))
    
    def draw_food(self, screen):
        radius = CELL_SIZE // 2
        pygame.draw.circle(
            screen, red, (self.position[0] * CELL_SIZE + radius, self.position[1] * CELL_SIZE + radius), radius)

class Game:
    def __init__(self,screen):
        self.screen = screen
        self.snek = Snek()
        self.apple = Apple()
        self.score = 0
        self.level = 1
        self.speed = 10
    
    def check_collision(self):

        if self.snek.body[0] == self.apple.position:
            self.snek.grow_snek()
            self.apple.random_position()
            self.score += 10 
            if self.score % 100 == 0:
                self.level_up()
        

    def level_up(self):
        self.level += 1
        self.speed += 2
    
    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_w:
                        self.snek.change_direction(up)

                    elif event.key == pygame.K_s:
                        self.snek.change_direction(down)

                    elif event.key == pygame.K_a:
                        self.snek.change_direction(left)

                    elif event.key == pygame.K_d:
                        self.snek.change_direction(right)
            
            if not self.snek.move():
                #game over
                running = False

            self.check_collision()
            self.screen.fill(black)
            #Draws the snek and the apples on the screen
            self.snek.draw(self.screen)
            self.apple.draw_food(self.screen)

            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {self.score}', True, white)
            level_text = font.render(f'Level: {self.level}', True, white)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(level_text, (10, 40))

            pygame.display.flip()
            clock.tick(self.speed)
            
if __name__ == "__main__":

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snek Game")

    game = Game(screen)
    game.run()



    pygame.quit()
