import pygame 
import sys

# 定义退出程序
def exitGame(use_pygame=True):
    if use_pygame: pygame.quit()
    sys.exit()
    
# 显示文字
def showText(screen, font, text, color, position):
    text_render = font.render(text, True, color)
    rect = text_render.get_rect()
    rect.left, rect.top = position
    screen.blit(text_render, rect)
    return rect.right

# 定义按钮
def Button(screen, position, text, buttoncolor=(120, 120, 120), linecolor=(20, 20, 20), textcolor=(255, 255, 255), bwidth=200, bheight=50):
    left, top = position
    pygame.draw.line(screen, linecolor, (left, top), (left+bwidth, top), 5)
    pygame.draw.line(screen, linecolor, (left, top-2), (left, top+bheight), 5)
    pygame.draw.line(screen, linecolor, (left, top+bheight), (left+bwidth, top+bheight), 5)
    pygame.draw.line(screen, linecolor, (left+bwidth, top+bheight), (left+bwidth, top), 5)
    pygame.draw.rect(screen, buttoncolor, (left, top, bwidth, bheight))
    
    font = pygame.font.SysFont('Consolas', 30)
    text_render = font.render(text, 1, textcolor)
    rect = text_render.get_rect()
    rect.centerx, rect.centery = left + bwidth / 2, top + bheight / 2
    
    return screen.blit(text_render, rect)

# 各个游戏界面（开始，结束等）
def Interface(screen, cfg, mode='game_start'):
    pygame.display.set_mode(cfg.SCREENSIZE)
    
    if mode == 'game_start':
        clock = pygame.time.Clock()
        while True:
            screen.fill((0,100,0))
            button_1 = Button(screen,(220, 150),'start game')
            button_2 = Button(screen,(220, 250),'quit game')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_1.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif button_2.collidepoint(pygame.mouse.get_pos()):
                        exitGame()
            pygame.display.update()
            clock.tick(cfg.FPS)
    elif mode == 'game_switch':
        clock = pygame.time.Clock()
        while True:
            screen.fill((0,100,0))
            button_1 = Button(screen, (220, 150), 'next level')
            button_2 = Button(screen, (220, 250), 'quit game')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_1.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif button_2.collidepoint(pygame.mouse.get_pos()):
                        exitGame()
            pygame.display.update()
            clock.tick(cfg.FPS)
    elif mode == 'game_end':
        clock = pygame.time.Clock()
        while True:
            screen.fill((0,100,0))
            button_1 = Button(screen, (220, 150), 'One more')
            button_2 = Button(screen, (220, 250), 'quit game')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_1.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif button_2.collidepoint(pygame.mouse.get_pos()):
                        exitGame()
            pygame.display.update()
            clock.tick(cfg.FPS)
    else:
        raise ValueError("出错了，请重启")