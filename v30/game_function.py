import sys, pygame
from time import sleep
from bullet import Bullet
from alien import Alien

def check_events(ai_game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: _check_play_button(ai_game, pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN: _check_keydown_events(event, ai_game)
        elif event.type == pygame.KEYUP: _check_keyup_events(event, ai_game)

def _check_play_button(ai_game, mouse_pos):
    if ai_game.play_button.rect.collidepoint(mouse_pos) and not ai_game.stats.game_active:
        ai_game.settings.initialize_dynamic_settings()
        ai_game.stats.reset_stats()
        ai_game.stats.game_active = True
        ai_game.sb.prep_images()
        ai_game.aliens.empty(); ai_game.bullets.empty()
        create_fleet(ai_game); pygame.mouse.set_visible(False)

def _check_keydown_events(event, ai_game):
    if event.key == pygame.K_RIGHT: ai_game.ship.moving_right = True
    elif event.key == pygame.K_LEFT: ai_game.ship.moving_left = True
    elif event.key == pygame.K_SPACE: _fire_bullet(ai_game)

def _check_keyup_events(event, ai_game):
    if event.key == pygame.K_RIGHT: ai_game.ship.moving_right = False
    elif event.key == pygame.K_LEFT: ai_game.ship.moving_left = False

def _fire_bullet(ai_game):
    if ai_game.stats.bullets_left > 0 and ai_game.stats.game_active:
        ai_game.bullets.add(Bullet(ai_game)); ai_game.stats.bullets_left -= 1; ai_game.sb.prep_bullets()

def create_fleet(ai_game):
    alien = Alien(ai_game); alien_w, alien_h = alien.rect.size
    for row in range(3):
        for col in range(int((ai_game.settings.screen_width - (2*alien_w)) // (1.5*alien_w))):
            new_alien = Alien(ai_game); new_alien.target_y = alien_h + 1.5 * alien_h * row
            new_alien.rect.y = -500; new_alien.x = alien_w + 1.5 * alien_w * col
            new_alien.rect.x = new_alien.x; ai_game.aliens.add(new_alien)

def update_bullets(ai_game):
    ai_game.bullets.update()
    for bullet in ai_game.bullets.copy():
        if bullet.rect.bottom <= 0: ai_game.bullets.remove(bullet)
    _check_bullet_alien_collisions(ai_game)
    if ai_game.stats.bullets_left == 0 and not ai_game.bullets and ai_game.aliens: _ship_hit(ai_game)

def _check_bullet_alien_collisions(ai_game):
    collisions = pygame.sprite.groupcollide(ai_game.bullets, ai_game.aliens, True, True)
    if collisions:
        for aliens in collisions.values(): ai_game.stats.score += 10 * len(aliens)
        ai_game.sb.prep_score(); _check_high_score(ai_game)

    if not ai_game.aliens:
        ai_game.bullets.empty()
        if ai_game.settings.game_level == ai_game.settings.max_level:
            ai_game.stats.game_active = False
            ai_game.stats.victory = True
            pygame.mouse.set_visible(True)
        else:
            ai_game.settings.increase_difficulty()
            ai_game.stats.bullets_left = ai_game.settings.max_bullets
            ai_game.ship.update_appearance()
            ai_game.sb.prep_images(); create_fleet(ai_game)

def _check_high_score(ai_game):
    """Check to see if there's a new high score and save it."""
    if ai_game.stats.score > ai_game.stats.high_score:
        ai_game.stats.high_score = ai_game.stats.score
        ai_game.sb.prep_high_score()
        # Save to file immediately so it's not lost if the game crashes
        ai_game.stats.save_high_score()

def update_aliens(ai_game):
    in_place = True
    for a in ai_game.aliens.sprites():
        if a.rect.y < a.target_y: a.rect.y += 8; in_place = False
    if in_place:
        _check_fleet_edges(ai_game); ai_game.aliens.update()
        if pygame.sprite.spritecollideany(ai_game.ship, ai_game.aliens): _ship_hit(ai_game)
        _check_aliens_bottom(ai_game)

def _check_fleet_edges(ai_game):
    for a in ai_game.aliens.sprites():
        if a.check_edges():
            for alien in ai_game.aliens.sprites(): alien.rect.y += ai_game.settings.fleet_drop_speed
            ai_game.settings.fleet_direction *= -1; break

def _ship_hit(ai_game):
    if ai_game.stats.ships_left > 1:
        ai_game.stats.ships_left -= 1; ai_game.stats.bullets_left = ai_game.settings.max_bullets
        ai_game.sb.prep_images(); ai_game.aliens.empty(); ai_game.bullets.empty()
        create_fleet(ai_game); sleep(0.5)
    else: 
        ai_game.stats.ships_left = 0
        ai_game.sb.prep_ships(); ai_game.stats.game_active = False; pygame.mouse.set_visible(True)

def _check_aliens_bottom(ai_game):
    for a in ai_game.aliens.sprites():
        if a.rect.bottom >= ai_game.screen.get_rect().bottom: _ship_hit(ai_game); break

def update_screen(ai_game):
    ai_game.screen.fill(ai_game.settings.bg_color)
    if ai_game.stats.game_active:
        for b in ai_game.bullets.sprites(): b.draw_bullet()
        ai_game.ship.blitme(); ai_game.aliens.draw(ai_game.screen); ai_game.sb.show_score()
    else:
        t = pygame.font.SysFont("Impact", 100).render("ALIEN SHOOTER", True, (0, 102, 204))
        ai_game.screen.blit(t, (ai_game.settings.screen_width//2 - t.get_width()//2, 100))
        msg_font = pygame.font.SysFont("Impact", 80)
        if ai_game.stats.victory:
            win_msg = msg_font.render("YOU SAVED EARTH!", True, (0, 200, 0))
            ai_game.screen.blit(win_msg, (ai_game.settings.screen_width//2 - win_msg.get_width()//2, 250))
        elif ai_game.stats.ships_left == 0:
            go_msg = msg_font.render("GAME OVER", True, (255, 0, 0))
            ai_game.screen.blit(go_msg, (ai_game.settings.screen_width//2 - go_msg.get_width()//2, 250))
        ai_game.play_button.check_hover(pygame.mouse.get_pos()); ai_game.play_button.draw_button()
    pygame.display.flip()