class KeyItem extends Item{
    def __init__(self, data):
        self.id = int(data["id"])
        self.name = data["name"]
        self.desc = data["desc"]
        self.door = data["door"]
        
    def Open(self, Place):
        if "goal" in place:
            return True
        else:
            return False
}

