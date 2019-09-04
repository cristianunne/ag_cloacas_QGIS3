from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *



class ClNodosTramosEntity():
    
    def __init__(self):
       
       self.cl_nodos_tramos_layer = None
       
    
    def initialize(self, cl_nodos_tramos_layer):
        
        self.cl_nodos_tramos_layer = cl_nodos_tramos_layer
        
        
        
    
    def addNodoTramo(self, id_tramo, id_cl_nodo):

        attr = [None] * len(self.cl_nodos_tramos_layer.fields())
        
        idx_id_tramo = self.cl_nodos_tramos_layer.fields().indexFromName("tramo_idtramo")
        idx_cl_nodo = self.cl_nodos_tramos_layer.fields().indexFromName("cl_nodos_id_cl_nodos")
     
        attr[idx_id_tramo] = id_tramo
        attr[idx_cl_nodo] = id_cl_nodo
        
        #inicio la edicion
        self.cl_nodos_tramos_layer.startEditing()
        
        feat = QgsFeature()
        feat.setAttributes(attr)
        
        if self.cl_nodos_tramos_layer.addFeature(feat):
          
            if self.cl_nodos_tramos_layer.commitChanges():
               
                return True
            else:
                self.cl_nodos_tramos_layer.rollBack()
                
                return False
        else:
            return False
        
        
    def deleteNodosTramos(self, feat_delete):

        self.cl_nodos_tramos_layer.startEditing()
        res = self.cl_nodos_tramos_layer.deleteFeature(feat_delete.id())
            
        if res:
                
            if self.cl_nodos_tramos_layer.commitChanges():
                return True
            else:
                self.cl_nodos_tramos_layer.rollBack()
                return False
        else:
            return False



