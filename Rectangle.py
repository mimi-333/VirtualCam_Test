import Shape
import cv2
import math


class Rectangle(Shape.Shape):
    def __init__(self, coodinates=((0, 0), (0, 0)), color=(255, 255, 255)):
        self.coodinates = coodinates    # (x1,y1),(x2,y2)
        self.color = color
        self.selected = False

    def expand(self, coodinates):
        self.selected = True
        self.coodinates = coodinates

    def move(self, coodinates):
        self.selected = True
        diff = [0, 0]
        for i in range(len(coodinates)):
            diff[i] = coodinates[i] - \
                (self.coodinates[0][i] + self.coodinates[1][i]) / 2

        coodinates = [[] for i in range(2)]
        for i in range(len(self.coodinates)):
            coodinates[i] = list(self.coodinates[i])

        for i in range(len(self.coodinates)):
            for j in range(len(self.coodinates[i])):
                coodinates[i][j] += diff[j]

        for i in range(len(coodinates)):
            coodinates[i] = tuple(coodinates[i])

        self.coodinates = tuple(coodinates)

    def isHit(self, coodinates):
        xy_range = [[self.coodinates[0][0], self.coodinates[1][0]],
                    [self.coodinates[0][1], self.coodinates[1][1]]]

        for i in range(2):
            xy_range[i] = [min(xy_range[i]), max(xy_range[i])]

        if xy_range[0][0] <= coodinates[0] <= xy_range[0][1]:
            if xy_range[1][0] <= coodinates[1] <= xy_range[1][1]:
                return True
        return False

    def nonSelected(self):
        self.selected = False

    def draw(self, img):
        color = self.color
        if self.selected:
            color = (255, 0, 0)

        img_height, img_width, _ = img.shape

        # (x1,x2), (y1,y2)
        rect_shape = [[self.coodinates[0][0] * img_width,
                       self.coodinates[1][0] * img_width],
                      [self.coodinates[0][1] * img_height,
                       self.coodinates[1][1] * img_height]]

        for i in range(len(rect_shape)):
            for j in range(len(rect_shape[i])):
                rect_shape[i][j] = math.floor(rect_shape[i][j])

        for idx, value in enumerate(rect_shape[0]):
            if value < 0:
                rect_shape[0][idx] = 0
            if img_width <= value:
                rect_shape[0][idx] = img_width - 1

        for idx, value in enumerate(rect_shape[1]):
            if value < 0:
                rect_shape[1][idx] = 0
            if img_height <= value:
                rect_shape[1][idx] = img_height - 1

        cv2.rectangle(img, (rect_shape[0][0], rect_shape[1][0]),
                      (rect_shape[0][1], rect_shape[1][1]), color, thickness=-1)
