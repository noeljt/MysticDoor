#different items add different funcionality to the game

class PaperItem extends Item{
    def __init__(self, data):
        self.id = int(data["id"])
        self.name = data["name"]
        self.desc = data["desc"]
        self.action = data["action"]
    
    def fire_action(self):
        #Light on fire
        self.name = "ash"
        self.desc = "The paper has been set ablaze"
}
