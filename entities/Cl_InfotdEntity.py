from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *

class Cl_InfotdEntity():
    def __init__(self, layer_cl_infotd):
        
        self.layer_cl_infotd = layer_cl_infotd
        
        
    def addPoint(self, point, feat_parcela, feat_tramo):
        #Inicio la edicion
        self.layer_cl_infotd.startEditing()

        #obtengo el ID de la Parcela
        id_parcela = feat_parcela['gid']
        #Obtengo el indice de dicho atributo
        fields = self.layer_cl_infotd.fields()

        idx_gid = fields.indexFromName("parcelas")
        idx_cl_tramos = fields.indexFromName("tramo_cltramos")

        #creo el arreglo vacion con la dimension de los atributos
        attrs = [None] * len(self.layer_cl_infotd.fields())
        
        #asigno el valor de id de la parcela
        attrs[idx_gid] = id_parcela
        attrs[idx_cl_tramos] = feat_tramo['gid']

        #creoe l feature para agregar
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPointXY(point))
        feature.setAttributes(attrs)
        res = self.layer_cl_infotd.addFeature(feature)
        
        if self.layer_cl_infotd.commitChanges():
            return res
        else:
            self.layer_cl_infotd.rollBack()
            return False
    
    def getLastPointAdded(self):
        
        features = self.layer_cl_infotd.getFeatures()
        last = None
        
        for feat in features:
            last = feat
            
        return last
    
    def changeId(self, last_line, last_point):
        
        self.layer_cl_infotd.startEditing()
        id_point = last_point['gid']
        id_idx = self.layer_cl_infotd.fieldNameIndex("trdom_cltrdom")
        gid_line = last_line['gid']
        
        self.layer_cl_infotd.changeAttributeValue(id_point, id_idx, gid_line)
        self.layer_cl_infotd.commitChanges()
    
    
    
    