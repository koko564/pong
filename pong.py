import pygame
import sys
from pygame.locals import *

pygame.init()

global score
score=0
fps=300
v=1

bfs=25
bf=pygame.font.Font('freesansbold.ttf', bfs)

width=800
height=600
border=20
ps=100
pos=40

black=(0,0,0)
white=(255,255,255)

screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('PONG')
Display=pygame.display.set_mode((width,height))

def arena():
	screen.fill((0,0,0))
	pygame.draw.rect(screen, white, ((0,0),(width,height)), border*2)
	pygame.draw.line(screen, white, (int(width/2),0),(int(width/2),height), (int(border/4)))

def Paddle(paddle):
	if paddle.bottom>height-border:
		paddle.bottom=height-border
	elif paddle.top<border:
		paddle.top=border

	pygame.draw.rect(screen, white, paddle)

def Ball(ball):
	pygame.draw.rect(screen, white, ball)

def moveball(ball, balldx, balldy):
	ball.x+=balldx
	ball.y+=balldy
	return ball

def check(ball, balldx, balldy):
	if ball.top==border or ball.bottom==(height-border):
		balldy=balldy*-1
	if ball.left==border or ball.right==(width-border):
		balldx=balldx*-1
	return balldx, balldy

def checkballhit(ball, paddle1, paddle2, balldx):
	if balldx==-1 and paddle1.right==ball.left and paddle1.top<ball.top and paddle1.bottom>ball.bottom:
		return -1
	elif balldx==1 and paddle2.left==ball.right and paddle2.top<ball.top and paddle2.bottom>ball.bottom:
		return -1
	else:
		return 1

def compPaddle(ball, balldx, paddle2):
	if balldx==-1:
		if paddle2.centery<(height/2):
			paddle2.y+=1
		elif paddle2.centery>(height/2):
			paddle2.y-=1
	elif balldx==1:
		if paddle2.centery<ball.centery:
			paddle2.y+=1
		else:
			paddle2.y-=1
	return paddle2

def Score(paddle1, ball, score, balldx):
	if ball.left==border: 
		return 0
	elif balldx==-1 and paddle1.right==ball.left and paddle1.top<ball.top and paddle1.bottom>ball.bottom:
		score+=1
		return score
	elif ball.right==width-border:
		score+=5
		return score
	else: 
		return score

def display(score):
	resS=bf.render('Score = %s' %(score), True, white)
	resR=resS.get_rect()
	resR.topleft=(width-200, 50)
	Display.blit(resS, resR)

def main():
	fpsclk=pygame.time.Clock()

	bx=width/2-border/2
	by=height/2-border/2
	p1pos=(height-ps)/2
	p2pos=(height-ps)/2
	
	score=0
	
	balldx=-1
	balldy=-1

	paddle1=pygame.Rect(pos, p1pos, border, ps)
	paddle2=pygame.Rect(width-pos-border, p2pos, border, ps)
	ball=pygame.Rect(bx, by, border, border)
	
	arena()
	Paddle(paddle1)
	Paddle(paddle2)
	Ball(ball)

	pygame.mouse.set_visible(0)

	while True:
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			elif event.type==MOUSEMOTION:
				mousex, mousey=event.pos
				paddle1.y=mousey

		arena()
		Paddle(paddle1)
		Paddle(paddle2)
		Ball(ball)

		ball=moveball(ball, balldx, balldy)
		balldx, balldy=check(ball, balldx, balldy)
		score=Score(paddle1, ball, score, balldx)
		balldx=balldx*checkballhit(ball, paddle1, paddle2, balldx)
		paddle2=compPaddle(ball, balldx, paddle2)
		

		display(score)
		
		pygame.display.update()
		fpsclk.tick(fps)


if __name__ == '__main__':
	main()