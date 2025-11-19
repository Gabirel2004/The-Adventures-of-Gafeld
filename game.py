import pgzrun
import random
from pygame import Rect

# --- CONFIGURAÇÕES DA TELA---
WIDTH = 800
HEIGHT = 600
TITLE = "Galfald: Caça à Lasanha"
# Variáveis Globais
game_state = "menu"
is_music = True 
is_sound = True
btn_start = Rect(WIDTH / 2 - 100, 300, 200, 50) # Ajustei a posição para centralizar melhor
btn_sound = Rect(WIDTH / 2 - 100, 370, 200, 50) # Ajustei a posição
btn_exit = Rect(WIDTH / 2 - 100, 440, 200, 50)  # Ajustei a posição
# --- CLASSES DOS PERSONAGENS ---
class Player(Actor):
    def __init__(self, pos):
        super().__init__("gato0", pos)  # Nome da imagem do ator
        self.idle_front_image = ["gato0","gato6"]
        self.idle_back_image = ["gato00","gato6"]
        self.walk_front_images = ["gato1","gato2"]
        self.walk_back_images = ["gato3","gato4"]
        self.is_direction = True # True = frente, False = costas
        self.frame_index = 0
        self.animation_speed = 0.1 # Velocidade da animação andado 
        self.animation_idle_speed = 0.01 # Velocidade da animação parado

        self.speed = 3 # Velocidade de movimento

    def get_idle_image(self, i):
        return self.idle_image[i]

    def update(self):
        is_moving = False
        if keyboard.left:
            self.x -= self.speed
            is_moving = True
            self.is_direction = False
        if keyboard.right:
            self.x += self.speed
            is_moving = True
            self.is_direction = True
        if keyboard.up:
            self.y -= self.speed
            is_moving = True
        if keyboard.down:
            self.y += self.speed
            is_moving = True
        self.check_bounds()
        self.animate(is_moving)    

    def check_bounds(self):
        if self.left < 0: self.left = 0
        if self.right > WIDTH: self.right = WIDTH    
        if self.top < 0: self.top = 0    
        if self.bottom > HEIGHT: self.bottom = HEIGHT  

    def animate(self, is_moving):
        if is_moving:
            self.frame_index += self.animation_speed
            if self.is_direction:
                if self.frame_index >= len(self.walk_front_images):
                    self.frame_index = 0
                self.image = self.walk_front_images[int(self.frame_index)]
            else:
                if self.frame_index >= len(self.walk_back_images):
                    self.frame_index = 0
                self.image = self.walk_back_images[int(self.frame_index)]
        else: # Se não estiver movendo, usa a imagem estática idle
            self.frame_index += self.animation_idle_speed
            if self.is_direction:
                if self.frame_index > len(self.idle_front_image):
                    self.frame_index = 0
                self.image = self.idle_front_image[int(self.frame_index)]
            else:
                if self.frame_index > len(self.idle_back_image):
                    self.frame_index = 0
                self.image = self.idle_back_image[int(self.frame_index)]          
# --- CLASSE DO INIMIGO ---
class Enemy(Actor):
    def __init__(self, pos):
        super().__init__("homem0",pos)
        self.idle_images = ["homem-3","homem-4"] 
        self.walk_front_images = ["homem0","homem01"] # Imagens de caminhada para frente
        self.walk_back_images = ["homem00","homem02"] # Imagens de caminhada para trás
        self.frame_idle_index = 0
        self.frame_index = 0
        self.animation_speed = 0.1 # Velocidade da animação
        self.animation_idle_speed = 0.05 # Velocidade da animação parado
        self.speed = 1 # Velocidade de movimento
        self.is_waiting = False       # Indica se o inimigo esta esperando
        self.wait_time = 120          # Tempo de espera em frames (60 frames = 1 segundo em 60 FPS)
        self.wait_counter = 0
        self.is_moving = False
        self.is_direction = True # True = direita, False = esquerda
        self.patrol_start = pos[0] - 100    # Inicio da patrulha
        self.patrol_end = pos[0] + 100      # Fim da patrulha

    def update(self):     
        if self.is_waiting: # Está esperando 
            self.wait_counter -= 1
            self.is_moving = False # Garante que a animacao idle esteja ativa
            self.frame_index = 0 # Zera o indice para começar a animacao idle          
            if self.wait_counter <= 0:
                self.is_waiting = False
                self.is_moving = True # Retoma o movimento na direcao ja invertida      
        elif self.is_direction: # Indo para a direita/frente
            if self.x < self.patrol_end:
                self.x += self.speed
                self.is_moving = True
            else:
                self.is_direction = False 
                self.is_moving = False  
                self.is_waiting = True    
                self.wait_counter = self.wait_time            
        else: # Indo para a esquerda/costas
            if self.x > self.patrol_start:
                self.x -= self.speed
                self.is_moving = True
            else:
                self.is_direction = True  
                self.is_moving = False   
                self.is_waiting = True    
                self.wait_counter = self.wait_time
        self.check_bounds()
        self.animate()

    def check_bounds(self):
        if self.left <= 0: self.left = 0; self.is_direction = True
        if self.right > WIDTH: self.right = WIDTH; self.is_direction = False    

    def animate(self):    
        if self.is_moving:
            self.frame_index += self.animation_speed
            if self.is_direction:
                if self.frame_index > len(self.walk_front_images):
                    self.frame_index = 0
                self.image = self.walk_front_images[int(self.frame_index)]
            else:
                if self.frame_index > len(self.walk_back_images):
                    self.frame_index = 0
                self.image = self.walk_back_images[int(self.frame_index)]
        else: # Se não estiver movendo, usa a imagem estática idle
            self.frame_idle_index += self.animation_idle_speed
            if self.frame_idle_index > len(self.idle_images):
                self.frame_idle_index = 0
            self.image = self.idle_images[int(self.frame_idle_index)]
