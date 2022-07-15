import pygame
import math
import random
import time
import colorspy as colors
from queue import PriorityQueue, Queue, LifoQueue

WIDTH=600
BIAS=128
pygame.init()
WIN=pygame.display.set_mode((WIDTH,WIDTH+BIAS))
pygame.display.set_caption("Path Finding Algorithm")

RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
WHITE=(255,255,255)
BLACK=(0,0,0)
PURPLE=(128,0,128)
ORANGE=(255,165,0)
GREY=(128,128,128)
TURQUOISE=(64,224,208)

def display_instructions(win,width):
	instrunctions=[ "• To generate random barriers press M or Press R for recursive maze",
					"• First place the Start Node",
					"• Then Place the End Node",
					"• Barriers can be placed by left click and removed by right click",
					"• Press (1) for A* (2) for Dijkstra (3) for BFS (4) for DFS ",
					"• Press C to clear"]

	font_size=16
	instruct_surface = pygame.Surface((width,8*font_size))
	instruct_surface.fill((230,230,250))
	font = pygame.font.SysFont('georgia', font_size)
	inst_count=len(instrunctions)
	for i in range(inst_count):
		inst=font.render(instrunctions[i],True,(128,0,0))
		pos=i*font_size
		instruct_surface.blit(inst,(0,pos+5))

	pygame.draw.rect(instruct_surface,ORANGE,(10,BIAS - font_size-5,10,10))
	instruct_surface.blit(font.render("Start node",True,(220,20,60)),(30,BIAS - font_size-10))

	pygame.draw.rect(instruct_surface,TURQUOISE,(210,BIAS - font_size-5,10,10))	#(25,25,112)
	instruct_surface.blit(font.render("End node",True,(25,25,112)),(230,BIAS - font_size-10))

	pygame.draw.rect(instruct_surface,BLACK,(410,BIAS - font_size-5,10,10))
	instruct_surface.blit(font.render("Barrier/Wall",True,(255,69,0)),(430,BIAS - font_size-10))

	WIN.blit(instruct_surface,(0,0))
	pygame.display.update(pygame.Rect(0,0,width,BIAS))


class Node:
	def __init__(self,row,col,width,total_rows):
		self.row=row
		self.col=col
		self.x=row*width
		self.y=(col*width)+BIAS
		self.color=WHITE
		self.neighbours=[]
		self.width=width
		self.total_rows=total_rows

	def get_pos(self):
		return self.row,self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color=WHITE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_start(self):
		self.color = ORANGE

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self,win):
		pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

	def update_neighbours(self,grid):
		self.neighbours=[]
		if self.row > 0 and not grid[self.row-1][self.col].is_barrier() :	#UP
			self.neighbours.append(grid[self.row-1][self.col])
		
		if self.col > 0 and not grid[self.row][self.col-1].is_barrier() :	#LEFT
			self.neighbours.append(grid[self.row][self.col-1])

		if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier() :	#DOWN
			self.neighbours.append(grid[self.row+1][self.col])
		
		if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier() :	#RIGHT
			self.neighbours.append(grid[self.row][self.col+1])

	def __lt__(self,other):
		pass


# we used manhatton distances for hurestic
def h(p1,p2):
	x1,y1 = p1
	x2,y2 = p2
	return abs(x1-x2) + abs(y1-y2)

def Astar_algorithm(draw,grid,start,end):
	count=0
	open_set=PriorityQueue()
	open_set.put((0,count,start))
	came_from={}
	g_score={node:float('inf') for row in grid for node in row}
	g_score[start] = 0
	f_score={node:float('inf') for row in grid for node in row}
	f_score[start] = h(start.get_pos(),end.get_pos())
	open_set_hash = {start}
	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current=open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			current.make_end()
			reconstruct_path(came_from,end,draw)
			start.make_start()
			return True

		for neighbour in current.neighbours:
			temp_g_score = g_score[current]+1

			if temp_g_score < g_score[neighbour]:
				came_from[neighbour] = current
				g_score[neighbour] = temp_g_score
				f_score[neighbour] = temp_g_score + h(neighbour.get_pos(),end.get_pos())
				if neighbour not in open_set_hash:
					count+=1
					open_set.put((f_score[neighbour],count,neighbour))
					open_set_hash.add(neighbour)
					neighbour.make_open()

		draw()

		if current!=start:
			current.make_closed()

	return False

def dijkstra_algo(draw,grid,start,end):
	pq=PriorityQueue()
	came_from={}
	dist={node:float('inf') for row in grid for node in row}
	dist[start]=0
	pq.put((0,start))

	while not pq.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygam.quit()


		d,curr=pq.get()

		if curr == end:
			curr.make_end()
			reconstruct_path(came_from,end,draw)
			start.make_start()
			return True

		for neighbour in curr.neighbours:
			temp_dist=dist[curr]+1
			if temp_dist<dist[neighbour]:
				dist[neighbour] = temp_dist
				came_from[neighbour]=curr
				pq.put((dist[neighbour],neighbour))
				neighbour.make_open()

		draw()
		if curr!=start:
			curr.make_closed()


def BFS_algo(draw,grid,start,end):
	q=Queue()
	dist={node:float('inf') for row in grid for node in row}
	dist[start]=0
	came_from={}
	q.put(start)
	while not q.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygam.quit()


		curr=q.get()

		if curr == end:
			curr.make_end()
			reconstruct_path(came_from,end,draw)
			start.make_start()
			return True

		for neighbour in curr.neighbours:
			temp_dist=dist[curr]+1
			if temp_dist<dist[neighbour]:
				dist[neighbour] = temp_dist
				came_from[neighbour]=curr
				q.put(neighbour)
				neighbour.make_open()

		draw()
		if curr!=start:
			curr.make_closed()


