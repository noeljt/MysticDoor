
class WeaponItem extends Item{
    def __init__(self, data):
        self.id = int(data["id"])
        self.name = data["name"]
        self.desc = data["desc"]
        self.action = data["action"]
    
    def getAction(self):
        return self.action
    
}

