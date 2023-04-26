import pygame

# 落子点计算
# 25，25   25，125  [(125-25+1)/2]+25=76

# 棋盘左侧棋子初始位置
greenPositions = [(76, 76, '虎', 5), (176, 176, '猫', 1), (276, 76, '象', 7),
                  (76, 276, 'trap', -1), (276, 276, '狼', 3), (176, 376, 'trap', -1),
                  (76, 476, 'trap', -1), (276, 476, '豹', 4), (176, 576, '狗', 2),
                  (76, 676, '狮', 6), (276, 676, '鼠', 0), (76, 376, 'home', -2)]

# 棋盘右侧棋子初始位置
redPositions = [(876, 76, '狮', 6), (676, 76, '鼠', 0), (776, 176, '狗', 2),
                (876, 276, 'trap', -1), (676, 276, '豹', 4), (776, 376, 'trap', -1),
                (876, 476, 'trap', -1), (676, 476, '狼', 3), (776, 576, '猫', 1),
                (876, 676, '虎', 5), (676, 676, '象', 7), (876, 376, 'home', -2)]

# 白格位置
blankPosition = [(176, 76), (376, 76), (476, 76), (576, 76), (776, 76),
                 (76, 176), (276, 176), (676, 176), (876, 176),
                 (176, 276), (776, 276),
                 (276, 376), (376, 376), (476, 376), (576, 376), (676, 376),
                 (176, 476), (776, 476),
                 (76, 576), (276, 576), (676, 576), (876, 576),
                 (176, 676), (376, 676), (476, 676), (576, 676), (776, 676), ]
# 水格位置  76<176 276<376<476 576<676
waterPosition = [(376, 176), (476, 176), (576, 176), (376, 276), (476, 276), (576, 276),
                 (376, 476), (476, 476), (576, 476), (376, 576), (476, 576), (576, 576)]

greenTargets = []
redTargets = []
blankTargets = []
waterTargets = []


# 棋子对象
# level 7(象) 6(狮) 5(虎) 4(豹) 3(狼) 2(狗) 1(猫) 0(鼠) -1(陷阱) -2(兽穴) -3(空白块) -4(水块)
# 过河对象：虎 狮 鼠    移动，吃，过河
# 常规对象：象 豹 狼 狗 猫    移动，吃
# 特殊对象：陷阱   不可移动，不可吃
class Target:
    x = 0
    y = 0
    targetLevel = -3
    targetName = 'target'
    rect = None
    group = None

    def __init__(self, x, y, targetName, targetLevel, group):
        self.x = x
        self.y = y
        self.targetName = targetName
        self.targetLevel = targetLevel
        self.group = group

        border = pygame.draw.circle(screen, group, (x, y), 49)
        text = f.render(targetName, True, 'black')
        textRect = text.get_rect()
        textRect.center = (x, y)
        # 包含圆形底座，中间字体
        # 调整坐标需要使用
        border = border.move(x, y)
        textRect.center = (x, y)
        self.rect = [border, textRect]
        screen.blit(text, textRect)


class Water(Target):
    def __init__(self, x, y, group):
        super().__init__(x, y, 'water', -4, group)


class Blank(Target):
    def __init__(self, x, y, group):
        super().__init__(x, y, 'blank', -3, group)


class Home(Target):
    def __init__(self, x, y, group):
        super().__init__(x, y, 'home', -2, group)


class Trap(Target):

    def __init__(self, x, y, group):
        super().__init__(x, y, 'trap', -1, group)


