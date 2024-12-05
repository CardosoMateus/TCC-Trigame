import pygame
import random
import math
from timer import Timer

class Drone:
    def __init__(self, caverna):
        self.display_surf = pygame.display.get_surface()
        self.game_font = pygame.font.Font(None, 30)
        self.caverna = caverna
        self.n_sessions = caverna.n_sessions
        self.curr_session = 0
        self.tentativas = 4
        self.pontos_acc = 0
        self.pontos_tempo = ""
        self.timer = Timer(240_000, True)
        
        self.session_times = []
        self.session_acc = []

        self.pos = (self.caverna.sessions[self.curr_session].x_pos, self.caverna.sessions[self.curr_session].otimo)
        self.next_pos = (self.caverna.sessions[self.curr_session + 1].x_pos, self.caverna.sessions[self.curr_session + 1].otimo)

        self.past_pos = []
        self.try_pos = []
        self.past_pos.append(self.pos)

        self.cateto_ops_m = round(abs(self.pos[1] - self.next_pos[1]), ndigits=2)
        self.cateto_adj = round(self.caverna.sessions[self.curr_session + 1].x_pos - self.pos[0], ndigits=2)
        self.hipotenusa = round(math.dist(self.pos, self.next_pos), ndigits=2)

        self.cateto_ops_m_surf = self.game_font.render("Distância Vertical: " + str(self.cateto_ops_m), True, 'black')
        self.cateto_adj_surf = self.game_font.render("Distância Horizontal: " + str(self.cateto_adj), True, 'black')
        self.hipotenusa_surf = self.game_font.render("Distância ao Ponto Médio: " + str(self.hipotenusa), True, 'black')

        self.tentativas_surf = self.game_font.render("Vidas = " + str(self.tentativas), True, 'black')
        self.tentativas_rect = self.tentativas_surf.get_rect(topleft = (100, 460))

        escolhas = ['sin', 'cos', 'tan']
        self.trig_rel = []
        for _ in range(0, self.n_sessions):
            self.trig_rel.append(random.choice(escolhas))
    
    def draw(self):        
        for pos in self.try_pos:
            if pos[1] < 0: 
                pygame.draw.circle(self.display_surf, 'blue', (pos[0], 0), 5)
                if self.pos[0] < pos[0]: pygame.draw.line(self.display_surf, 'blue', self.pos, (pos[0], 0))

            elif pos[1] > 400: 
                pygame.draw.circle(self.display_surf, 'blue', (pos[0], 400), 5)
                if self.pos[0] < pos[0]: pygame.draw.line(self.display_surf, 'blue', self.pos, (pos[0], 400))

            else: 
                pygame.draw.circle(self.display_surf, 'blue', pos, 5)
                if self.pos[0] < pos[0]: pygame.draw.line(self.display_surf, 'blue', self.pos, pos)

        for i in range(0, self.curr_session + 1):
            pygame.draw.circle(self.display_surf, 'red', self.past_pos[i], 5)
            if i > 0:
                pygame.draw.line(self.display_surf, 'red', self.past_pos[i-1], self.past_pos[i], 2)

        if self.curr_session < self.n_sessions and self.tentativas > 0:
            self.display_surf.blit(self.tentativas_surf, self.tentativas_rect)

            tempo = self.timer.tempo_passado()
            minutos = tempo // 60_000
            segundos = (tempo - (minutos * 60_000)) // 1000
        
            if minutos < 10: minutos_text = '0' + str(minutos)
            else: minutos_text = str(minutos)
        
            if segundos < 10: segundos_text = '0' + str(segundos)
            else: segundos_text = str(segundos)
        
            tempo_texto = minutos_text + ":" + segundos_text

            timer_surf = self.game_font.render(tempo_texto, True, 'black')
            self.display_surf.blit(timer_surf, (100, 500))
            
            if self.trig_rel[self.curr_session] == 'sin':
                self.display_surf.blit(self.cateto_ops_m_surf, (100, 540))
                self.display_surf.blit(self.hipotenusa_surf, (100, 580))
        
            elif self.trig_rel[self.curr_session] == 'cos':
                self.display_surf.blit(self.cateto_adj_surf, (100, 540))
                self.display_surf.blit(self.hipotenusa_surf, (100, 580))
        
            else: 
                self.display_surf.blit(self.cateto_ops_m_surf, (100, 540))
                self.display_surf.blit(self.cateto_adj_surf, (100, 580))
    
    def move(self, angle):
        answer = math.tan(math.radians(angle)) * self.cateto_adj
        pos_answer = self.pos[1] - answer
        
        if self.tentativas > 1:
            if pos_answer < self.caverna.sessions[self.curr_session + 1].h_obstaculo_inf and pos_answer > self.caverna.sessions[self.curr_session + 1].h_obstaculo_sup:
                self.curr_session += 1
                self.pos = (self.caverna.sessions[self.curr_session].x_pos, pos_answer)
                self.past_pos.append(self.pos)
                
                self.session_times.append(self.timer.tempo_passado())
                self.session_acc.append(1 - abs((self.caverna.sessions[self.curr_session].otimo - self.pos[1]) / self.caverna.sessions[self.curr_session].otimo))

                if self.curr_session < self.n_sessions:
                    self.next_pos = (self.caverna.sessions[self.curr_session + 1].x_pos, self.caverna.sessions[self.curr_session + 1].otimo)

                    self.cateto_ops_m = round(abs(self.pos[1] - self.next_pos[1]), ndigits=2)
                    self.cateto_adj = round(self.caverna.sessions[self.curr_session + 1].x_pos - self.pos[0], ndigits=2)
                    self.hipotenusa = round(math.dist(self.pos, self.next_pos), ndigits=2)

                    self.cateto_ops_m_surf = self.game_font.render("Distância Vertical: " + str(self.cateto_ops_m), True, 'black')
                    self.cateto_adj_surf = self.game_font.render("Distância Horizontal: " + str(self.cateto_adj), True, 'black')
                    self.hipotenusa_surf = self.game_font.render("Distância ao Ponto Médio: " + str(self.hipotenusa), True, 'black')

                    self.timer.ativar()

                    return 0
            
                elif self.curr_session == self.n_sessions:
                    self.timer.desativar()
                    tempo = 0

                    for i in self.session_times: tempo += i

                    for j in self.session_acc: self.pontos_acc += j

                    tempo = round(tempo / self.n_sessions)
                    minutos = tempo // 60_000
                    segundos = (tempo - (minutos * 60_000)) // 1000

                    minutos_text = ""
                    segundos_text = ""

                    if minutos < 10: minutos_text = '0' + str(minutos)
                    else: minutos_text = str(minutos)

                    if segundos < 10: segundos_text = '0' + str(segundos)
                    else: segundos_text = str(segundos)

                    self.pontos_tempo = minutos_text + ":" + segundos_text
                    self.pontos_acc = round((self.pontos_acc / (self.n_sessions + (4 - self.tentativas))) * 100, ndigits = 2)

                    return 1

            else:
                self.try_pos.append((self.caverna.sessions[self.curr_session + 1].x_pos, pos_answer))
                self.tentativas -= 1
                self.tentativas_surf = self.game_font.render("Vidas = " + str(self.tentativas), True, 'black')
                self.session_acc.append(0)
                return 0

        else:
            self.tentativas -= 1
            return 2
