
class Camera:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y
    
    def follow(self, x=0, y=0):
        self.x += 0.1 * (x - self.x)
        self.y += 0.1 * (y - self.y)

cam = Camera()