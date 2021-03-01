# 创建Pygame窗口以及响应用户输入
import pygame
from pygame.sprite import Group

from src.settings.settings import Settings
from src.ship.ship import Ship
from src.alien.alien import Alien
from src.game_functions import game_functions as gf
from src.game_stats.game_stats import GameStats
from  src.button.button import Button
from  src.game_stats.scoreboard import Scoreboard

def run_game():
    # initialize game, settings and screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    # 设置游戏窗口
    pygame.display.set_caption("Alien Invasion")

    # 创建play按钮
    play_button = Button(ai_settings, screen, "Play")

    bg_color = ai_settings.bg_color
    ship = Ship(screen, ai_settings)
    alien = Alien(ai_settings, screen)
    stats = GameStats(ai_settings)
    # 创建记分牌
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建存储和管理所有子弹的编组
    bullets = Group()
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, aliens, ship)

    # start game cycle
    while True:
        gf.check_events(ship, ai_settings, screen, bullets, stats, play_button, aliens, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen,  ship, bullets, aliens, sb, stats)
        # gf.create_fleet(ai_settings, screen, aliens, ship)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets,sb)
        # else:
        #     print("game over")
        # 用背景色填充屏幕
        # 每次循环都重绘屏幕
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, sb)


run_game()