class NormalAnimal(Target):
    isTrapped = False
    isAlive = False

    def __init__(self, x, y, targetName, targetLevel, isTrapped, isAlive, group):
        super().__init__(x, y, targetName, targetLevel, group)
        self.isTrapped = isTrapped
        self.isAlive = isAlive

    def move(self, targetX, targetY):
        # 普通动物只有上下左右移动
        if (targetX, targetY) not in [(self.x + 100, self.y), (self.x - 100, self.y), (self.x, self.y + 100),
                                      (self.x, self.y - 100)]:
            return False
        print("可以移动")
        # 移动不允许进入水
        if (targetX, targetY) in waterPosition:
            return False
        print("没有进水")
        # 遍历所有对象，是否有坐标重叠
        # 绿方对象
        print("敌方遍历")
        for i in greenTargets if self.group == 'red' else redTargets:
            # 有重叠
            if (i.x, i.y) == (targetX, targetY):
                # 队伍相同
                if i.group == self.group:
                    # 是自己的陷阱
                    if i.targetLevel == -1:
                        rect(self.group, self.x, self.y, targetX, targetY, self.targetName)
                        self.x = targetX
                        self.y = targetY
                        return True
                    print("同队伍")
                    return False
                elif self.tryEat(i):
                    print("吃得掉")
                    if i.targetName not in ["trap", "home"]:
                        print("移除了" + i.targetName)
                        redTargets.remove(i)
                    return True
                else:
                    print("吃不掉")
                    return False

        print("友方遍历")
        # 红方对象
        for i in redTargets if self.group == 'red' else greenTargets:
            # 有重叠
            if (i.x, i.y) == (targetX, targetY):
                # 队伍相同
                if i.group == self.group:
                    # 是自己的陷阱
                    if i.targetLevel == -1:
                        rect(self.group, self.x, self.y, targetX, targetY, self.targetName)
                        self.x = targetX
                        self.y = targetY
                        return True
                    print("同队伍")
                    return False
                # 队伍不同
                elif self.tryEat(i):
                    print("吃得掉" + i.targetName)
                    if i.targetName not in ["trap","home"]:
                        print("移除了"+i.targetName)
                        redTargets.remove(i)
                    return True
                # 队伍不同还吃不掉
                else:
                    print("吃不掉")
                    return False
        # 正常移动，没有重叠
        # 新格子画棋子，旧格子画白格
        rect(self.group, self.x, self.y, targetX, targetY, self.targetName)
        # 是否在本方陷阱
        for i in redTargets if self.group == 'red' else greenTargets:
            if i.targetName == 'trap':
                if (self.x, self.y) == (i.x, i.y):
                    # 新地点用模型覆盖
                    pygame.draw.circle(screen, self.group, (self.x, self.y), 49)
                    # 重新写字体
                    text = f.render("trap", True, 'black')
                    textRect = text.get_rect()
                    textRect.center = (self.x, self.y)
                    # 刷新屏幕
                    screen.blit(text, textRect)
        # 是否被困住
        if self.isTrapped:
            self.isTrapped = False
            # 新地点用模型覆盖
            pygame.draw.circle(screen, 'green' if self.group == 'red' else 'red', (self.x, self.y), 49)
            # 重新写字体
            text = f.render("trap", True, 'black')
            textRect = text.get_rect()
            textRect.center = (self.x, self.y)
            # 刷新屏幕
            screen.blit(text, textRect)
        # 移动到新格子
        self.x = targetX
        self.y = targetY

        print("正常移动")
        return True

    def tryEat(self, target0):
        print(target0.targetName)
        # 对象是陷阱
        if target0.targetLevel == -1:
            print("踩陷阱")
            self.isTrapped = True
            # 陷阱覆盖但是不删除
            rect(self.group, self.x, self.y, target0.x, target0.y, self.targetName)
            self.x = target0.x
            self.y = target0.y
            return True

        # 自身在陷阱
        if self.isTrapped:
            print("中陷阱了")
            return False
        # 对象在陷阱
        if target0.isTrapped:
            rect(self.group, self.x, self.y, target0.x, target0.y, self.targetName)
            print('陷阱杀')
            self.x = target0.x
            self.y = target0.y
            return True
        # 老鼠吃大象
        if (self.targetLevel == 0) & (target0.targetLevel == 7):
            print('老鼠吃大象')
            # 清除目标对象，进入单元格
            rect(self.group, self.x, self.y, target0.x, target0.y, self.targetName)
            self.x = target0.x
            self.y = target0.y
            return True
        # 大象吃
        if (self.targetLevel == 7) & (target0.targetLevel != 0):
            print('大象吃', self.targetLevel, target0.targetLevel)
            rect(self.group, self.x, self.y, target0.x, target0.y, self.targetName)
            self.x = target0.x
            self.y = target0.y
            return True
        # 除了大象之外的
        if (self.targetLevel != 7) & (self.targetLevel >= target0.targetLevel):
            print('正常吃', self.targetLevel, target0.targetLevel)
            # 清除目标对象，进入单元格
            rect(self.group, self.x, self.y, target0.x, target0.y, self.targetName)
            self.x = target0.x
            self.y = target0.y
            return True
        return False


