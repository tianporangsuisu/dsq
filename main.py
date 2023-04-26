
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
# 上方水格
waterPosition1 = [(376, 176), (476, 176), (576, 176), (376, 276), (476, 276), (576, 276)]
# 下方水格
waterPosition2 = [(376, 476), (476, 476), (576, 476), (376, 576), (476, 576), (576, 576)]

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

    def __init__(self, x, y, targetName, targetLevel):
        self.x = x
        self.y = y
        self.targetName = targetName
        self.targetLevel = targetLevel


class Water(Target):
    def __init__(self, x, y):
        super().__init__(x, y, 'water', -4)


class Blank(Target):
    def __init__(self, x, y):
        super().__init__(x, y, 'blank', -3)


class Home(Target):
    def __init__(self, x, y):
        super().__init__(x, y, 'home', -2)


class Trap(Target):

    def __init__(self, x, y):
        super().__init__(x, y, 'trap', -1)


class NormalAnimal(Target):
    isTrapped = False
    isAlive = False

    def __init__(self, x, y, targetName, targetLevel, isTrapped, isAlive):
        super().__init__(x, y, targetName, targetLevel)
        self.isTrapped = isTrapped
        self.isAlive = isAlive

    # 只考虑移动
    def move(self, targetX, targetY):
        toMove = [(targetX+100,targetY),(targetX-100,targetY),(targetX,targetY+100),(targetX,targetY-100)]
        # 可以移动
        if (targetX,targetY) in toMove:
            # 普通动物不许走河
            if (targetX, targetY) in waterPosition1:
                return False

            # 调用方法移动，更新属性，有动物就调用自身吃方法
            for i in

            if (targetX, targetY) in [(self.x + 100, self.y), (self.x, self.y + 100), (self.x - 100, self.y),
                                      (self.x, self.y - 100)]:
                self.x = targetX, self.y = targetY
                return True
            return False


    def tryEat(self, targetLevel, isTrapped):
        if targetLevel == -1:
            self.isTrapped = True
            return True
        if (self.targetLevel > targetLevel & self.isTrapped != True) | isTrapped == True:
            return True
        return False


class SpecialAnimal(NormalAnimal):
    def __init__(self, x, y, targetName, targetLevel,isAlive,isTrapped):
        super().__init__(x, y, targetName, targetLevel,isAlive,isTrapped)

    def jumpOver(self):
        if True:
            return True


def getPosition(x, y):
    for i in range(7):
        if abs(x - 76 - 100 * i) < 50:
            mx = 76 + 100 * i
            for j in range(9):
                if abs(y - 76 - 100 * j) < 50:
                    my = 76 + 100 * j
                    return mx, my
    return -1, -1


def getTarget(turn, x, y):
    (mx, my) = getPosition(x, y)
    if (mx, my) == (-1, -1):
        return -5
    if turn == 0:
        for target in redTargets:
            if target.x == y & target.y == y:
                return target.targetLevel
    else:
        for target in greenTargets:
            if target.x == y & target.y == y:
                return target.targetLevel
    return

def move(oldx,oldy,newx,newy,turn):
    for i in (greenPositions if turn == 0 else redPositions):
        # 原地不动
        if (i[0], i[1]) == (mmx, mmy):
            print("未移动")
        # 上下左右移动
        else:
            # 获取可以移动的单元格
            moves = getMove(oldx,oldy)
            # 目的地可以移动到
            if (newx,newy) in moves:
                # 循环校验目的地是否有敌对动物
                for j in (redPositions if turn == 0 else greenPositions):
                    # 目的地有敌对动物
                    if (j[0], j[1]) == (newx,newy):
                        # 我是大象 你是老鼠
                        if i[3]==7 & j[3]==0:
                            1







def getMove(x,y):
    toMove = []
    # 右侧移动
    if (x,y+100) in waterPosition:
        toMove.append((x,y+300))
    else:
        toMove.append((x, y + 100))

    # 上侧移动
    if (x+100,y) in waterPosition:
        toMove.append((x+400,y))
    else:
        toMove.append((x+100,y))

    # 左侧移动
    if (x, y - 100) in waterPosition:
        toMove.append((x, y - 300))
    else:
        toMove.append((x, y - 100))

    # 下侧移动
    if (x - 100, y) in waterPosition:
        toMove.append((x - 400, y))
    else:
        toMove.append((x - 100, y))

    return toMove

def printObj():
    1


if __name__ == "__main__":
    print(pygame.font.get_fonts())
    # 初始化
    pygame.init()
    f = pygame.font.SysFont(['fangsong', 'microsoftsansserif'], 25)

    # 设置表格大小    (100*7+50)*(100*9+50)   单格大小100*100 边框 25*25
    screen = pygame.display.set_mode((950, 750))
    pygame.display.set_caption("斗兽棋")
    screen.fill('white')

    # 创建空白格对象
    for i in blankPosition:
        blankTargets.append(Blank(i[0], i[1]))

    # 创建水格对象,画水单元格
    for i in waterPosition:
        waterTargets.append(Water(i[0], i[1]))
    pygame.draw.rect(screen, 'lightblue', (325, 125, 300, 200))
    pygame.draw.rect(screen, 'lightblue', (325, 425, 300, 200))

    # 绿方棋子对象及图像
    for i in greenPositions:
        pygame.draw.circle(screen, (0, 255, 0), (i[0], i[1]), 49)
        text = f.render(i[2], True, 'black')
        textRect = text.get_rect()
        textRect.center = (i[0], i[1])
        screen.blit(text, textRect)
        if i[2] in ["狮",'虎','鼠']:
            greenTargets.append(SpecialAnimal(i[0], i[1], i[2], i[3],True,False))
        else:
            greenTargets.append(NormalAnimal(i[0], i[1], i[2], i[3],True,False))
    # 红方棋子对象及图像
    for i in redPositions:
        pygame.draw.circle(screen, (255, 0, 0), (i[0], i[1]), 49)
        text = f.render(i[2], True, 'black')
        textRect = text.get_rect()
        textRect.center = (i[0], i[1])
        screen.blit(text, textRect)
        if i[2] in ["狮", '虎', '鼠']:
            greenTargets.append(SpecialAnimal(i[0], i[1], i[2], i[3], True, False))
        else:
            greenTargets.append(NormalAnimal(i[0], i[1], i[2], i[3],True,False))

    # 棋盘横向线
    for i in range(8):
        pygame.draw.line(screen, 'black', (25, 25 + i * 100), (925, 25 + i * 100), 1)

    # 棋盘纵向线
    for i in range(10):
        pygame.draw.line(screen, 'black', (25 + i * 100, 25), (25 + i * 100, 725), 1)


    # turn决定回合  0绿回合
    turn = 0
    (mx,my)=(0,0)
    (mmx,mmy)=(0,0)
    selectedAnimal = None

    # 事件监听
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            exit('已结束')
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mx, my) = event.pos
            (mx, my) = getPosition(mx, my)
            for i in (greenTargets if turn == 0 else redTargets):
                if (i.x,i.y)==(mx,my):
                    selectedAnimal = i
                    print(i.targetName+"is selected!")
                    break
        if event.type == pygame.MOUSEBUTTONUP:
            (mmx,mmy) = event.pos
            (mmx,mmy) = getPosition(mmx,mmy)
            selectedAnimal.move(mmx,mmy)

        pygame.display.flip()
