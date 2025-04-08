class DogProxy:
    def __init__(self):
        super().__init__()
        self.dog_actor = None
        self.player_id = 0
        self.player_name = ""
        self.game_id = 0
        self.status = 0
        # 0 - file game.id not found; 1 - not connected to server; 2 - connected without match; 3 - waiting move (even if it's the local player's turn)
        self.move_order = 0
        self.url = "https://api-dog-server.herokuapp.com/"

    def get_status(self):
        return self.status
