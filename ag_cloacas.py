# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AGCloacas
                                 A QGIS plugin
 Pluging realizado para la administración del Sistema de Cloacas
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-08-11
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Aguas de Corrientes
        email                : cristian297@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
import sys
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
import qgis


try:
    from qgis.PyQt.QtWidgets import *
except:
    pass


# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog

import os.path
from .CloacasConexion import CloacasConexion
from .tools.modifiedattributetool import ModifiedAttributeTool



class AGCloacas:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'AGCloacas_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.actions = []

        self.toolbar = self.iface.addToolBar(u'AGCloacas')
        self.toolbar.setObjectName(u'AGCloacas')




    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.modified_attr_tool = ModifiedAttributeTool(self.iface, self.toolbar)
        self.toolbar.addSeparator()

        self.conexion_tool = CloacasConexion(self.iface, self.toolbar)
        self.toolbar.addSeparator()



    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                "#&AGCloacas",
                action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def tr(self, message):

        return QCoreApplication.translate('AGCloacas', message)

