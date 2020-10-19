#QGraphicsScene是一个可视化的界面，只管理项目
from PyQt5.QtWidgets import QGraphicsScene


class Scene(QGraphicsScene):
    def __init__(self, parent=None):
        super(Scene, self).__init__(parent)
        #用x,y定位鼠标位置，在一开始都置为-1
        self.x = -1
        self.y = -1
        # 判断是否打乱过与是否选择过图片
        self.if_upset = False
        self.now_selected = -1


    #在该Scene上记录鼠标点击的动作
    def mousePressEvent(self, event):
        if self.if_make_upset is False:
            return
        pos = event.scenePos()
        self.x = pos.x()
        self.y = pos.y()