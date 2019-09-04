from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *

#Obtengo la clase de Tramos para convertir
from .ClTramosEntity import ClTramosEntity
import operator



class ClDirectionEntity():
    
    def __init__(self):
        
        self.cl_direction = None

    def initialize(self, cl_direction):
        
        self.cl_direction = cl_direction

    def addDirection(self, tramo_select):
        
        #instancio la clase cltramosentity
        self.cltramosentity = ClTramosEntity()
        
        #Obtengo los puntos del tramo seleccionado
        array_point_tramo =  self.cltramosentity.getVertexTramoAsPoint(tramo_select)
        
        #obtengo el centroide el tramo utilizando el lentg / 2 porque sino se sale de la linea
        long = tramo_select.geometry().length() / 2
        
        #hago una interpolacion en la linea y obtengo el punto medio
        centroide = tramo_select.geometry().interpolate(long).asPoint()

        #obtengo el numero de vertices
        num_ver =  self.cltramosentity.getNumVertex(tramo_select)
        diccionario = {}
        
        if num_ver > 2:
            i = 0
            for point in array_point_tramo:
                
                diccionario[i] = centroide.distance(QgsPointXY(point.x(), point.y()))
                i = i + 1
                
       
        resultado = sorted(diccionario.items(), key=operator.itemgetter(1))
       
        mem_line_segment = self.segmentLineToLine(tramo_select)
        
        linea_target = None
        
        for linea in mem_line_segment.getFeatures():
            buffer = QgsGeometry.fromPointXY(QgsPointXY(centroide.x(), centroide.y())).buffer(0.2, 1)
            
            if linea.geometry().intersects(buffer):
                linea_target = linea
       
        
        #obtengo los vertices de la linea target como point
        linea_target_point = self.cltramosentity.getVertexTramoAsPoint(linea_target)
        
        point_select = linea_target_point[1]
        
        #calculo el angulo de orientacion del icono
        angulo = centroide.azimuth(QgsPointXY(point_select.x(), point_select.y())) + 2
               
        #inicio la edicion de cl_direction
        id_tramo = tramo_select['gid']
        
        self.cl_direction.startEditing()
        
          #obtengo los atributos
        attrs = [None] * len(self.cl_direction.fields())
        
        #obtengo el id de la clave foranea
        idx_tramo = self.cl_direction.fields().indexFromName("tramo_idtramo")
        idx_angulo = self.cl_direction.fields().indexFromName("angulo")
        
        #asigno el id a la clave foranea
        attrs[idx_tramo] = id_tramo
        attrs[idx_angulo] = angulo
        
        #creo un feature
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(centroide.x(), centroide.y())))
        feature.setAttributes(attrs)
        res = self.cl_direction.addFeature(feature)
        
        if res:
            
            if self.cl_direction.commitChanges():
                return True
            else:
                self.cl_direction.rollBack()
                return False
        else:
            return False

    def changeDirection(self, dir_select):

        angulo = dir_select['angulo']

        if angulo > 180:
            angulo = angulo - 180
        else:
            angulo = angulo + 180

        #obtengo los indices de las columnas
        idx_angulo = self.cl_direction.fields().indexFromName("angulo")

        attrs = {idx_angulo: angulo}

        if self.cl_direction.dataProvider().changeAttributeValues({dir_select.id() : attrs}):

            return True
        else:
            return False

    def createMemLayer(self, vector_layer, name):

        CRS = vector_layer.crs().postgisSrid()
 
        URI = "MultiLineString?crs=epsg:"+str(CRS)+"&field=id:integer""&index=yes"
        #create memory layer
        mem_layer = QgsVectorLayer(URI,
                            name,
                            "memory")
        return mem_layer
    
    def deleteDirection(self, dir_select):

        self.cl_direction.startEditing()

        res = self.cl_direction.deleteFeature(dir_select.id())
        if res:
            if self.cl_direction.commitChanges():
                return True
            else:
                self.cl_direction.rollBack()
                return False
    
        return False 

    def deleteDirectionByTramo(self, tramo_select):

        #obtengo el id del tramo
        id_tramo = tramo_select.id()

        for feat in self.cl_direction.getFeatures():

            if feat['tramo_idtramo'] == id_tramo:
                self.cl_direction.startEditing()

                res = self.cl_direction.deleteFeature(feat.id())
                if res:

                    if self.cl_direction.commitChanges():
                        return True
                    else:
                        self.cl_direction.rollBack()
                        return False
    
        return False

    def loadVectorLayer(self, array_line, mem_layer):
        # Arrayline contiene los puntos de las lineas
        # Prepare mem_layer for editing
        mem_layer.startEditing()
        n_seg = len(array_line)
        feature = QgsFeature()
        feature = []
        for i in range(n_seg):
            feat = QgsFeature()
            feature.append(feat)

        for i in range(n_seg):
            feature[i].setGeometry(QgsGeometry.fromPolyline(array_line[i]))
            feature[i].setAttributes([i])
        mem_layer.addFeatures(feature)
        mem_layer.commitChanges()
        return mem_layer

    def segmentLineToLine(self, tramo_select):
        # Obtengo los puntos del tramo seleccionado
        array_point_tramo = self.cltramosentity.getVertexTramoAsPoint(tramo_select)
        num_point_poly = len(array_point_tramo)
        mem_layer = self.createMemLayer(self.cl_direction, "segment_line")
        array_line = []
        for i in range(num_point_poly - 1):
            # accedo al primer punto
            segmento = []
            segmento.append(array_point_tramo[i])
            segmento.append(array_point_tramo[i + 1])
            array_line.append(segmento)
        # Guarda el vector de linea creado
        vector_line = self.loadVectorLayer(array_line, mem_layer)
        return vector_line