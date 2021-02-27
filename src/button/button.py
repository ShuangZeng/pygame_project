import pygame.font

class Button():
    def  __init__(self, ai_settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 200,50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        # None-默认字体
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮只创建一次
        self.prep_msg(msg)

    def prep_msg(self, msg):
        # 将msg渲染为图像
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 用fill（）绘制按钮矩形，用blit（）传递图像和关联的rect对象，从而在屏幕绘制
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)