from pySAXS.guisaxs.qt import plugin
from pySAXS.guisaxs.qt import dlgXeuss3Surveyor
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import os
from pySAXS.guisaxs.qt import UV_vis_Xeuss3_interface_Fini
#from pySAXS.guisaxs.qt import startpyFAICalib

classlist=['pluginSurveyorXeuss3','pluginUV_Vis']#,'pluginFAI',]

class pluginSurveyorXeuss3(plugin.pySAXSplugin):
    menu="Data Treatment"
    subMenu="Xeuss3"
    subMenuText="Xeuss3 Surveyor"
    icon="numero-3.png"
    toolbar=True
        
    def execute(self):
        #display the FAI dialog box
        parameterfile=None#self.parent.pref.get("parameterfile",'pyFAI')
        #print "XEUSS"
        self.dlg=dlgXeuss3Surveyor.XeussSurveyorDialog(self.parent,parameterfile)
        self.dlg.show()


class pluginUV_Vis(plugin.pySAXSplugin):
    menu = "Data Treatment"
    subMenu = "Xeuss3"
    subMenuText = "UV Vis treatment"
    icon = "Logo_UV-vis-Em.png"
    toolbar=True
    # subMenuText="Background and Data correction"


    def execute(self):
        self.dlg = UV_vis_Xeuss3_interface_Fini.UV_Vis_Ui_Dialog()
        self.dlg.show()
        # keep the dialog on the scope not to be garbage collected
        self.parent.dialogUV=self.dlg
