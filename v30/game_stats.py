import os

class GameStats:
    """Track statistics for Alien Shooter."""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        
        self.game_active = False
        self.victory = False 
        
        # Load high score from a file
        self.high_score = self._load_high_score()

    def _load_high_score(self):
        """Read high score from a file, or return 0 if file doesn't exist."""
        if os.path.exists('highscore.txt'):
            try:
                with open('highscore.txt', 'r') as f:
                    return int(f.read())
            except (ValueError, IOError):
                return 0
        return 0

    def save_high_score(self):
        """Write the current high score to the file."""
        try:
            with open('highscore.txt', 'w') as f:
                f.write(str(self.high_score))
        except IOError:
            print("Error saving high score.")

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.bullets_left = self.settings.max_bullets
        self.score = 0
        self.victory = False