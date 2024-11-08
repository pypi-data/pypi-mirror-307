import pygame
import time

class ElectroxGame:
    def __init__(self, name="Electrox Game", window_size="medium"):
        pygame.init()

        # Game name and window setup
        self.name = name
        self.window_size = self.get_window_size(window_size)
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.name)

        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()

        # Player data
        self.players = {}
        self.running = False

        # Popup management
        self.popups = []
        self.last_popup_time = pygame.time.get_ticks()  # Track the time of the last popup

    def get_window_size(self, size):
        if size == "small":
            return (400, 400)
        elif size == "medium":
            return (800, 800)
        elif size == "max":
            return (1200, 1200)
        else:
            raise ValueError("The window size can't be applied: choose 'small', 'medium', or 'max'.")

    def create_player(self, player_name):
        if player_name in self.players:
            print("Error: Player already exists.")
        else:
            # Red color for player character
            self.players[player_name] = {"x": 50, "y": 50, "color": (255, 0, 0)}
            print(f"Player '{player_name}' created successfully.")

    def move_player(self, player_name, direction):
        if player_name not in self.players:
            print("Error: Player does not exist.")
            return

        player = self.players[player_name]
        # Adjust movement step size
        if direction == "left":
            player["x"] -= 10
        elif direction == "right":
            player["x"] += 10
        elif direction == "up":
            player["y"] -= 10
        elif direction == "down":
            player["y"] += 10
        else:
            print("Error: Invalid direction.")
            return
        print(f"Moved '{player_name}' {direction}.")

    def spawn_popup(self, image_path, title="Popup Ad"):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_popup_time > 1700:  # 1700 ms = 1.7 seconds
            popup = ElectroxPopup(self, image_path, title)
            self.popups.append(popup)
            self.last_popup_time = current_time

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # Assuming a single player named 'me' for testing
                elif event.key == pygame.K_LEFT:
                    self.move_player(player_name="me", direction="left")
                elif event.key == pygame.K_RIGHT:
                    self.move_player(player_name="me", direction="right")
                elif event.key == pygame.K_UP:
                    self.move_player(player_name="me", direction="up")
                elif event.key == pygame.K_DOWN:
                    self.move_player(player_name="me", direction="down")

            for popup in self.popups:
                popup.handle_event(event)

    def update(self):
        # Placeholder for game state updates
        pass

    def draw(self):
        # Fill background color
        self.window.fill((0, 0, 0))  # Black background

        # Draw each player
        for player in self.players.values():
            pygame.draw.circle(self.window, player["color"], (player["x"], player["y"]), 15)

        # Draw popups
        for popup in self.popups:
            popup.draw()

    def run_game(self):
        self.running = True
        self.create_player("me")  # Create a default player

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()

class ElectroxPopup:
    def __init__(self, game, image_path, title="Popup Ad"):
        self.game = game
        self.title = title
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (300, 200))
        self.rect = self.image.get_rect(center=(self.game.window_size[0] // 2, self.game.window_size[1] // 2))
        self.showing = True
        self.close_button_rect = pygame.Rect(self.rect.right - 20, self.rect.top, 20, 20)

    def draw(self):
        if self.showing:
            overlay = pygame.Surface(self.game.window_size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.game.window.blit(overlay, (0, 0))
            self.game.window.blit(self.image, self.rect.topleft)
            pygame.draw.rect(self.game.window, (255, 0, 0), self.close_button_rect)
            font = pygame.font.Font(None, 20)
            text = font.render('X', True, (255, 255, 255))
            self.game.window.blit(text, (self.close_button_rect.x + 5, self.close_button_rect.y))

def handle_event(self, event):
    if self.showing and event.type == pygame.MOUSEBUTTONDOWN:
        # Check if the click is on the close button
        if self.close_button_rect.collidepoint(event.pos):
            self.showing = False
        # Check if the title contains a specific substring (case-insensitive example)
        elif "mario" in self.title.lower():
            # Perform an action if the title contains the word "special"
            for _ in range(5):
                self.game.spawn_popup("mario.jpg", "3 days until mario steals your liver")
