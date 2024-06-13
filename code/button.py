import pygame

#button class
class Button():
	def __init__(self, x, y, font, text, text_col):

		self.text_col = text_col
		self.text_surf = font.render(text, True, self.text_col)
		self.x, self.y = x, y
		self.text_rect = self.text_surf.get_frect(center = (self.x,self.y))
		self.clicked = False
		self.border_rect = self.text_rect
		self.border_rect_scale_limit = (self.text_rect.width+20, self.text_rect.height+20)

	def draw(self, surface):
		active = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.text_rect.collidepoint(pos):
			if self.border_rect.size < self.border_rect_scale_limit:
				self.border_rect = self.border_rect.inflate(2,2)
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				active = True
		else:
			if self.border_rect.size > self.text_surf.get_frect(midbottom = (self.x,self.y)).size:
				self.border_rect = self.border_rect.inflate(-2,-2)

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.text_surf, self.text_rect)
		pygame.draw.rect(surface, self.text_col, self.border_rect.inflate(20,30), 5, 10)

		return active