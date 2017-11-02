from random import choice


class Narrator:

    move = ["You stumble along", "You wander", "You head"]
    roomLeadin = ["You can see", "There is"]

    def __init__(self):
        pass

    @staticmethod
    def randMoveNarration():
        return choice(Narrator.move)

    @staticmethod
    def randRoomLeadin():
        return choice(Narrator.roomLeadin)
