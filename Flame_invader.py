import pygame
import sys
import random
from functools import partial
import pygame_menu as pm
import datetime

global user_name
user_name = "Player"
global selected_difficulty_index
selected_difficulty_index = 0

class GameState:
    def __init__(self, screen, dragon_sprites=None):
        self.screen = screen
        self.is_running = True
        self.ship_speed = 10
        self.animation_speed = 8
        self.animation_counter = 0
        self.enemy_spawn_timer = 0
        self.enemy_spawn_rate = 100
        self.enemy_yellow_spawn_timer = 0
        self.enemy_yellow_spawn_rate = 240
        self.enemy_green_spawn_timer = 0
        self.enemy_green_spawn_rate = 420
        self.score = 0
        self.fireballs = []
        self.enemies = []
        self.enemies_yellow = []
        self.enemies_green = []
        self.coins = []
        self.speed_lvl = 1
        self.attack_lvl = 1
        self.defense_lvl = 1
        self.upgrade_points = 0
        self.coin_spawn_timer = 0
        self.dragon_health = 100
        self.fireball_damage = 100
        self.defense = 1
        self.music_enabled = False
        self.music_volume = 1

    def update_difficulty(self, new_difficulty):
        print("Difficulty updated to:", new_difficulty)
        self.difficulty = new_difficulty
        self.enemy_spawn_rate = 100 * self.difficulty
        self.enemy_yellow_spawn_rate = 240 * self.difficulty
        self.enemy_green_spawn_rate = 420 * self.difficulty

