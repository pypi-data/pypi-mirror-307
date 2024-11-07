import pygame

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

    def update(self):
        # Placeholder for game state updates
        pass

    def draw(self):
        # Fill background color
        self.window.fill((0, 0, 0))  # Black background

        # Draw each player
        for player in self.players.values():
            pygame.draw.circle(self.window, player["color"], (player["x"], player["y"]), 15)

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
