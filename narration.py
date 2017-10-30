from random import choice


class Narration:

    move = ["You stumble along", "You wander", "You head"]
    room_leadin = ["You can see", "There is"]

    def __init__(self):
        pass

    @staticmethod
    def rand_move_narration():
        return choice(Narration.move)

    @staticmethod
    def rand_room_leadin():
        return choice(Narration.room_leadin)
