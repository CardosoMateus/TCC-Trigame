import pygame, sys, math, datetime, csv
from settings import *
from buttons import Button, Slider
from levels import Caverna
from drone import Drone

class Game:
    def __init__(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.game_logo = pygame.image.load("logo.png").convert_alpha()
        self.game_logo_rect = self.game_logo.get_rect(center = (640, 120))

        # Fontes
        self.title_font = pygame.font.Font(None, 120)
        self.text_font = pygame.font.Font(None, 45)
        self.game_font = pygame.font.Font(None, 30)

        # Textos do menu
        self.texts = {}
        self.game_name_surf = self.title_font.render(GAME_NAME, True, 'black')
        self.game_name_rect = self.game_name_surf.get_rect(center = (640, 120))

        self.vitoria_surf = self.text_font.render('Vitória', True, 'black')
        self.vitoria_rect = self.vitoria_surf.get_rect(center = (640, 430))

        self.derrota_surf = self.text_font.render("Derrota", True, 'black')
        self.derrota_rect = self.derrota_surf.get_rect(center = (640, 430))

        self.ranking_title_surf = self.text_font.render("Histórico", True, 'black')
        self.ranking_title_rect = self.ranking_title_surf.get_rect(center = (640, 120))

        self.data_surf = self.game_font.render('Data', True, 'black')
        self.data_rect = self.data_surf.get_rect(midtop = (340, 150))

        self.pontos_acc_surf = self.game_font.render('Precisão', True, 'black')
        self.pontos_acc_rect = self.pontos_acc_surf.get_rect(midtop = (540, 150))

        self.pontos_tempo_surf = self.game_font.render('Tempo', True, 'black')
        self.pontos_tempo_rect = self.pontos_tempo_surf.get_rect(midtop = (740, 150))

        self.dificuldade_surf = self.game_font.render('Difculdade', True, 'black')
        self.dificuldade_rect = self.dificuldade_surf.get_rect(midtop = (940, 150))

        self.credits_title_surf = self.text_font.render('Créditos', True, 'black')
        self.credits_title_rect = self.credits_title_surf.get_rect(center = (640, 120))

        self.credits_line_1_surf = self.game_font.render('Jogo desenvolvido para o TCC de', True, 'black')
        self.credits_line_1_rect = self.credits_line_1_surf.get_rect(center = (640, 180))

        self.credits_line_2_surf = self.game_font.render('Mateus Rodrigues Marques Cardoso', True, 'black')
        self.credits_line_2_rect = self.credits_line_2_surf.get_rect(center = (640, 220))

        self.credits_line_3_surf = self.game_font.render('Sob orientação de', True, 'black')
        self.credits_line_3_rect = self.credits_line_3_surf.get_rect(center = (640, 260))

        self.credits_line_4_surf = self.game_font.render('Eurico Luiz Prospero Ruivo', True, 'black')
        self.credits_line_4_rect = self.credits_line_4_surf.get_rect(center = (640, 300))

        self.diff_select_surf = self.text_font.render('Selecione a dificuldade', True, 'black')
        self.diff_select_rect = self.diff_select_surf.get_rect(center = (640, 120))

        # Botões
        self.play_button = Button('Jogar', 200, 40, (540, 300))
        self.tutorial_button = Button('Como Jogar', 200, 40, (540, 360))
        self.ranking_button = Button('Histórico', 200, 40, (540, 420))
        self.credits_button = Button('Créditos', 200, 40, (540, 480))
        self.quit_button = Button('Sair', 200, 40, (540, 540))
        self.play_again_button = Button('Jogar Novamente', 200, 40, (320, 620))
        self.save_button = Button('Salvar', 200, 40, (540, 620))

        self.level_facil_button = Button('Iniciante', 200, 40, (540, 240))
        self.level_medio_button = Button('Intermediário', 200, 40, (540, 300))
        self.level_dificil_button = Button('Avançado', 200, 40, (540, 360))
        self.return_main_menu = Button('Voltar', 200, 40, (540, 420))

        self.return_res_button = Button('Voltar ao Menu', 200, 40, (760, 620))
        self.return_rank_button = Button('Voltar', 200, 40, (540, 540))
        self.return_jogo_button = Button('Voltar', 200, 40, (850, 620))
        self.return_tutorial_button = Button('Voltar', 130, 40, (575, 670))

        self.tutorial_prox_button = Button('Próximo', 130, 40, (725, 670))
        self.tutorial_ante_button = Button('Anterior', 130, 40, (425, 670))
        
        self.reposta = Button("Resposta", 200, 40, (850, 560))

        self.angles = Slider((950, 500), 300, 40, 0.5, -89, 89)

        # Dados
        self.menu_state = 'main'
        self.game_state = 'inicio'
        self.tutorial_state = 0
        self.dificuldade = None

        self.result = {'vitoria': False,
                       'data': None,
                       'precisão' : 0,
                       'tempo': 0,
                       'dificuldade': None}
        
        self.images_loaded = False
        self.jogo_salvo = False

    def run(self):
        # Game Loop
        while True:
            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_surf.fill('white')

            match self.menu_state:
                case 'main':
                    #self.display_surf.blit(self.game_name_surf, self.game_name_rect)
                    self.display_surf.blit(self.game_logo, self.game_logo_rect)

                    if self.play_button.draw(): self.menu_state = 'jogo'

                    if self.tutorial_button.draw(): self.menu_state = 'tutorial'

                    if self.ranking_button.draw(): self.menu_state = 'ranking'

                    if self.credits_button.draw(): self.menu_state = 'creditos'

                    if self.quit_button.draw():
                        pygame.quit()
                        sys.exit()
                
                case 'jogo':
                    match self.game_state:
                        case 'inicio':
                            self.dificuldade = None
                            self.display_surf.blit(self.diff_select_surf, self.diff_select_rect)

                            if self.level_facil_button.draw():
                                data = datetime.datetime.now()
                                caverna = Caverna(4, 220, (70, 100), 120)
                                drone = Drone(caverna)
                                self.angles.reset()
                                self.game_state = 'jogando'
                                self.jogo_salvo = False
                                self.dificuldade = 'Fácil'

                            if self.level_medio_button.draw():
                                data = datetime.datetime.now()
                                caverna = Caverna(8, 140, (50, 80), 50)
                                drone = Drone(caverna)
                                self.angles.reset()
                                self.game_state = 'jogando'
                                self.jogo_salvo = False
                                self.dificuldade = 'Médio'

                            if self.level_dificil_button.draw():
                                data = datetime.datetime.now()
                                caverna = Caverna(12, 100, (30, 60), 30)
                                drone = Drone(caverna)
                                self.angles.reset()
                                self.game_state = 'jogando'
                                self.jogo_salvo = False
                                self.dificuldade = 'Difícil'
                            
                            if self.return_main_menu.draw():
                                self.menu_state = 'main'

                        case 'jogando':
                            angle_atual = self.angles.get_value()
                            sen_angle = round(math.sin(math.radians(angle_atual)), ndigits = 2)
                            cos_angle = round(math.cos(math.radians(angle_atual)), ndigits = 2)
                            tan_angle = round(math.tan(math.radians(angle_atual)), ndigits = 2)

                            angle_value_surf = self.game_font.render(str(angle_atual) + ' graus', True, 'black')
                            angle_value_rect = angle_value_surf.get_rect(center = (950, 440))

                            sen_surf = self.game_font.render("sen(" + str(angle_atual) + ") = " + str(sen_angle), True, 'black')
                            sen_rect = sen_surf.get_rect(topleft = (520, 500))

                            cos_surf = self.game_font.render("cos(" + str(angle_atual) + ") = " + str(cos_angle), True, 'black')
                            cos_rect = cos_surf.get_rect(topleft = (520, 540))

                            tan_surf = self.game_font.render("tan(" + str(angle_atual) + ") = " + str(tan_angle), True, 'black')
                            tan_rect = tan_surf.get_rect(topleft = (520, 580))

                            caverna.draw()
                            drone.draw()
                            
                            self.angles.draw()
                            self.display_surf.blit(angle_value_surf, angle_value_rect)
                            self.display_surf.blit(sen_surf, sen_rect)
                            self.display_surf.blit(cos_surf, cos_rect)
                            self.display_surf.blit(tan_surf, tan_rect)

                            if self.reposta.draw():
                                match drone.move(self.angles.get_value()):
                                    case 0: self.angles.reset()

                                    case 1:
                                        self.game_state = 'resultado'
                                        self.result['vitoria'] = True
                                        self.result['data'] = data.strftime("%c")
                                        self.result['precisão'] = drone.pontos_acc
                                        self.result['tempo'] = drone.pontos_tempo
                                        self.result['dificuldade'] = self.dificuldade
                                
                                    case 2:
                                        self.game_state = 'resultado'
                                        self.result['vitoria'] = False
                        
                            if self.return_jogo_button.draw():
                                self.game_state = 'inicio'
                                self.menu_state = 'main'

                        case 'resultado':
                            caverna.draw()
                            drone.draw()

                            if self.play_again_button.draw(): 
                                self.menu_state = 'jogo'
                                self.game_state = 'inicio'
                            
                            if self.return_res_button.draw():
                                self.menu_state = 'main'
                                self.game_state = 'inicio'

                            if self.result['vitoria']:
                                self.display_surf.blit(self.vitoria_surf, self.vitoria_rect)

                                acc_jogo_surf = self.game_font.render("Precisão média: " + str(self.result['precisão']) + " %", True, 'black')
                                acc_jogo_rect = acc_jogo_surf.get_rect(midtop = (640, 480))

                                tempo_jogo_surf = self.game_font.render("Tempo médio: " + str(self.result['tempo']), True, 'black')
                                tempo_jogo_rect = tempo_jogo_surf.get_rect(midtop = (640, 520))

                                self.display_surf.blit(acc_jogo_surf, acc_jogo_rect)
                                self.display_surf.blit(tempo_jogo_surf, tempo_jogo_rect)

                                if self.save_button.draw() and not self.jogo_salvo:
                                    ranking = []
                                    with open('ranking.csv', 'r') as ranking_file:
                                        csvreader = csv.reader(ranking_file, delimiter = ',', lineterminator = '\n')
                                        for row in csvreader:
                                            ranking.append(row)
                                    
                                    ranking.append([self.result['data'], str(self.result['precisão']), self.result['tempo'], self.result['dificuldade']])

                                    with open('ranking.csv', 'w') as ranking_file:
                                        csv.writer(ranking_file, delimiter = ',', lineterminator = '\n').writerows(ranking)

                            else:
                                self.display_surf.blit(self.derrota_surf, self.derrota_rect)
                
                case 'ranking':
                    self.display_surf.blit(self.ranking_title_surf, self.ranking_title_rect)
                    self.display_surf.blit(self.data_surf, self.data_rect)
                    self.display_surf.blit(self.pontos_acc_surf, self.pontos_acc_rect)
                    self.display_surf.blit(self.pontos_tempo_surf, self.pontos_tempo_rect)
                    self.display_surf.blit(self.dificuldade_surf, self.dificuldade_rect)

                    ranking = []
                    with open('ranking.csv', 'r') as ranking_file:
                        csvreader = csv.reader(ranking_file, delimiter = ',', lineterminator = '\n')
                        for row in csvreader:
                            ranking.append(row)

                    rank = 0
                    
                    if len(ranking) <= 10:
                        for line in ranking:
                            y_pos = 190 + (30 * (rank))

                            score_data_surf = self.game_font.render(line[0], True, 'black')
                            score_data_rect = score_data_surf.get_rect(midtop = (340, y_pos))

                            score_acc_surf = self.game_font.render(line[1] + " %", True, 'black')
                            score_acc_rect = score_acc_surf.get_rect(midtop = (540, y_pos))

                            score_tempo_surf = self.game_font.render(line[2], True, 'black')
                            score_tempo_rect = score_tempo_surf.get_rect(midtop = (740, y_pos))

                            score_diff_surf = self.game_font.render(line[3], True, 'black')
                            score_diff_rect = score_diff_surf.get_rect(midtop = (940, y_pos))

                            self.display_surf.blit(score_data_surf, score_data_rect)
                            self.display_surf.blit(score_acc_surf, score_acc_rect)
                            self.display_surf.blit(score_tempo_surf, score_tempo_rect)
                            self.display_surf.blit(score_diff_surf, score_diff_rect)
                        
                            rank += 1
                    
                    elif len(ranking) > 10:
                        for i in range(-10, 0):
                            y_pos = 190 + (30 * (rank))

                            score_data_surf = self.game_font.render(ranking[i][0], True, 'black')
                            score_data_rect = score_data_surf.get_rect(midtop = (340, y_pos))

                            score_acc_surf = self.game_font.render(ranking[i][1], True, 'black')
                            score_acc_rect = score_acc_surf.get_rect(midtop = (540, y_pos))

                            score_tempo_surf = self.game_font.render(ranking[i][2], True, 'black')
                            score_tempo_rect = score_tempo_surf.get_rect(midtop = (740, y_pos))

                            score_diff_surf = self.game_font.render(ranking[i][3], True, 'black')
                            score_diff_rect = score_diff_surf.get_rect(midtop = (940, y_pos))

                            self.display_surf.blit(score_data_surf, score_data_rect)
                            self.display_surf.blit(score_acc_surf, score_acc_rect)
                            self.display_surf.blit(score_tempo_surf, score_tempo_rect)
                            self.display_surf.blit(score_diff_surf, score_diff_rect)
                        
                            rank += 1

                    if self.return_rank_button.draw(): self.menu_state = 'main'
                
                case 'creditos':
                    self.display_surf.blit(self.credits_title_surf, self.credits_title_rect)
                    self.display_surf.blit(self.credits_line_1_surf, self.credits_line_1_rect)
                    self.display_surf.blit(self.credits_line_2_surf, self.credits_line_2_rect)
                    self.display_surf.blit(self.credits_line_3_surf, self.credits_line_3_rect)
                    self.display_surf.blit(self.credits_line_4_surf, self.credits_line_4_rect)

                    if self.return_rank_button.draw(): self.menu_state = 'main'

                case 'tutorial':
                    if not self.images_loaded:
                        img_pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        tutorial_img = []

                        for i in range(1, 7):
                            temp_surf = pygame.image.load("Tutorial/" + str(i) + ".png").convert_alpha()
                            temp_rect = temp_surf.get_rect(center = img_pos)
                            tutorial_img.append((temp_surf, temp_rect))

                        self.images_loaded = True
                    
                    self.display_surf.blit(tutorial_img[self.tutorial_state][0], tutorial_img[self.tutorial_state][1])

                    if self.return_tutorial_button.draw(): 
                        self.tutorial_state = 0
                        self.menu_state = 'main'

                    if self.tutorial_state == 0:
                        if self.tutorial_prox_button.draw():
                            self.tutorial_state += 1
                    
                    elif self.tutorial_state > 0 and self.tutorial_state < 5:
                        if self.tutorial_prox_button.draw():
                            self.tutorial_state += 1
                        
                        if self.tutorial_ante_button.draw():
                            self.tutorial_state -= 1
                    
                    elif self.tutorial_state == 5:
                        if self.tutorial_ante_button.draw():
                            self.tutorial_state -= 1
                            
            pygame.display.update()
            self.clock.tick(60)

g = Game()
g.run()