#!/usr/bin/env python3
"""
Child class for cartaportes from ALDIA company
"""

import re, sys, os
from .ecuapass_info_cartaporte import CartaporteInfo
from .ecuapass_extractor import Extractor
from .ecuapass_data import EcuData
from .ecuapass_utils import Utils

#----------------------------------------------------------
USAGE = "\
Extract information from document fields analized in AZURE\n\
USAGE: ecuapass_info_cartaportes.py <Json fields document>\n"
#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args = sys.argv
	docFieldsFilename = args [1]
	runningDir = os.getcwd ()
	CartaporteInfo = CartaporteAldia (docFieldsFilename, runningDir)
	mainFields = CartaporteInfo.extractEcuapassFields ()
	Utils.saveFields (mainFields, docFieldsFilename, "Results")

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class CartaporteAldia (CartaporteInfo):
	def __init__ (self, docFieldsFilename, runningDir, ecudocFields=None):
		super().__init__ (docFieldsFilename, runningDir, ecudocFields)

	def getEmpresaInfo (self):
		return EcuData.getEmpresaInfo ("ALDIA")

	#------------------------------------------------------------
	# In ALDIA: Deposito in last line of field 21_Instrucciones
	#------------------------------------------------------------
	def getDepositoMercancia (self):
		try:
			text         = Utils.getValue (self.fields, "21_Instrucciones")
			lineDeposito = text.split ("\n")[-1]
			reBodega     = r':\s*(.*)'
			bodega       = Extractor.getValueRE (reBodega, lineDeposito)
			depositosDic = Extractor.getDataDic ("depositos_tulcan.txt", self.resourcesPath)
			for id, textBodega in depositosDic.items ():
				if bodega in textBodega:
					print (f"+++ Deposito '{id}' : '{textBodega}'")
					return id
			raise
		except:
			Utils.printx (f"+++ No se puedo obtener deposito desde texto '{text}'")
			return "||LOW"


	#-------------------------------------------------------------------
	# Get subject info: nombre, dir, pais, ciudad, id, idNro 
	# ALDIA format: <Nombre>\nID\n<Direccion>\n<CiudadPais>-
	#-------------------------------------------------------------------
	def getSubjectInfo (self, key):
		subject = {"nombre":None, "direccion":None, "pais": None, 
				   "ciudad":None, "tipoId":None, "numeroId": None}
		try:
			text	   = Utils.getValue (self.fields, key)
			textLines  = text.split ("\n")
			lowString  = ""
			if len (textLines) != 4:
				lowString = "||LOW"
			subject ["nombre"]     = textLines [0] + lowString
			idInfo                 = Extractor.getIdInfo (textLines [1])
			subject ["tipoId"]     = idInfo ["tipoId"]  + lowString
			subject ["numeroId"]   = idInfo ["numeroId"] + lowString
			subject ["direccion"]  = textLines [2] + lowString
			ciudadPais = Extractor.getCiudadPais (textLines [3], self.resourcesPath)
			subject ["ciudad"]     = ciudadPais [0] + lowString
			subject ["pais"]       = ciudadPais [1] + lowString
			print (f"+++ Sujeto '{key}': '{subject}'")
		except:
			Utils.printException (f"Obteniendo datos del sujeto: '{key}' en el texto: '{text}'")
		return subject

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

