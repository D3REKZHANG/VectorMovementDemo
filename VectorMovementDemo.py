import pygame,sys,math,random
from pygame.locals import *

pygame.init()
pygame.font.init()

class Ball(object):

	def __init__(self):
		self.x, self.y = WIDTH/2, HEIGHT/2
		self.radius = 10 
		self.vx, self.vy = 0,0
		self.dest_x, self.dest_y = WIDTH/2, HEIGHT/2
		self.prev_x,self.prev_y = WIDTH/2, HEIGHT/2

		self.dist = 0

	def follow(self):

		global SPEED

		self.dest_x, self.dest_y = pygame.mouse.get_pos()

		rise = self.dest_y - self.y
		run = self.dest_x - self.x
		length = math.sqrt(rise**2 + run**2)

		rise/=length
		run/=length

		self.vx = run*SPEED
		self.vy = rise*SPEED
			
	def update(self):

		global SPEED

		self.x += self.vx
		self.y += self.vy

		dist = math.sqrt((self.prev_x - self.x)**2 + (self.prev_y - self.y)**2)

		if(dist+self.dist>=DIST):
			self.vx, self.vy = 0,0
			self.prev_x,self.prev_y = self.x,self.y
			self.dist = 0

		# Wall bounce
		if self.x <= 0 or self.x >= WIDTH-self.radius:
			self.vx *= -1
			self.prev_x = self.x
			self.prev_y = self.y
			self.dist += dist
		if self.y <= 0 or self.y >= HEIGHT-self.radius:
			self.vy *= -1
			self.prev_x = self.x
			self.prev_y = self.y
			self.dist += dist

		if((int(SPEED) > 1 and int(SPEED) < 25) or (int(SPEED) == 1 and SPEED_CHANGE > 0) or (int(SPEED) == 25 and SPEED_CHANGE < 0)):
			SPEED += SPEED_CHANGE

	def draw(self):
		pygame.draw.circle(window, (255,255,255), (int(self.x),int(self.y)), self.radius)

class Guideline(object):
	def __init__(self, ball, dist):
		self.ball = ball
		self.dist = dist
		self.end_x,self.end_y = 0,0

	def update(self):
		global DIST
		
		mx,my = pygame.mouse.get_pos()

		rise = self.ball.y - my
		run = self.ball.x - mx
		ball_mouse_dist = math.sqrt(rise**2 + run**2)

		rem_dist = self.dist-ball_mouse_dist
		ratio = ball_mouse_dist/rem_dist
			
		self.end_y = my - rise/ratio
		self.end_x = mx - run/ratio

		if((DIST > 30 and DIST < 350) or (DIST == 30 and DIST_CHANGE > 0) or (DIST == 350 and DIST_CHANGE < 0)):
			DIST += DIST_CHANGE

		self.dist = DIST

	def get_slope(self):
		mx,my = pygame.mouse.get_pos()

		rise = self.ball.y - my
		run = self.ball.x - mx

		if run == 0:
			return -99

		return -rise/run

	def draw(self):
		global RANGECIRCLE
		if self.ball.vx == 0 and self.ball.vy == 0:
			pygame.draw.line(window, (0,255,255), (self.ball.prev_x,self.ball.prev_y),(self.end_x,self.end_y),1)
			
			# Reflection
			rise = self.end_y - self.ball.y
			run = self.end_x - self.ball.x
			length = math.sqrt(rise**2 + run**2)

			if self.end_x > 800:
				off_screen_run = run - (800-self.ball.x)
				ratio = run/off_screen_run
				off_screen_length = length/ratio 
				height = math.sqrt(off_screen_length**2-off_screen_run**2)
				if(self.end_y > self.ball.y):
					height = -height
				pygame.draw.line(window, (0,255,255),(800,self.end_y+height), (800-off_screen_run,self.end_y),1)
			if self.end_x < 0:
				off_screen_run = run + self.ball.x
				ratio = run/off_screen_run
				off_screen_length = length/ratio 
				height = math.sqrt(off_screen_length**2-off_screen_run**2)
				if(self.end_y > self.ball.y):
					height = -height
				pygame.draw.line(window, (0,255,255),(0,self.end_y+height), (-off_screen_run,self.end_y),1)

			if self.end_y > 600:
				off_screen_rise = rise - (600-self.ball.y)
				ratio = rise/off_screen_rise
				off_screen_length = length/ratio 
				width = math.sqrt(off_screen_length**2-off_screen_rise**2)
				if(self.end_x > self.ball.x):
					width = -width
				pygame.draw.line(window, (0,255,255),(self.end_x+width,600), (self.end_x,600-off_screen_rise),1)

			if self.end_y < 0:
				off_screen_rise = rise + self.ball.y
				ratio = rise/off_screen_rise
				off_screen_length = length/ratio 
				width = math.sqrt(off_screen_length**2-off_screen_rise**2)
				if(self.end_x > self.ball.x):
					width = -width
				pygame.draw.line(window, (0,255,255),(self.end_x+width,0), (self.end_x,-off_screen_rise),1)

			if RANGECIRCLE:
				pygame.draw.circle(window, (0,255,255), (int(self.ball.prev_x),int(self.ball.prev_y)),self.dist,1)

