import pygame, random, pygbag, asyncio
from Obstacle import *
from Player import *
from Scrollable import *
pygame.init()


async def main():
    mainClock = pygame.time.Clock()

    # Window Setup
    screen = pygame.display.set_mode((160*5, 144*5))
    screen_rect = screen.get_rect()
    pygame.display.set_caption("Throtl")
    pygame.display.set_icon(pygame.image.load("Icon.png"))
    canvas = pygame.Surface((160, 144))
    canvas_rect = canvas.get_rect()

    def updateCanvasScale(canvas_rect):
        canvas_rect = canvas_rect.fit(screen_rect)
        canvas_rect.center = screen_rect.center
        return pygame.transform.scale(canvas, canvas_rect.size)

    # Font Rendering
    text_font = pygame.font.Font("NESCyrillic.ttf", 15)

    def draw_text(text, font, text_col, x, y, origin):
            img = font.render(text, False, text_col)
            rect = img.get_rect()
            match origin:
                case "Center":
                    rect.center = (x,y)
                case "TopLeft":
                    rect.topleft = (x,y)
                case "TopRight":
                    rect.topright = (x,y)
            canvas.blit(img, (rect.x,rect.y))

    # Audio Import
    music = pygame.mixer.Sound("Audio/Music.ogg")
    music.set_volume(0.05)
    music.play(loops=-1)
    isMusicPlaying = True
    music_playOnce = True
    jump_sfx = [0,0,0,0] 
    jump_sfx[0] = pygame.mixer.Sound("Audio/Jump.ogg")
    jump_sfx[1] = pygame.mixer.Sound("Audio/Jump2.ogg")
    jump_sfx[2] = pygame.mixer.Sound("Audio/Jump3.ogg")
    jump_sfx[3] = pygame.mixer.Sound("Audio/Jump4.ogg")
    boom_sfx = pygame.mixer.Sound("Audio/boom.ogg")
    boom_sfx_playOnce = True
    score_sfx = pygame.mixer.Sound("Audio/Score.ogg")
    score_sfx.set_volume(0.2)
    score5_sfx = pygame.mixer.Sound("Audio/Score5.ogg")
    score5_sfx.set_volume(0.2)
    score10_sfx = pygame.mixer.Sound("Audio/Score10.ogg")
    score10_sfx.set_volume(0.2)

    # Game Objects and Variables
    player = Player("Player/idle", canvas)
    obstacle = Obstacle(canvas)

    speed = 5

    ground = Scrollable("ground", canvas, 0, 121)
    clouds = Scrollable("clouds", canvas, 0, 16)
    clouds2 = Scrollable("clouds2", canvas, 0, 20)

    score = 0
    canBeScored = True

    # Main Menu
    Main_Menu_BG_Sprite = pygame.image.load("Sprites/MainMenuBG.png").convert_alpha()
    Main_Menu_Selection_Index = 0
    # Game Loop
    runtime = True
    curScene = "Main_Menu"
    isGameRunning = True
    framerate = 60
    while runtime:
        canvas.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runtime = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if curScene == "Main_Menu":
                        if Main_Menu_Selection_Index >= 1:
                            Main_Menu_Selection_Index = 0
                        else:
                            Main_Menu_Selection_Index += 1
                        score_sfx.play()
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if curScene == "Main_Menu":
                        if Main_Menu_Selection_Index == 0:
                            Main_Menu_Selection_Index = 1
                        else:
                            Main_Menu_Selection_Index -= 1
                        score_sfx.play()
                if event.key == pygame.K_SPACE:
                    match curScene:
                        case "Game":
                            if isGameRunning: player.accelerating = True
                            else:
                                isGameRunning = True
                                obstacle.x = 176 + random.randint(160, 320)
                                speed = 3
                                score = 0
                                boom_sfx_playOnce = True
                                music.play()
                        case "Main_Menu":
                            match Main_Menu_Selection_Index:
                                case 0:
                                    curScene = "Game" # Enter Game
                                    isGameRunning = True
                                    obstacle.x = 176 + random.randint(160, 320)
                                    speed = 3
                                    score = 0
                                    boom_sfx_playOnce = True
                                case 1:
                                    pass # Enter Score Menu
                if event.key == pygame.K_ESCAPE:
                    if not isGameRunning: curScene = "Main_Menu"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    match curScene:
                        case "Game":
                            if isGameRunning:
                                player.accelerating = False
                                if speed < 4:
                                    player.jump(4)
                                else:
                                    player.jump(speed)
                                if not player.isJumping:
                                    jump_sfx[random.randrange(0,3)].play()

                            
        
        match curScene:
            case "Game":

                clouds2.x -= speed * 0.2
                clouds2.update()

                player.update()

                obstacle.x -= speed
                obstacle.update()

                ground.x -= speed 
                ground.update()
                clouds.x -= speed * 0.5
                clouds.update()

                #UI
                pygame.draw.rect(canvas, (0,0,0), (0, 0, 160,16))
                draw_text("Score: " + str(score), text_font, (255,255,255), 10,2, "TopLeft")
                draw_text("MPH: " + str(int(speed) * 10), text_font, (255,255,255), 150,2, "TopRight")

                if isGameRunning:
                    # Scoring
                    if obstacle.x < player.x:
                        if canBeScored:
                            if (score + 1) % 10 == 0:
                                score10_sfx.play()
                            elif (score + 1) % 5 == 0:
                                score5_sfx.play()
                            else:
                                score_sfx.play()
                            canBeScored = False
                            score += 1
                    elif obstacle.x > player.x:
                        canBeScored = True
                    
                    # Player Acceleration
                    match player.accelerating:
                        case True:
                            if not speed > 6: speed += 0.03
                        case _ if player.isJumping:
                            pass
                        case False:
                            if not speed <= 2: speed -= 0.3

                else: # Game Over UI
                    draw_text("Game Over!", text_font, (255,255,255), 80, 47, "Center")
                    draw_text("Space: play again", text_font, (255,255,255), 80,  57, "Center")
                    draw_text("ESC: main menu", text_font, (255,255,255), 80, 67, "Center")
                    if boom_sfx_playOnce:
                        boom_sfx.play()
                        boom_sfx_playOnce = False
                
                # Game Over Condition
                if obstacle.mask.overlap(player.mask, (obstacle.x - player.x, obstacle.y - player.y)):
                    music.stop()
                    isMusicPlaying = False
                    music_playOnce = True
                    isGameRunning = False
                    speed = 0
                    player.accelerating = False
            case "Main_Menu":
                if not isMusicPlaying and music_playOnce == True: 
                    music.play(loops=-1)
                    music_playOnce = False
                canvas.blit(Main_Menu_BG_Sprite, (0,0))

                match Main_Menu_Selection_Index:
                    case 0:
                        draw_text("> Play <", text_font, (255,255,255), 80, 82, "Center")
                        draw_text("Scores", text_font, (255,255,255), 80, 92, "Center")
                    case 1:
                        draw_text("Play", text_font, (255,255,255), 80, 82, "Center")
                        draw_text("> Scores <", text_font, (255,255,255), 80, 92, "Center")
                

        # Update Screen
        screen.blit(updateCanvasScale(canvas_rect), (0,0))
        pygame.display.flip()
        mainClock.tick(framerate)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())