class SpecialAnimal(NormalAnimal):
    def __init__(self, x, y, targetName, targetLevel, isTrapped, isAlive, group):
        super().__init__(x, y, targetName, targetLevel, isTrapped, isAlive, group)

    def jumpOver(self):
        if True:
            return True


def rect(group, oldx, oldy, newx, newy, targetName):
    # 旧地点用白格覆盖
    pygame.draw.rect(screen, 'white', ((oldx - 49, oldy - 49), (98, 98)))
    # 新地点用模型覆盖
    pygame.draw.circle(screen, group, (newx, newy), 49)
    # 重新写字体
    text = f.render(targetName, True, 'black')
    textRect = text.get_rect()
    textRect.center = (newx, newy)
    # 刷新屏幕
    screen.blit(text, textRect)


# 获取单元格中心
def getPosition(x, y):
    for i in range(9):
        if abs(x - 76 - 100 * i) < 50:
            mx = 76 + 100 * i
            for j in range(9):
                if abs(y - 76 - 100 * j) < 50:
                    my = 76 + 100 * j
                    return mx, my
    return -1, -1


if __name__ == "__main__":

    # 初始化
    pygame.init()
    f = pygame.font.SysFont(['fangsong', 'microsoftsansserif'], 25)

    # 设置表格大小    (100*7+50)*(100*9+50)   单格大小100*100 边框 25*25
    screen = pygame.display.set_mode((950, 750))
    pygame.display.set_caption("斗兽棋")
    screen.fill('white')

    # 创建水格对象,画水单元格
    for i in waterPosition:
        waterTargets.append(Water(i[0], i[1], 'blue'))
    pygame.draw.rect(screen, 'lightblue', (325, 125, 300, 200))
    pygame.draw.rect(screen, 'lightblue', (325, 425, 300, 200))

    # 绿方棋子对象及图像
    for i in greenPositions:
        if i[2] in ["狮", '虎', '鼠']:
            greenTargets.append(SpecialAnimal(i[0], i[1], i[2], i[3], False, True, 'green'))
        elif i[2] == "home":
            greenTargets.append(Home(i[0], i[1], 'green'))
        elif i[2] == "trap":
            greenTargets.append(Trap(i[0], i[1], 'green'))
        else:
            greenTargets.append(NormalAnimal(i[0], i[1], i[2], i[3], False, True, 'green'))
    # 红方棋子对象及图像
    for i in redPositions:
        if i[2] in ["狮", '虎', '鼠']:
            redTargets.append(SpecialAnimal(i[0], i[1], i[2], i[3], False, True, 'red'))
        elif i[2] == "home":
            redTargets.append(Home(i[0], i[1], 'red'))
        elif i[2] == "trap":
            redTargets.append(Trap(i[0], i[1], 'red'))
        else:
            redTargets.append(NormalAnimal(i[0], i[1], i[2], i[3], False, True, 'red'))

    # 棋盘横向线
    for i in range(8):
        pygame.draw.line(screen, 'black', (25, 25 + i * 100), (925, 25 + i * 100), 1)

    # 棋盘纵向线
    for i in range(10):
        pygame.draw.line(screen, 'black', (25 + i * 100, 25), (25 + i * 100, 725), 1)

    # turn决定回合  0绿回合
    turn = 1
    (mx, my) = (0, 0)
    (mmx, mmy) = (0, 0)
    currentAnimal = None

    # 事件监听
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            exit('已结束')
        # 左键按下选中
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mx, my) = event.pos
            (mx, my) = getPosition(mx, my)
            for i in (greenTargets if (turn % 2) == 0 else redTargets):
                if (i.x, i.y) == (mx, my):
                    if i.targetName in ["trap", "home"]:
                        continue
                    currentAnimal = i
                    break
        # 左键松开判断：1.是否在允许单元格 2.是否有动物占据 3.
        if event.type == pygame.MOUSEBUTTONUP:
            # 获取松开点坐标
            (mmx, mmy) = event.pos
            # 获取坐标格中心点
            (mmx, mmy) = getPosition(mmx, mmy)
            # 尝试移动
            if currentAnimal == None:
                continue
            elif currentAnimal.targetLevel >= 0:
                if currentAnimal.move(mmx, mmy):
                    turn += 1
                    currentAnimal = None
            print("red" if turn % 2 == 1 else "green")

        pygame.display.flip()
