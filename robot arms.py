# Free Sound: https://pgtd.tistory.com/110
# assignment: meet CEO and talk to him.
# assignment: play sound when bounce up

import pygame
import numpy as np

RED = (255, 0, 0)

FPS = 60   # frames per second

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

# def CirclesOverlap (c1, c2):
#     dist12 = np.sqrt( (c1.x - c2.x)**2 + (c1.y - c2.y)**2 )
#     if dist12 < c1.radius + c2.radius:
#         return True # if overlaps
#     return False

def CirclesOverlap (c1, c2):
    dist12 = np.sqrt( (c1.position[0] - c2.position[0])**2 + (c1.position[1] - c2.position[1])**2 )
    if dist12 < c1.radius + c2.radius:
        return True # if overlaps
    return False

class MyCircle():
    def __init__(self, x, y, vx, vy, radius=40, color=None, sound = None):
        self.radius = radius 
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy 
        self.ax = 0
        self.ay = .1
        self.org_color = color if color is not None else (100, 200, 255)
        self.color = self.org_color
        self.sound = sound
        return
    
    def update(self):
        
        self.x = self.x + self.vx 
        if self.x + self.radius >= WINDOW_WIDTH:
            self.vx = -1. * self.vx 
        if self.x - self.radius < 0:
            self.vx = -1. * self.vx 

        self.y = self.y + self.vy
        self.vy = self.vy + self.ay 
        if self.y < 0:
            self.vy = 0
            self.y = self.radius + 10
        if self.y + self.radius >= WINDOW_HEIGHT:
            self.vy = -1 * self.vy 
            if self.sound is not None:
                # self.sound.play()
                pass
        return
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                           [self.x, self.y], 
                           radius = self.radius, )

    def print(self,):
        print("my class self.number = ", self.number)
        return
# 

def getRegularPolygon(nV, radius=1.):
    angle_step = 360. / nV 
    half_angle = angle_step / 2.

    vertices = []
    for k in range(nV):
        degree = angle_step * k 
        radian = np.deg2rad(degree + half_angle)
        x = radius * np.cos(radian)
        y = radius * np.sin(radian)
        vertices.append( [x, y] )
    #
    print("list:", vertices)

    vertices = np.array(vertices)
    print('np.arr:', vertices)
    return vertices



class myTriangle():
    def __init__(self, radius=50, color=(100,0,0), vel=[5.,0]):
        self.radius = radius
        self.vertices = getRegularPolygon(3, radius=self.radius)

        self.color = color

        self.angle = 0.
        self.angvel = np.random.normal(5., 7)

        self.position = np.array([0.,0]) #
        # self.position = self.vertices.sum(axis=0) # 2d array
        self.vel = np.array(vel)
        self.tick = 0

    def update(self,):
        self.tick += 1
        self.angle += self.angvel
        self.position += self.vel

        if self.position[0] >= WINDOW_WIDTH:
            self.vel[0] = -1. * self.vel[0]

        if self.position[0] < 0:
            self.vel[0] *= -1.

        if self.position[1] >= WINDOW_HEIGHT:
            self.vel[1] *= -1.

        if self.position[1] < 0:
            self.vel[1] *= -1

        # print(self.tick, self.position)

        return

    def draw(self, screen):
        R = Rmat(self.angle)
        points = self.vertices @ R.T + self.position
        pygame.draw.polygon(screen, self.color, points)
#

class myPolygon():
    def __init__(self, nvertices = 3, radius=70, color=(100,0,0), vel=[5.,0]):
        self.radius = radius
        self.nvertices = nvertices
        self.vertices = getRegularPolygon(self.nvertices, radius=self.radius)

        self.color = color
        self.color_org = color 

        self.angle = 0.
        self.angvel = np.random.normal(5., 7)

        self.position = np.array([0.,0]) #
        # self.position = self.vertices.sum(axis=0) # 2d array
        self.vel = np.array(vel)
        self.tick = 0

    def update(self,):
        self.tick += 1
        self.angle += self.angvel
        self.position += self.vel

        if self.position[0] >= WINDOW_WIDTH:
            self.vel[0] = -1. * self.vel[0]

        if self.position[0] < 0:
            self.vel[0] *= -1.

        if self.position[1] >= WINDOW_HEIGHT:
            self.vel[1] *= -1.

        if self.position[1] < 0:
            self.vel[1] *= -1

        # print(self.tick, self.position)

        return

    def draw(self, screen):
        R = Rmat(self.angle)
        points = self.vertices @ R.T + self.position

        pygame.draw.polygon(screen, self.color, points)
#

def update_list(alist):
    for a in alist:
        a.update()
#
def draw_list(alist, screen):
    for a in alist:
        a.draw(screen)
#

def Rmat(degree):
    rad = np.deg2rad(degree) 
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([ [c, -s, 0],
                   [s,  c, 0], [0,0,1]])
    return R

