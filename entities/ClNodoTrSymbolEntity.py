from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *


#Importo las entidades
from .ClTramosEntity import ClTramosEntity


class ClNodoTrSymbolEntity():
    
    def __init__(self):
        
        self.cl_nodo_tr_symbol = None
        
    
    def initialize(self, cl_nodo_tr_symbol):
        self.cl_nodo_tr_symbol = cl_nodo_tr_symbol    
    
    
    def addNodoSymbol(self, tramo, type_simbol, ini_fin):
        
        cl_tramos_entity = ClTramosEntity()
        
        vertices = cl_tramos_entity.getVertexTramoAsPoint(tramo)
        
        angulo = self.getAngulo(cl_tramos_entity, tramo, ini_fin)
       
      
        
        attrs = [None] * len(self.cl_nodo_tr_symbol.fields())
        
        #obtengo el id del tipo de symbol
        idx_type_symbol = self.cl_nodo_tr_symbol.fields().indexFromName("ty_sym")
        idx_type_angulo = self.cl_nodo_tr_symbol.fields().indexFromName("angulo")
        #asigno el tipo de feature
        attrs[idx_type_symbol] = type_simbol
        attrs[idx_type_angulo] = angulo
        
        self.cl_nodo_tr_symbol.startEditing()
        #creo un feature
        feature = QgsFeature()
        
        #elijo el 1er vertice como point
        point = None
        if ini_fin == True:
            point = vertices[0]
            
        else:
            num_ver = len(vertices)
            point = vertices[num_ver - 1]

        feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(point.x(), point.y())))
        feature.setAttributes(attrs)
        res = self.cl_nodo_tr_symbol.addFeature(feature)
        
        if res:
            
            if self.cl_nodo_tr_symbol.commitChanges():
                return True
            else:
                self.cl_nodo_tr_symbol.rollBack()
                return False
        else:
            return False

    def deleteNodoSymbol(self, tramo, option, layer_cl_tramos):

        # la variable option determina si es el simbolo de inicio o de fin True es Inicio, FALSE es Final
        # obtengo el id del Symbolo
        id_nodo = None
        # Variable que guarda el numero de tramos que comparten el nodo
        num_tramos_ref = 0

        if option:
            id_nodo = tramo['id_nodo_symbol_inicio']
            for feat_tramos in layer_cl_tramos.getFeatures():

                if feat_tramos['id_nodo_symbol_inicio'] == id_nodo:
                    num_tramos_ref = num_tramos_ref + 1

                if feat_tramos['id_nodo_symbol_final'] == id_nodo:
                    num_tramos_ref = num_tramos_ref + 1


        else:
            id_nodo = tramo['id_nodo_symbol_final']
            for feat_tramos in layer_cl_tramos.getFeatures():

                if feat_tramos['id_nodo_symbol_final'] == id_nodo:
                    num_tramos_ref = num_tramos_ref + 1

                if feat_tramos['id_nodo_symbol_inicio'] == id_nodo:
                    num_tramos_ref = num_tramos_ref + 1

        # Debo verificar que el nodo final o inicial no este referenciado en otro tramo

        self.cl_nodo_tr_symbol.startEditing()

        if num_tramos_ref <= 1:
            res = self.cl_nodo_tr_symbol.deleteFeature(id_nodo)

        else:
            # Seteo a Null los id
            # obtengo los indices de los atributos
            idx_nodo_inicio = layer_cl_tramos.fields().indexFromName("id_nodo_symbol_inicio")
            idx_nodo_final = layer_cl_tramos.fields().indexFromName("id_nodo_symbol_final")

            attrs = {idx_nodo_inicio: None, idx_nodo_final: None}

            layer_cl_tramos.startEditing()
            res = layer_cl_tramos.changeAttributeValues(tramo.id(), attrs)
            layer_cl_tramos.commitChanges()

        if res:

            if self.cl_nodo_tr_symbol.commitChanges():
                return True
            else:
                self.cl_nodo_tr_symbol.rollBack()
                return False
        else:

            return False
    
    def getAngulo(self, cl_tramos_entity, tramo_select, ini_fin):
        
        num_vert = cl_tramos_entity.getNumVertex(tramo_select)
        
        point_tramo = cl_tramos_entity.getVertexTramoAsPoint(tramo_select)
        angulo = None
        
        if ini_fin:
            angulo = point_tramo[0].azimuth(point_tramo[1])
        
        else:
            angulo = point_tramo[num_vert - 2].azimuth(point_tramo[num_vert - 1])
        
        return angulo

    def getExistSymbolInicio(self, tramo):
        
        cl_tramos_entity = ClTramosEntity()
        
        #Obtengo los puntos del tramo
        points_tramo = cl_tramos_entity.getVertexTramoAsPoint(tramo)
        
        #Consulto la tabla cl_nodo_tr_symbol para saber si hay un punto en esa coordenada
        
        feats_tr_symbol =  self.cl_nodo_tr_symbol.getFeatures()
        
        #reccoro la capa y obtengo cada feature
        
        for feat in feats_tr_symbol:
            point_symbol = feat.geometry().asPoint()
            
            #ACA EVALUO SI EL PUNTO ES IGUAL
            if point_symbol == points_tramo[0]:
                return feat
        
        #Imprimo los datos
        return False
    
    def getExistSymbolFinal(self, tramo):
        
        cl_tramos_entity = ClTramosEntity()
        
        #Obtengo los puntos del tramo
        points_tramo = cl_tramos_entity.getVertexTramoAsPoint(tramo)
        
        num_vert = len(points_tramo)
        #Consulto la tabla cl_nodo_tr_symbol para saber si hay un punto en esa coordenada
        feats_tr_symbol =  self.cl_nodo_tr_symbol.getFeatures()
        
        #reccoro la capa y obtengo cada feature
        for feat in feats_tr_symbol:
            point_symbol = feat.geometry().asPoint()
            
            if point_symbol == points_tramo[num_vert - 1]:
                return feat

        return False

    def getLastPointAdded(self):

        features = self.cl_nodo_tr_symbol.getFeatures()
        last = None
        valor = -1
        for feat in features:
            if feat['gid'] > valor:
                valor = feat['gid']
                last = feat
        return last

    def getTypeSimbol(self, tramo):

        id_tramo = tramo['id_nodo_symbol_inicio']
        for feat in self.cl_nodo_tr_symbol.getFeatures():

            if feat['gid'] == id_tramo:
                return feat['ty_sym']

        return False