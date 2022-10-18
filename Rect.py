import pygame


class Rect:
    def __init__(self, width, height, x_max, y_max, position_increment_x):
        self.width = width
        self.height = height
        self.x_max = x_max
        self.y_max = y_max
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.x_max * position_increment_x
        self.rect.centery = self.y_max / 2

    def update(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def get_rect(self):
        return self.rect

    def move(self, x, y):
        if (self.rect.x + x > 0) and (self.rect.x + x + self.width < self.x_max): self.rect.x = self.rect.x + x
        if (self.rect.y + y > 0) and (self.rect.y + y + self.height < self.y_max): self.rect.y = self.rect.y + y

    def move_with_return(self, x, y):
        if self.rect.x + x + self.width >= self.x_max:
            self.rect.x = -1
        elif self.rect.y + y + self.height >= self.y_max:
            self.rect.y = -1
        else:
            self.rect.x = self.rect.x + x
            self.rect.y = self.rect.y + y

    def to_show(self, text, screen):
        screen.blit(text, self.rect)

    def delete(self):
        self.rect.centerx += self.x_max * 1000
        self.rect.centery += self.y_max * 1000
        
    def reset(self):
        self.rect.centerx -= self.x_max * 1000
        self.rect.centery -= self.y_max * 1000
