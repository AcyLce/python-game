3
# 定义游戏中主要的元素，包括正反派，墙，背景，毒苹果，炸弹

import random
import pygame
import copy



# 定义各个角色
class Hero(pygame.sprite.Sprite):
  def __init__(self, imagepaths, coordinate, blocksize, map_parser, **kwargs):
    pygame.sprite.Sprite.__init__(self)
    
    self.imagepaths = imagepaths
    self.image = pygame.image.load(imagepaths[-1])
    self.image = pygame.transform.scale(self.image, (blocksize, blocksize))
    self.rect = self.image.get_rect()
    self.rect.left, self.rect.top = coordinate[0] * blocksize, coordinate[1] * blocksize
    self.coordinate = coordinate
    self.blocksize = blocksize
    self.map_parser = map_parser
    self.hero_name = kwargs.get('hero_name')
    
    # 定义炸弹冷却时间
    self.bomb_cooling_time = 5000
    self.bomb_cooling_count = 0
       
    # AI角色随机移动时间
    self.randommove_cooling_time = 100
    self.randommove_cooling_count = 0
    
    # 定义生命值 
    self.health_value = 50
    
  # 定义角色移动
  def move(self, direction):
    self.__updateImage(direction)
    if direction == 'left':
      if self.coordinate[0]-1 < 0 or self.map_parser.getElemByCoordinate([self.coordinate[0]-1, self.coordinate[1]]) in ['w', 'x', 'z']:
        return False
      self.coordinate[0] = self.coordinate[0] - 1
    elif direction == 'right':
      if self.coordinate[0]+1 >= self.map_parser.width or self.map_parser.getElemByCoordinate([self.coordinate[0]+1, self.coordinate[1]]) in ['w', 'x', 'z']:
        return False
      self.coordinate[0] = self.coordinate[0] + 1
    elif direction == 'up':
      if self.coordinate[1]-1 < 0 or self.map_parser.getElemByCoordinate([self.coordinate[0], self.coordinate[1]-1]) in ['w', 'x', 'z']:
        return False
      self.coordinate[1] = self.coordinate[1] - 1
    elif direction == 'down':
      if self.coordinate[1]+1 >= self.map_parser.height or self.map_parser.getElemByCoordinate([self.coordinate[0], self.coordinate[1]+1]) in ['w', 'x', 'z']:
        return False
      self.coordinate[1] = self.coordinate[1] + 1
    else:
      raise ValueError("出错了")
    self.rect.left, self.rect.top = self.coordinate[0] * self.blocksize, self.coordinate[1] * self.blocksize
    return True
  
  # AI角色移动
  def randomAction(self, dt):
    # AI角色冷却倒计时
    if self.randommove_cooling_count > 0:
      self.randommove_cooling_count -= dt
    action = random.choice(['left', 'left', 'right', 'right', 'up', 'up', 'down', 'down', 'dropbomb'])
    flag = False
    if action in ['left', 'right', 'up', 'down']:
      if self.randommove_cooling_count <= 0:
        flag = True
        self.move(action)
        self.randommove_cooling_count = self.randommove_cooling_time
    elif action in ['dropbomb']:
      if self.bomb_cooling_count <= 0:
        flag = True
        self.bomb_cooling_count = self.bomb_cooling_time
    return action,flag
  
  # 制造炸弹
  def generateBomb(self,imagepath, digitalcolor, explode_imagepath):
    return Bomb(imagepath=imagepath, coordinate=copy.deepcopy(self.coordinate), blocksize = self.blocksize, digitalcolor = digitalcolor, explode_imagepath = explode_imagepath)
  
  # 把角色画到屏幕上
  def draw(self, screen, dt):
    # 炸弹冷却倒计时
    if self.bomb_cooling_count > 0:
      self.bomb_cooling_count -= dt
    screen.blit(self.image, self.rect)
    return True
  
  # 角色吃毒苹果
  def eatFruit(self,fruit_sprite_group):
    eaten_fruit = pygame.sprite.spritecollide(self, fruit_sprite_group, True, None)
    for fruit in eaten_fruit:
      self.health_value -= fruit.value
      
  # 改变角色朝向,使用不同的朝向图
  def __updateImage(self, direction):
    directions = ['left', 'right', 'up', 'down']
    idx = directions.index(direction)
    self.image = pygame.image.load(self.imagepaths[idx])
    self.image = pygame.transform.scale(self.image, (self.blocksize, self.blocksize))
  



# 定义背景
class BackGround(pygame.sprite.Sprite):
  def __init__(self, imagePath, coordinate, blockSize,**kwargs):
    pygame.sprite.Sprite.__init__(self)
    
    self.image = pygame.image.load(imagePath)
    self.image = pygame.transform.scale(self.image, (blockSize, blockSize))
    
    self.rect = self.image.get_rect()
    self.rect.left = coordinate[0] * blockSize
    self.rect.top = coordinate[1] * blockSize
    self.blocksize = blockSize
    self.coordinate = coordinate
    
  # 将背景画到屏幕上
  def draw(self, screen):
    screen.blit(self.image, self.rect)
    return True
  
  
