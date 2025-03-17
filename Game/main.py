import pygame, sys, random, csv #Imports modules that the program utilizes
from button import Button #Imports the Button class from the button.py file 

# Initialization
pygame.init() #Initializes the pygame module
pygame.display.set_caption('Pong') #Sets the window caption to say "Pong"
pygame.mixer.pre_init(44100,-16,1, 1024) #Initializes the sound output of pygame
screen_width = 1280 #Initializes the window size
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
light_grey = (200,200,200) #Initializes the light grey color
clock = pygame.time.Clock() #Initializes pygame's clock
font = pygame.font.Font('assets\Minecraft.ttf', 30) #Initializes the main font used in the game
player_score = 0 #Initializes the two variables used to display the score in the game
opponent_score = 0

# Buttons + Text, sets the fonts used and sets up the buttons
main_menu_font = pygame.font.Font('assets\Minecraft.ttf', 50).render('Welcome to Pong',False,'#FFFFFF')
mode_font = pygame.font.Font('assets\Minecraft.ttf', 50).render('Choose your mode',False,'#FFFFFF')
difficulty_font = pygame.font.Font('assets\Minecraft.ttf', 50).render('Choose your difficulty',False,'#FFFFFF')
play_button = Button('PLAY',200,40,(540,220),6)
options_button = Button('DIFFICULTY',200,40,(540,340),6)
quit_button = Button('QUIT',200,40,(540,460),6)
back_button = Button('BACK',200,40,(540,580),6)
single_player_button = Button('SINGLE PLAYER',300,40,(490,220),6)
multiplayer_button = Button('MULTIPLAYER',300,40,(490,340),6)
simulation_button = Button('SIMULATION',300,40,(490,460),6)
easy_button = Button('EASY',200,40,(540,220),6)
medium_button = Button('NORMAL',200,40,(540,340),6)
hard_button = Button('HARD',200,40,(540,460),6)

# Rects, initializes the rectangles used in the game
ball = pygame.Rect(screen_width / 2 - 7.5, screen_height / 2 - 7.5, 15, 15)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 50, 10,100)
opponent = pygame.Rect(10, screen_height / 2 - 50, 10,100)
player_2 = pygame.Rect(10, screen_height / 2 - 50, 10,100)
opponent_2 = pygame.Rect(screen_width - 20, screen_height / 2 - 50, 10,100)

# Speeds, sets the speeds for objects in teh game
ball_speed_x = 9
ball_speed_y = 9
opponent_speed = 8
opponent_2_speed = 8
player_speed = 0
player_2_speed = 0

# Sounds
hit_sound = pygame.mixer.Sound("assets\pong.ogg")
score_sound = pygame.mixer.Sound("assets\score.ogg")

def ball_start(): #Defines the starting position of the ball
    global ball_speed_x, ball_speed_y

    ball.center = (screen_width/2, screen_height/2) #Positions the ball at the center of the screen
    ball_speed_y *= random.choice((1,-1)) #Makes the ball start in a random x and y direction
    ball_speed_x *= random.choice((1,-1))

