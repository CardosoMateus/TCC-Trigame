from pygame.time import get_ticks

class Timer:
    def __init__(self, duration, autoativar = False):
        self.duration = duration
        self.inicio = 0
        self.ativo = False
        if autoativar: self.ativar()
    
    def ativar(self):
        self.ativo = True
        self.inicio = get_ticks()

    def desativar(self):
        self.ativo = False
        self.inicio = 0
    
    def tempo_passado(self):
        return get_ticks() - self.inicio

    def update(self):
        if self.ativo:
            tempo_atual = get_ticks()
            if tempo_atual - self.inicio >= self.duration:
                self.desativar()
                return True
            return False
        return False
