import pygame
from sys import exit
from random import randint,choice

game_active = False
score = 0
start_time = 0
current_level = 1
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
class GameState():
    def __init__(self):
        self.state = 'level1'
    def clear_obstacles(self):
        obstacle_group.empty() 
    def level1(self):
        global game_active 
        global start_time 
        global score 
        global current_level
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
        
            if  game_active: 
              if event.type == obstacle_timer1:
                 obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
              if score >= 20 :
                   
                    current_level = 1
                    self.clear_obstacles()  
                    self.state = 'trans'
            
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                  game_active = True 
                
                start_time = int(pygame.time.get_ticks()/1000)
       
    def trans(self):
        if game_active:
            global current_level
            screen.fill((0, 0, 0))  # Use a black background for the level complete screen
            level_complete_text = level_complete_font.render(f'Level {current_level} Complete!', True, (255, 255, 255))
            level_complete_rect = level_complete_text.get_rect(center=(400, 200))
            screen.blit(level_complete_text, level_complete_rect)
            pygame.display.update()
            pygame.time.delay(2000)  # Delay for 2 seconds before advancing to the next level
            current_level += 1  # Move to the next level
        else:
            screen.fill((94,129,162))
            screen.blit(player_stand,player_stand_rect)
            score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
            score_message_rect = score_message.get_rect(center = (400,330))
            screen.blit(game_name,game_name_rect)
            if score == 0:
                 screen.blit(game_message,game_message_rect)
            else:
                screen.blit(score_message,score_message_rect)
                current_level=1
               

    def level2(self):
        global game_active 
        global start_time 
        global score 
        global current_level

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if  game_active:
              if event.type == obstacle_timer2:
                 obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
              if score >= 40:
                    current_level = 2
                    self.state = 'win'
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                  game_active = True
                
                start_time = int(pygame.time.get_ticks()/1000)
    def win(self):
        global current_level
        screen.fill((0, 0, 0))  # Use a black background for the level complete screen
        level_complete_text = level_complete_font.render(f'Level {current_level} Complete! YOU WIN !!!', True, (255, 255, 255))
        level_complete_rect = level_complete_text.get_rect(center=(400, 200))
        screen.blit(level_complete_text, level_complete_rect)
        pygame.display.update()
        pygame.time.delay(3000)  # Delay for 2 seconds before advancing to the next level
        current_level += 1  # Move to the next level
        pygame.quit()
        exit()

    
    def state_manager(self):
        global current_level
        global score
        if current_level == 1:
           self. level1()
           if score >=20 :
                self.clear_obstacles()  
                self.trans()
          
                
        
        if current_level == 2:
            self. level2()
            if game_active == False:
                self.trans()
            
            if score >=40:
                self.win()
            
                
            
        
         
def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True
    
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
game_state = GameState() 
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
level_complete_font = pygame.font.Font(None, 50)
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)


player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group() 

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()




#intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner',False,(111,196,169))
game_name_rect = player_stand.get_rect(center = (400,130))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))

#Timer
obstacle_timer1 =pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer1,2000)
obstacle_timer2 =pygame.USEREVENT +2
pygame.time.set_timer(obstacle_timer2,1500)




while True:
    
    game_state.state_manager()
    if game_active: 
               
            screen.blit(sky_surface,(0,0))
            screen.blit(ground_surface,(0,300)) 
            score = display_score()
            player.draw(screen)
            player.update()
            obstacle_group.draw(screen)
            obstacle_group.update()
            game_active = collision_sprite()
    else:
            screen.fill((94,129,162))
            screen.blit(player_stand,player_stand_rect)
            score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
            score_message_rect = score_message.get_rect(center = (400,330))
            screen.blit(game_name,game_name_rect)
            if score == 0: 
                 screen.blit(game_message,game_message_rect)
            else:
                screen.blit(score_message,score_message_rect)
                score=0
               
    pygame.display.update()
    clock.tick(60) 