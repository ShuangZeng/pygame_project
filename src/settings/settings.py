class Settings():
# 存储《外星人入侵》的所有设置的类
    def __init__(self):
        # 初始化游戏设置
        # 屏幕设置
        # pygame中颜色由RGB值指定
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (135, 206, 235)
        self.bullets_allowed = 5

        # 子弹设置
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60

        # 有外星人撞到边缘时下移的速度
        self.fleet_drop_seed = 10
        # 以什么速度加快游戏节奏
        self.speedup_scale = 1.2
        # 击败外星人点数的增加速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    #     计分
        self.alien_points = 50
    def initialize_dynamic_settings(self):
#     初始化随游戏进行而变化的设置
        self.ship_speed = 1.5
        self.ship_limit = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1

    def increase_speed(self):
        # 提高速度设置
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