def DFS_algo(draw,grid,start,end):
	stack=LifoQueue()

	came_from={}
	visited=set()

	stack.put(start)
	
	while not stack.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygam.quit()


		curr=stack.get()
		visited.add(curr)

		if curr == end:
			curr.make_end()
			reconstruct_path(came_from,end,draw)
			start.make_start()
			return True

		for neighbour in curr.neighbours:
			if neighbour not in visited:
				came_from[neighbour]=curr
				stack.put(neighbour)
				neighbour.make_open()

		draw()

		if curr!=start:
			curr.make_closed()

	return False



def reconstruct_path(came_from,current,draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def random_maze(win,grid,width):
	for row in grid:
		for node in row:
			if random.random() < 0.25:
				node.color=BLACK
				node.draw(win)
	pygame.display.update(pygame.Rect(0,BIAS,width,width))


# 1 -> horizontal
# 2 -> vertical
def recursive_maze(grid,istart,iend,jstart,jend):
	width = jend - jstart
	height = iend - istart

	if width < 2 or height < 2:
		return

	if height>width:
		orientation = 1
	elif width > height:
		orientation = 2
	else:
		orientation = random.randint(1,2)

	if orientation==1:
		# print("s=",istart+1,"e=",iend-1)
		i = random.randint(istart+1,iend-1)
		
		for j in range(jstart,jend+1):
			grid[i][j].color = BLACK

		gap = random.randint(jstart,jend)
		# hole=[i,gap]
		grid[i][gap].color=WHITE
		if gap==jend:
			grid[i][gap-1].color=WHITE
		else:
			grid[i][gap+1].color=WHITE
		pygame.display.update(pygame.Rect(0,BIAS,WIDTH,WIDTH))
		recursive_maze(grid,istart,i-1,jstart,jend)
		recursive_maze(grid,i+1,iend,jstart,jend)
	else:
		# print("s=",jstart+1,"e=",jend-1)
		j = random.randint(jstart+1,jend-1)
		
		for i in range(istart,iend+1):
			grid[i][j].color = BLACK

		gap = random.randint(istart,iend)
		grid[gap][j].color=WHITE
		if gap==iend:
			grid[gap-1][j].color=WHITE
		else:
			grid[gap+1][j].color=WHITE
		pygame.display.update(pygame.Rect(0,BIAS,WIDTH,WIDTH))
		recursive_maze(grid,istart,iend,jstart,j-1)
		recursive_maze(grid,istart,iend,j+1,jend)

def make_grid(rows,width):
	grid=[]
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			grid[i].append(Node(i,j,gap,rows))

	return grid

def draw_grid(win,rows,width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win,GREY,(0,i*gap+BIAS),(width,i*gap+BIAS))
		for j in range(rows):
			pygame.draw.line(win,GREY,(j*gap,0+BIAS),(j*gap,width+BIAS))

def draw(win,grid,rows,width):
	win.fill(WHITE)
	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win,rows,width)
	pygame.display.update(pygame.Rect(0,BIAS,width,width))

def get_clicked_pos(pos,rows,width):
	gap = width // rows
	y,x = pos
	row = y // gap
	col = (x-BIAS) // gap
	# print(row," ",col)
	return row,col

def main(win,width):
	ROWS = 50
	grid = make_grid(ROWS,width)

	start = None
	end = None

	run = True
	started = False

	r_maze=True
	# display_instructions(win,width)
	while run:
		display_instructions(win,width)
		draw(win,grid,ROWS,width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if started:
				continue

			if pygame.mouse.get_pressed()[0]:
				r_maze=False
				pos=pygame.mouse.get_pos()
				row,col = get_clicked_pos(pos,ROWS,width)
				if row<0 or col<0:
					continue
				node = grid[row][col]
				if not start and node!=end:
					start=node
					start.make_start()
				elif not end and node!=start:
					end = node
					end.make_end()
				elif node!=start and node != end:
					node.make_barrier()
			elif pygame.mouse.get_pressed()[2]:
				pos=pygame.mouse.get_pos()
				row,col=get_clicked_pos(pos,ROWS,width)
				node=grid[row][col]
				node.reset()
				if node == start:
					start=None
				elif node == end:
					end=None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1 and not started:
					for row in grid:
						for node in row:
							node.update_neighbours(grid)

					Astar_algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)

				if event.key == pygame.K_2 and not started:
					for row in grid:
						for node in row:
							node.update_neighbours(grid)
					dijkstra_algo(lambda: draw(win,grid,ROWS,width),grid,start,end)

				if event.key == pygame.K_3 and not started:
					for row in grid:
						for node in row:
							node.update_neighbours(grid)
					BFS_algo(lambda: draw(win,grid,ROWS,width),grid,start,end)

				if event.key == pygame.K_4 and not started:
					for row in grid:
						for node in row:
							node.update_neighbours(grid)
					DFS_algo(lambda: draw(win,grid,ROWS,width),grid,start,end)

				if event.key == pygame.K_m and r_maze:
					r_maze=False
					random_maze(win,grid,width)

				if event.key == pygame.K_r and r_maze:
					r_maze=False
					for i in range(ROWS):
						grid[i][0].color=BLACK
						grid[0][i].color=BLACK
						grid[i][ROWS-1].color=BLACK
						grid[ROWS-1][i].color=BLACK
					pygame.display.update(pygame.Rect(0,BIAS,width,width))
					recursive_maze(grid,1,ROWS-2,1,ROWS-2)

				if event.key == pygame.K_c:
					start=None
					end=None
					started=False
					r_maze=True
					grid = make_grid(ROWS,width)
			

	pygame.quit()



if __name__=="__main__":
	main(WIN,WIDTH)