#-----------------------------------------------------------
# Copyright (C) 2015 Martin Dobias
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.core import QgsVectorFileWriter,QgsWkbTypes,QgsProject,QgsMapLayer

def classFactory(iface):
    return MinimalPlugin_exp(iface)


class MinimalPlugin_exp:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction('qgzGPKG', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        # Optimal wäre natürlich wenn ein GEopackage erzeugt wird, welches 
        # als Namen den qgis-Projekt-Namen enthält [und am Ort des Projekts existiert]
        # und alle Vektor-Layer enthält
        #tempdir = r'/home/volker/corona_workspace/'
        project_directory = QgsProject.instance().readPath("./")+"/".lstrip()
        file_name = QgsProject.instance().fileName()
        #gpkg_name = project_directory + 'Export_Geopackage'
        gpkg_name = file_name.replace('.qgz','.gpkg').replace('.qgs','.gpkg')
        print(gpkg_name)
        #for vLayer in self.iface.mapCanvas().layers():
        #   QgsVectorFileWriter.writeAsVectorFormat(vLayer, project_directory + vLayer.name() + ".shp", "utf-8", vLayer.crs(), "ESRI Shapefile")
        

        for layer in  QgsProject.instance().mapLayers().values() : 
            if  layer.type() == QgsMapLayer.VectorLayer:
                options = QgsVectorFileWriter.SaveVectorOptions() 
                options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer #Update mode
                options.EditionCapability = QgsVectorFileWriter.CanAddNewLayer 
                options.layerName = layer.name()  
                print("Update mode")
                _writer = QgsVectorFileWriter.writeAsVectorFormat(layer, gpkg_name, options)
                if _writer:
                        print(layer.name(), _writer)
                if _writer[0] == QgsVectorFileWriter.ErrCreateDataSource :
                    print("Create mode")
                    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile #Create mode
                    _writer= QgsVectorFileWriter.writeAsVectorFormat(layer, gpkg_name, options)
                    if _writer:
                            print(layer.name(), _writer)
            else:
                print("one more raster-layer")
        QMessageBox.information(None, 'Minimal plugin', 'Alle Layer wurden ins Geopackage '+gpkg_name +' exportiert!')