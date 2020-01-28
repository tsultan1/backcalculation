from matplotlib.widgets import RectangleSelector

class PersistentRectangleSelector(RectangleSelector):

    def release(self, event):
        super(PersistentRectangleSelector, self).release(event)
        self.to_draw.set_visible(True)
        self.canvas.draw()