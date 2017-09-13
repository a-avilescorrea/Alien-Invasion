import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_events(settings, game_board, stats, play_button, ship,
                 aliens, bullets, sb):
    """Respond to keyboard presses and interaction"""
    for event in pygame.event.get():
        # Check the current event
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, settings, game_board, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, game_board, stats, ship, aliens, bullets,
                              play_button, mouse_x, mouse_y, sb)


def check_keydown(event, settings, game_board, ship, bullets):
    """Respond to Keystrokes"""
    # Move the ship either right or left
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, game_board, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup(event, ship):
    """Respond to key releases"""
    # Stop moving the ship right or left
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(game_settings, game_board, stats, ship, aliens, bullets,
                      play_button, mouse_x, mouse_y, sb):
    """check to see if button is pressed"""
    button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_click and not stats.game_active:
        # Reset stats and hide mouse
        game_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.game_active = True

        # Reset scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty lists
        aliens.empty()
        bullets.empty()

        # Create a new fleet
        create_fleet(game_settings, game_board, ship, aliens)
        ship.center_ship()


def update_bullets(game_settings, game_board, ship, aliens, bullets, stats, sb):
    """A method to update bullets"""
    # Update positions
    bullets.update()

    # Delete Bullets as the leave the board
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_collisions(game_settings, game_board, ship, aliens, bullets, stats, sb)


def check_collisions(game_settings, game_board, ship, aliens, bullets, stats, sb):
    """Check for collisions between bullets and aliens
        remove any ships and bullets that have collided"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += game_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # Check if new fleet is required
    if len(aliens) == 0:
        # Destroy remaining bullets and create a new fleet
        bullets.empty()
        game_settings.increase_speed()

        # increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(game_settings, game_board, ship, aliens)


def fire_bullet(settings, game_board, ship, bullets):
    """A method to fire bullets"""
    # Create a new bullet and add it to group if limit hasn't been reached
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, game_board, ship)
        bullets.add(new_bullet)


def update_game_board(game_settings, game_board, stats, ship, aliens,
                      bullets, button, score_board):
    """Updates the game board for the game"""
    # Redraw the board with every pass through
    game_board.fill(game_settings.bg_color)
    # Redraw all the bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(game_board)

    # Show the score
    score_board.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        button.draw_button()

    # Make the board visible
    pygame.display.flip()


def create_fleet(game_settings, game_board, ship, aliens):
    """A method to draw the fleet of Aliens"""
    alien = Alien(game_settings, game_board)
    number_aliens = get_num_aliens(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens
    for row_num in range(number_rows):
        for alien_number in range(number_aliens):
            create_alien(game_settings, game_board, aliens, alien_number, row_num)


def get_num_aliens(settings, alien_width):
    """Calculates the number of aliens that fit into a row"""
    avail_space_horiz = settings.board_width - (2 * alien_width)
    return int(avail_space_horiz / (2 * alien_width))


def create_alien(game_settings, game_board, aliens, alien_num, row_number):
    """Create an alien and place it in row"""
    alien = Alien(game_settings, game_board)
    alien_width = alien.rect.width
    alien.x = alien_width + (2 * alien_width * alien_num)
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(game_settings, ship_height, alien_height):
    """A method to get the number of rows for the game"""
    available_y = (game_settings.board_length - (3 * alien_height) - ship_height)
    return int(available_y / (2 * alien_height))


def update_aliens(game_settings, stats, game_board, ship, aliens, bullets, sb):
    """A method to update the pos of aliens"""
    check_fleet_edge(game_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions and aliens hitting the bottom
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, stats, game_board, ship, aliens, bullets, sb)
    check_aliens_bottom(game_settings, stats, game_board, ship, aliens, bullets, sb)


def ship_hit(game_settings, stats, game_board, ship, aliens, bullets, sb):
    """Respond to a ship being hit by and alien"""
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # Update the ScoreBoard
        sb.prep_ships()

        # Empty Bullets and aliens
        aliens.empty()
        bullets.empty()

        # Create and center a new ship
        create_fleet(game_settings, game_board, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        stats.reset_stats()


def check_fleet_edge(game_settings, aliens):
    """Checks to see if any Alien in the fleet has reached the  edge"""
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_dir(game_settings, aliens)
            break


def change_fleet_dir(game_settings, aliens):
    """Changes the direction of the fleet"""
    for alien in aliens.sprites():
        alien.rect.y += game_settings.alien_drop_speed
    game_settings.fleet_direction *= -1


def check_aliens_bottom(game_settings, stats, game_board, ship, aliens, bullets, sb):
    """Checks to see if the aliens have reached the bottom of the screen"""
    board_rect = game_board.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= board_rect.bottom:
            # This is the same as a ship getting hit
            ship_hit(game_settings, stats, game_board, ship, aliens, bullets, sb)
            break


def check_high_score(stats, sb):
    """Check for new high scores"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
