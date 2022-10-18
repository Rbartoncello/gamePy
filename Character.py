import random
from select import select
import pygame
from Rect import Rect
import time


class Character:
    def __init__(self, width, height, image_path, x_max, y_max, position_increment, sound_path=None):
        self.width = width
        self.height = height
        self.character = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
        self.x_max = x_max
        self.y_max = y_max
        self.rect = Rect(self.width, self.height, self.x_max, self.y_max, position_increment)
        self.x = 0
        self.y = 0
        self.speed = 1
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)

    def get_rect(self):
        return self.rect.get_rect()

    def move_by_key(self, key_list):
        if key_list[pygame.K_LEFT]:
            self.rect.move(- 1, 0)
        if key_list[pygame.K_RIGHT]:
            self.rect.move(1, 0)
        if key_list[pygame.K_UP]:
            self.rect.move(0, - 1)
        if key_list[pygame.K_DOWN]:
            self.rect.move(0, 1)

    def move(self):
        self.rect.move_with_return(self.speed, self.speed)

    def increase_speed(self):
        self.speed = self.speed + 1

    def update(self, x, y):
        self.rect.update(x, y)

    def update_random(self):
        self.x = random.randrange(0 + self.width / 2, self.x_max - self.width / 2)
        self.y = random.randrange(0 + self.height / 2, self.y_max - self.height / 2)
        self.update(self.x, self.y)

    def edit_scale(self, width, height):
        self.width = width
        self.height = height
        self.character = pygame.transform.scale(self.character, (self.width, self.height))
        self.get_rect().width = self.width
        self.get_rect().height = self.height

    def get_character(self):
        return self.character

    def delete(self):
        self.rect.delete()

    def to_show(self, screen):
        screen.blit(self.character, self.rect)

    def do_sound(self, background_sound, seconds):
        background_sound.stop()
        self.sound.play()
        self.sound.set_volume(1)
        time.sleep(seconds)
        self.sound.stop()
        background_sound.play()

    def get_lenght_sound(self):
        return self.sound.get_length()
    
    def set_image(self, image_path):
        self.character = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
