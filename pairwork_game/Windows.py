from PyQt5.QtWidgets import QApplication
from pair_work import Ui_MainWindow
from Scene import Scene
import sys
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5 import QtWidgets, QtGui
from PIL import Image, ImageQt
import random

class MyMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        #调用Ui_MainWindow开启Ui
        self.setupUi(self)



        # 将可以进行的操作的判断赋初值
        self.if_opened = False
        self.if_upset = False


        # 定位白块的位置
        # 方向
        # 0  1  2  3
        # 上 下 左 右
        self.white = -1
        self.direction = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        #最后利用此输出答案路径
        self.step_direction = [0, 1, 2, 3]

        #为了实现功能而需要的各种参数如下
        # 图像，保存原始图片
        self.image = None
        # 存储图像文件路径
        self.image_name = None
        # 场景，这里的scene是Scene的一个实例
        self.scene = Scene(self)
        # 列表元素总数，分块总数
        self.number = 9
        # 分块的图片列表
        self.image_cuts = []
        # 图的数组保存形式
        self.map = []
        # 合并的图片（主要操作展示对象）
        self.combine_image = None

        # 维度
        self.dim = 3
        # 单个边长 （width, height）
        self.x = 0
        self.y = 0

        # 槽函数（将按钮与功能连接起来）
        self.mess.clicked.connect(self.Upset)
        self.choose.clicked.connect(self.openfile)
        self.Read.clicked.connect(self.progress_read)

        self.Save.clicked.connect(self.progress_save)


        #计数
        self.c=0





    #鼠标控制还原
    def mousePressEvent(self, event):

        if self.scene.x == -1 or self.scene.y == -1:
            return
        if self.scene.if_make_upset is False:
            return
        x_rem = self.scene.x % self.x
        y_rem = self.scene.y % self.y
        x = int(self.scene.x / self.x)
        y = int(self.scene.y / self.y)

        if x_rem > 0:
            x += 1
        if y_rem > 0:
            y += 1
        s = (y-1)*self.dim + (x-1)

        if s == self.scene.now_selected:
            return
        if self.map[s] == 0:
            return

        self.scene.now_selected = s
        self.white = self.map.index(0)

        """
        横为 x 上 方向右
        竖为 y 左 方向下
        """
        tx = int(self.white / self.dim)
        ty = int(self.white % self.dim)

        find = False
        for i in range(4):
            sx = tx + self.direction[i][0]
            sy = ty + self.direction[i][1]

            if sx > self.dim-1 or sx < 0 or sy > self.dim-1 or sy < 0:
                continue
            if self.map[sx*self.dim + sy] == self.map[s]:
                find = True
                break

        if find:
            self.map[self.white], self.map[s] = self.map[s], self.map[self.white]
            self.image_cuts[self.white], self.image_cuts[s] = self.image_cuts[s], self.image_cuts[self.white]

            self.white = s

            self.combine()
            self.show_image()
        else:
            return


    #打乱图片的方法（mess功能对应的函数）
    def Upset(self):



        # 判断原图是否为空
        if self.image is None:
            return

        flag = False
        #将打乱置为True
        self.if_upset = True
        #记录图片被打乱，未选择图片，x,y赋初值
        self.scene.if_make_upset = True
        self.scene.x = -1
        self.scene.y = -1
        self.scene.now_selected = -1
        self.x = self.image.size[0] / 3
        self.y = self.image.size[1] / 3
        #计算出XY在此维度下应有的大小
        x = self.x
        y = self.y
        #清空图片碎的列表
        self.image_cuts.clear()
        #按照XY的大小切割图片
        count = 0
        for j in range(3):
            for i in range(3):
                #将最后一块置为白色
                if count == 8:
                    a_image = Image.new('RGB', (self.image.size[0], self.image.size[1]), color='#FFFFFF')
                    area = (0, 0, x, y)
                    im = a_image.crop(area)
                    self.image_cuts.append(im)
                    count = count + 1
                    break

                area = (i * x, j * y, i * x + x, j * y + y)
                image = self.image
                im = image.crop(area)
                self.image_cuts.append(im)
                count = count + 1

        # 数组形态的图赋初值
        self.map.clear()
        for k in range(count - 1):
            self.map.append(k + 1)
        self.map.append(0)
        self.number = count
        while flag is False:
            # 打乱图片碎
            for i in range(int((count / 3) * (count / 3)) + 1):
                n = random.randint(0, count - 1)
                m = n
                while n == m:
                    m = random.randint(0, count - 1)
                o = m
                while o == m or o == n:
                    o = random.randint(0, count - 1)
                if n > m:
                    n, m = m, n
                if m > o:
                    m, o = o, m
                self.map[n], self.map[m] = self.map[m], self.map[n]
                self.map[m], self.map[o] = self.map[o], self.map[m]
                self.image_cuts[n], self.image_cuts[m] = self.image_cuts[m], self.image_cuts[n]
                self.image_cuts[m], self.image_cuts[o] = self.image_cuts[o], self.image_cuts[m]


            #判断是否有解
            flag = self.whether_reduction()
        #将图片碎拼回图片（方法在下面）
        self.combine()
        #显示完整图片（方法在下面）
        self.show_image()
        #将白块赋为0
        self.white = self.map.index(0)

    #合并图片的方法
    def combine(self):
        #新建一张图片
        new_image = Image.new('RGBA', (self.image.size[0], self.image.size[1]))
        count = 0
        #将碎图片拼好存为新图
        for j in range(3):
            for i in range(3):
                location = (int(i * self.x), int(j * self.y))
                new_image.paste(self.image_cuts[count], location)
                count = count + 1
        #deep复制新图
        self.combine_image = new_image.copy()

    #读取图片文件的方法（choose功能对应的函数）
    def openfile(self):

        #如果已经有图片被打开了，那么清空画布
        if self.if_opened is True:
            self.scene.clear()
        #设此时没有图片被打乱
        self.if_opened = True
        self.scene.if_make_upset = False
        #获得图片的名字和类型，这几种图片类型都可以打开
        image_name, image_type = QFileDialog.getOpenFileName(self, "选择图片", "./pics","*.jpg;;*.png;;*.bmp;;All Files (*)")
        #打开对应的文件
        self.image = Image.open(image_name)
        #将图片赋给合并的图片（
        self.combine_image = self.image
        self.image_name = image_name
        #按照大小缩放图片
        pix = QtGui.QPixmap(image_name)
        item = QtWidgets.QGraphicsPixmapItem(pix)
        self.scene.addItem(item)
        self.View.setScene(self.scene)




    #显示图片的方法
    def show_image(self):
        #清空画布
        self.scene.clear()
        #图片赋值
        image = ImageQt.ImageQt(self.combine_image)
        #缩放图片
        pix = QtGui.QPixmap.fromImage(image)
        item = QtWidgets.QGraphicsPixmapItem(pix)
        self.scene.addItem(item)
        self.View.setScene(self.scene)


    #保存进度的方法（Save功能对应的函数）
    def progress_save(self):

        #如果被打乱
        if self.if_upset:
            #将图片碎拼成图片
            self.combine()
            #将当时状态的拼接图片保存到文件夹中并命名待用
            self.combine_image.save("./pics/combine_image.bmp")
            #将原本的图片保存在文件夹中,这里我也不知道为什么只能存为bmp
            self.image.save("./pics/save.bmp")
            #打开text文件夹中的文件list
            file = open('./text/list.txt', 'w')
            #将映射存入list.txt
            for i in range(len(self.map)):
                file.write(str(self.map[i]))
                file.write('\t')
            #将维度存入维度文档
           # file = open('./text/dim.txt', 'w')
           # file.write(str(self.dim))
           # file.close()
        return

    #读取进度的方法（Read功能对应的函数）
    def progress_read(self):

        #清空画布
        if self.if_opened is True:
            self.scene.clear()

        self.if_opened = True
        self.scene.if_make_upset = True
        self.if_upset = True
        self.scene.now_selected = -1
        #读取保存进度时的图片
        image_name = "./pics/combine_image.bmp"
        self.combine_image = Image.open(image_name)
        self.image = Image.open("./pics/save.bmp")
        self.image_name = image_name

        # 选择维度
        # self.dim = self.selectHard.value()
        #读取维度文件
       # file = open('./text/dim.txt', 'r')
       # data = file.read()
       # self.dim = int(data)
       # file.close()
        dim=3
       # dim = self.dim
        #根据维度获得XY
        self.x = self.combine_image.size[0] / dim
        self.y = self.combine_image.size[1] / dim
        x = self.x
        y = self.y

        # 分块信息清空
        self.image_cuts.clear()
        self.map.clear()
        #再次切割图片
        count = 0
        for j in range(dim):
            for i in range(dim):
                area = (i * x, j * y, i * x + x, j * y + y)
                image = Image.open(self.image_name)
                im = image.crop(area)
                self.image_cuts.append(im)
                count = count + 1

        # 将保存的数组形态的List赋值给List
        file = open('./text/list.txt', 'r')
        #按行读取内容
        data = file.readlines()
        #临时存储
        map1 = []
        for i in data:
            k = i.strip()
            j = k.split('\t')
            map1.append(j)
        file.close()
        for i in range(len(map1[0])):
            self.map.append(int(map1[0][i]))
        self.number = count
        #将图片碎拼起来并显示
        self.combine()
        self.show_image()

        self.image_name = "./pics/save.bmp"



    #判断是否能够还原
    def whether_reduction(self):

        res = 0
        count = self.number
        for i in range(count):
            for j in range(i+1, count):
                if self.map[j] == 0:
                    continue
                if self.map[j] < self.map[i]:
                    res += 1

        if res % 2 == 0 and self.dim == 3 or (res + abs(int(self.map.index(0) / self.dim) - (self.dim - 1))) % 2 == 0:
            return True
        return False




if __name__=="__main__":
    app=QApplication(sys.argv)
    myWin=MyMainWindow()
    myWin.show()
    sys.exit(app.exec())