def ball_animation(): #Defines how the ball moves
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    
    ball.x += ball_speed_x #Changes the ball's x position by the value of ball_speed_x
    ball.y += ball_speed_y #Changes the ball's y position by the value of ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height: #If the top or bottom of the ball touches the top or bottom of the screen it reverses the y speed
        ball_speed_y *= -1
    
    if ball.left <= 0: #If the left edge of the ball touches the wall behind the opponent paddle it plays the score sound, resets the ball and adds 1 to the player's score
        pygame.mixer.Sound.play(score_sound)
        ball_start()
        player_score += 1

    if ball.right >= screen_width: #If the right edge of the ball touches the wall behind the player paddle it plays the score sound, it resets the ball and adds 1 to the opponent's score
        pygame.mixer.Sound.play(score_sound)
        ball_start()
        opponent_score += 1     

    if ball.colliderect(player) or ball.colliderect(opponent_2) and ball_speed_x > 0: #If the ball touches a paddle on the right and is going to the right
        pygame.mixer.Sound.play(hit_sound) #It plays the sound of the ball hitting the paddle
        if abs(ball.right - player.left) or abs(ball.right - opponent_2.left) < 10: #If the ball is less than 10 pixels of the paddle
            ball_speed_x *= -1 #Reverses the ball's x speed
        elif abs(ball.bottom - player.top) or abs (ball.bottom - opponent_2.top) < 10 and ball_speed_y > 0: #If the ball is less than 10 pixels from top of the paddle and is going down 
            ball_speed_y *= -1 #Reverses the ball's y speed
        elif abs(ball.top - player.bottom) or abs(ball.top - opponent_2.bottom) < 10 and ball_speed_y < 0: #If the ball is less than 10 pixels from the bottom of the paddle and is going up
            ball_speed_y *= -1 #Reverses the ball's y speed

                
    if ball.colliderect(opponent) or ball.colliderect(player_2) and ball_speed_x < 0:
        pygame.mixer.Sound.play(hit_sound)
        if abs(ball.left - opponent.right) or abs(ball.left - player_2.right) < 10:
            ball_speed_x *= -1  
        elif abs(ball.bottom - opponent.top) or abs(ball.bottom - player_2.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) or abs(ball.top - player_2.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1
        
def player_animation(player, player_speed):
    player.y += player_speed #Changes the player's position by the value of player_speed

    if player.top <= 0: #If the top of the paddle goes above the screen it resets the top of the paddle to be exactly at the top to prevent it clipping into the wall
        player.top = 0
    if player.bottom >= screen_height: #If the bottom of the paddle goes below the screen it resets the bottom of the paddle to be exactly at the bottom
        player.bottom = screen_height
        
def opponent_ai(opponent, opponent_speed):
    if opponent.top < ball.y:  #If the paddle is below the ball
        opponent.y += opponent_speed #The paddle goes down
    if opponent.bottom > ball.y: #If the paddle is above the ball
        opponent.y -= opponent_speed #The paddle goes up

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill('Black')
        screen.blit(main_menu_font, (450,75))
        play_button.draw()
        options_button.draw()
        quit_button.draw()
        if quit_button.run: #If the button is clicked, quits the game
            pygame.quit()
            sys.exit()
        if play_button.run: #If the button is clicked, brings the player to the gamemode screem
            mode()
        if options_button.run: #If the button is clicked, brings the player to the options screen
            options()
            
        pygame.display.update()
        clock.tick(60)

def options():
    global opponent_speed, offset_main
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill('Black')
        screen.blit(difficulty_font, (400,75))
        easy_button.draw()
        medium_button.draw()
        hard_button.draw()
        back_button.draw()
        if back_button.run:
            main_menu()
        if easy_button.run: #If the button is clicked, sets the opponent speed to 7
            opponent_speed = 7
        if medium_button.run: #If the button is clicked, sets the opponent speed to 8
            opponent_speed = 8
        if hard_button.run: #If the button is clicked, sets the opponent speed to 10
            opponent_speed = 10
        pygame.display.update()
        clock.tick(60)
        
def mode():
    global player_score, opponent_score
    if player_score or opponent_score > 0:
        player_score = 0
        opponent_score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill('Black')
        screen.blit(mode_font, (425,75))
        single_player_button.draw()
        multiplayer_button.draw()
        simulation_button.draw()
        back_button.draw()
        if back_button.run: #If the button is clicked, brings the player to the main menu
            main_menu()
        if single_player_button.run: #If the button is clicked, brings the player to the singeplayer game
            single_player()
        if multiplayer_button.run: #If the button is clicked, brings the player to the multiplayer game
            multiplayer()
        if simulation_button.run: #If the button is clicked, brings the player to the simulation mode
            simulation()
        pygame.display.update()
        clock.tick(60)

def single_player():
    global player_speed, player_score, opponent_score
    ball_start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: #If a key is pressed
                if event.key == pygame.K_UP: #If it's the up arrow
                    player_speed -= 8.5 #Sets the player_speed to -8.5
                if event.key == pygame.K_DOWN:
                    player_speed += 8.5
                if event.key == pygame.K_ESCAPE: #If the escape key is pressed
                    scores = [opponent_score, player_score] #Saves the scores into a list
                    with open ('scores\single_player_scores.csv', 'a') as file: #Writes the scores into a file
                        csv.writer(file).writerow(scores)
                    player_score = 0 #Resets the scores
                    opponent_score = 0
                    mode() #Brings the player to the gamemode screen
            if event.type == pygame.KEYUP: #If a key is released
                if event.key == pygame.K_UP: #If it's the up arrow
                    player_speed += 8.5 #Sets the speed back to 0
                if event.key == pygame.K_DOWN:
                    player_speed -= 8.5

        ball_animation() #Runs the game logic functions
        player_animation(player, player_speed)
        opponent_ai(opponent, opponent_speed)

        screen.fill('Black') #Draws all the objects on a black background
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))
        player_text = font.render(f'{player_score}',False,'#FFFFFF')
        opponent_text = font.render(f'{opponent_score}',False,'#FFFFFF')
        screen.blit(player_text,(660,345))
        screen.blit(opponent_text,(600,345))
        
        pygame.display.update()
        clock.tick(60)
        
