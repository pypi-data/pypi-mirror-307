#!/usr/bin/env python3

import os, sys, re

from .ecuapass_info_manifiesto import ManifiestoInfo
from .ecuapass_data import EcuData
from .ecuapass_utils import Utils
from .ecuapass_extractor import Extractor  # Extracting basic info from text

#----------------------------------------------------------
USAGE = "\
Extract information from document fields analized in AZURE\n\
USAGE: ecuapass_info_manifiesto.py <Json fields document>\n"
#----------------------------------------------------------
def main ():
	args = sys.argv
	fieldsJsonFile = args [1]
	runningDir = os.getcwd ()
	mainFields = ManifiestoInfo.extractEcuapassFields (fieldsJsonFile, runningDir)
	Utils.saveFields (mainFields, fieldsJsonFile, "Results")

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class ManifiestoAldia (ManifiestoInfo):
	def __init__(self, fieldsJsonFile, runningDir):
		super().__init__ (fieldsJsonFile, runningDir)

	#-- get empresa info
	def getEmpresaInfo (self):
		return EcuData.getEmpresaInfo ("ALDIA")

	
	#------------------------------------------------------------------
	# Permisos info: Overwritten in subclasses
	#------------------------------------------------------------------
	def getPermisosInfo (self):
		originario = self.fields ["02_Permiso_Originario"]
		servicios  = self.fields ["03_Permiso_Servicios"]

		permisos = {"tipoPermisoCI"    : "1" if originario.startswith ("CI") else None,
			        "tipoPermisoPEOTP" : "1" if originario.startswith ("PE") else None,
			        "tipoPermisoPO"    : "1" if originario.startswith ("PO") else None,
			        "permisoOriginario": originario,
			        "permisoServicios1": servicios
		}
		return permisos

	#------------------------------------------------------------------
	# Get four certificado strings
	#------------------------------------------------------------------
	def getCheckCertificado (self, vehicleType, key):
		text          = self.fields [key]
		print (f"+++ textCertificado '{text}'")

		# Get
		cbzMatches    = re.search (r"Cabezote:\s*([\w-]+)?\s*([\w-]+)?", text)
		trlMatches    = re.search (r"Trailer:\s*([\w-]+)?\s*([\w-]+)?", text)
		cabezoteCerts = [cbzMatches.group(i) if cbzMatches and cbzMatches.group(i) else None for i in range(1, 3)]
		trailerCerts  = [trlMatches.group(i) if trlMatches and trlMatches.group(i) else None for i in range(1, 3)]

		# Check
		cabezote        = self.formatCertificadoString (cabezoteCerts [1], "VEHICULO")
		trailer         = self.formatCertificadoString (trailerCerts  [1], "REMOLQUE")
		cabezoteChecked = self.checkCertificado (cabezote, "VEHICULO")
		trailerChecked  = self.checkCertificado (trailer, "REMOLQUE")
		
		print (f"+++ Certificados: '{cabezoteChecked}', '{trailerChecked}'")

		return cabezoteChecked if vehicleType == "VEHICULO" else trailerChecked


	def checkCertificado (self, certificadoString, vehicleType):
		try:
			if vehicleType == "VEHICULO":
				pattern = re.compile (r'^CH-(CO|EC)-\d{4,5}-\d{2}')
			elif vehicleType == "REMOLQUE":
				pattern = re.compile (r'^(CRU|CR)-(CO|EC)-\d{4,5}-\d{2}')

			if (certificadoString == None): 
				return "||LOW" if vehicleType == "VEHICULO" else None

			if bool (pattern.match (certificadoString)) == False:
				Utils.printx (f"Error validando certificado de <{vehicleType}> en texto: '{certificadoString}'")
				certificadoString = "||LOW"
		except:
			Utils.printException (f"Obteniendo/Verificando certificado '{certificadoString}' para '{vehicleType}'")

		return certificadoString;

	#-----------------------------------------------------------
	#-- Search for embalaje in alternate ecufield 11
	#-----------------------------------------------------------
	def getBultosInfoManifiesto (self):
		mercancia = super ().getBultosInfoManifiesto ()
		print (f"+++ mercancia parcial: '{mercancia}'")

		# Cantidad en Cantidad
		mercancia ["cantidad"] = Extractor.getNumber (self.fields ["30_Mercancia_Bultos"])
		text = self.fields ["31_Mercancia_Embalaje"]
		print (f"+++ text embalaje '{text}'")
		mercancia ["embalaje"] = Extractor.getTipoEmbalaje (self.fields ["31_Mercancia_Embalaje"])

		print (f"+++ Mercancia '{mercancia}'")
		return mercancia

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

