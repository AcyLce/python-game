import random
import sys
import pygame
import os


from GameElements import Fruit, Hero, showText, Interface, readMap


# 配置文件路径
class FilePath():
  
    # 设置一些基本信息
    SCREENSIZE = (640,480) 
    RED = (255,0,0)
    BLACK = (0,0,0)
    WHITE = (255,255, 255)     
    YELLOW = (255,255,0)
    BLUE = (0, 0, 255)

    # 设置每一块的大小
    BLOCKSIZE =30
    
    # 设置FPS
    FPS = 30
    
    # 设置音乐
    BGMPATH =os.path.join(os.getcwd(), 'resources/audios/bgm.mp3')
    
    # 设置毒水果路径
    FRUITPATHS=[os.path.join(os.getcwd(), path) for path in \
        ['resources/images/misc/banana.png', 'resources/images/misc/cherry.png']]
    
    # 设置背景
    BackGroundPATHS=[os.path.join(os.getcwd(), path) for path in \
        ['resources/images/misc/bg0.png', 'resources/images/misc/bg1.png', 'resources/images/misc/bg2.png']]
    
    # 设置游戏地图
    GAMEMAPPATHS=[os.path.join(os.getcwd(), path) for path in \
        ['resources/maps/1.map', 'resources/maps/2.map']]
    
    # 设置墙的路径
    WALLPATHS=[os.path.join(os.getcwd(), path) for path in \
        ['resources/images/misc/wall0.png', 'resources/images/misc/wall1.png', 'resources/images/misc/wall2.png']]
    
    # 设置炸弹爆炸
    BOMBPATH=os.path.join(os.getcwd(), 'resources/images/misc/bomb.png')
    FIREPATH=os.path.join(os.getcwd(), 'resources/images/misc/fire.png')
    
    # 设置角色图片路径
    HEROBATMANPATHS=[os.path.join(os.getcwd(), path) for path in \
        ['resources/images/batman/left.png', 'resources/images/batman/right.png', 'resources/images/batman/up.png', 'resources/images/batman/down.png']]
    HERODKPATHS=[os.path.join(os.getcwd(), path) for path in \
        ['resources/images/dk/left.png', 'resources/images/dk/right.png', 'resources/images/dk/up.png', 'resources/images/dk/down.png']]
    HEROZELDAPATHS=[os.path.join(os.getcwd(), path) for path in \
        ['resources/images/zelda/left.png', 'resources/images/zelda/right.png', 'resources/images/zelda/up.png', 'resources/images/zelda/down.png']]
    

