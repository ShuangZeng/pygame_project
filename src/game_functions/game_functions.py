import sys
import pygame

from time import sleep

from src.alien.alien import Alien
from src.ship.bullet import Bullet


def check_keydown_events(event, ship, ai_settings, screen, bullets):
    if event.key == pygame.K_RIGHT:
        # 飞船向右移动
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    #             创建子弹，并加入编组,检查子弹数
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ship, ai_settings, screen, bullets, stats, play_button, aliens, sb):
    # 响应按键和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, ai_settings, screen, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, ship, aliens, bullets, sb)

def check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, ship, aliens, bullets, sb):
    button_clicked = play_button.rect.collidepoint(mouse_x,  mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        # 游戏开始后光标不可见
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score
        sb.prep_level
        sb.prep_ships()

# 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

#         创建新外星人并且让ship居中
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

def update_bullets(ai_settings, screen, ship, bullets, aliens, sb, stats):
    bullets.update()

    # 删除到达屏幕顶端的的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_colllision(aliens, bullets, ai_settings, screen, ship, sb, stats)
    # 打印剩余子弹确认删除
    # print(len(bullets))
    # 检查是否有子弹击中外星人，如果是，删除子弹和外星人

    # print(len(aliens))


def check_bullet_alien_colllision(aliens, bullets, ai_settings, screen, ship, sb, stats):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        # 防止子弹过宽射中多个外星人没有计分
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    #     删除现有子弹并新建外星人
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, aliens, ship)


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


# 计算每行可容纳是多少外星人
def get_alien_number(ai_settings, alien_width):
    available_space = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    # 避免反复访问rect
    alien_width = alien.rect.width
    # 创建一个外星人并放在当前行，同时外星人横坐标不断右移
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    # print(alien.rect.x, alien.rect.y)


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_fleet(ai_settings, screen, aliens, ship):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_alien_number(ai_settings, alien.rect.width)
    numeber_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(numeber_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
            # print(row_number, alien_number)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_seed
    ai_settings.fleet_direction *= -1


# def remove_alien(aliens, screen):
#     for alien in aliens:
#         screen_rect = screen.get_rect()
#         if alien.rect.bottom >= screen_rect.bottom -  (alien.rect.height * 2):
#             aliens.remove(alien)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    #     响应撞到的飞船
    print(stats.ships_left)
    # 从0到3，要想限制3个飞船，不能遍历到0的位置
    if stats.ships_left > 1:
        stats.ships_left -= 1
        sb.prep_ships()
    # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

    # 创建一群新的外星人，并将飞船放在屏幕底端中央
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        sleep(0.5)
        # print(stats.ships_left)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # remove_alien(aliens, screen)
    #     检查外星人和飞船碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
    check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, sb):
    # 更新屏幕图像，并切换到新屏幕
    # 每次循环都重绘屏幕
    screen.fill(ai_settings.bg_color)

    # 在飞船和外星人后面绘制所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    # for alien in aliens.sprites():
    #     alien.blitme()
    aliens.draw(screen)
    sb.show_score()
    # 如果游戏处于非活动状态，绘制按钮
    if not stats.game_active:
        play_button.draw_button()


    # 让最近绘制屏幕可见
    pygame.display.flip()
