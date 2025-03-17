import math as m
import json

g = 6.676 * 10**-11
c = 3.0 * 10**8

class Time:
    def __init__(self, deltaTime=0.1):
        self.deltaTime = deltaTime
    def dilateTimeGrav(self,mass1,mass2):
        pass
    def dilateTimeSpeed(self,velocity):
        pass

time = Time()

class Rigidbody2D:
    def __init__(self, initialVelocity=tuple, initialPosition=tuple, mass=float, freezeObj=bool):
        self.velocity = initialVelocity
        self.position = initialPosition
        self.mass = mass
        self.dir = 0
        with open("physicsObjects.json", "w") as file:
            json.dump("")

        with open("physicsObjects.json", "r") as file:
            self.objList = json.load(file)
        
    def data(self):
        print("Current Stats:")
        print("Delta Time is", time.deltaTime)
        print("Current Position:", self.position)
        print("Current Velocity:", self.velocity)
        print("Direction:",self.dir)
        print("Mass:", self.mass)
        dist = self.distanceTo(self.objList[self.findClosestBody()])
        if (dist <= 1.5*10^6):
            print("")
            print("Refrence Data:")
            print("Altitude:", dist)
            print("Longitude:", 90 * m.cos(self.position[0]))
            print("Latitude:", 90 * m.sin(self.position[1]))

    def pointAt(self,otherPos=tuple):
        mult = 0
        if (otherPos[1]<self.position[1]):
            mult = 1
        self.dir = m.atan2(otherPos-self.position)+(180*mult)

    def findClosestBody(self):
        distance = 1.0 * 10**100000
        closeID = 0
        selfID = self.objList.index(self.position)
        for id in range(0,len(self.objList)-1):
            if id != selfID:
                dist = self.distance(self.objList[id])
                if dist < distance:
                    distance = dist
                    closeID = id
        return closeID
    
    def accelerate(self,speed=float):
        self.velocity[0] += speed*m.sin(self.dir)
        self.velocity[1] += speed*m.cos(self.dir)

    def applyForce(self, force=float):
        self.accelerate((force/self.mass)*time.deltaTime)

    def distanceTo(self,otherObj=tuple):
        return m.sqrt((otherObj[0]-self.position[0])**2+(otherObj[1]-self.position[1])**2)
    
    def gravity(self,mode=int,strength=float):
        if (mode == 1):
            self.velocity[1] -= strength
        elif (mode == 2):
            id = self.findClosestBody()
            objPos = self.objList[id]
            self.pointAt(objPos)
            self.applyForce(g*(self.mass*objPos[2]/self.distanceTo(objPos)))
        elif (mode == 0):
            pass
        else:
            ValueError