class Coin:
    def __init__(self, x, y, speed=2):
        self.x = x
        self.y = y
        self.speed = speed
        self.sprites = load_sprite_sheet(pygame.image.load("Texture/coin.png"), 8, 1)
        self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def update(self):
        self.y += self.speed
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Button:
    def __init__(self, text, x, y, width, height, font_size, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.action = action
        self.font = pygame.font.Font(None, self.font_size)
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Enemy:
    def __init__(self, x, y, speed=2):
        self.x = x
        self.y = y
        self.speed = speed
        self.sprites = load_sprite_sheet(pygame.image.load("Texture/enemy.png"), 3, 1)
        self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.health = 100

    def update(self):
        self.y += self.speed
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Enemy_yellow:
    def __init__(self, x, y, speed=3):
        self.x = x
        self.y = y
        self.speed = speed
        self.sprites = load_sprite_sheet(pygame.image.load("Texture/enemy_yellow.png"), 3, 1)
        self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.health = 200

    def update(self):
        self.y += self.speed
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Enemy_green:
    def __init__(self, x, y, speed=1):
        self.x = x
        self.y = y
        self.speed = speed
        self.sprites = load_sprite_sheet(pygame.image.load("Texture/enemy_green.png"), 3, 1)
        self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.health = 300

    def update(self):
        self.y += self.speed
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Fireball:
    def __init__(self, x, y, speed=10):
        self.x = x
        self.y = y
        self.speed = speed
        self.sprites = load_sprite_sheet(pygame.image.load("Texture/fireball.png"), 1, 6)
        self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def update(self):
        self.y -= self.speed
        self.current_sprite += 0.2
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

def main_menu(screen, state):
    width, height = screen.get_size()
    menu_background = pygame.image.load("Texture/menu_background.png")
    buttons = [
        Button("Play", width // 2 - 150, height // 2 - 120, 300, 70, 48, action="play"),
        Button("Shop", width // 2 - 150, height // 2 - 40, 300, 70, 48, action="shop"),
        Button("Options", width // 2 - 150, height // 2 + 40, 300, 70, 48, action="options"),
        Button("Quit", width // 2 - 150, height // 2 + 120, 300, 70, 48, action="quit")
    ]
    menu_running = True
    while menu_running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_hovered(mouse_pos):
                        if button.action == "quit":
                            pygame.quit()
                            sys.exit()
                        if button.action == "play":
                            state = game_loop(screen, state)
                        if button.action == "shop":
                            state = shop_menu(screen, state)
                        if button.action == "options":
                            option(screen, state)
        screen.fill((0, 0, 0))
        screen.blit(menu_background, (0, 0))
        for button in buttons:
            button.draw(screen)
        pygame.display.update()

def load_sprite_sheet(sheet, columns, rows):
    sheet_width, sheet_height = sheet.get_size()
    sprite_width = sheet_width // columns
    sprite_height = sheet_height // rows
    sprites = []
    for row in range(rows):
        for col in range(columns):
            rect = pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height)
            image = pygame.Surface(rect.size).convert()
            image.blit(sheet, (0, 0), rect)
            image.set_colorkey((0, 0, 0))
            sprites.append(image)
    return sprites

def game_loop(screen, state):
    clock = pygame.time.Clock()
    background_image = pygame.image.load("Texture/game_background.jpg")
    dragon_sheet = pygame.image.load("Texture/dragon_bleu.png")
    dragon_sprites = load_sprite_sheet(dragon_sheet, 3, 1)
    ship_x = screen.get_width() / 2 - dragon_sprites[0].get_width() / 2
    ship_y = screen.get_height() - dragon_sprites[0].get_height() - 100
    dragon_index = 0
    while state.is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fireball_x = ship_x + dragon_sprites[0].get_width() / 2
                    fireball_y = ship_y
                    state.fireballs.append(Fireball(fireball_x, fireball_y))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            main_menu(screen, state)
        if keys[pygame.K_LEFT]:
            ship_x -= state.ship_speed
            if ship_x < 0:
                ship_x = 0
        if keys[pygame.K_RIGHT]:
            ship_x += state.ship_speed
            if ship_x > screen.get_width() - dragon_sprites[0].get_width():
                ship_x = screen.get_width() - dragon_sprites[0].get_width()
        state.animation_counter += 1
        if state.animation_counter >= state.animation_speed:
            dragon_index = (dragon_index + 1) % len(dragon_sprites)
            state.animation_counter = 0

        for fireball in state.fireballs[:]:
            fireball.update()
            fireball_rect = pygame.Rect(fireball.x, fireball.y, fireball.image.get_width(), fireball.image.get_height())
            fireball_removed = False

            for enemy in state.enemies[:]:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.image.get_width(), enemy.image.get_height())
                if fireball_rect.colliderect(enemy_rect):
                    state.fireballs.remove(fireball)
                    fireball_removed = True
                    enemy.health -= state.fireball_damage
                    if enemy.health <= 0:
                        state.enemies.remove(enemy)
                        state.score += 1
                    break

            if fireball_removed:
                continue

            for enemy_yellow in state.enemies_yellow[:]:
                enemy_yellow_rect = pygame.Rect(enemy_yellow.x, enemy_yellow.y, enemy_yellow.image.get_width(), enemy_yellow.image.get_height())
                if fireball_rect.colliderect(enemy_yellow_rect):
                    if not fireball_removed:
                        state.fireballs.remove(fireball)
                        fireball_removed = True
                    enemy_yellow.health -= state.fireball_damage
                    if enemy_yellow.health <= 0:
                        state.enemies_yellow.remove(enemy_yellow)
                        state.score += 2
                    break

            if fireball_removed:
                continue

            for enemy_green in state.enemies_green[:]:
                enemy_green_rect = pygame.Rect(enemy_green.x, enemy_green.y, enemy_green.image.get_width(), enemy_green.image.get_height())
                if fireball_rect.colliderect(enemy_green_rect):
                    if not fireball_removed:
                        state.fireballs.remove(fireball)
                        fireball_removed = True
                    enemy_green.health -= state.fireball_damage
                    if enemy_green.health <= 0:
                        state.enemies_green.remove(enemy_green)
                        state.score += 3

            if not fireball_removed and fireball.y < -fireball.image.get_height():
                state.fireballs.remove(fireball)

        screen.blit(background_image, (0, 0))
        screen.blit(dragon_sprites[dragon_index], (ship_x, ship_y))
        for fireball in state.fireballs:
            screen.blit(fireball.image, (fireball.x - 70, fireball.y - 70))

        state.enemy_spawn_timer += 1
        if state.enemy_spawn_timer >= state.enemy_spawn_rate:
            enemy_x = random.randint(0, screen.get_width() - 64)
            state.enemies.append(Enemy(enemy_x, -64))
            state.enemy_spawn_timer = 0
        for enemy in state.enemies[:]:
            enemy.update()
            if enemy.y > screen.get_height():
                state.dragon_health -= 20 * state.defense
                state.enemies.remove(enemy)
            else:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.image.get_width(), enemy.image.get_height())
                dragon_rect = pygame.Rect(ship_x, ship_y, dragon_sprites[0].get_width(), dragon_sprites[0].get_height())
                if dragon_rect.colliderect(enemy_rect):
                    state.dragon_health -= 10 * state.defense
                    state.enemies.remove(enemy)
        for enemy in state.enemies:
            enemy.draw(screen)

        state.enemy_yellow_spawn_timer += 1
        if state.enemy_yellow_spawn_timer >= state.enemy_yellow_spawn_rate:
            enemy_x_yellow = random.randint(0, screen.get_width() - 64)
            state.enemies_yellow.append(Enemy_yellow(enemy_x_yellow, -64))
            state.enemy_yellow_spawn_timer = 0
        for enemy_yellow in state.enemies_yellow[:]:
            enemy_yellow.update()
            if enemy_yellow.y > screen.get_height():
                state.dragon_health -= 20 * state.defense
                state.enemies_yellow.remove(enemy_yellow)
            else:
                enemy_yellow_rect = pygame.Rect(enemy_yellow.x, enemy_yellow.y, enemy_yellow.image.get_width(), enemy_yellow.image.get_height())
                dragon_rect = pygame.Rect(ship_x, ship_y, dragon_sprites[0].get_width(), dragon_sprites[0].get_height())
                if dragon_rect.colliderect(enemy_yellow_rect):
                    state.dragon_health -= 10 * state.defense
                    state.enemies_yellow.remove(enemy_yellow)
        for enemy_yellow in state.enemies_yellow:
            enemy_yellow.draw(screen)

        state.enemy_green_spawn_timer += 1
        if state.enemy_green_spawn_timer >= state.enemy_green_spawn_rate:
            enemy_x_green = random.randint(0, screen.get_width() - 64)
            state.enemies_green.append(Enemy_green(enemy_x_green, -64))
            state.enemy_green_spawn_timer = 0
        for enemy_green in state.enemies_green[:]:
            enemy_green.update()
            if enemy_green.y > screen.get_height():
                state.dragon_health -= 20 * state.defense
                state.enemies_green.remove(enemy_green)
            else:
                enemy_green_rect = pygame.Rect(enemy_green.x, enemy_green.y, enemy_green.image.get_width(), enemy_green.image.get_height())
                dragon_rect = pygame.Rect(ship_x, ship_y, dragon_sprites[0].get_width(), dragon_sprites[0].get_height())
                if dragon_rect.colliderect(enemy_green_rect):
                    state.dragon_health -= 10 * state.defense
                    state.enemies_green.remove(enemy_green)
        for enemy_green in state.enemies_green:
            enemy_green.draw(screen)

        state.coin_spawn_timer += 1
        if state.coin_spawn_timer >= 1000:
            coin_x = random.randint(0, screen.get_width() - 64)
            state.coins.append(Coin(coin_x, -64))
            state.coin_spawn_timer = 0
        for coin in state.coins[:]:
            coin.update()
            coin_rect = pygame.Rect(coin.x, coin.y, coin.image.get_width(), coin.image.get_height())
            dragon_rect = pygame.Rect(ship_x, ship_y, dragon_sprites[0].get_width(), dragon_sprites[0].get_height())
            if coin.y > screen.get_height():
                state.coins.remove(coin)
            elif coin_rect.colliderect(dragon_rect):
                state.coins.remove(coin)
                state.upgrade_points += 1
        for coin in state.coins:
            coin.draw(screen)
        if state.dragon_health <= 0:
            game_over(screen, state)
        font = pygame.font.Font(None, 74)
        text = font.render("Score: " + str(state.score), True, (255, 255, 255))
        upgrade_text = font.render("Upgrade: " + str(state.upgrade_points), True, (255, 255, 255))
        health_text = font.render("Health: " + str(int(state.dragon_health)), True, (255, 255, 255))
        screen.blit(health_text, (800, 10))
        screen.blit(upgrade_text, (1630, 10))
        screen.blit(text, (10, 10))
        pygame.display.update()
        clock.tick(60)

def shop_menu(screen, state):
    width, height = screen.get_size()
    shop_background = pygame.image.load("Texture/shop_background.png")
    attack_icon = pygame.image.load("Texture/attack_icon.png")
    attack_icon = pygame.transform.scale(attack_icon, (100, 100))
    defense_icon = pygame.image.load("Texture/defense_icon.png")
    defense_icon = pygame.transform.scale(defense_icon, (100, 100))
    speed_icon = pygame.image.load("Texture/speed_icon.png")
    speed_icon = pygame.transform.scale(speed_icon, (100, 100))
    button_images = [attack_icon, defense_icon, speed_icon]

    font = pygame.font.Font(None, 36)

    def modify_speed(state):
        if (state.upgrade_points >= 1):
            state.upgrade_points -= 1
            state.ship_speed += 2
            state.speed_lvl += 1
            print("Speed increased to:", state.ship_speed, "LVL:", state.speed_lvl)

    def modify_attack(state):
        if (state.upgrade_points >= 1):
            state.upgrade_points -= 1
            state.fireball_damage += 100
            state.attack_lvl += 1
            print("Attack increased to:", state.attack_lvl, "LVL:", state.attack_lvl)

    def modify_defense(state):
        if (state.upgrade_points >= 1):
            state.upgrade_points -= 1
            state.defense -= 0.1
            state.defense_lvl += 1
            print("Defense increased to:", state.defense, "LVL:", state.defense_lvl)

    buttons = [
        Button("Attack", width // 2 - 300, height // 2 + 50, 100, 50, 32, action=lambda: modify_attack(state)),
        Button("Defense", width // 2 - 50, height // 2 + 50, 100, 50, 32, action=lambda: modify_defense(state)),
        Button("Speed", width // 2 + 200, height // 2 + 50, 100, 50, 32, action=lambda: modify_speed(state))
    ]

    shop_running = True
    while shop_running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    shop_running = False
                    return state
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_hovered(mouse_pos):
                        button.action()
        screen.fill((0, 0, 0))
        screen.blit(shop_background, (0, 0))
        for i, button in enumerate(buttons):
            image = button_images[i]
            image_x = button.x + button.width // 2 - image.get_width() // 2
            image_y = button.y - image.get_height() - 10
            screen.blit(image, (image_x, image_y))
            button.draw(screen)

        speed_lvl_text = font.render(f"LVL: {state.speed_lvl}", True, (255, 255, 255))
        speed_lvl_text_pos = (width // 2 + 215, height // 2 + 110)
        screen.blit(speed_lvl_text, speed_lvl_text_pos)

        attack_lvl_text = font.render(f"LVL: {state.attack_lvl}", True, (255, 255, 255))
        attack_lvl_text_pos = (width // 2 - 285, height // 2 + 110)
        screen.blit(attack_lvl_text, attack_lvl_text_pos)

        defense_lvl_text = font.render(f"LVL: {state.defense_lvl}", True, (255, 255, 255))
        defense_lvl_text_pos = (width // 2 - 35, height // 2 + 110)
        screen.blit(defense_lvl_text, defense_lvl_text_pos)

        upgrade_text = font.render("Upgrade: " + str(state.upgrade_points), True, (255, 255, 255))
        screen.blit(upgrade_text, (30, 30))

        pygame.display.update()

def game_over(screen, state):
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)
    write_score_to_file(state.score)
    state = GameState(screen)
    main_menu(screen, state)
    return state

def set_volume(value):
    pygame.mixer.music.set_volume(value)

def music(state, toggle_state=None):
    if not hasattr(state, 'music_initialized') or not state.music_initialized:
        pygame.mixer.music.load("Sound/music.mp3")
        pygame.mixer.music.play(-1)
        state.music_initialized = True

    state.music_enabled = not state.music_enabled
    if state.music_enabled:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

def option(screen, state):
    width, height = screen.get_size()
    menu = pm.Menu('Options', width, height, theme=pm.themes.THEME_DARK)

    new_difficulty = [
        ("Easy", 1),
        ("Medium", 0.5),
        ("Hard", 0.3),
        ("Impossible", 0)
    ]

    def on_difficulty_change(selected_option, value, **kwargs):
        global selected_difficulty_index
        if isinstance(selected_option, tuple) and isinstance(selected_option[0], tuple):
            _, difficulty_value = selected_option[0]
            selected_difficulty_index = [option[1] for option in new_difficulty].index(difficulty_value)
        else:
            print("selected_option n'est pas structuré comme attendu:", selected_option)
        print(f"Selected difficulty: {difficulty_value}")
        state.update_difficulty(difficulty_value)

    def update_user_name(value, **kwargs):
        global user_name
        user_name = value

    def choose_name():
        global user_name
        menu.add.text_input("Username : ", default=user_name, onchange=update_user_name)

    choose_name()
    menu.add.dropselect('Difficulty', new_difficulty, default=selected_difficulty_index, max_selected=1, selection_box_height=4, onchange=on_difficulty_change)
    menu.add.toggle_switch('Pause Music', not state.music_enabled, onchange=partial(music, state))
    menu.add.range_slider('Volume', default=pygame.mixer.music.get_volume(), range_values=(0, 1), increment=0.1, onchange=set_volume)
    menu.add.button('Back', main_menu, screen, state)

    option_running = True
    while option_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    option_running = False

        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)

        pygame.display.update()

    return state

def write_score_to_file(score):
    name = user_name
    difficulty = selected_difficulty_index
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("scores.txt", "a") as file:
        file.write(f"User: {name} - Date: {date_time} - Score: {score} - Difficulty {selected_difficulty_index}\n")

pygame.init()
width = 1920
height = 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flame Invader")
state = GameState(screen)
music(state)
main_menu(screen, state)
pygame.quit()