def multiplayer():
    global player_speed, player_2_speed, player_score, opponent_score
    ball_start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_speed -= 8.5
                if event.key == pygame.K_DOWN:
                    player_speed += 8.5
                if event.key == pygame.K_w:
                    player_2_speed -= 8.5
                if event.key == pygame.K_s:
                    player_2_speed += 8.5
                if event.key == pygame.K_ESCAPE:
                    scores = [opponent_score, player_score]
                    with open ('scores\multiplayer_scores.csv', 'a') as file:
                        csv.writer(file).writerow(scores)
                    player_score = 0
                    opponent_score = 0
                    mode()   
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player_speed += 8.5
                if event.key == pygame.K_DOWN:
                    player_speed -= 8.5
                if event.key == pygame.K_w:
                    player_2_speed += 8.5
                if event.key == pygame.K_s:
                    player_2_speed -= 8.5

        
        ball_animation()
        player_animation(player, player_speed)
        player_animation(player_2, player_2_speed)

        screen.fill('Black')
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, player_2)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))
        player_text = font.render(f'{player_score}',False,'#FFFFFF')
        player_2_text = font.render(f'{opponent_score}',False,'#FFFFFF')
        screen.blit(player_text,(660,345))
        screen.blit(player_2_text,(600,345))
        
        pygame.display.update()
        clock.tick(60)
        
def simulation():
    global player_score, opponent_score
    ball_start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scores = [opponent_score, player_score]
                    with open ('scores\sim_scores.csv', 'a') as file:
                        csv.writer(file).writerow(scores)
                    player_score = 0
                    opponent_score = 0
                    mode()
        if player_score >= 5 or opponent_score >= 5: #If either score is 5 or above
            scores = [opponent_score, player_score] 
            with open ('scores\sim_scores.csv', 'a') as file:
                csv.writer(file).writerow(scores)
            player_score = 0
            opponent_score = 0
            ball_start() #Puts the ball back in the starting position and restarts the game

                    
        ball_animation()
        opponent_ai(opponent, opponent_speed)
        opponent_ai(opponent_2, opponent_2_speed)

        screen.fill('Black')
        pygame.draw.rect(screen, light_grey, opponent_2)
        pygame.draw.rect(screen, light_grey, opponent)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))
        player_text = font.render(f'{player_score}',False,'#FFFFFF')
        opponent_text = font.render(f'{opponent_score}',False,'#FFFFFF')
        screen.blit(player_text,(660,345))
        screen.blit(opponent_text,(600,345))
        
        pygame.display.update()
        clock.tick(60)

main_menu()