def Tmat(tx, ty):
    Translation = np.array( [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    return Translation
#

def draw(P, H, screen, color=(100, 200, 200)):
    R = H[:2,:2]
    T = H[:2, 2]
    Ptransformed = P @ R.T + T 
    pygame.draw.polygon(screen, color=color, 
                        points=Ptransformed, width=3)
    return
#


def main():
    pygame.init() # initialize the engine

    sound = pygame.mixer.Sound("assets/diyong.mp3")
    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    clock = pygame.time.Clock()

    w = 200
    h = 50
    Wi=10
    Hi=50
    X = np.array([ [0,0], [w, 0], [w, h], [0, h] ])
    GX = np.array([ [0,0], [Wi,0],[Wi,Hi],[0,Hi]])
    GY = np.array([ [0,0], [Hi,0],[Hi,Wi],[0,Wi]])
    position = [WINDOW_WIDTH/2, WINDOW_HEIGHT - 100]
    jointangle1 = 10
    jointangle1_1 = 0
    jointangle2_1 = 0
    jointangle3_1 = 0
    joint_angle_change_1=0
    joint_angle_change_2=0
    joint_angle_change_3=0
    joint_angle_grip=30
    sp_pre=False
    a=5
    tick = 0
    done = False
    while not done:
        tick += 1
        # input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    joint_angle_change_1-=10
                if event.key == pygame.K_RIGHT:
                    joint_angle_change_1+=10
                if event.key == pygame.K_UP:
                    joint_angle_change_2-=10
                if event.key == pygame.K_DOWN:
                    joint_angle_change_2+=10
                if event.key == pygame.K_a:
                    joint_angle_change_3-=10
                if event.key == pygame.K_d:
                    joint_angle_change_3+=10
                if event.key ==pygame.K_SPACE:
                    sp_pre= not sp_pre

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN, pygame.K_a, pygame.K_d, pygame.K_SPACE):
                    joint_angle_change_1=0
                    joint_angle_change_2=0
                    joint_angle_change_3=0
        if sp_pre:
            joint_angle_grip-=a
            if joint_angle_grip==-60 or joint_angle_grip==60:
                a=-a
    #while not done:
     #   tick += 1
        #  input handling
      #  for event in pygame.event.get():
       #     if event.type == pygame.QUIT:
        #        done = True
        # drawing
        screen.fill( (200, 254, 219))

        # base
        pygame.draw.circle(screen, (255,0,0), position, radius=3)
        H0 = Tmat(position[0], position[1]) @ Tmat(0, -h)
        draw(X, H0, screen, (0,0,0)) # base

        # arm 1
        H1 = H0 @ Tmat(w/2, 0)  
        x, y = H1[0,2], H1[1,2] # joint position
        H11 = H1 @ Rmat(-90) @ Tmat(0,-h/2)
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        jointangle1 =  40* np.sin(np.deg2rad(joint_angle_change_1))
        jointangle1_1+=jointangle1
        H12 = H11 @ Tmat(0, h/2) @ Rmat(jointangle1_1) @ Tmat(0, -h/2)    
        draw(X, H12, screen, (200,200,0)) # arm 1, 90 degree

        # arm 2
        H2 = H12 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 2
        x, y = H2[0,2], H2[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        jointangle2 = 40 * np.sin(np.deg2rad(joint_angle_change_2)) #
        jointangle2_1+=jointangle2
        H21 = H2 @ Rmat(jointangle2_1) @ Tmat(0, -h/2)
        draw(X, H21, screen, (0,0, 200))

        H3 = H21 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 3
        x, y = H3[0,2], H3[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        jointangle3 = 40 * np.sin(np.deg2rad(joint_angle_change_3)) #
        jointangle3_1+=jointangle3
        H31 = H3 @ Rmat(jointangle3_1) @ Tmat(0, -h/2)
        draw(X, H31, screen, (0,0, 200))

        G = H31 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 2
        x, y = G[0,2], G[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3)
        G_1 = G @ Rmat(0) @ Tmat(0, -h/2)
        draw(GX,G_1,screen, (0,0,10))

        G1= G_1 @ Tmat(Wi,0) @Tmat(0,Hi) # joint 2
        x, y = G1[0,2], G1[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3)
        G1_1 = G1 @ Rmat(-joint_angle_grip) @ Tmat(0,-Wi/2)
        draw(GY,G1_1,screen, (0,0,10))

        G1= G_1 @ Tmat(Wi,0) @Tmat(0,0) # joint 2
        x, y = G1[0,2], G1[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3)
        G1_1 = G1 @ Rmat(joint_angle_grip) @ Tmat(0,-Wi/2)
        draw(GY,G1_1,screen, (0,0,10))




        pygame.display.flip()
        clock.tick(FPS)
    # end of while
# end of main()

if __name__ == "__main__":
    main()