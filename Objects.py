import math
import pygame

class Object:
    def __init__(self, win, coords, center, color = "black", vel = (0,0), angular_vel = 0):
        """Wall(window, x-position, y-position, width, height)"""
        self.win = win
        self.vertex_coordinates = coords # list of tuple coordinates
        self.color = color
        self.centerMass = center # tuple
        self.vel = vel # velocity of all points (tuple)
        self.mass = 1
        self.angular_velocity = angular_vel
        # self.moment_of_inertia = self.determine_moment()
        self.elasticity = 0.9
        self.max_radius = self.find_farthest_distance()
        self.WIN_WIDTH, self.WIN_HEIGHT = self.win.get_size()

    def draw(self):
        pygame.draw.polygon(self.win, self.color, self.get_vertex_coordinates())    

    def get_vertex_coordinates(self):
        return self.vertex_coordinates
            
    def auto_move(self):
        # changes all coordinates in self.vertex_coordinates
        new_x = self.centerMass[0] + self.vel[0]
        new_y = self.centerMass[1] + self.vel[1]
        self.centerMass = (new_x, new_y)
        for i in range(len(self.vertex_coordinates)):
            new_x = self.vertex_coordinates[i][0] + self.vel[0]
            new_y = self.vertex_coordinates[i][0] + self.vel[1]
            self.vertex_coordinates[i] = (new_x, new_y)
        
    def auto_rotate(self):
        # rotates the object around the center of mass
        for i in range(len(self.vertex_coordinates)):
            x, y = self.vertex_coordinates[i]
            x -= self.centerMass[0]
            y = self.centerMass[1] - y
            mag = math.sqrt(x**2 + y**2)
            dir = math.atan2(y,x)
            newx = mag*math.cos(dir + self.angular_velocity) + self.centerMass[0]
            newy = self.centerMass[1] - mag*math.sin(dir + self.angular_velocity)
            self.vertex_coordinates[i] = (newx,newy)

    #def bounce(self):
        # changes the position and velocity after a bounce
        # checks to see if the bounce passes through any additional objects
        
    def wall_bounce(self):
        """Bounces objects off of walls assuming self.max_radius
            as the radius of the hitbox"""
        cx, cy = self.centerMass
        vx, vy = self.vel
        if cx - self.max_radius < 0: # checks if the LEFT edge is outside of the window
            #reduces the speed and reverses the $x-component:
            vx *= -self.elasticity
            vy *= self.elasticity
            for i in range(len(self.vertex_coordinates)):
                x, y = self.vertex_coordinates[i]
                dx = x + 2*(self.max_radius - cx) # moves x away from the wall linearly
                dy = y
                self.vertex_coordinates[i] = (dx,dy) # changes the coordinates of all points
            cx = cx + 2*(self.max_radius - cx) # reflects the center of mass across the wall
        if cx + self.max_radius > self.WIN_WIDTH: # checks the RIGHT edge
            vx *= -self.elasticity
            vy *= self.elasticity
            for i in range(len(self.vertex_coordinates)):
                x, y = self.vertex_coordinates[i]
                dx = x - 2 * (cx+ self.max_radius -self.WIN_WIDTH)
                dy = y
                self.vertex_coordinates[i] = (dx,dy)
            cx = cx - 2 * (cx+ self.max_radius -self.WIN_WIDTH)
        if cy - self.max_radius < 0:
            vy *= -self.elasticity
            vx *= self.elasticity
            for i in range(len(self.vertex_coordinates)):
                x, y = self.vertex_coordinates[i]
                dx = x
                dy = y + 2*(self.max_radius - cy)
                self.vertex_coordinates[i] = (dx,dy)
            cy = cy + 2*(self.max_radius - cy)
        if cy + self.max_radius > self.WIN_HEIGHT:
            vy *= -self.elasticity
            vx *= self.elasticity
            for i in range(len(self.vertex_coordinates)):
                x, y = self.vertex_coordinates[i]
                dx = x
                dy = y - 2 * (cy+ self.max_radius -self.WIN_HEIGHT)
                self.vertex_coordinates[i] = (dx,dy)
            cy = cy - 2 * (cy+ self.max_radius -self.WIN_HEIGHT)
        self.vel = (vx, vy)
        self.centerMass = (cx, cy)
        
    def find_farthest_distance(self):
        """This function finds the furthest distance from centerMass to a vertex point"""
        cx, cy = self.centerMass
        max_distance = 0
        for x,y in self.vertex_coordinates:
            distance = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            if distance > max_distance:
                max_distance = distance
        return max_distance 
    
class Rocket(Object):
    def __init__(self, win, center, angle):
        coords = self.determine_coordinates(center)
        super().__init__(win, coords, center, color = "red", angular_vel = angle  - math.pi/2)
        self.auto_rotate()
        self.angular_velocity = 0
        self.direction = angle # Measured in radians

    def determine_coordinates(self, center):
        topcoord = (center[0],center[1] - 10)
        leftcoord = (center[0] - 5,center[1] + 5)
        rightcoord = (center[0] + 5,center[1] + 5)
        return [topcoord, rightcoord, leftcoord]
    
    def move(self,spacebar):
        
        vx,vy = self.vel

        if spacebar:
            addspeed = 0.1

            vx += addspeed*math.cos(self.direction)
            vy -= addspeed*math.sin(self.direction)
        
        self.vel = (vx,vy)
        
        newx = self.centerMass[0] + self.vel[0]
        newy = self.centerMass[1] + self.vel[1]

        self.centerMass = (newx,newy)

        for i in range(len(self.vertex_coordinates)):
            x, y = self.vertex_coordinates[i]
            dx = x + self.vel[0] #new x value
            dy = y + self.vel[1] #new y value
            self.vertex_coordinates[i] = (dx,dy)
        
        self.wall_bounce()

    def rotate(self,whichbutton):
        # This function rotates the character 'a' radians
        self.change_angularV(whichbutton)

        self.direction += self.angular_velocity
        while self.direction >= math.pi:
            self.direction -= math.tau
        while self.direction < -math.pi:
            self.direction += math.tau
        
        for i in range(len(self.vertex_coordinates)):
            x, y = self.vertex_coordinates[i]
            x -= self.centerMass[0]
            y = self.centerMass[1] - y
            mag = math.sqrt(x**2 + y**2)
            dir = math.atan2(y,x)
            newx = mag*math.cos(dir + self.angular_velocity) + self.centerMass[0]
            newy = self.centerMass[1] - mag*math.sin(dir + self.angular_velocity)
            self.vertex_coordinates[i] = (newx,newy)

    def change_angularV(self,whichbutton):
        button_impulse = math.tau/800 # measured in degrees per second squared
        friction = math.tau/800 # measured in degrees per second squared
        max_angularV = math.tau/60 # measured in degrees per second


        if whichbutton == 2:
            friction = button_impulse

        if whichbutton == 1:
            self.angular_velocity += button_impulse
            if self.angular_velocity >= max_angularV:
                self.angular_velocity = max_angularV
        elif whichbutton == -1:
            self.angular_velocity -= button_impulse
            if self.angular_velocity <= -max_angularV:
                self.angular_velocity = -max_angularV
        elif self.angular_velocity < -friction:
            self.angular_velocity += friction
        elif self.angular_velocity > friction:
            self.angular_velocity -= friction
        else:
            self.angular_velocity = 0


