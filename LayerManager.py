class LayerManager:
    def __init__(self):
        self.object_list = []
        self.count = 0
        self.selected = None

    def register(self, ShapeObject):
        if self.count == 0:
            self.object_list.append(ShapeObject)
            self.count = 30 * 0.5
            self.selected = ShapeObject

    def getSelectedObj(self):
        if self.selected != None:
            return self.selected
        else:
            return None

    def cancelSelection(self):
        self.selected = None
        for obj in self.object_list:
            obj.nonSelected()

    def selectObj(self, ShapeObject):
        if self.selected != None:
            print("Selection Failure")
        else:
            self.selected = ShapeObject
            self.updateObj(ShapeObject)

    def updateObj(self, ShapeObject):
        obj = self.pickUpObj(ShapeObject)
        self.object_list.append(obj)

    def checkHit(self, coodinates):
        for obj in reversed(self.object_list):
            if coodinates != ():
                if obj.isHit(coodinates):
                    self.selectObj(obj)
                    return obj
            else:
                obj.nonSelected()

    def delete(self, ShapeObject):
        self.selected = None
        self.pickUpObj(ShapeObject)

    def pickUpObj(self, ShapeObject):
        value = ShapeObject
        for idx, obj in enumerate(self.object_list):
            if obj is ShapeObject:
                value = self.object_list.pop(idx)
                return value
        return ShapeObject

    def draw(self, img):
        if self.count != 0:
            self.count -= 1
        for obj in self.object_list:
            obj.draw(img)
