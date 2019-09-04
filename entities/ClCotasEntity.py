from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *

from .ClTramosEntity import ClTramosEntity


class ClCotasEntity():
    
    def __init__(self):
      
        
        self.cl_cotas_layer = None
        
        
    def initialize(self, cl_cotas_layer):
        
        self.cl_cotas_layer = cl_cotas_layer


    def addCotaInicio(self, feat_tramo, valor_cota_inicio):

        #inicio la edicion del layer
        self.cl_cotas_layer.startEditing()

        # creo el arreglo vacion con la dimension de los atributos
        attrs = [None] * len(self.cl_cotas_layer.fields())

        idx_cota= self.cl_cotas_layer.fields().indexFromName("cota")
        idx_tramo_idtramos = self.cl_cotas_layer.fields().indexFromName("tramo_idtramos")
        idx_angulo = self.cl_cotas_layer.fields().indexFromName("angulo")

        attrs[idx_cota] = valor_cota_inicio
        attrs[idx_tramo_idtramos] = feat_tramo.id()

        idx_tipo = self.cl_cotas_layer.fields().indexFromName("tipo")
        attrs[idx_tipo] = "Inicio"

        #calculo el angulo de la cota y su ubicacion
        if self.anguloInicioCota(feat_tramo) >= 90:
            attrs[idx_angulo] = (self.anguloInicioCota(feat_tramo) - 90) * (-1)

        elif self.anguloInicioCota(feat_tramo) > 0 and self.anguloInicioCota(feat_tramo) < 90:
            attrs[idx_angulo] = (90 - self.anguloInicioCota(feat_tramo))

        elif self.anguloInicioCota(feat_tramo) < 0 and self.anguloInicioCota(feat_tramo) > -90:
            attrs[idx_angulo] = (90 + self.anguloInicioCota(feat_tramo)) * (-1)


        elif self.anguloInicioCota(feat_tramo) < -90 and self.anguloInicioCota(feat_tramo) >= -180:

            attrs[idx_angulo] = ((self.anguloInicioCota(feat_tramo) * (-1))) - 90

        else:
            attrs[idx_angulo] = self.anguloInicioCota(feat_tramo)

        vertices = feat_tramo.geometry().asMultiPolyline()[0]
        #creoe l feature para agregar
        feature = QgsFeature()

        #elijo el 1er vertice como point
        point = self.evaluatedPositionInicio(feat_tramo, vertices)
        feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(point.x(), point.y())))
        feature.setAttributes(attrs)

        if self.cl_cotas_layer.addFeature(feature):
            if self.cl_cotas_layer.commitChanges():
                return True
            else:
                self.cl_cotas_layer.rollBack()
                return False
        else:
            return False

        
    def addCotaFinal(self, feat_tramo, valor_cota_final):


        # inicio la edicion del layer
        self.cl_cotas_layer.startEditing()

        # creo el arreglo vacion con la dimension de los atributos
        attrs = [None] * len(self.cl_cotas_layer.fields())

        idx_cota = self.cl_cotas_layer.fields().indexFromName("cota")
        idx_tramo_idtramos = self.cl_cotas_layer.fields().indexFromName("tramo_idtramos")
        idx_angulo = self.cl_cotas_layer.fields().indexFromName("angulo")


        attrs[idx_cota] = valor_cota_final
        attrs[idx_tramo_idtramos] = feat_tramo.id()
        idx_tipo = self.cl_cotas_layer.fields().indexFromName("tipo")
        attrs[idx_tipo] = "Fin"

        # calculo el angulo de la cota y su ubicacion
        if self.anguloInicioCota(feat_tramo) >= 90:
            attrs[idx_angulo] = (self.anguloInicioCota(feat_tramo) - 90) * (-1)

        elif self.anguloInicioCota(feat_tramo) > 0 and self.anguloInicioCota(feat_tramo) < 90:
            attrs[idx_angulo] = (90 - self.anguloInicioCota(feat_tramo))

        elif self.anguloInicioCota(feat_tramo) < 0 and self.anguloInicioCota(feat_tramo) > -90:
            attrs[idx_angulo] = (90 + self.anguloInicioCota(feat_tramo)) * (-1)


        elif self.anguloInicioCota(feat_tramo) < -90 and self.anguloInicioCota(feat_tramo) >= -180:

            attrs[idx_angulo] = ((self.anguloInicioCota(feat_tramo) * (-1))) - 90

        else:
            attrs[idx_angulo] = self.anguloInicioCota(feat_tramo)

        vertices = feat_tramo.geometry().asMultiPolyline()[0]
        # creoe l feature para agregar
        feature = QgsFeature()

        # elijo el 1er vertice como point
        point = self.evaluatedPositionFinal(feat_tramo, vertices)

        feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(point.x(), point.y())))
        feature.setAttributes(attrs)

        if self.cl_cotas_layer.addFeature(feature):
            if self.cl_cotas_layer.commitChanges():
                return True
            else:
                self.cl_cotas_layer.rollBack()
                return False
        else:
            return False


    def evaluatedPositionInicio(self, feat_line, vertices):
        
        point = None
     
        
        if(vertices[0].x() < vertices[1].x() and vertices[0].y() == vertices[1].y()):
            
            point_int = feat_line.geometry().interpolate(10)
            point = QgsPoint(point_int.asPoint().x(), point_int.asPoint().y() + 8)
      
            
        elif (vertices[0].x() > vertices[1].x() and vertices[0].y() == vertices[1].y()):
            
            point_int = feat_line.geometry().interpolate(10)
            point = QgsPoint(point_int.asPoint().x(), point_int.asPoint().y() - 8)
           
        
        elif (vertices[0].x() == vertices[1].x() and vertices[0].y() > vertices[1].y()):
            
             point_int = feat_line.geometry().interpolate(10)
             point = QgsPoint(point_int.asPoint().x() + 8, point_int.asPoint().y())
            
        
        elif (vertices[0].x() == vertices[1].x() and vertices[0].y() < vertices[1].y()):
            
             point_int = feat_line.geometry().interpolate(10)
             point = QgsPoint(point_int.asPoint().x() - 8, point_int.asPoint().y())
           
             
        elif (vertices[0].x() < vertices[1].x() and vertices[0].y() > vertices[1].y()):
             point_int = feat_line.geometry().interpolate(10).asPoint()
             dif_y =  vertices[0].y() - point_int.y()
             res_y = 8 - dif_y
             
             point = QgsPoint(vertices[0].x() + 12, vertices[0].y() + res_y)
     
             
             
             
        elif (vertices[0].x() > vertices[1].x() and vertices[0].y() < vertices[1].y()):
            point_int = feat_line.geometry().interpolate(10).asPoint()
            dif_y =  point_int.y() - vertices[0].y()
            res_y = (8 - dif_y) * (-1)
            
            point = QgsPoint(vertices[0].x() -12, vertices[0].y() + res_y)
             
             
        elif (vertices[0].x() < vertices[1].x() and vertices[0].y() < vertices[1].y()):
            point_int = feat_line.geometry().interpolate(10).asPoint()
            #aca lo que tengo que evaluar es la x
            dif_x =  point_int.x() - vertices[0].x()
            dif_y = point_int.y() - vertices[0].y()
            
            res_x = dif_x - 10
            res_y = 10 - dif_y
         
            
            if res_x < 4:
                res_x = res_x - 4
            
            point = QgsPoint(point_int.x() + res_x, vertices[0].y() + 10)
             
            
        
        elif (vertices[0].x() > vertices[1].x() and vertices[0].y() > vertices[1].y()):
            point_int = feat_line.geometry().interpolate(10).asPoint()
             
            #punto utilizado como referencia
            point_aux = QgsPoint(vertices[0].x(), point_int.y())

             
            res = 12 - (point_aux.x() - point_int.x())
            
            res_y = -12 + (vertices[0].y() - point_int.y())
            
            if res < 6:
                res = res + 6 
             
            point = QgsPoint(point_int.x() + res, point_int.y() + res_y)

        
        return point


    def evaluatedPositionFinal(self, feat_line, vertices):
        point = None
        
        #invierto el orden de los vertices
        vertices = vertices[::-1]
        
        feat_line = QgsFeature(feat_line.fields())
        feat_line.setGeometry(QgsGeometry.fromPolylineXY(vertices))

        if(vertices[0].x() < vertices[1].x() and vertices[0].y() == vertices[1].y()):
            
            point_int = feat_line.geometry().interpolate(10)
            point = QgsPoint(point_int.asPoint().x(), point_int.asPoint().y() + 8)
  
            
        elif (vertices[0].x() > vertices[1].x() and vertices[0].y() == vertices[1].y()):
            
            point_int = feat_line.geometry().interpolate(10)
            point = QgsPoint(point_int.asPoint().x(), point_int.asPoint().y() - 8)
          
        
        elif (vertices[0].x() == vertices[1].x() and vertices[0].y() > vertices[1].y()):
            
             point_int = feat_line.geometry().interpolate(10)
             point = QgsPoint(point_int.asPoint().x() + 8, point_int.asPoint().y())
     
        
        elif (vertices[0].x() == vertices[1].x() and vertices[0].y() < vertices[1].y()):
            
             point_int = feat_line.geometry().interpolate(10)
             point = QgsPoint(point_int.asPoint().x() - 8, point_int.asPoint().y())
           
             
        elif (vertices[0].x() < vertices[1].x() and vertices[0].y() > vertices[1].y()):
             point_int = feat_line.geometry().interpolate(10).asPoint()
             dif_y =  vertices[0].y() - point_int.y()
             res_y = 8 - dif_y
             
             point = QgsPoint(vertices[0].x() + 12, vertices[0].y() + res_y)
          
             
             
             
        elif (vertices[0].x() > vertices[1].x() and vertices[0].y() < vertices[1].y()):
            point_int = feat_line.geometry().interpolate(10).asPoint()
            dif_y =  point_int.y() - vertices[0].y()
            res_y = (8 - dif_y) * (-1)
            
            point = QgsPoint(vertices[0].x() -12, vertices[0].y() + res_y)
        
             
        elif (vertices[0].x() < vertices[1].x() and vertices[0].y() < vertices[1].y()):
            point_int = feat_line.geometry().interpolate(10).asPoint()
            #aca lo que tengo que evaluar es la x
            dif_x =  point_int.x() - vertices[0].x()
            dif_y = point_int.y() - vertices[0].y()
            
            res_x = dif_x - 10
            res_y = 10 - dif_y
            
            if res_x < 4:
                res_x = res_x - 4
            
            point = QgsPoint(point_int.x() + res_x, vertices[0].y() + 10)
    
            
        
        elif (vertices[0].x() > vertices[1].x() and vertices[0].y() > vertices[1].y()):
            point_int = feat_line.geometry().interpolate(10).asPoint()
             
            #punto utilizado como referencia
            point_aux = QgsPoint(vertices[0].x(), point_int.y())
 
            res = 12 - (point_aux.x() - point_int.x())
            
            res_y = -12 + (vertices[0].y() - point_int.y())
            
            if res < 6:
                res = res + 6 
             
            point = QgsPoint(point_int.x() + res, point_int.y() + res_y)

        
        return point


    def deleteCotas(self, tramo_select):
        
         #obtengo el id del tramo
        id_tramo = tramo_select.id()
        
        #recorro el layer nodo y obtengo el id de los nodos que tiene el tramo seleccionado
        
        nodos_feat = self.cl_cotas_layer.getFeatures()
        
        arre_nodos = []
        
        for feat in nodos_feat:
            if id_tramo == feat['tramo_idtramos']:
                arre_nodos.append(feat.id())
                
        
        #con los id recorro el layer y los borro
        self.cl_cotas_layer.startEditing()
        
        res = self.cl_cotas_layer.deleteFeatures(arre_nodos)
        
        if res:
            
            if self.cl_cotas_layer.commitChanges():
                return True
            else:
                self.cl_cotas_layer.rollBack()
                return False
        else:
            return False
        
        
    def anguloInicioCota(self, tramo_select):
        
        cl_tramos_entity = ClTramosEntity()
        array_vertices = cl_tramos_entity.getVertexTramoAsPoint(tramo_select)
        
         #calculo el angulo de orientacion del icono
        angulo = array_vertices[0].azimuth(array_vertices[1])
        
        return angulo
        
    def anguloFinalCota(self, tramo_select):
        
        cl_tramos_entity = ClTramosEntity()
        array_vertices = cl_tramos_entity.getVertexTramoAsPoint(tramo_select)
        
        num_vert = len(array_vertices)
        
        if num_vert > 2:
            #calculo el angulo de orientacion del icono
            angulo = array_vertices[num_vert - 2].azimuth(array_vertices[num_vert - 1])
        else:
            angulo = array_vertices[1].azimuth(array_vertices[0])
        
        return angulo      
          
        
        