from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *

from .ClNodosTramosEntity import ClNodosTramosEntity

class ClNodosEtiquetaEntity():
    
    def __init__(self):
       
       self.cl_nodos_etiqueta_layer = None
       
    
    def initialize(self, cl_nodos_etiqueta_layer):
        
        self.cl_nodos_etiqueta_layer = cl_nodos_etiqueta_layer
        

    
    def addNodoEtiquetaToInicio(self, tramo_select, cl_nodos_entity):

        attrs_etiqueta = [None] * len(self.cl_nodos_etiqueta_layer.fields())

        idx_idclnodo = self.cl_nodos_etiqueta_layer.fields().indexFromName("nodo_cl_nodo")
        #obtengo el id del cl_nodo de inicio del tramo

        cl_nodo_feat = cl_nodos_entity.getInitialNodoByTramoTouches(tramo_select)

        if cl_nodo_feat != False:

            #consulto que no exista el cl_nodo_etiqueta
            res_exists = False

            for feature in self.cl_nodos_etiqueta_layer.getFeatures():
                if feature['nodo_cl_nodo'] == cl_nodo_feat.id():

                    res_exists = True

            if res_exists == False:

                attrs_etiqueta[idx_idclnodo] = cl_nodo_feat.id()
                point = cl_nodo_feat.geometry().asPoint()
                #Inicio la edicion
                self.cl_nodos_etiqueta_layer.startEditing()

                feat = QgsFeature()

                point_ = QgsPointXY(point.x() + 25, point.y())

                feat.setGeometry(QgsGeometry().fromPointXY(point_))
                feat.setAttributes(attrs_etiqueta)

                if self.cl_nodos_etiqueta_layer.addFeature(feat):
                    if self.cl_nodos_etiqueta_layer.commitChanges():

                        return True
                    else:
                        self.cl_nodos_etiqueta_layer.rollBack()
                        return False
                else:
                    return False
            else:
                return True
        else:
            return False


    def addNodoEtiquetaToFinal(self, tramo_select, cl_nodos_entity):

        attrs_etiqueta = [None] * len(self.cl_nodos_etiqueta_layer.fields())

        idx_idclnodo = self.cl_nodos_etiqueta_layer.fields().indexFromName("nodo_cl_nodo")
        #obtengo el id del cl_nodo de inicio del tramo

        cl_nodo_feat = cl_nodos_entity.getFinalNodoByTramoTouches(tramo_select)

        if cl_nodo_feat != False:

            #consulto que no exista el cl_nodo_etiqueta
            res_exists = False

            for feature in self.cl_nodos_etiqueta_layer.getFeatures():
                if feature['nodo_cl_nodo'] == cl_nodo_feat['gid']:
                    res_exists = True

            if res_exists == False:
                attrs_etiqueta[idx_idclnodo] = cl_nodo_feat['gid']
                point = cl_nodo_feat.geometry().asPoint()
                #Inicio la edicion
                self.cl_nodos_etiqueta_layer.startEditing()

                feat = QgsFeature()

                point_ = QgsPointXY(point.x() + 25, point.y())

                feat.setGeometry(QgsGeometry().fromPointXY(point_))
                feat.setAttributes(attrs_etiqueta)

                if self.cl_nodos_etiqueta_layer.addFeature(feat):
                    if self.cl_nodos_etiqueta_layer.commitChanges():

                        return True
                    else:
                        self.cl_nodos_etiqueta_layer.rollBack()
                        return False
                else:
                    return False
            else:
                return True
        else:
            return False

    def setAttributeById(self, id_clnodo, ztn, id_tramo):

        layer_cl_nodos_tramos = QgsProject.instance().mapLayersByName('cl_nodos_tramos')[0]
        # Intancio la Clase CLNodosTramos

        cl_nodos_tramos_entity = ClNodosTramosEntity()
        cl_nodos_tramos_entity.initialize(layer_cl_nodos_tramos)

        idx_ztn_eti = self.cl_nodos_etiqueta_layer.fields().indexFromName("ztn")

        feature = QgsFeature()

        # Recorro la capa y obtengo el feature
        for feat in self.cl_nodos_etiqueta_layer.getFeatures():

            if feat['nodo_cl_nodo'] == id_clnodo:
                feature = feat

        self.cl_nodos_etiqueta_layer.startEditing()
        self.cl_nodos_etiqueta_layer.changeAttributeValue(feature.id(), idx_ztn_eti, ztn)
        self.cl_nodos_etiqueta_layer.commitChanges()

        res = cl_nodos_tramos_entity.addNodoTramo(id_tramo, id_clnodo)

    """def getLastPointAdded(self):
        
        features = self.cl_nodos_etiqueta_layer.getFeatures()
        last = None
        valor = -1
        
        for feat in features:
            if feat.id() > valor:
                valor = feat.id()
                last = feat
        return last"""