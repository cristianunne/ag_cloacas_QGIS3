from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *

class ClNodosEtiqueta2Entity():

    def __init__(self):
        self.cl_nodos_etiqueta2_layer = None

    def initialize(self, cl_nodos_etiqueta2_layer):
        self.cl_nodos_etiqueta2_layer = cl_nodos_etiqueta2_layer

    def addNodoEtiqueta2ToInicio(self, tramo_select, cl_nodos_entity):

        attrs_etiqueta = [None] * len(self.cl_nodos_etiqueta2_layer.fields())

        idx_idclnodo = self.cl_nodos_etiqueta2_layer.fields().indexFromName("nodos_clnodos")
        #obtengo el id del cl_nodo de inicio del tramo

        cl_nodo_feat = cl_nodos_entity.getInitialNodoByTramoTouches(tramo_select)

        if cl_nodo_feat != False:

            #consulto que no exista el cl_nodo_etiqueta
            res_exists = False

            for feature in self.cl_nodos_etiqueta2_layer.getFeatures():
                if feature['nodos_clnodos'] == cl_nodo_feat['gid']:
                    res_exists = True

            if res_exists == False:
                attrs_etiqueta[idx_idclnodo] = cl_nodo_feat['gid']
                point = cl_nodo_feat.geometry().asPoint()
                #Inicio la edicion
                self.cl_nodos_etiqueta2_layer.startEditing()

                feat = QgsFeature()

                point_ = QgsPoint(point.x() + 7, point.y())

                feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(point_.x(), point_.y())))
                feat.setAttributes(attrs_etiqueta)

                if self.cl_nodos_etiqueta2_layer.addFeature(feat):
                    if self.cl_nodos_etiqueta2_layer.commitChanges():

                        return True
                    else:
                        self.cl_nodos_etiqueta2_layer.rollBack()
                        return False
                else:
                    return False
            else:
                return True
        else:
            return False

    def addNodoEtiqueta2ToFinal(self, tramo_select, cl_nodos_entity):

        attrs_etiqueta = [None] * len(self.cl_nodos_etiqueta2_layer.fields())

        idx_idclnodo = self.cl_nodos_etiqueta2_layer.fields().indexFromName("nodos_clnodos")
        #obtengo el id del cl_nodo de inicio del tramo

        cl_nodo_feat = cl_nodos_entity.getFinalNodoByTramoTouches(tramo_select)

        if cl_nodo_feat != False:

            #consulto que no exista el cl_nodo_etiqueta
            res_exists = False

            for feature in self.cl_nodos_etiqueta2_layer.getFeatures():
                if feature['nodos_clnodos'] == cl_nodo_feat['gid']:
                    res_exists = True

            if res_exists == False:
                attrs_etiqueta[idx_idclnodo] = cl_nodo_feat['gid']
                point = cl_nodo_feat.geometry().asPoint()
                #Inicio la edicion
                self.cl_nodos_etiqueta2_layer.startEditing()

                feat = QgsFeature()

                point_ = QgsPoint(point.x() + 7, point.y())

                feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(point_.x(), point_.y())))
                feat.setAttributes(attrs_etiqueta)

                if self.cl_nodos_etiqueta2_layer.addFeature(feat):
                    if self.cl_nodos_etiqueta2_layer.commitChanges():

                        return True
                    else:
                        self.cl_nodos_etiqueta2_layer.rollBack()
                        return False
                else:
                    return False
            else:
                return True
        else:
            return False