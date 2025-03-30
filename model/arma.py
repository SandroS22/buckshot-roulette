class Gun:
    def __init__(self):
        self.__mag_limit = 6
        self.__current_loaded = 0
    
    def shoot(self):
        print("bang")