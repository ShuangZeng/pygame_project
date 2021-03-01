#管理飞船行为
import pygame
import self as self
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, screen, ai_settings):
        super().__init__()
        # 初始化飞船并设置初始位置,screen决定了飞船绘制到什么地方
        self.screen = screen
        self.ai_settings = ai_settings
        #加载飞船图像并获取外界矩形
        self.image = pygame.image.load('./images/airplain.PNG')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 处理rect 对象时，可使用矩形四角和中心的 x 和 y 坐标。可通过设置这些值来指定矩形的位置。

        #把每艘新船放在屏幕底部中央,.centerx （飞船中心的x 坐标）,bottom （飞船下边缘的y 坐标）
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        #移动标志
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
    #     让飞船在屏幕上居中
        self.center = self.screen_rect.centerx

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed

        # 更新self.center 后，我们再根据它来
        # 更新控制飞船位置的self.rect.centerx 。self.rect.centerx 将只存储self.center 的整数部分，但对显示飞船而言，这问题不大
        self.rect.centerx = self.center


    def blitme(self):
        # 指定位置绘制飞船
        self.screen.blit(self.image, self.rect)