if __name__ == "__main__":
	WIDTH, HEIGHT = 800,600

	window = pygame.display.set_mode((WIDTH,HEIGHT),pygame.DOUBLEBUF,32)
	pygame.display.set_caption("Vector Movement Demo")
	
	clock = pygame.time.Clock()

	DIST = 200
	DIST_CHANGE = 0
	SPEED = 10
	SPEED_CHANGE = 0

	STATE = 'intro'

	GRID = False
	DOTS = False
	RANGECIRCLE = True

	b = Ball()
	g = Guideline(b,DIST)

	courier20 = pygame.font.SysFont('courier new', 20)

while(1):

	if STATE == "intro":

		window.fill((0,0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				STATE = "main"

		text = [
			"Vector Movement Demo",
			"",
			"Up Down Arrow Keys controls range",
			"Left Right Arrow Keys controls speed",
			"",
			"Press any key to continue"
		]

		for x in range(0,len(text)):
			window.blit(courier20.render(text[x],False,(255,255,255)), (20,20+x*20))


	elif STATE == "main":
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if b.vx == 0 and b.vy == 0:
					b.follow()
			if event.type == pygame.KEYDOWN:
				if event.key == K_UP:
					DIST_CHANGE = 1
				elif event.key == K_DOWN:
					DIST_CHANGE = -1
				if event.key == K_LEFT:
					SPEED_CHANGE = -0.2
				elif event.key == K_RIGHT:
					SPEED_CHANGE = 0.2
				if event.key == K_g:
					GRID = not GRID
				if event.key == K_d:
					DOTS = not DOTS
				if event.key == K_SPACE:
					RANGECIRCLE = not RANGECIRCLE
			if event.type == pygame.KEYUP:
				if event.key == K_UP or event.key == K_DOWN:
					DIST_CHANGE = 0
				if event.key == K_LEFT or event.key == K_RIGHT:
					SPEED_CHANGE = 0

		window.fill((0,0,0))

		# Update 
		b.update()
		g.update()
		# Draw 
		b.draw()
		g.draw()
		
		# Dots
		if DOTS:
			for x in range(9):
				for y in range(7):
					pygame.draw.circle(window, (255,255,255), (x*100,y*100),3)

		if GRID:
			for x in range(8):
				pygame.draw.line(window, (255,255,255), (x*100,0),(x*100,600))
			for y in range(6):
				pygame.draw.line(window, (255,255,255), (0,y*100),(800,y*100))

		text = [
			"Range: {}".format(DIST),
			"Speed: {}".format(int(SPEED)),
			"Slope: {:.2f}".format(g.get_slope()),
			"Ball  Position: ({},{})".format(int(b.x),int(b.y)),
			"Mouse Position: ({},{})".format(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
		]

		# Backdrop
		s = pygame.Surface((320,120))
		s.set_alpha(200)
		s.fill((0,0,0))
		window.blit(s,(10,10))

		# Drawing Text
		for x in range(0,len(text)):
			window.blit(courier20.render(text[x],False,(255,255,255)), (20,20+x*20))

		window.blit(courier20.render("D to toggle dots",False,(255,255,255)),(20,520))
		window.blit(courier20.render("G to toggle grid",False,(255,255,255)),(20,540))
		window.blit(courier20.render("SPACE for range",False,(255,255,255)),(20,560))

		

	pygame.display.update()
	clock.tick(60)
	


