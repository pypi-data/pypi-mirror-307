#!/usr/bin/env python3

import re, os, json, sys
from traceback import format_exc as traceback_format_exc
from datetime import datetime, timedelta

from .ecuapass_info import EcuInfo
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
	fieldsJsonFile = args [1]
	runningDir = os.getcwd ()
	mainFields = CartaporteInfo.extractEcuapassFields (fieldsJsonFile, runningDir)
	Utils.saveFields (mainFields, fieldsJsonFile, "Results")

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class CartaporteInfo (EcuInfo):

	def __init__ (self, fieldsJsonFile, runningDir, ecudocFields=None):
		super().__init__ ("CARTAPORTE", fieldsJsonFile, runningDir, ecudocFields)

#	#-- Create an instance from ecudocFields dict
#	@classmethod
#	def fromEcudocFields (cls, ecudocFields):
#		instance         = cls ()
#		instance.fields  = ecudocFields
#		return instance

	#-- Get data and value from document main fields"""
	def extractEcuapassFields (self, analysisType="BOT"):
		logFile, stdoutOrg= Utils.redirectOutput ("log-extraction-cartaporte.log")
		try:
			#--------------------------------------------------------------
			print ("\n>>>>>> Carta de Porte Internacional por Carretera <<<")
			#--------------------------------------------------------------
			self.ecudoc ["01_Distrito"]	         = self.getDistrito ()
			self.ecudoc ["02_NumeroCPIC"]        = self.getNumeroDocumento ()
			self.ecudoc ["03_MRN"]               = self.getMRN ()
			self.ecudoc ["04_MSN"]               = self.getMSN () 
			self.ecudoc ["05_TipoProcedimiento"] = self.getTipoProcedimiento ()

			#-- Empresa
			self.ecudoc ["06_EmpresaTransporte"] = self.getNombreEmpresa ()
			self.ecudoc ["07_DepositoMercancia"] = self.getDepositoMercancia ()
			self.ecudoc ["08_DirTransportista"]	 = self.getDireccionEmpresa ()
			self.ecudoc ["09_NroIdentificacion"] = self.getIdNumeroEmpresa ()

			#--------------------------------------------------------------
			# print ("\n>>>>>> Datos Generales de la CPIC: Sujetos <<<<<<<<")
			#--------------------------------------------------------------
			#-- Remitente 
			remitente                             = Utils.checkLow (self.getSubjectInfo ("02_Remitente"))
			self.ecudoc ["10_PaisRemitente"]      = remitente ["pais"]
			self.ecudoc ["11_TipoIdRemitente"]    = remitente ["tipoId"]
			self.ecudoc ["12_NroIdRemitente"]     = remitente ["numeroId"]
			self.ecudoc ["13_NroCertSanitario"]	  = None
			self.ecudoc ["14_NombreRemitente"]    = remitente ["nombre"]
			self.ecudoc ["15_DireccionRemitente"] = remitente ["direccion"]

			#-- Destinatario 
			destinatario                             = Utils.checkLow (self.getSubjectInfo ("03_Destinatario"))
			self.ecudoc ["16_PaisDestinatario"]	     = destinatario ["pais"] 
			self.ecudoc ["17_TipoIdDestinatario"]    = destinatario ["tipoId"] 
			self.ecudoc ["18_NroIdDestinatario"]     = destinatario ["numeroId"] 
			self.ecudoc ["19_NombreDestinatario"]    = destinatario ["nombre"] 
			self.ecudoc ["20_DireccionDestinatario"] = destinatario ["direccion"] 

			#-- Consignatario 
			consignatario                             = Utils.checkLow (self.getSubjectInfo ("04_Consignatario"))
			self.ecudoc ["21_PaisConsignatario"]      = consignatario ["pais"] 
			self.ecudoc ["22_TipoIdConsignatario"]    = consignatario ["tipoId"] 
			self.ecudoc ["23_NroIdConsignatario"]     = consignatario ["numeroId"] 
			self.ecudoc ["24_NombreConsignatario"]    = consignatario ["nombre"] 
			self.ecudoc ["25_DireccionConsignatario"] = consignatario ["direccion"] 

			#-- Notificado 
			notificado                                = self.getSubjectInfo ("05_Notificado")
			self.ecudoc ["26_NombreNotificado"]	      = notificado ["nombre"] 
			self.ecudoc ["27_DireccionNotificado"]    = notificado ["direccion"] 
			self.ecudoc ["28_PaisNotificado"]         = notificado ["pais"] 

			#--------------------------------------------------------------
			# print ("\n>>>>>> Datos Generales de la CPIC: Locaciones <<<<<<<<")
			#--------------------------------------------------------------
			#-- Recepcion 
			recepcion                           = self.getLocationInfo ("06_Recepcion")
			self.ecudoc ["29_PaisRecepcion"]    = recepcion ["pais"] 
			self.ecudoc ["30_CiudadRecepcion"]  = recepcion ["ciudad"] 
			self.ecudoc ["31_FechaRecepcion"]   = recepcion ["fecha"] 

			#-- Embarque location box
			embarque                           = self.getLocationInfo ("07_Embarque")
			self.ecudoc ["32_PaisEmbarque"]    = embarque ["pais"] 
			self.ecudoc ["33_CiudadEmbarque"]  = embarque ["ciudad"] 
			self.ecudoc ["34_FechaEmbarque"]   = embarque ["fecha"] 

			#-- Entrega location box
			entrega	                          = self.getLocationInfo ("08_Entrega")
			self.ecudoc ["35_PaisEntrega"]    = entrega ["pais"] 
			self.ecudoc ["36_CiudadEntrega"]  = entrega ["ciudad"] 
			self.ecudoc ["37_FechaEntrega"]   = entrega ["fecha"] 

			#--------------------------------------------------------------
			# print ("\n>>>>>> Datos Generales de la CPIC: Condiciones <<<<<<<<")
			#--------------------------------------------------------------
			condiciones                              = Utils.checkLow (self.getCondiciones ())
			self.ecudoc ["38_CondicionesTransporte"] = condiciones ["transporte"]
			self.ecudoc ["39_CondicionesPago"]       = condiciones ["pago"]

			unidades                       = self.getUnidadesMedidaInfo ()
			bultosInfo                     = self.getBultosInfoCartaporte (analysisType)
			self.ecudoc ["40_PesoNeto"]	   = unidades ["pesoNeto"]
			self.ecudoc ["41_PesoBruto"]   = unidades ["pesoBruto"]
			self.ecudoc ["42_TotalBultos"] = bultosInfo ["cantidad"]
			self.ecudoc ["43_Volumen"]	   = unidades ["volumen"]
			self.ecudoc ["44_OtraUnidad"]  = unidades ["otraUnidad"]

			# Incoterm
			text                                = self.fields ["16_Incoterms"]
			incoterms                           = self.getIncotermInfo (text)
			self.ecudoc ["45_PrecioMercancias"]	= incoterms ["precio"]
			self.ecudoc ["46_INCOTERM"]	        = incoterms ["incoterm"] 
			self.ecudoc ["47_TipoMoneda"]       = incoterms ["moneda"] 
			self.ecudoc ["48_PaisMercancia"]    = incoterms ["pais"] 
			self.ecudoc ["49_CiudadMercancia"]	= incoterms ["ciudad"] 

			# Gastos
			gastos                                     = self.getGastosInfo ()
			self.ecudoc ["50_GastosRemitente"]         = gastos ["fleteRemi"] 
			self.ecudoc ["51_MonedaRemitente"]	       = gastos ["monedaRemi"] 
			self.ecudoc ["52_GastosDestinatario"]      = gastos ["fleteDest"] 
			self.ecudoc ["53_MonedaDestinatario"]      = gastos ["monedaDest"] 
			self.ecudoc ["54_OtrosGastosRemitente"]    = gastos ["otrosGastosRemi"] 
			self.ecudoc ["55_OtrosMonedaRemitente"]    = gastos ["otrosMonedaRemi"] 
			self.ecudoc ["56_OtrosGastosDestinatario"] = gastos ["otrosGastosDest"] 
			self.ecudoc ["57_OtrosMonedaDestinataio"]  = gastos ["otrosMonedaDest"] 
			self.ecudoc ["58_TotalRemitente"]          = gastos ["totalGastosRemi"] 
			self.ecudoc ["59_TotalDestinatario"]       = gastos ["totalGastosDest"] 

			# Documentos remitente
			self.ecudoc ["60_DocsRemitente"]   = self.getDocsRemitente ()

			# Emision location box
			emision	                           = self.getLocationInfo ("19_Emision")
			self.ecudoc ["61_FechaEmision"]    = emision ["fecha"] 
			self.ecudoc ["62_PaisEmision"]     = emision ["pais"] 
			self.ecudoc ["63_CiudadEmision"]   = emision ["ciudad"] 
			
			# Instrucciones y Observaciones
			instObs	                           = self.getInstruccionesObservaciones ()
			self.ecudoc ["64_Instrucciones"]   = instObs ["instrucciones"]
			self.ecudoc ["65_Observaciones"]   = instObs ["observaciones"]
			#self.ecudoc ["64_Instrucciones"]   = None
			#self.ecudoc ["65_Observaciones"]   = None

			# Detalles
			self.ecudoc ["66_Secuencia"]      = "1"
			self.ecudoc ["67_TotalBultos"]    = self.ecudoc ["42_TotalBultos"]
			self.ecudoc ["68_Embalaje"]       = bultosInfo ["embalaje"]
			self.ecudoc ["69_Marcas"]         = bultosInfo ["marcas"]
			self.ecudoc ["70_PesoNeto"]	      = self.ecudoc ["40_PesoNeto"]
			self.ecudoc ["71_PesoBruto"]      = self.ecudoc ["41_PesoBruto"]
			self.ecudoc ["72_Volumen"]	      = self.ecudoc ["43_Volumen"]
			self.ecudoc ["73_OtraUnidad"]     = self.ecudoc ["44_OtraUnidad"]

			# IMOs
			self.ecudoc ["74_Subpartida"]       = None
			self.ecudoc ["75_IMO1"]             = None
			self.ecudoc ["76_IMO2"]             = None
			self.ecudoc ["77_IMO2"]             = None
			self.ecudoc ["78_NroCertSanitario"] = self.ecudoc ["13_NroCertSanitario"]
			self.ecudoc ["79_DescripcionCarga"] = bultosInfo ["descripcion"]

			# Update fields depending of other fields (or depending of # "empresa")
			self.updateExtractedEcuapassFields ()

		except:
			Utils.printx (f"ALERTA: Problemas extrayendo información del documento '{self.docFieldsPath}'")
			Utils.printx (traceback_format_exc())
			raise

		Utils.redirectOutput ("log-extraction-cartaporte.log", logFile, stdoutOrg)
		return (self.ecudoc)

	#------------------------------------------------------------------
	#-- First level functions for each Ecuapass field
	#------------------------------------------------------------------
	def getMSN (self):
		MSN = self.empresa ["MSN"]
		return MSN if MSN else "||LOW"

	#------------------------------------------------------------
	# Return the code number from the text matching a "deposito"
	#-- BOTERO-SOTO en casilla 21 o 22, NTA en la 22 ------------
	#------------------------------------------------------------
	def getDepositoMercancia (self):
		for casilla in ["21_Instrucciones", "22_Observaciones"]:
			text = ""
			try:
				text        = Utils.getValue (self.fields, casilla)
				reWordSep  = r'\s+(?:EL\s+)?'
				#reBodega    = rf'BODEGA[S]?\s+\b(\w*)\b'
				reBodega    = rf'BODEGA[S]?{reWordSep}\b(\w*)\b'
				bodegaText  = Extractor.getValueRE (reBodega, text)
				if bodegaText != None:
					Utils.printx (f"Extrayendo código para el deposito '{bodegaText}'")
					depositosDic = Extractor.getDataDic ("depositos_tulcan.txt", self.resourcesPath)
					
					for id in depositosDic:
						if bodegaText in depositosDic [id]:
							return id
			except:
				Utils.printException (f"Obteniendo bodega desde texto '{text}'")
		return "||LOW"

	#-------------------------------------------------------------------
	#-- Get location info: ciudad, pais, fecha -------------------------
	#-- Boxes: Recepcion, Embarque, Entrega ----------------------------
	#-------------------------------------------------------------------
	def getLocationInfo (self, key):
		text     = self.fields [key]
		location = Extractor.extractLocationDate (text, self.resourcesPath, key)
		print (f"+++ Location/Date for '{key}': '{location}'")
		return (location)

	#-- Called when update extracted fields
	#-- Add one or tww weeks to 'entrega' from 'embarque' date
	def getFechaEntrega (self, fechaEntrega=None):
		try:
			if fechaEntrega == "||LOW" or fechaEntrega is None:
				fechaEmbarque = self.ecudoc ["34_FechaEmbarque"]
				fechaEmbarque = datetime.strptime (fechaEmbarque, "%d-%m-%Y") # Fecha igual a la de Embarque

				weeksFechaEntrega = EcuData.weeksFechaEntrega [self.getIdEmpresa()]
				fechaEntrega      = fechaEmbarque + timedelta (weeks=weeksFechaEntrega)

				if self.getTipoProcedimiento () == "TRANSITO":
					fechasEntregaEmpresa ["LOGITRANS"] = fechaEmbarque + timedelta (weeks=2)

				fechaEntrega = fechaEntrega.strftime ("%d-%m-%Y") + "||LOW"
				return fechaEntrega
		except:
			Utils.printException ("Obteniendo información de Fecha de entrega")

		return fechaEntrega

	#-----------------------------------------------------------
	# Get "transporte" and "pago" conditions
	#-----------------------------------------------------------
	def getCondiciones (self):
		conditions = {'pago':None, 'transporte':None}
		# Condiciones transporte
		text = self.fields ["09_Condiciones"]
		try:
			if "SIN CAMBIO" in text.upper():
				conditions ["transporte"] = "DIRECTO, SIN CAMBIO DEL CAMION"
			elif "CON CAMBIO" in text.upper():
				conditions ["transporte"] = "DIRECTO, CON CAMBIO DEL TRACTO-CAMION"
			elif "TRANSBORDO" in text.upper():
				conditions ["transporte"] = "TRANSBORDO"
		except:
			Utils.printException ("Extrayendo condiciones de transporte en texto", text)

		# Condiciones pago
		try:
			if "CREDITO" in text:
				conditions ["pago"] = "POR COBRAR||LOW"
			elif "ANTICIPADO" in text:
				conditions ["pago"] = "PAGO ANTICIPADO||LOW"
			elif "CONTADO" in text:
				conditions ["pago"] = "PAGO ANTICIPADO||LOW"
			else:
				pagoString = Extractor.getDataString ("condiciones_pago.txt", self.resourcesPath)
				rePagos    = rf"\b({pagoString})\b" # RE to find a match string
				pago       = Extractor.getValueRE (rePagos, text)
				conditions ["pago"] = pago if pago else "POR COBRAR||LOW"
		except:
			Utils.printException ("Extrayendo condiciones de pago en texto:", text)

		print (f"+++ Condiciones Pago/Transporte '{conditions}'")
		return (conditions)

	#-----------------------------------------------------------
	# Get info from unidades de medida:"peso neto, volumente, otras
	#-----------------------------------------------------------
	def getUnidadesMedidaInfo (self):
		unidades = {"pesoNeto":None, "pesoBruto": None, "volumen":None, "otraUnidad":None}
		try:
			unidades ["pesoNeto"]   = Extractor.getNumber (self.fields ["13a_Peso_Neto"])
			unidades ["pesoBruto"]  = Extractor.getNumber (self.fields ["13b_Peso_Bruto"])
			unidades ["volumen"]    = Extractor.getNumber (self.fields ["14_Volumen"])
			unidades ["otraUnidad"] = Extractor.getNumber (self.fields ["15_Otras_Unidades"])

			for k,value in unidades.items():
				unidades [k] = "" if not value else Utils.stringToAmericanFormat (value)

			print (f"+++ Unidades de Medida: '{unidades}'")
		except:
			Utils.printException ("Obteniendo información de 'Unidades de Medida'")
		return unidades

	#-----------------------------------------------------------
	# Get 'total bultos' and 'tipo embalaje' 
	# Uses base function "getBultosInfo" with cartaporte fields
	#-----------------------------------------------------------
	def getBultosInfoCartaporte (self, analysisType="BOT"):
		ecuapassFields = {"cantidad": "10_CantidadClase_Bultos", "marcas":
			   "11_MarcasNumeros_Bultos", "descripcion": "12_Descripcion_Bultos"}

		bultosInfo = self.getBultosInfo (ecuapassFields, analysisType)
		print (f"+++ Mercancia info '{bultosInfo}'")
		return bultosInfo

	#--------------------------------------------------------------------
	#-- Search "pais" for "ciudad" in previous document boxes
	#--------------------------------------------------------------------
	def searchPaisPreviousBoxes (self, ciudad, pais):
		try:
			# Search 'pais' in previos boxes
			if (ciudad != None and pais == None):
				if self.ecudoc ["30_CiudadRecepcion"] and ciudad in self.ecudoc ["30_CiudadRecepcion"]:
					pais = self.ecudoc ["29_PaisRecepcion"]
				elif self.ecudoc ["33_CiudadEmbarque"] and ciudad in self.ecudoc ["33_CiudadEmbarque"]:
					pais = self.ecudoc ["32_PaisEmbarque"]
				elif self.ecudoc ["36_CiudadEntrega"] and ciudad in self.ecudoc ["36_CiudadEntrega"]:
					pais = self.ecudoc ["35_PaisEntrega"]

		except:
			Utils.printException ("Obteniendo informacion de 'mercancía'")
		return ciudad, pais

	#-----------------------------------------------------------
	# Get info from 'documentos recibidos remitente'
	#-----------------------------------------------------------
	def getDocsRemitente (self):
		docs = None
		try:
			docs = self.fields ["18_Documentos"]
			print (f"+++ Documentos info: '{docs}'")
		except:
			Utils.printException("Obteniendo valores 'DocsRemitente'")
		return docs

	#-----------------------------------------------------------
	#-- Get instrucciones y observaciones ----------------------
	#-----------------------------------------------------------
	def getInstruccionesObservaciones (self):
		instObs = {"instrucciones":None, "observaciones":None}
		try:
			instObs ["instrucciones"] = self.fields ["21_Instrucciones"]
			instObs ["observaciones"] = self.fields ["22_Observaciones"]
			print (f"+++ 21: Instrucciones info: {instObs['instrucciones']}")
			print (f"+++ 22: Observaciones info: {instObs['observaciones']}")
		except:
			Utils.printException ("Obteniendo informacion de 'Instrucciones y Observaciones'")
		return instObs

	#-----------------------------------------------------------
	# Get 'gastos' info: monto, moneda, otros gastos
	#-----------------------------------------------------------
	def getGastosInfo (self):
		gastos = {"fleteRemi":None, "monedaRemi":None,       "fleteDest":None,       "monedaDest":None,
			"otrosGastosRemi":None, "otrosMonedaRemi":None, "otrosGastosDest":None, "otrosMonedaDest": None,
			"totalGastosRemi":None, "totalMonedaRemi": None, "totalGastosDest":None, "totalMonedaDest":None}
		try:
			# DESTINATARIO:
			USD = "USD"
			gastos ["fleteDest"]	   = self.fields ["17_Gastos:ValorFlete,MontoDestinatario"]
			gastos ["monedaDest"]      = USD if gastos ["fleteDest"] else None
			gastos ["otrosGastosDest"] = self.fields ["17_Gastos:OtrosGastos,MontoDestinatario"]
			gastos ["otrosMonedaDest"] = USD if gastos ["otrosGastosDest"] else None
			gastos ["totalGastosDest"] = self.fields ["17_Gastos:Total,MontoDestinatario"]
			gastos ["totalMonedaDest"] = USD if gastos ["totalGastosDest"] else None

			# REMITENTE: 
			gastos ["fleteRemi"]       = self.fields ["17_Gastos:ValorFlete,MontoRemitente"]
			gastos ["monedaRemi"]      = USD if gastos ["fleteRemi"] else None
			gastos ["otrosGastosRemi"] = self.fields ["17_Gastos:OtrosGastos,MontoRemitente"]
			gastos ["otrosMonedaRemi"] = USD if gastos ["otrosGastosRemi"] else None
			gastos ["totalGastosRemi"] = self.fields ["17_Gastos:Total,MontoRemitente"]
			gastos ["totalMonedaRemi"] = USD if gastos ["totalGastosRemi"] else None

			for k in gastos.keys ():
				if not "moneda" in k.lower ():
					gastos [k] = None if gastos [k] == "" else gastos[k]
					gastos [k] = Utils.stringToAmericanFormat (gastos [k])
		except:
			Utils.printException ("Obteniendo valores de 'gastos'")

		print (f"+++ Gastos info: '{gastos}'")
		return gastos

	#-------------------------------------------------------------------
	#-- For NTA and BYZA:
	#   Get subject info: nombre, dir, pais, ciudad, id, idNro ---------
	#-- BYZA format: <Nombre>\n<Direccion>\n<PaisCiudad><TipoID:ID> -----
	#-------------------------------------------------------------------
	#-- Get subject info: nombre, dir, pais, ciudad, id, idNro
