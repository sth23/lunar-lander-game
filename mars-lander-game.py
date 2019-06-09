"""
Final Project: Mars Lander Game
Author: Sean
Credit: Tutorials
Assignment: Create an old-school Mars Lander game
"""

from ggame import App, RectangleAsset, PolygonAsset, CircleAsset, ImageAsset, TextAsset, Frame, Sprite, LineStyle, Color
import math
import random

# Colors & lines
red = Color(0xff0000, 1.0)
orange = Color(0xffa500, 1.0)
yellow = Color(0xffff00, 1.0)
green = Color(0x00ff00, 1.0)
blue = Color(0x0000ff, 1.0)
purple = Color(0x800080, 1.0)
black = Color(0x000000, 1.0)
white = Color(0xffffff, 1.0)
gray = Color(0x888888, 0.5)
noline = LineStyle(0, black)
whiteline = LineStyle(1, white)

class Explosion(Sprite):
    asset = ImageAsset("explosion1.png", Frame(0,0,128,128), 10, 'horizontal')
    
    def __init__(self, position):
        super().__init__(Explosion.asset, position)
        self.fxcenter = self.fycenter = 0.5
        self.countup = 0
        self.countdown = 10
        
    def step(self):
        # Manage explosion animation
        if self.countup < 10:
            self.setImage(self.countup%10)
            self.countup += 1
        else:
            self.setImage(self.countdown%10)
            self.countdown -= 1
            if self.countdown == 0:
                self.destroy()

class Turrain(Sprite):
    def __init__(self, asset, position):
        super().__init__(asset, position)
        
class LandingArea(Sprite):
    def __init__(self, asset, position):
        super().__init__(asset, position)
        
class FuelBar(Sprite):
    def __init__(self, fuel):
        self.fuelbar = RectangleAsset(fuel, 23, noline, red)
        super().__init__(self.fuelbar, (12, 10))
        FuelLevel(fuel)
        
class FuelLevel(Sprite):
    def __init__(self, fuel):
        self.fuellevel = TextAsset("Fuel: " + str(fuel))
        super().__init__(self.fuellevel, (10, 10))
        
class Lander(Sprite):
    ship = PolygonAsset([(0,15), (7.5,0), (15,15), (7.5,7.5)], noline, black)
    
    def __init__(self, position):
        self.radius = 7
        super().__init__(Lander.ship, position, CircleAsset(self.radius))
        self.vx = 0
        self.vy = 0
        self.gravity = 0.01
        self.wind = 0
        self.thrust = 0.05
        self.vr = 0.1
        self.rotation = 0
        self.paused = True
        self.fxcenter = self.fycenter = 0.5
        self.speed = 0
        self.speedlimit = 1
        self.landed = False
        self.crashed = False
        self.thrusting = False
        self.landingarea = False
        self.fuellimit = 100
        self.fuel = self.fuellimit
        
        MarsLanderGame.listenKeyEvent("keydown", "up arrow", self.thrustOn)
        MarsLanderGame.listenKeyEvent("keyup", "up arrow", self.thrustOff)
        MarsLanderGame.listenKeyEvent("keydown", "right arrow", self.rotateRight)
        MarsLanderGame.listenKeyEvent("keydown", "left arrow", self.rotateLeft)
        MarsLanderGame.listenKeyEvent("keydown", "space", self.togglePause)
        
    def thrustOn(self, event):
        self.thrusting = True
        if self.fuel > 0:
            self.fuel -= 1
        
    def thrustOff(self, event):
        self.thrusting = False
        
    def rotateRight(self, event):
        if self.paused == False:
            self.rotation -= self.vr
        
    def rotateLeft(self, event):
        if self.paused == False:
            self.rotation += self.vr
        
    def togglePause(self, event):
        self.paused = not self.paused
        
    def step(self):
        if self.paused == False and self.landed == False and self.crashed == False:
            if self.thrusting and self.fuel > 0:
                self.vx += -self.thrust * math.sin(self.rotation)
                self.vy += -self.thrust * math.cos(self.rotation)
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravity
            self.vx += self.wind * 0.001
            self.speed = (self.vx ** 2 + self.vy ** 2) ** 0.5
        