# 定义炸弹
class Bomb(pygame.sprite.Sprite):
  def __init__(self, imagepath, coordinate, blocksize, digitalcolor, explode_imagepath, **kwargs):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load(imagepath)
    self.image = pygame.transform.scale(self.image, (blocksize, blocksize))
    self.explode_imagepath = explode_imagepath
    self.rect = self.image.get_rect()
    
    # 定义像素
    self.rect.left = coordinate[0] * blocksize
    self.rect.top = coordinate[1] * blocksize
    
    # 定义坐标，其中元素块为单位长度
    self.coordinate = coordinate
    self.blocksize = blocksize
    
    # 定义炸弹伤害威力
    self.harm_value = 1    
    
    # 定义爆炸持续时间
    self.exploding_count = 1000 * 1  
      
    # 定义爆炸的倒计时
    self.explode_millisecond = 6000 * 1 - 1 
    self.explode_second = int(self.explode_millisecond / 1000)
    self.start_explode = False
    
      
    # 该炸弹是否还存在
    self.is_being = True
    self.font = pygame.font.SysFont('Consolas', 20)
    self.digitalcolor = digitalcolor
    
  # 将炸弹画到屏幕上
  def draw(self,screen,dt,map_parser):
    if not self.start_explode:
      # 定义爆炸倒计时
      self.explode_millisecond -= dt
      self.explode_second = int(self.explode_millisecond / 1000)
      if self.explode_millisecond < 0:
        self.start_explode = True
        
      screen.blit(self.image, self.rect)
      
      text = self.font.render(str(self.explode_second), True, self.digitalcolor)
      rect = text.get_rect(center=(self.rect.centerx-5, self.rect.centery+5))
      screen.blit(text, rect)
      return False
    else:
      # 定义爆炸持续倒计时
      self.exploding_count -= dt
      if self.exploding_count > 0:
        return self.__explode(screen, map_parser)
      else:
        self.is_being = False
        return False
      
  # 定义炸弹爆炸效果
  def __explode(self, screen, map_parser):
    explode_area = self.__calcExplodeArea(map_parser.instances_list)
    for each in explode_area:
      image = pygame.image.load(self.explode_imagepath)
      image = pygame.transform.scale(image, (self.blocksize, self.blocksize))
      rect = image.get_rect()
      rect.left, rect.top = each[0] * self.blocksize, each[1] * self.blocksize
      screen.blit(image, rect)
    return explode_area
  
  #定义爆炸区域"__calcExplodeArea"
  def __calcExplodeArea(self, instances_list):
    explode_area = []
    
    # 墙可以挡住爆炸扩散, 且爆炸仅在游戏地图范围内
    for ymin in range(self.coordinate[1], self.coordinate[1]-5, -1):
      if ymin < 0 or instances_list[ymin][self.coordinate[0]] in ['w', 'x', 'z']:
        break
      explode_area.append([self.coordinate[0], ymin])
      
    for ymax in range(self.coordinate[1]+1, self.coordinate[1]+5):
      if ymax >= len(instances_list) or instances_list[ymax][self.coordinate[0]] in ['w', 'x', 'z']:
        break
      explode_area.append([self.coordinate[0], ymax])
      
    for xmin in range(self.coordinate[0], self.coordinate[0]-5, -1):
      if xmin < 0 or instances_list[self.coordinate[1]][xmin] in ['w', 'x', 'z']:
        break
      explode_area.append([xmin, self.coordinate[1]])
      
    for xmax in range(self.coordinate[0]+1, self.coordinate[0]+5):
      if xmax >= len(instances_list[0]) or instances_list[self.coordinate[1]][xmax] in ['w', 'x', 'z']:
        break
      explode_area.append([xmax, self.coordinate[1]])
      
    return explode_area
  
# 定义墙
class Wall(pygame.sprite.Sprite):
  def __init__(self, imagepath, coordinate, blocksize, **kwargs):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load(imagepath)
    self.image = pygame.transform.scale(self.image, (blocksize, blocksize))
    self.rect = self.image.get_rect()
    self.rect.left = coordinate[0] * blocksize
    self.rect.top =  coordinate[1] * blocksize
    self.coordinate = coordinate
    self.blocksize = blocksize
    
  # 将墙画到屏幕上
  def draw(self, screen):
    screen.blit(self.image, self.rect)
    return True
  

# 定义水果
class Fruit(pygame.sprite.Sprite):
  def __init__(self, imagepath, coordinate, blocksize,**kwargs):
    pygame.sprite.Sprite.__init__(self)
    self.kind = imagepath.split('/')[-1].split('.')[0]
    if self.kind == 'banana':
      self.value = 5
    elif self.kind == 'cherry':
      self.value = 10
    else:
      raise ValueError("出错了")
    
    self.image = pygame.image.load(imagepath)
    self.image = pygame.transform.scale(self.image, (blocksize, blocksize))
    self.rect = self.image.get_rect()
    self.rect.left, self.rect.top = coordinate[0] * blocksize, coordinate[1] * blocksize
    self.coordinate = coordinate
    self.blocksize = blocksize
    
  # 加载毒水果到屏幕
  def draw(self, screen):
    screen.blit(self.image, self.rect)
    return True 

      
    
      