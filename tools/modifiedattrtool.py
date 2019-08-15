from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from qgis.gui import *
#from qgis.core import QgsFeature, QgsGeometry, QgsPoint

class ModifiedAttrTool(QgsMapTool):
    
    select_ = pyqtSignal(object)
    
    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())

        self.iface = iface
        self.qpoint = None
        self.geom_Sel = None
        self.canvas = iface.mapCanvas()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                  "      c None",
                                  ".     c #FF0000",
                                  "+     c #FFFFFF",
                                  "                ",
                                  "       +.+      ",
                                  "      ++.++     ",
                                  "     +.....+    ",
                                  "    +.     .+   ",
                                  "   +.   .   .+  ",
                                  "  +.    .    .+ ",
                                  " ++.    .    .++",
                                  " ... ...+... ...",
                                  " ++.    .    .++",
                                  "  +.    .    .+ ",
                                  "   +.   .   .+  ",
                                  "   ++.     .+   ",
                                  "    ++.....+    ",
                                  "      ++.++     ",
                                  "       +.+      "]))
    
        
    def canvasPressEvent(self,e):
       self.qpoint = self.toMapCoordinates(e.pos())
            
    def canvasMoveEvent(self,event):
         pass
  
    def canvasReleaseEvent(self,event):

        res = self.selecciona(self.qpoint)
        
        if res == True:
            layer = self.canvas.currentLayer()
            #inicio la edicion
            layer.startEditing()
            form = self.iface.getFeatureForm(layer, self.geom_Sel)
            form.setModal(True)
            
            #Devuelve 1 si apreta ACEPTAR o 0 si CANCELAR
            aa = form.exec_()
            
            if aa == 1:
                layer.commitChanges()
            else:
                layer.rollBack()
            #form.show()
            
        else:
            self.select_.emit(False)

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def deactivate(self):

        pass
    
    def selecciona(self, point):
        
        #Borro la seleccion actual
        mc = self.iface.mapCanvas()
        
        for layer in mc.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
            mc.refresh()
        
        pntGeom = QgsGeometry.fromPointXY(self.qpoint)
        pntBuffer = pntGeom.buffer((mc.mapUnitsPerPixel()*2), 0)
        rectan = pntBuffer.boundingBox()
        cLayer = mc.currentLayer()
        cLayer.selectByRect(rectan,False)
        
        feats = cLayer.selectedFeatures()
        n = len(feats)

        #si n es mayor a1 deselecciono todo los demas a expecion del primer elemento
        if n >= 1:
            if n > 1:
                i = 1
                
                while (i < n):
                    cLayer.deselect(feats[i].id())
                    i = i + 1

                self.geom_Sel = cLayer.selectedFeatures()[0]
            
            else:
                self.geom_Sel = cLayer.selectedFeatures()[0]
            
            mc.refresh()
            return True
        else:
            return False
        
        
        