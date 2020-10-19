from PIL import Image
import random

class Mess():
    def __init__(self, parent=None):
        self.map=[]
        self.dim=3
        self.image_cuts=[]
    def mess(self) -> object:
        im_path = "pics/H_.jpg"
        dim = 3
        image = Image.open(im_path)
        x = image.size[0] / dim
        y = image.size[1] / dim
        # 计算出XY在此维度下应有的大

        # 清空图片碎的列表

        # 按照XY的大小切割图片
        count = 0
        for j in range(dim):
            for i in range(dim):
                # 将最后一块置为白色
                if count == dim * dim - 1:
                    a_image = Image.new('RGB', (image.size[0], image.size[1]), color='#FFFFFF')
                    area = (0, 0, x, y)
                    im = a_image.crop(area)
                    self.image_cuts.append(im)
                    count = count + 1
                    break

                area = (i * x, j * y, i * x + x, j * y + y)

                im = image.crop(area)
                self.image_cuts.append(im)
                count = count + 1

        # 数组形态的图赋初值
        flag=False
        for k in range(count - 1):
            self.map.append(k + 1)
        self.map.append(0)
        number = count
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

                self.image_cuts[n], self.image_cuts[m] = self.image_cuts[m], self.image_cuts[n]
                self.image_cuts[m], self.image_cuts[o] = self.image_cuts[o], self.image_cuts[m]

                self.map[n], self.map[m] = self.map[m], self.map[n]
                self.map[m], self.map[o] = self.map[o], self.map[m]
            # 判断是否有解
            flag = self.whether_reduction()
        # 将图片碎拼回图片（方法在下面）
        image_save=self.combine()
        # 显示完整图片（方法在下面）
        # 将白块赋为0
        self.white = self.map.index(0)
        image_save.save(r'pics/mess.png')


    # 合并图片的方法
    def combine(self):
        # 新建一张图片
        new_image = Image.new('RGBA', (900, 900))
        count = 0
        x = 300
        y = 300
        # 将碎图片拼好存为新图
        for j in range(self.dim):
            for i in range(self.dim):
                location = (int(i * x), int(j * y))
                new_image.paste(self.image_cuts[count], location)
                count = count + 1
        # deep复制新图
        combine_image = new_image.copy()
        return combine_image


    def whether_reduction(self):

        res = 0
        count = 9
        for i in range(count):
            for j in range(i+1, count):
                if self.map[j] == 0:
                    continue
                if self.map[j] < self.map[i]:
                    res += 1

        if res % 2 == 0 or (res + abs(int(self.map.index(0) / self.dim) - (self.dim - 1))) % 2 == 0:
            return True
        return False


def main():
    #    img=mess()
    #    img.save("./source/mess.jpg")
    a=Mess()
    a.mess()








main()