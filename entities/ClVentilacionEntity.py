from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *


#Importo las entidades
from .ClTramosEntity import ClTramosEntity



class ClVentilacionEntity():
    
    def __init__(self):
        
        self.cl_ventilacion_layer = None
        
    def initialize(self, cl_ventilacion):
        
        self.cl_ventilacion_layer = cl_ventilacion
        
        
    def addVentilacion(self, tramo):
        
        #distancia a la que se agregara el nodo de ventilacion
        distance = 6
        
        #obtengo el id del tramo
        id_tramo = tramo.id()
        
        #obtengo el angulo de los dos puntos.. Primero obtengo el tramo como vertices
        cl_tramos_entity = ClTramosEntity()
        
        tramo_array_point = cl_tramos_entity.getVertexTramoAsPoint(tramo)
        
        angulo = self.getAngleVertex1_2(tramo_array_point)

        #convierto el feat a geometry
        geom_tramo = tramo.geometry()
        
        #Obtengo el punto de la interpolacion
        point = geom_tramo.interpolate(distance).asPoint()
        
        self.cl_ventilacion_layer.startEditing()
        
        #obtengo los atributos
        attrs = [None] * len(self.cl_ventilacion_layer.fields())
        
        #obtengo el id de la clave foranea
        idx_tramo = self.cl_ventilacion_layer.fields().indexFromName("tramo_idtramo")
        idx_angulo = self.cl_ventilacion_layer.fields().indexFromName("angulo")

        #asigno el id a la clave foranea
        attrs[idx_tramo] = id_tramo
        attrs[idx_angulo] = angulo
        
        #creo un feature
        feature = QgsFeature()

        feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(point.x(), point.y())))

        feature.setAttributes(attrs)
        res = self.cl_ventilacion_layer.addFeature(feature)
        
        if res:
            
            if self.cl_ventilacion_layer.commitChanges():
                return True
            else:
                self.cl_ventilacion_layer.rollBack()
                return False
        else:
            return False
        
        
    
    def getAngleVertex1_2(self, array_vertex):
        
        #Obtengo los dos vertices iniciales
        point1 = array_vertex[0]
        point2 = array_vertex[1]
        
        res = point1.azimuth(point2)
        
        return res
    
    
    def deleteVentilacion(self, tramo):
        
        id_tramo = tramo['gid']
        
        for feat in self.cl_ventilacion_layer.getFeatures():
            
            if feat['tramo_idtramo'] == id_tramo:
                self.cl_ventilacion_layer.startEditing()
                
                res = self.cl_ventilacion_layer.deleteFeature(feat.id())
                if res:
            
                    if self.cl_ventilacion_layer.commitChanges():
                        return True
                    else:
                        self.cl_ventilacion_layer.rollBack()
                        return False
    
        return False 
