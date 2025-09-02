import math as m

class Vec2:
    def __init__(self):
        pass
    def newVec2(self,x,y):
        return [x,y]
    def monoVec2(self, x):
        return [x,x]
    def addVec2(self, vec1, vec2):
        return [vec1[0]+vec2[0],vec1[1]+vec2[1]]
    def subtractVec2(self, vec1, vec2):
        return [vec1[0]-vec2[0],vec1[1]-vec2[1]]
    def multiplyVec2(self, vec1, vec2):
        return [vec1[0]*vec2[0],vec1[1]*vec2[1]]
    def divideVec2(self, vec1, vec2):
        return [vec1[0]/vec2[0],vec1[1]/vec2[1]]
    def dotProduct(self, vec1, vec2):
        return vec1[0]*vec2[0] + vec1[1]*vec2[1]
    def magnitude2(self, vec):
        return m.sqrt(vec[0]**2 + vec[1]**2)
    def normalize2(self, vec):
        mag = self.magnitude2(vec)
        return [vec[0]/mag,vec[1]/mag]

class Time:
    def __init__(self, deltaTime):
        dt = deltaTime
    def setDeltaTimeTo(self, val):
        dt = val
    def changeDeltaTimeBy(self, val):
        dt += val

class Settings:
    def __init__(self, frictionAmount):
        friction = frictionAmount

vec = Vec2()

time = Time(0.1)

physics = Settings(0.9)

class physics2D:
    def __init__(self, initialPos, initialVel, weight, direction):
        pos = initialPos
        vel = initialVel
        mass = weight
        dir = direction
    def accelerate(self, speed):
        self.vel[0] += speed * m.sin(dir)
        self.vel[1] += speed * m.cos(dir)
    def force(self, force):
        self.accelerate((force / self.mass) * time.dt)
    def stepSimulation(self):
        vec.multiplyVec2(self.vel,vec.monoVec2(physics.friction))
        vec.addVec2(self.pos,self.vel)

rigidbody = physics2D([0,0],[0,0],5,0)