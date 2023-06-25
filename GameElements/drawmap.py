import random
from .roles import Wall, BackGround


# 解析map文件
class readMap():
  def __init__(self, mapfilepath, bg_paths, wall_paths, blocksize, **kwargs):
    self.instances_list=self.__parse(mapfilepath)
    self.bg_paths=bg_paths
    self.wall_paths=wall_paths
    self.blocksize=blocksize
    self.height=len(self.instances_list)
    self.width=len(self.instances_list[0])
    self.screen_size=(blocksize * self.width, blocksize * self.height)
    
  # 画地图
  def draw(self, screen):
    for j in range(self.height):
      for i in range(self.width):
        instance= self.instances_list[j][i]
        if instance== 'w':
          elem= Wall(self.wall_paths[0], [i, j], self.blocksize)
        elif instance== 'x':
          elem= Wall(self.wall_paths[1], [i, j], self.blocksize)
        elif instance == 'z':
          elem = Wall(self.wall_paths[2], [i, j], self.blocksize)
        elif instance == '0':
          elem = BackGround(self.bg_paths[0], [i, j], self.blocksize)
        elif instance== '1':
          elem = BackGround(self.bg_paths[1], [i, j], self.blocksize)
        elif instance== '2':
          elem = BackGround(self.bg_paths[2], [i, j], self.blocksize)
        else:
          raise ValueError("地图加载出错")
        
        elem.draw(screen)
        
  # 获取空地
  def randomGetSpace(self, used_spaces=None):
    while True:
      i = random.randint(0, self.width-1)
      j = random.randint(0, self.height-1)
      coordinate = [i, j]
      if used_spaces and coordinate in used_spaces:
        continue
      instance = self.instances_list[j][i]
      if instance in ['0', '1', '2']:
        break
      
    return coordinate
  
  # 获取元素类型
  def getElemByCoordinate(self, coordinate):
    return self.instances_list[coordinate[1]][coordinate[0]]
  
  # 获取map文件
  def __parse(self, mapfilepath):
    list1 = []
    with open(mapfilepath) as f:
      for line in f.readlines():
        list2 = []
        for a in line:
          if a in ['w', 'x', 'z', '0', '1', '2']:
            list2.append(a)
        list1.append(list2)
    return list1