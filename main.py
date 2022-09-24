'''
2022.9.20
近日复习了Python基础，想要实际做一些项目，
选择做一个贪吃蛇的小游戏来锻炼自己的编程能力

'''

'''
思路：
1.开发工具选择pygame：
   pygame可以对程序的框架进行制作

一个小蛇，有初始长度，循环检测键盘按键的’wasd‘改变它行动的方向，它的行动有速度

随机生成食物，

小蛇吃到食物增长

小蛇撞到墙，或者自己，会死亡
'''
import random
import pygame
import keyboard
class Snake(object):

    def __init__(self,direction,x,y):   # 小蛇初始位置(x,y)由鼠标的点击来决定，移动方向direction
        self.direction = direction
        self.x = x
        self.y = y
        self.len = 10
        self.alive = True
        self.body = []
        self.turn_left_times = 0
        self.turn_right_times = 0
        for i in range(0,self.len):
            self.body.append([self.x,self.y+i ])
        self.head = self.body[0]

    def turn_left(self):
        print('turn left')
        if self.direction == 1:
            self.head[0] = self.head[0] - 1
            self.direction = 3

        elif self.direction == 2:
            self.head[0] = self.head[0] + 1
            self.direction = 4

        elif self.direction == 3:
            self.head[1] = self.head[1] - 1
            self.direction = 2

        elif self.direction == 4:
            self.head[1] = self.head[1] + 1
            self.direction = 1
        self.body[0] = self.head
        print(self.direction)
    def turn_right(self):
        print('turn right')
        if self.direction == 1:
            self.head[0] = self.head[0] + 1
            self.direction = 4

        elif self.direction == 2:
            self.head[0] = self.head[0] - 1
            self.direction = 3

        elif self.direction == 3:
            self.head[1] = self.head[1] + 1
            self.direction = 1

        elif self.direction == 4:
            self.head[1] = self.head[1] - 1
            self.direction = 2

        self.body[0] = self.head
        print(self.direction)
    def go_on(self):
        if self.direction == 1:
            self.head[1] = self.head[1] + 1
        elif self.direction == 2:
            self.head[1] = self.head[1] - 1
        elif self.direction == 3:
            self.head[0] = self.head[0] - 1
        elif self.direction == 4:
            self.head[0] = self.head[0] + 1
        self.body[0] = self.head

    def move(self):   #小蛇在转折点，断开，被视为2条线 #只有左右两个方向
        # for i in range(self.len-1, 1, -1):
        #     self.body[i]=self.body[i-1] #身体2-尾节的更新
        #
        # [x, y] = self.head
        # self.body[1] = [x, y] #第2节的更新
        #
        # key_list = pygame.key.get_pressed()
        # if key_list[pygame.K_LEFT]:
        #     self.turn_left()
        #     self.turn_left_times += 1
        #
        # if key_list[pygame.K_RIGHT]:
        #     self.turn_right()
        #     self.turn_right_times += 1
        #
        # self.go_on()  #     头部的更新
        # 不知道为什么,用get_pressed()很坑,转向函数会被多次调用


# '''
# 在转向这里我犯了一个愚蠢的错误，把四个方向设为1，2，3，4。然后写了四个并列的if
# 结果本意是让他们中只有一个运行
# 结果它们会顺着运行，导致结果令人迷惑
# 如果只想让一个选项运行，千万要检查这种顺序，并列的语句会不会按顺序发生好多次
# '''
        for i in range(self.len - 1, 1, -1):
            self.body[i] = self.body[i - 1]  # 身体2-尾节的更新
        [x, y] = self.head
        self.body[1] = [x, y]  # 第2节的更新
    def draw(self,screen):
        for i in range(0,self.len):
            pygame.draw.circle(screen,(0,0,0),(self.body[i][0],self.body[i][1]),2,1)
        # pygame.draw.circle(screen,(0,0,0),(self.x, self.y), 15,1)

    def eat(self,Food):
        distance =  ( (self.head[0] - Food.x)**2 + (self.head[1] - Food.y)**2 )**(1/2)
        if distance <= 3:
            Food.eaten()
            self.len += 1
            self.body.append([])

    def die(self):
        if self.head[0] < 0 or self.head[0] > 800 or self.head[1] < 0 or self.head[1] > 600:
            self.alive =False
            print('die')
        for i in range(0,self.len):
            for j in range(0,self.len):
                if self.body[i] == self.body[j] and i != j:
                    self.alive = False
                    print('die')


class Food(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.remain=True
    def pop(self,screen):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 3, 3)

    def eaten(self):
        self.remain=False

def main():
    count = 0  # 调查turn函数连续调用的计数器
    foods=[]
    counter=0
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    # 设置当前窗口的标题
    pygame.display.set_caption('贪吃蛇')
    # 设置窗口名称
    running = True
    born = False
    while running:
        # 从消息队列中获取事件并对事件进行处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not born:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x,y = event.pos
                    direction = random.randint(1,4)
                    snake = Snake(direction,x,y)
                    born = True
            if born:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        snake.turn_left()
                    if event.key == pygame.K_LEFT:
                        snake.turn_right()

        screen.fill((255, 255, 255))

        if born:
            snake.move()
            snake.go_on()
            snake.draw(screen)
            snake.die()
            if snake.alive == False:
                born = False
                foods.clear()

        counter += 1
        if counter == 50:
            fx = random.randint(1,800)
            fy = random.randint(1,600)
            food=Food(fx,fy)
            foods.append(food)
            counter = 0

        for food in foods:
            if born:
                snake.eat(food)
            if food.remain:
                food.pop(screen)

        pygame.display.flip()
        pygame.time.delay(10)


if __name__ == '__main__':
    main()

