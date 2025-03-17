import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.Font('assets\Minecraft.ttf', 30)

class Button: #Decleares the button class
    def __init__(self,text,width,height,pos,elevation): #Defnies parameters of the button
        self.pressed = False
        self.run = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y = pos[1]
        
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#848482'
        
        self.bottom_rect = pygame.Rect(pos,(width,elevation))
        self.bottom_color = '#171717'
        
        self.text_surface = font.render(text,False,'#FFFFFF')
        self.text_rect = self.text_surface.get_rect(center = self.top_rect.center)
        self.text_rect.height -= 5
        
    def draw(self): #Defines how the button is displayed on the screen
        self.top_rect.y = self.original_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        
        pygame.draw.rect(screen,self.bottom_color,self.bottom_rect)
        pygame.draw.rect(screen,self.top_color,self.top_rect)
        screen.blit(self.text_surface,self.text_rect)
        self.check_click()
        
    def check_click(self): #Checks if the button has been clicked or not
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos): #If the mouse cursor is over the button
            self.top_color = '#2b2b2b'
            if pygame.mouse.get_pressed()[0]: #If the left mouse button was presed
                self.dynamic_elevation = 0
                self.pressed = True
            else: #After the button is released
                if self.pressed == True:
                    self.dynamic_elevation = self.elevation
                    self.pressed = False
                    self.run = True
        else: #After the mouse cursor stopped hovering over the mouse if the mouse button was clicked but not released over the button
            self.dynamic_elevation = self.elevation
            self.top_color = '#848482'
            self.run = False