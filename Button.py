import random
from select import select
import pygame
from Rect import Rect
import time


class Button:
    def __init__(self, width, height, x_max, y_max, center_x, center_y, text, sound_path):
        self.width = width
        self.height = height
        self.x_max = x_max
        self.y_max = y_max
        self.text = text
        self.rect_view = pygame.Rect(0, 0, self.width, self.height)
        self.rect_view.centerx = center_x
        self.rect_view.centery = center_y
        self.rect_text = pygame.Rect(0, 0, self.text.get_width(), self.text.get_height())
        self.rect_text.centerx = center_x
        self.rect_text.centery = center_y
        self.sound = pygame.mixer.Sound(sound_path)

    def get_center_y(self): return self.rect_view.centery

    def get_rect_view(self): return self.rect_view

    def to_show(self, color_background, screen):
        pygame.draw.rect(screen, color_background, self.rect_view, border_radius=10)
        screen.blit(self.text, self.rect_text)

    def do_sound(self, background_sound):
        background_sound.stop()
        self.sound.play()
        self.sound.set_volume(1)
        time.sleep(1)
        self.sound.stop()
        background_sound.play()
