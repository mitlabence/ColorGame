from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

COLOR_NAMES = {100: "red", 10: "green", 1: "blue", 11: "cyan", 110: "yellow", 101: "magenta", 111: "white", 000: "black" }
QT_COLORS = {"red": Qt.red, "green": Qt.green, "blue": Qt.blue, "cyan": Qt.cyan, "yellow": Qt.yellow, "magenta": Qt.magenta, "white": Qt.white, "black": Qt.black}


class Color:
    def __init__(self, r, g, b):
        self.update(r, g, b)
    def update(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.val = 100*self.r + 10*self.g + self.b
        self.name = COLOR_NAMES[self.val]
    def __add__(self, other_color):
        """
        Move in the RGB spectrum. To the original color "color", add "add_color" following the rules:
        R + R = R, same for G and B
        R + G = Y
        R + B = M
        G + B = C
        R + B + G = W (White)
        """
        return Color(self.r or other_color.r, self.g or other_color.g, self.b or other_color.b)
    def __str__(self):
        """
        Print name of color.
        """
        return COLOR_NAMES[int(f"{self.r}{self.g}{self.b}")]
    def __eq__(self, other_color):
        return ((self.r == other_color.r) and (self.g == other_color.g) and (self.b == other_color.b))
    def getQtColor(self):
        return QT_COLORS[self.name]


COLORS = {"white": Color(1, 1, 1)}

from random import randint #for random color generation
def generateRandomColor():
    return Color(randint(0, 1), randint(0, 1), randint(0, 1))

"""
TODO https://www.learnpyqt.com/examples/moonsweeper/ use this to set up a grid of fixed size.
"""

class Tile(QWidget):
    color_change = pyqtSignal(int, int, Color)
    def __init__(self, x, y, color, *args, **kwargs):
        super(Tile, self).__init__(*args, **kwargs)
        #self.setFixedSize(QSize(40, 40))
        self.x = x
        self.y = y
        self.color = color

    def paintEvent(self, event):
        """
        What happens on click is implemented here
        """
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        r = event.rect()

        outer, inner = Qt.gray, self.color.getQtColor()

        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)
    
    def addColor(self, new_color):
        self.color = self.color + new_color

    def click(self):
        if self.color != COLORS["white"]:
            self.color_change.emit(self.x, self.y, self.color)
            self.color.update(0, 0, 0)
            self.update()
    def mouseReleaseEvent(self, e):
        if (e.button() == Qt.LeftButton):
            self.click()

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.b_size = 16

        w = QWidget()
        vb = QVBoxLayout()

        self.grid = QGridLayout()
        self.grid.setSpacing(1)

        vb.addLayout(self.grid)
        w.setLayout(vb)
        w.setFixedSize(800, 800)

        self.setCentralWidget(w)

        self.init_map()
        self.show()
    def init_map(self):
        # Add positions to the map
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = Tile(x, y, generateRandomColor())
                self.grid.addWidget(w, y, x)
                w.color_change.connect(self.change_surrounding)
    def get_surrounding(self, x, y):
        """
        Returns a list of the neighboring Tile items.
        """
        positions = []
        for xi in range(max(0, x - 1), min(x + 2, self.b_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_size)):
                positions.append(self.grid.itemAtPosition(yi, xi).widget())
        return positions
    def change_surrounding(self, x, y, own_color):
        for tile in self.get_surrounding(x, y):
            tile.addColor(own_color)
            tile.update()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()


"""
TODO: Create interesting rules. An idea: whenever a tile changes white, it "explodes", and all neighbors get the same color as it did to turn white. I.e. if it got red added, then all neighbors get red added.
"""