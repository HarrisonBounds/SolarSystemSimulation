import random
import pygame
import math

pygame.init() #Intialize the pygame module

WIDTH, HEIGHT = 2100, 1100 #Size of our window in pixels : MY WINDOW SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #gives us a "pygame surface" aka a window

pygame.display.set_caption("Planet Simulation in out Solar System") #Title of our window

WHITE = (255, 255, 255) #RGB
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
CRIMSON = (220, 20, 60)
BROWN = (165, 42,42)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    #Constants
    AU = 149.6e6 * 1000 #One "astronomical unit" distance from Earth to the sun IN METERS
    G = 6.67e-11 #gravitational constant (force of attraction between two bodies)
    SCALE = 100 / AU #1AU = 100 pixels : Draws objects to scale in our window
    TIMESTEP = 3600 * 12 #Lets us look at the simulation on a quicker scale : one day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass #in kilograms

        self.orbit = [] #array of the points the plantes travel along to draw the orbit path
        self.sun = False #Tells us if the item is the sun (we dont want the sun to move)
        self.distance_to_sun = 0

        #Set velocity
        self.x_velocity = 0
        self.y_velocity = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2 #Offset our planets so they are based around the center of our window
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                #Calculates the x and y position of the orbits to scale
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2

                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2) #This will draw a line in between the points

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2)) #Draws the text in the center of the planet

    #This method calculates the force of attraction between the current object and another object
    def attraction(self, other): #other is the other planet
        other_x, other_y = other.x, other.y
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2) 

        if other.sun: #if the other object is the sun, we just calculate the distance to the sun
            self.distance_to_sun = distance

        #Calculate the force of attraction
        force = (self.G * self.mass * other.mass) / (distance ** 2) #This is the "straight line" force between the objects
        #We need to get the x and y component of this force
        theta = math.atan2(distance_y, distance_x) #atan2 takes the tan of y/x and gives us the angle
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    #This method updates the position of each planet based on its attraction to all the other planets
    #Calculate the velocity of the planets and move them by that amount accordingly
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet: #we dont want to calculate the force of attraction between a planet and itself
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        #Now calculate velocity
        self.x_velocity += total_fx / self.mass * self.TIMESTEP #Use F=ma --> a=F/m : we sum the forces up to move in the correct orbit
        self.y_velocity += total_fy / self.mass * self.TIMESTEP

        #Calculate update the position of the planets
        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP

        self.orbit.append((self.x, self.y))

#loop to keep our program running
def main():
    run = True
    #set a frame rate : if we didn't have this, the program would run at the speed of this computer (make it look normal)
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * pow(10, 30)) #Initializing the sun object
    sun.sun = True #Tells us that this is the sun

    #Set each of our planets
    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10 ** 23)
    #have a starting y velocity so our planets can move in a a correct orbit : the planets would only move on the x plane if we didnt set this
    #Note : if you have a postive distance from the sun, you need to have a negative y_velocity
    #This is so the planets will move in the correct direction : orbital velocity
    mercury.y_velocity = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10 ** 24)
    venus.y_velocity = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10 ** 24)
    earth.y_velocity = 29.783 * 1000 #km/s * 1000 = m/s

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10 ** 23)
    mars.y_velocity = 24.077 * 1000

    jupiter = Planet(5.203 * Planet.AU, 0, 25, CRIMSON, 1.9 * 10 ** 27)
    jupiter.y_velocity = -13.1 * 1000

    saturn = Planet(9.539 * Planet.AU, 0, 23, BROWN, 5.69 * 10 ** 26)
    saturn.y_velocity = -9.7 * 1000

    uranus = Planet(19.18 * Planet.AU, 0, 18, LIGHT_BLUE, 8.68 * 10 ** 25)
    uranus.y_velocity = -6.8 * 1000

    neptune = Planet(30.06 * Planet.AU, 0, 20, DARK_BLUE, 1.02 * 10 ** 26)
    neptune.y_velocity = -5.4 * 1000
   

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    stars = []
    num_of_stars = 100
    for i in range(num_of_stars):
        stars.append([random.randint(0, WIDTH), random.randint(0, HEIGHT)])
    
    

    #Runs our loop until we click the x button (top right corner)
    while run:
        clock.tick(60) #Times we update per second (max of 60 times per second)
        WIN.fill((0, 0, 0)) #we have to redraw our background to update the window : we would see multiple planets if we didnt do this
        for i in range(100):
            pygame.draw.circle(WIN, WHITE, (stars[i][0], stars[i][1]), 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)


        pygame.display.update()

    pygame.quit()

main()