# --- FUNÇÕES PRINCIPAIS DO JOGO ---
def draw():
    screen.clear() 
    if game_state == "menu":
        screen.fill("black") # Fundo preto
        start_music()
        screen.draw.text("The Adventures of Gafeld", center=(WIDTH / 2, 150), fontsize=60, color="orange")
        screen.draw.filled_rect(btn_start, "blue")# Desenhar Botão JOGAR
        screen.draw.text("Play", center=btn_start.center, fontsize=30)
        screen.draw.filled_rect(btn_sound, "blue")  # Desenhar Botão SOM
        msg_som = "SOUND: ON" if not is_sound else "SOUND: OFF" # Traduzido
        screen.draw.text(msg_som, center=btn_sound.center, fontsize=30)
        screen.draw.filled_rect(btn_exit, "red")   # Desenhar Botão SAIR
        screen.draw.text("Quit", center=btn_exit.center, fontsize=30)
    elif game_state == "game":
        screen.blit("floresta", (0,0)) # Descomente se tiver um cenário
        player.draw()
        for enemy in enemies:
            enemy.draw()
        goal.draw()
    elif game_state == "game_over":
        screen.fill("red")
        screen.draw.text("GAME OVER", center=(WIDTH / 2, HEIGHT / 2 - 50), fontsize=60, color="white")
        screen.draw.text("Press SPACE to return to Menu", center=(WIDTH / 2, HEIGHT / 2 + 50), fontsize=40, color="white")
        stop_game()
    elif game_state == "victory":
        screen.fill("blue")
        screen.draw.text("YOU WIN!", center=(WIDTH / 2, HEIGHT / 2 - 50), fontsize=60, color="white")
        screen.draw.text("Press SPACE to return to Menu", center=(WIDTH / 2, HEIGHT / 2 + 50), fontsize=40, color="white")
        stop_game()

def start_music():
    if is_music:
        music.play("music_trilha")
        music.set_volume(0.3)

def stop_game():
    music.stop()

def reset_game_elements():
    """Reseta a posição do player, inimigos e objetivo para um novo jogo."""
    global player, enemies, goal, is_sound
    player.pos = (WIDTH // 2, 0)
    is_sound = True
    enemies.clear()
    enemy_generate(4) # Primeira leva de inimigos
    enemy_generate(1.5) # Segunda leva de inimigos
    goal.pos = (WIDTH / 2, 560)

def update():
    global game_state, player, enemies, goal, is_sound

    if game_state == "game":
        player.update()
        for enemy in enemies:
            enemy.update()
            if player.colliderect(enemy):
                game_state = "game_over"    
        if player.colliderect(goal):
            game_state = "victory"
    elif game_state == "game_over":
        if is_sound : sounds.game_over.play(); is_sound = False
        if keyboard.space:
            game_state = "menu" # Muda o estado do jogo para menu
            reset_game_elements() # Reseta os elementos do jogo
    elif game_state == "victory":
        if is_sound : sounds.gaifelddddddd.play(); is_sound = False 
        if keyboard.space:
            game_state = "menu" # Muda o estado do jogo para menu
            reset_game_elements() # Reseta os elementos do jogo

def on_mouse_down(pos):
    global game_state, is_sound     

    if game_state == "menu":
        if btn_start.collidepoint(pos):
            game_state = "game"
            reset_game_elements() # Reseta os elementos do jogo ao iniciar um novo jogo   
        elif btn_sound.collidepoint(pos):
            is_music = not is_music # Inverte o estado do som
        elif btn_exit.collidepoint(pos):
            quit()

def enemy_generate(pos_factor):
    for i in range(4):
        x = random.randint(50, WIDTH - 50)
        enemy = Enemy((x, HEIGHT / pos_factor))
        enemies.append(enemy)
# --- INICIALIZAÇÃO DOS OBJETOS DO JOGO ---
player = Player((WIDTH // 2, 0))
enemies = []
enemy_generate(4) 
enemy_generate(1.5)
goal = Actor("lasanha", (WIDTH / 2, 560))
pgzrun.go()