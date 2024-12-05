from settings import *
import pygame
from random import randrange

class Session:
    def __init__(self, index, prev_pos, first, size, obstacles):
        self.size = size
        self.index = index
        self.piso_caverna = 400
        self.teto_caverna = 0
        self.obstacle_interval = randrange(obstacles[0], obstacles[1])
        self.faixa_inferior = self.piso_caverna - self.obstacle_interval
        self.faixa_superior = self.teto_caverna + self.obstacle_interval

        self.otimo = randrange(self.faixa_superior, self.faixa_inferior)
        self.h_obstaculo_inf = self.otimo + int((self.obstacle_interval / 2))
        self.h_obstaculo_sup = self.otimo - int((self.obstacle_interval / 2))

        self.h_piso = randrange(self.h_obstaculo_inf, self.piso_caverna)
        self.h_teto = randrange(self.teto_caverna, self.h_obstaculo_sup)
        
        if first:
            self.x_pos = prev_pos
        else:
            self.x_pos = prev_pos + self.size + randrange(-25, 25)

class Caverna:
    def __init__(self, n_sessions, size, obstacles, pos_ini):
        self.display_surf = pygame.display.get_surface()
        self.game_state = 'jogo'
        self.n_sessions = n_sessions
        self.sessions = self.gen_sessions(size, obstacles, pos_ini)

        while self.sessions[-1].x_pos - self.sessions[0].x_pos > 1200:
            self.sessions = self.gen_sessions(size, obstacles, pos_ini)

    def print_sessions(self):
        for i in self.sessions:
            print("Atributos de " + str(i))
            print("Altura do teto: " + str(i.h_teto))
            print("Altura do obstáculo superior: " + str(i.h_obstaculo_sup))
            print("Altura viável: " + str(i.h_viavel))
            print("Altura do obstáculo inferior: " + str(i.h_obstaculo_inf))
            print("Altura do piso: " + str(i.h_piso))
            print("Posição Horizontal do início da Seção: " + str(i.w_session))
            print("")

    def gen_sessions(self, size, obstacles, pos_ini):
        lista = []
        curr_session = 0
        while curr_session <= self.n_sessions:
            if curr_session == 0:
                new_session = Session(curr_session, pos_ini, True, size, obstacles)
            else:
                new_session = Session(curr_session, lista[curr_session-1].x_pos, False, size, obstacles)
            
            lista.append(new_session)
            curr_session += 1
        
        return lista

    def draw(self):
        pygame.draw.line(self.display_surf, 'black', (0, 400), (1280, 400))
        for i in range(0, len(self.sessions) - 1):
            pygame.draw.line(self.display_surf,
                             'black',
                             (self.sessions[i].x_pos, self.sessions[i].h_teto),
                             (self.sessions[i+1].x_pos, self.sessions[i+1].h_teto))
            
            pygame.draw.line(self.display_surf,
                             'black',
                             (self.sessions[i].x_pos, self.sessions[i].h_piso),
                             (self.sessions[i+1].x_pos, self.sessions[i+1].h_piso))
        
        for i in self.sessions:
            pygame.draw.line(self.display_surf,
                             'black',
                             (i.x_pos, i.h_obstaculo_sup),
                             (i.x_pos, i.h_teto))
            
            pygame.draw.line(self.display_surf,
                             'black',
                             (i.x_pos, i.h_obstaculo_inf),
                             (i.x_pos, i.h_piso))