# 开始游戏
def gameStart(FilePath):
  
  # 将游戏初始化
  pygame.init()
  pygame.mixer.init()
  pygame.mixer.music.load(FilePath.BGMPATH)
  
  #音乐循环播放
  pygame.mixer.music.play(-1, 0.0)
  
  screen = pygame.display.set_mode(FilePath.SCREENSIZE)
  pygame.display.set_caption('BombersGame 炸弹鬼才')
  
  # 开始界面
  Interface(screen, FilePath, mode='game_start')
  
  # 开启游戏循环
  font = pygame.font.SysFont('Consolas', 15)
  for gamemap_path in FilePath.GAMEMAPPATHS:
    # 设置地图
    mapImageParsing =readMap(gamemap_path, bg_paths=FilePath.BackGroundPATHS, wall_paths=FilePath.WALLPATHS, blocksize=FilePath.BLOCKSIZE)
    
    # 地图占用
    usedSpaces =[]
    
    # 判断游戏胜利的标志
    victorySign=False
    
    # 设置毒水果      
    poisonousFruits = pygame.sprite.Group() 
    for i in range(8):
      coordinate =mapImageParsing.randomGetSpace(usedSpaces)
      poisonousFruits.add(Fruit(random.choice(FilePath.FRUITPATHS), coordinate=coordinate, blocksize=FilePath.BLOCKSIZE))
      usedSpaces.append(coordinate)
     
    # 安置炸弹
    bombs =pygame.sprite.Group() 
     
    # 电脑角色
    aiRoles = pygame.sprite.Group()
    coordinate = mapImageParsing.randomGetSpace(usedSpaces)
    aiRoles.add(Hero(imagepaths=FilePath.HEROBATMANPATHS, coordinate=coordinate, blocksize=FilePath.BLOCKSIZE, map_parser=mapImageParsing, hero_name='AI1'))
    usedSpaces.append(coordinate)
    coordinate = mapImageParsing.randomGetSpace(usedSpaces)
    aiRoles.add(Hero(imagepaths=FilePath.HERODKPATHS, coordinate=coordinate, blocksize=FilePath.BLOCKSIZE, map_parser=mapImageParsing, hero_name='AI2'))
    usedSpaces.append(coordinate)
    
    # 我方角色
    coordinate=mapImageParsing.randomGetSpace(usedSpaces)
    selfRoles=Hero(imagepaths=FilePath.HEROZELDAPATHS, coordinate=coordinate, blocksize=FilePath.BLOCKSIZE, map_parser=mapImageParsing, hero_name='self')
    usedSpaces.append(coordinate)
    
    
    # 游戏循环
    screen =pygame.display.set_mode(mapImageParsing.screen_size)
    clock =pygame.time.Clock()
    while True:
      dt = clock.tick(FilePath.FPS)
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit(-1)
          
        # 设置游戏操作方式，空格为安置炸弹，↑↓←→键控制上下左右
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP:
            selfRoles.move('up')
          elif event.key == pygame.K_DOWN:
            selfRoles.move('down')
          elif event.key == pygame.K_LEFT:
            selfRoles.move('left')
          elif event.key == pygame.K_RIGHT:
            selfRoles.move('right')
          elif event.key == pygame.K_SPACE:
            if selfRoles.bomb_cooling_count <= 0:
              bombs.add(selfRoles.generateBomb(imagepath=FilePath.BOMBPATH, digitalcolor=FilePath.YELLOW, explode_imagepath=FilePath.FIREPATH))
      screen.fill(FilePath.WHITE)
      
      # 电脑AI随机行动
      for hero in aiRoles:
        action, flag = hero.randomAction(dt)
        if flag and action == 'dropbomb':
          bombs.add(hero.generateBomb(imagepath=FilePath.BOMBPATH, digitalcolor=FilePath.YELLOW, explode_imagepath=FilePath.FIREPATH))
      
      # 游戏角色吃到毒水果会减少生命值
      selfRoles.eatFruit(poisonousFruits)
      for hero in aiRoles:
        hero.eatFruit(poisonousFruits)
         
      # 将角色加载到屏幕上
      mapImageParsing.draw(screen)
      for bomb in bombs:
        if not bomb.is_being:
          bombs.remove(bomb)
        explode_area = bomb.draw(screen, dt, mapImageParsing)
        if explode_area:
          
          # 处于爆炸中的角色生命值不断下降
          if selfRoles.coordinate in explode_area:
            selfRoles.health_value -= bomb.harm_value
          for hero in aiRoles:
            if hero.coordinate in explode_area:
              hero.health_value -= bomb.harm_value
      poisonousFruits.draw(screen)
      for hero in aiRoles:
        hero.draw(screen, dt)
      selfRoles.draw(screen, dt)
      
      # 所有角色的生命值显示在左上角
      pos_x = showText(screen, font, text=selfRoles.hero_name + ": " + str(selfRoles.health_value), color=FilePath.YELLOW, position=[5, 5])
      for hero in aiRoles:
        pos_x, pos_y = pos_x+15, 5
        pos_x = showText(screen, font, text=hero.hero_name + ": " + str(hero.health_value), color=FilePath.YELLOW, position=[pos_x, pos_y])
      
      # 游戏结束条件：两边有一方生命值先降至0以下
      if selfRoles.health_value <= 0:
        victorySign = False
        break
      for hero in aiRoles:
        if hero.health_value <= 0:
          aiRoles.remove(hero)
      if len(aiRoles) == 0:
        victorySign = True
        break
      pygame.display.update()
      clock.tick(FilePath.FPS)
    if victorySign:
      Interface(screen, FilePath, mode='game_switch')
    else:
      break
  Interface(screen, FilePath, mode='game_end')

# 开始运行
while True:
  gameStart(FilePath)
