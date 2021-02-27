import pygame
from pygame.sprite import Sprite

from src.ship.ship import Ship

class Alien(Sprite):

    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载外星人图像，并设置rect属性
        self.image = pygame.image.load('./images/alien.png')
        self.rect = self.image.get_rect()

        # 外星人最初在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 存储外星人准确位置
        self.x = float(self.rect.x)

    def check_edges(self):
        # 如果外星人位于边缘，返回true
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        # elif self.rect.bottom >= screen_rect.bottom - (2 * self.rect.bottom):
        #     return True




    def update(self):
    #     向右移动外星人
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
    #     self.x += self.ai_settings.alien_speed_factor
        self.rect.x = self.x

    def blitme(self):
        # 在指定位置绘制外星人
        self.screen.blit(self.image, self.rect)