class MarsLanderGame(App):
    def __init__(self):
        super().__init__()
        
        print('Press "space" to pause / unpause game.  Press "right arrow" to rotate lander clockwise.  Press "left arrow" to rotate lander counterclockwise.  Press "up arrow" to activate lander\'s thrusters.')
        print('Aim for the red landing area.')
        print('')
        
        self.lander = Lander((self.width / 2, 30))
        
        self.landingarea = 0
        self.turrainheight = 0
        self.turrainwidth = 30
        self.createTurrain()
        self.turrain = []
        self.landingarea = []
        self.deltaheight = 0
        
        MarsLanderGame.listenKeyEvent("keydown", "enter", self.playAgain)
        
    def playAgain(self, event):
        for lander in self.getSpritesbyClass(Lander):
            lander.paused = True
            lander.landed = False
            lander.crashed = False
            if lander.landingarea == True:
                self.resetLander(lander)
                [turrain.destroy() for turrain in self.getSpritesbyClass(Turrain)]
                [landingarea.destroy() for landingarea in self.getSpritesbyClass(LandingArea)]
                self.createTurrain()
                lander.landingarea = False
            else:
                self.resetLander(lander)

    def resetLander(self, lander):
        lander.x = self.width / 2
        lander.y = 30
        lander.rotation = 0
        lander.vx = 0
        lander.vy = 0
        lander.fuel = lander.fuellimit
        
    def createTurrain(self):
        self.turrainheight = random.randint(self.height * 3 // 4, self.height - 20)
        self.landingarea = random.randint(2, self.width // self.turrainwidth - 2)
        for x in range(0, self.width // self.turrainwidth + 1):
            self.deltaheight = random.randint(-30,30)
            while self.deltaheight == 0:
                self.deltaheight = random.randint(-30,30)
            self.turrainheight = self.turrainheight + self.deltaheight
            if self.turrainheight > self.height - 10:
                self.turrainheight -= 50
            elif self.turrainheight < 50:
                self.turrainheight += 50
            
            if self.landingarea != x:
                Turrain(RectangleAsset(self.turrainwidth, self.height * 2, noline, black), (x * self.turrainwidth, self.turrainheight))
            else:
                LandingArea(RectangleAsset(self.turrainwidth, self.height * 2, noline, red), (x * self.turrainwidth, self.turrainheight))
                
        self.lander.wind = random.randint(-5,5)
        self.windstrength = ["Very Strong West Wind", "Strong West Wind", "Moderate West Wind", "Light to Moderate West Wind", "Light West Wind", "No Wind", "Light East Wind", "Light to Moderate East Wind", "Moderate East Wind", "Strong East Wind", "Very Strong East Wind"]
        print(self.windstrength[self.lander.wind + 5])
        print("")
        print('Press "Space" to start game')
        print("")
        
    def crash(self, lander):
        Explosion((lander.x, lander.y))
        lander.x = -100
        lander.y = -100
        lander.crashed = True
        print('You crashed')
        print('Press "Enter" to play again')
        print("")
        
    def miss(self, lander):
        lander.landed = True
        lander.rotation = 0
        print('You missed the landing zone')
        print('Press "Enter" to play again')
        print("")
        
    def step(self):
        for lander in self.getSpritesbyClass(Lander):
            if lander.landed == False and lander.crashed == False:
                [fuelbar.destroy() for fuelbar in self.getSpritesbyClass(FuelBar)]
                [fuellevel.destroy() for fuellevel in self.getSpritesbyClass(FuelLevel)]
                FuelBar(lander.fuel)
                lander.step()
                self.turrain = lander.collidingWithSprites(Turrain)
                self.landingarea = lander.collidingWithSprites(LandingArea)
                if self.turrain:
                    if lander.rotation > 1 or lander.rotation < -1 or lander.speed > lander.speedlimit:
                        self.crash(lander)
                    elif lander.x - lander.radius < self.turrain[0].x or lander.x + lander.radius > self.turrain[0].x + self.turrainwidth:
                        self.crash(lander)
                    else:
                        self.miss(lander)
                elif self.landingarea:
                    if lander.rotation > 1 or lander.rotation < -1 or lander.speed > lander.speedlimit:
                        self.crash(lander)
                    elif lander.x - lander.radius < self.landingarea[0].x or lander.x + lander.radius > self.landingarea[0].x + self.turrainwidth:
                        self.crash(lander)
                    else:
                        lander.landed = True
                        lander.landingarea = True
                        lander.rotation = 0
                        #lander.speedlimit -= 0.05
                        print('You landed successfully!  Congratulations!')
                        print('Press "Enter" to play again')
                        print("")
                elif lander.x < 10 or lander.x > self.width - 10:
                        self.miss(lander)
                        lander.x = -100
                        lander.y = -100
        self.turrain = []
        self.landingarea = []
                    
        [explosion.step() for explosion in self.getSpritesbyClass(Explosion)]
            
        
myapp = MarsLanderGame()
myapp.run()