#	def getSubjectInfo (self, subjectType):
#		text	= Utils.getValue (self.fields, subjectType)
#		subject = Extractor.getSubjectInfoFromText (text, self.resourcesPath, subjectType)
#		return (subject)

	#-------------------------------------------------------------------
	#-- Get subject info: nombre, dir, pais, ciudad, id, idNro ---------
	#-- NTA format: <Nombre> <Direccion> <ID> <PaisCiudad> -----
	#-------------------------------------------------------------------
	#-- Get subject info: nombre, dir, pais, ciudad, id, idNro
	def getSubjectInfo (self, key):
		subject = {"nombre":None, "direccion":None, "pais": None, 
		           "ciudad":None, "tipoId":None, "numeroId": None}
		text	= Utils.getValue (self.fields, key)
		try:
			text    = re.sub ("\s*//\s*", "", text)   # For SILOG "//" separator cartaportes
			print (f"\n\n+++ Subject Info: Inital Text '{subject}' '{text}'")
			text, subject = Extractor.removeSubjectId (text, subject, key)
			print (f"+++ Subject Info: Removed Id '{subject}' '{text}'")
			text, subject = Extractor.removeSubjectCiudadPais (text, subject, self.resourcesPath, key)
			print (f"+++ Subject Info: Removed Ciudad-Pais '{subject}' '{text}'")
			text, subject = Extractor.removeSubjectNombreDireccion (text, subject, key)
			print (f"+++ Subject Info: Removed NombreDireccion '{subject}' '{text}'")
		except:
			Utils.printException (f"Obteniendo datos del sujeto: '{key}' en el texto: '{text}'")

		return (subject)

	#-------------------------------------------------------------------
	#-- Get pais destinatario
	#-------------------------------------------------------------------
	def getPaisDestinatario (self):
		return self.ecudoc ["16_PaisDestinatario"]

	#-----------------------------------------------------------
	#-----------------------------------------------------------
	# Basic functions
	#-----------------------------------------------------------
	#-----------------------------------------------------------
	def getPaisDestinoDocumento (self):
		try:
			paisDestino = self.getPaisDestinatario ()
			if not paisDestino:
				paisDestino = self.ecudoc ["35_PaisEntrega"] 
			return paisDestino
		except:
			return None

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

