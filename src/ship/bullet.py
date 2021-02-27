import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    def __init__(self, ai_settings, screen, ship):
        # 在飞船所处位置创建子弹对象
        # super表示继承sprite，通过精灵，将游戏相关元素编组，从而操作编组中所有元素
        # super(Bullet,self).__init__()
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.ship = ship
        # self.screen = screen

        # 因为子弹并非基于图像，必须使用pygame.Rect类从空白创建矩形，此类需要提供x、y坐标和宽度、高度。在（0，0）处创建一个子弹矩形，再设置正确位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        # 向上移动子弹，更新子弹位置的小数值.在屏幕中向上移动，意味着y坐标不断减小--
        # 在Pygame和许多图形框架中，原点位于左上角。因此，在1200x800游戏窗口上，左上角为（0，0），左下角为（0，800）。如果要从屏幕上移，请逐渐减小y值。
        self.y -= self.speed_factor
        # 更新子弹位置
        self.rect.y = self.y

    def draw_bullet(self):
        # 在屏幕上绘制子弹
        pygame.draw.rect(self.screen, self.color, self.rect)
