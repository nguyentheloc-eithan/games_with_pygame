import pygame
from pygame import mixer
from os.path import join
from random import randint
from datetime import timedelta


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed=1000):
        super().__init__()
        self.image = pygame.image.load(
            join('../images', 'laser.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.pos = pygame.math.Vector2(self.rect.center)

    def update(self, dt):
        self.pos.y -= self.speed * dt
        self.rect.center = self.pos
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos, constraint):
        super().__init__()
        self.image = pygame.image.load(
            join('../images', 'meteor.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200
        self.constraint = constraint

    def update(self, dt):
        self.pos.y += self.speed * dt
        self.rect.center = self.pos
        if self.rect.top > self.constraint[1]:
            self.reset_position()

    def reset_position(self):
        self.pos.x = randint(
            self.rect.width, self.constraint[0] - self.rect.width)
        self.pos.y = -self.rect.height
        self.rect.center = self.pos


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint):
        super().__init__()
        self.image = pygame.image.load(
            join('../images', 'player.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.score = 0

        # Movement attributes
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 600
        self.constraint = constraint

        # Shooting cooldown
        self.can_shoot = True
        self.shoot_cooldown = 500
        self.last_shot_time = 0

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]

    def move(self, dt):
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        self.pos += self.direction * self.speed * dt
        self.pos.x = max(0 + self.rect.width/2,
                         min(self.constraint[0] - self.rect.width/2, self.pos.x))
        self.pos.y = max(0 + self.rect.height/2,
                         min(self.constraint[1] - self.rect.height/2, self.pos.y))
        self.rect.center = self.pos

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            self.can_shoot = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_shoot:
            self.last_shot_time = current_time
            self.can_shoot = False
            return True
        return False

    def update(self, dt):
        self.input()
        self.move(dt)


class Game:
    def __init__(self):
        pygame.init()
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720
        self.display_surface = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('Space Shooter')

        # Sound setup
        mixer.init()
        self.laser_sound = mixer.Sound(join('../audio', 'laser.wav'))
        self.explosion_sound = mixer.Sound(join('../audio', 'explosion.wav'))
        self.damage_sound = mixer.Sound(join('../audio', 'damage.ogg'))
        self.background_music = mixer.Sound(join('../audio', 'game_music.wav'))

        # Set volumes
        self.laser_sound.set_volume(0.3)
        self.explosion_sound.set_volume(0.4)
        self.damage_sound.set_volume(0.5)
        self.background_music.set_volume(0.2)

        # Start background music
        self.background_music.play(-1)

        # Font setup
        self.font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 32)

        # Clock setup
        self.clock = pygame.time.Clock()

        # Game constants
        self.MATCH_DURATION = 60  # 1 minute in seconds

        # Initialize game
        self.initialize_game()

    def initialize_game(self):
        # Restart background music
        self.background_music.stop()
        self.background_music.play(-1)

        # Game state
        self.game_active = True
        self.meteors_destroyed = 0

        # Timer setup
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0

        # Spawn timer setup
        self.spawn_timer = 0
        self.spawn_interval = 20
        self.spawn_amount = 5

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()
        self.meteor_sprites = pygame.sprite.Group()

        # Player setup
        self.player = Player((self.WINDOW_WIDTH/2, self.WINDOW_HEIGHT/2),
                             (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.all_sprites.add(self.player)

        # Background elements
        self.star_surf = pygame.image.load(
            join('../images', 'star.png')).convert_alpha()
        self.star_positions = [(randint(0, self.WINDOW_WIDTH), randint(
            0, self.WINDOW_HEIGHT)) for _ in range(20)]

        # Create initial meteors
        self.spawn_meteors(self.spawn_amount)

        # Reset announcement
        self.announcement_time = pygame.time.get_ticks()
        self.show_announcement = False

    def spawn_meteors(self, amount):
        for _ in range(amount):
            meteor = Meteor(
                (randint(0, self.WINDOW_WIDTH), -100),
                (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
            )
            self.meteor_sprites.add(meteor)
            self.all_sprites.add(meteor)

    def handle_collisions(self):
        # Check for laser hits on meteors
        for laser in self.laser_sprites:
            meteor_hits = pygame.sprite.spritecollide(
                laser, self.meteor_sprites, True)
            if meteor_hits:
                self.explosion_sound.play()
                laser.kill()
                self.meteors_destroyed += len(meteor_hits)
                self.spawn_meteors(len(meteor_hits))

        # Check for meteor hits on player
        if pygame.sprite.spritecollide(self.player, self.meteor_sprites, False):
            self.damage_sound.play()
            self.background_music.stop()
            self.game_active = False
            self.final_time = self.elapsed_time

    def display_score(self):
        score_text = f'Score: {self.meteors_destroyed}'
        score_surf = self.small_font.render(score_text, True, 'white')
        score_rect = score_surf.get_rect(topleft=(20, 20))
        self.display_surface.blit(score_surf, score_rect)

        if self.game_active:
            self.elapsed_time = (pygame.time.get_ticks() -
                                 self.start_time) // 1000
        time_text = f'Time: {str(timedelta(seconds=self.elapsed_time))}'
        time_surf = self.small_font.render(time_text, True, 'white')
        time_rect = time_surf.get_rect(topleft=(20, 60))
        self.display_surface.blit(time_surf, time_rect)

    def create_button(self, text, pos, width=200, height=50):
        button_surf = pygame.Surface((width, height))
        button_surf.fill('white')
        button_rect = button_surf.get_rect(center=pos)

        text_surf = self.small_font.render(text, True, 'black')
        text_rect = text_surf.get_rect(center=button_rect.center)

        return button_surf, button_rect, text_surf, text_rect

    def display_game_over(self):
        game_over_surf = self.font.render('GAME OVER', True, 'white')
        game_over_rect = game_over_surf.get_rect(
            center=(self.WINDOW_WIDTH/2, self.WINDOW_HEIGHT/2 - 150))

        score_text = f'Meteors Destroyed: {self.meteors_destroyed}'
        score_surf = self.font.render(score_text, True, 'white')
        score_rect = score_surf.get_rect(
            center=(self.WINDOW_WIDTH/2, self.WINDOW_HEIGHT/2 - 50))

        time_text = f'Survival Time: {str(timedelta(seconds=self.final_time))}'
        time_surf = self.font.render(time_text, True, 'white')
        time_rect = time_surf.get_rect(
            center=(self.WINDOW_WIDTH/2, self.WINDOW_HEIGHT/2 + 50))

        retry_button, retry_rect, retry_text, retry_text_rect = self.create_button(
            'Retry', (self.WINDOW_WIDTH/2 - 120, self.WINDOW_HEIGHT/2 + 150))
        exit_button, exit_rect, exit_text, exit_text_rect = self.create_button(
            'Exit', (self.WINDOW_WIDTH/2 + 120, self.WINDOW_HEIGHT/2 + 150))

        self.display_surface.blit(game_over_surf, game_over_rect)
        self.display_surface.blit(score_surf, score_rect)
        self.display_surface.blit(time_surf, time_rect)
        self.display_surface.blit(retry_button, retry_rect)
        self.display_surface.blit(exit_button, exit_rect)
        self.display_surface.blit(retry_text, retry_text_rect)
        self.display_surface.blit(exit_text, exit_text_rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        if mouse_clicked:
            if retry_rect.collidepoint(mouse_pos):
                self.initialize_game()
            elif exit_rect.collidepoint(mouse_pos):
                return False
        return True

    def display_announcement(self):
        if self.show_announcement:
            announcement_surf = self.font.render(
                'Next Level', True, 'white')
            announcement_rect = announcement_surf.get_rect(
                center=(self.WINDOW_WIDTH/2, self.WINDOW_HEIGHT/2))
            self.display_surface.blit(announcement_surf, announcement_rect)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.game_active:
                # Shooting
                if self.player.shoot():
                    self.laser_sound.play()
                    laser = Laser(self.player.rect.midtop)
                    self.laser_sprites.add(laser)
                    self.all_sprites.add(laser)

                # Update spawn timer
                self.spawn_timer += dt
                if self.spawn_timer >= self.spawn_interval:
                    self.spawn_timer = 0
                    self.spawn_amount += 2
                    self.spawn_meteors(self.spawn_amount)

                    if not self.show_announcement:
                        self.show_announcement = True
                        self.announcement_time = pygame.time.get_ticks()

                if self.show_announcement:
                    if pygame.time.get_ticks() - self.announcement_time >= 2000:
                        self.show_announcement = False

                # Update
                self.all_sprites.update(dt)
                self.handle_collisions()

                # Draw
                self.display_surface.fill('darkgrey')

                # Draw stars
                for pos in self.star_positions:
                    self.display_surface.blit(self.star_surf, pos)

                # Draw all sprites
                self.all_sprites.draw(self.display_surface)

                # Display score and timer
                self.display_score()

                # Display announcement
                self.display_announcement()

            else:
                # Game over screen
                self.display_surface.fill('darkgrey')
                running = self.display_game_over()

            pygame.display.update()

        pygame.quit()
        mixer.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
