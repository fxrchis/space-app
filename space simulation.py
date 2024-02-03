from asyncio.format_helpers import _format_callback_source
import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Simulation")
white = (255,255,255)
yellow = (245, 224, 66)
blue = (49, 83, 176)
beige = (214, 207, 171)
gray = (166, 166, 166)
red = (181, 113, 62)
font = pygame.font.SysFont("comicsans", 16)

class Planets:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    scale = 250 / AU
    timestep = 3600 * 24

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distanceToSun = 0

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x * self.scale + WIDTH / 2
        y = self.y * self.scale + HEIGHT / 2

        if len(self.orbit) > 2:

            newPoints = []
            for point in self.orbit:
                x,y = point
                x = x * self.scale + WIDTH / 2
                y = y * self.scale + HEIGHT / 2
                newPoints.append((x,y))
        
            pygame.draw.lines(win, self.color, False, newPoints, 2)

        pygame.draw.circle(win, self.color, (x,y), self.radius)

        if not self.sun:
            distance_text = font.render(f"{self.name}: {round(self.distanceToSun / 1000)}km", 1, white)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other): # gravitation attraction between sun and object
        other_x, other_y  = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2) #dist between object

        if other.sun:
            self.distanceToSun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x,force_y
    
    def update_pos(self, planets): # velocity of planet
        total_fx = total_fy = 0

        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet) 
            total_fx += fx # forces of x and y
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.timestep
        self.y_vel += total_fy / self.mass * self.timestep

        self.x += self.x_vel * self.timestep
        self.y += self.y_vel * self.timestep
        self.orbit.append((self.x,self.y))

def main():
    run = True
    clock = pygame.time.Clock()
    
    sun = Planets(0, 0, 30, yellow, 1.98892 * 10 ** 30, "Sun")
    sun.sun = True
    
    mercury = Planets(0.387 * Planets.AU, 0, 8, gray, 3.285 * 10 ** 23, "Mercury")
    mercury.y_vel = -47.4 * 1000

    venus = Planets(0.723 * Planets.AU, 0, 14, beige, 4.87 * 10 ** 24, "Venus")
    venus.y_vel = -35.02 * 1000

    mars = Planets(-1.524 * Planets.AU, 0, 12, red, 6.39 * 10 ** 23, "Mars")
    mars.y_vel = 24.077 * 1000

    earth = Planets(-1*Planets.AU, 0, 16, blue, 5.9742 * 10 ** 24, "Earth")
    earth.y_vel = 29.783 * 1000

    planets = [sun, earth, mercury, venus, mars]

    while run:
        clock.tick(60)
        win.fill((0,0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_pos(planets)
            planet.draw(win)

        pygame.display.update()
    pygame.quit()
main()