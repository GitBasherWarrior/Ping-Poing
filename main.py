import pygame
import pygame.locals
import random

class Game(object):
    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption("Ping Poing")
        self.rect = self.surface.get_rect()
    
    def draw(self, *args):
        bg = (255,255,255)
        self.surface.fill(bg)
        for arg in args:
            arg.draw_on(self.surface)
        pygame.display.update()

class Drawble(object):
    def __init__(self, x, y, width, height, color=(0,255,75)):
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.Surface([width, height], pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(x=x, y=y)

    def draw_on(self, surface):
        surface.blit(self.surface, self.rect)

class Ball(Drawble):
    def __init__(self, x, y, width, height, color=(0,255,75), x_speed=3, y_speed=3):
        super(Ball, self).__init__(x, y, width, height, color)
        pygame.draw.ellipse(self.surface, self.color, [0, 0, self.width, self.height])
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.start_x = x
        self.start_y = y
    
    def bounce_y(self):
        self.y_speed += random.randint(1,3) 
        self.y_speed *= -1

    def bounce_x(self):
        self.x_speed += random.randint(1,3)
        self.x_speed *= -1

    def reset(self):
        self.rect.x,self.rect.y = self.start_x,self.start_y
        self.y_speed = 3
        self.x_speed = 3
        self.bounce_y()

    def move(self, board, *args):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.x < 0 or self.rect.x > board.surface.get_width():
            self.bounce_x()
        if self.rect.y < 0 or self.rect.y > board.surface.get_height():
            self.bounce_y()
        for rocket in args:
            if self.rect.colliderect(rocket.rect):
                self.bounce_y()
        

class Racket(Drawble):
    def __init__(self, x, y, width, height, color=(78,255,4), max_speed=100):
        super(Racket, self).__init__(x, y, width, height, color)
        self.surface.fill(color)
        self.max_speed = max_speed
    
    def move(self, x):
        delta = x - self.rect.x
        if abs(delta) > self.max_speed:
            delta = self.max_speed if delta > 0 else -self.max_speed
        self.rect.x += delta

class ArtificialInteligence(object):
    def __init__(self, racket, ball, max_speed=3):
        self.racket = racket
        self.ball = ball
        self.max_speed = max_speed

    def move(self):
        x = self.ball.rect.centerx
        self.racket.move(x)
        

class Judge(object):
    def __init__(self, board, ball, *args):
        self.board = board
        self.ball = ball
        self.rockets = args
        self.score = [0,0]
        pygame.font.init()
        font_path = pygame.font.match_font("Times New Roman")
        self.font = pygame.font.Font(font_path, 36)
    
    def update_score(self, board_height):
        if self.ball.rect.y < 0:
            self.score[0] += 1
            self.ball.reset()
        elif self.ball.rect.y > board_height:
            self.score[1] += 1
            self.ball.reset()
    
    def draw_text(self, surface, text, x, y):
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = x,y
        surface.blit(text_surface, text_rect)

    def draw_on(self, surface):
        height = self.board.surface.get_height()
        self.update_score(height)
        width = self.board.surface.get_width()
        self.draw_text(surface, f"Player {self.score[0]}", width/2, height*0.02)   
        self.draw_text(surface, f"Computer {self.score[1]}", width/2, height*0.07)  

class PongGame(object):
    def __init__(self, width, height):
        pygame.init()
        self.game = Game(width, height)
        self.fps = pygame.time.Clock()
        self.ball = Ball(width//2, height//2, 20, 20)
        self.player1 = Racket(width=60, height=10, x=width/2, y=height-15)
        self.player2 = Racket(width=60, height=10, x=width/2, y=5, color=(255,0,0))
        self.ai = ArtificialInteligence(self.player2, self.ball)
        self.judge = Judge(self.game, self.ball, self.player2, self.ball)

    def run(self):
        while not self.handle_events():
            self.ball.move(self.game, self.player1, self.player2)
            self.game.draw(self.ball, self.player1, self.player2, self.judge)
            self.ai.move()
            self.fps.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.locals.MOUSEMOTION:
                x,y = event.pos
                self.player1.move(x)


if __name__ == "__main__":
    game = PongGame(720, 720)
    game.run()