import pygame

class Button:
    def __init__(self, text, width, heigth, pos):
        self.gui_font = pygame.font.Font(None, 30)
        self.display_surf = pygame.display.get_surface()
        self.pressed = False
        self.elevation = 6
        self.dynamic_elevation = self.elevation
        self.original_y_pos = pos[1]

        self.top_rect = pygame.Rect(pos, (width, heigth))
        self.top_color = '#475F77'

        self.bottom_rect = pygame.Rect(pos, (width, self.elevation))
        self.bottom_color = '#354B5E'

        self.text_surf = self.gui_font.render(text, True, 'white')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    
    def draw(self):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(self.display_surf, self.bottom_color, self.bottom_rect, border_radius = 12)
        pygame.draw.rect(self.display_surf, self.top_color, self.top_rect, border_radius = 12)
        self.display_surf.blit(self.text_surf, self.text_rect)
        return self.check_click()
    
    def check_click(self):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.pressed = False
                    action = True
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'

        return action

class Slider:
    def __init__(self, pos, width, height, initial_value, min, max):
        self.display_surf = pygame.display.get_surface()
        self.pos = pos
        self.size = (width, height)

        self.hovered = False
        self.pressed = False

        self.left_pos = self.pos[0] - (width // 2)
        self.right_pos = self.pos[0] + (width // 2)
        self.top_pos = self.pos[1] - (height // 2)

        offset_pos = (self.left_pos, self.top_pos)

        self.min = min
        self.max = max
        self.initial_value = (self.right_pos - self.left_pos) * initial_value

        self.back_rect = pygame.Rect(offset_pos, (width, height))
        self.back_color = '#809ab0'

        self.button_rect = pygame.Rect((self.left_pos + self.initial_value - 5, self.top_pos), (10, height))
        self.button_color = '#475F77'
    
    def move_button(self):
        mouse_pos = pygame.mouse.get_pos()[0]

        if mouse_pos < self.left_pos:
            mouse_pos = self.left_pos
        
        if mouse_pos > self.right_pos:
            mouse_pos = self.right_pos

        self.button_rect.centerx = mouse_pos
    
    def draw(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.back_rect.collidepoint(mouse_pos):
            self.button_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
        
        else:
            self.button_color = '#475F77'

        if not pygame.mouse.get_pressed()[0]:
            self.pressed = False
        
        if self.button_rect.collidepoint(mouse_pos):
            self.hovered = True
        
        if self.pressed:
            self.move_button()
            self.hovered = True
        
        else:
            self.hovered = False

        pygame.draw.rect(self.display_surf, self.back_color, self.back_rect, border_radius = 12)
        pygame.draw.rect(self.display_surf, self.button_color, self.button_rect, border_radius = 12)
    
    def get_value(self):
        val_range = self.right_pos - self.left_pos
        button_val = self.button_rect.centerx - self.left_pos

        return round((button_val / val_range) * (self.max - self.min) + self.min)
    
    def reset(self):
        self.button_rect.centerx = self.left_pos + self.initial_value
