import pygame
import random
import os
pygame.mixer.init()
pygame.init()

#colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

#game title
screen_width  = 900
screen_height = 600
gamewindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Saanp")
pygame.display.update()



#game specific variables

font = pygame.font.SysFont(None, 50)
clock = pygame.time.Clock()
def textscreen(text , color , x ,y ):
    screen_text = font.render(text, True , color)
    gamewindow.blit(screen_text, [x,y])
def plot_snake(gamewindow , black ,snk_list, Snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gamewindow, black, [x, y, Snake_size, Snake_size])
def home():
    exit_game = False
    pygame.mixer.music.load("assets\intro.mp3")
    pygame.mixer.music.play()
    while not exit_game:
        gamewindow.fill((233,210,229))
        textscreen("Saanp" ,black ,370,250)
        textscreen("Press Spacebar to play" , black , 240 , 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("assets\music.mp3")
                    pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()
        clock.tick(60)


#game loop

def gameloop():
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = f.read()
    exit_game = False
    game_over = False
    Snake_x = 45
    Snake_y = 55
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    Snake_size = 30
    food_x = random.randint(0, screen_width/2)
    food_y = random.randint(0, screen_height/2)
    fps = 50
    Score = 0
    snk_list = []
    snk_length = 1
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gamewindow.fill(white)
            textscreen("Game over!!Press Enter to restart. ",red , 200, 200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        home()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y=0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y=0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x=0
                    if event.key == pygame.K_DOWN:
                        velocity_y=init_velocity
                        velocity_x=0
                    if event.key == pygame.K_q:
                        Score+=10
            Snake_x=Snake_x+velocity_x
            Snake_y=Snake_y+velocity_y

            if abs(food_x-Snake_x)<11 and abs(food_y - Snake_y)<11 :
                Score=Score+10
                food_x = random.randint(0, screen_width/1.5)
                food_y = random.randint(0, screen_height/1.5)
                snk_length+=5
                if Score>int(highscore):
                    highscore= Score

            gamewindow.fill(white)
            textscreen("Score :" + str(Score)+"HighScore :" + str(highscore), red, 5, 5)
            pygame.draw.rect(gamewindow, red, [food_x, food_y, Snake_size, Snake_size])

            head=[]
            head.append(Snake_x)
            head.append(Snake_y)
            snk_list.append(head)
            if len(snk_list) > snk_length:
                del snk_list[0]
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load("assets\exit.mp3")
                pygame.mixer.music.play()
            if Snake_x <0 or Snake_x>screen_width or Snake_y<0 or Snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load("assets\exit.mp3")
                pygame.mixer.music.play()
            plot_snake(gamewindow, black, snk_list, Snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
home()