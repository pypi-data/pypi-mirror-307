#!/usr/bin/env python3

import re, os, json, sys
from traceback import format_exc as traceback_format_exc

from .ecuapass_info import EcuInfo
from .ecuapass_utils import Utils
from .ecuapass_extractor import Extractor  # Extracting basic info from text

#----------------------------------------------------------
USAGE = "\
Extract information from document fields analized in AZURE\n\
USAGE: ecuapass_info_manifiesto.py <Json fields document>\n"
#----------------------------------------------------------
def main ():
	args = sys.argv
	docFieldsPath = args [1]
	runningDir = os.getcwd ()
	mainFields = ManifiestoInfo.extractEcuapassFields (docFieldsPath, runningDir)
	Utils.saveFields (mainFields, docFieldsPath, "Results")

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class ManifiestoInfo (EcuInfo):
	def __init__ (self, fieldsJsonFile, runningDir, ecudocFields=None):
		super().__init__ ("MANIFIESTO", fieldsJsonFile, runningDir, ecudocFields)

	def __str__(self):
		return f"MANIFIESTO" 

	#-- Get data and value from document main fields
	def extractEcuapassFields (self, analysisType="BOT"):
		Utils.runningDir   = self.runningDir      # Dir to copy and get images and data
		logFile, stdoutOrg = Utils.redirectOutput ("log-extraction-manifiesto.log")

		try:
			#print ("\n>>>>>> Identificacion del Transportista Autorizado <<<")
			transportista                         = self.getTransportistaInfo ()
			self.ecudoc ["01_TipoProcedimiento"] = transportista ["procedimiento"]
			self.ecudoc ["02_Sector"]             = transportista ["sector"]
			self.ecudoc ["03_Fecha_Emision"]      = transportista ["fechaEmision"]
			self.ecudoc ["04_Distrito"]           = transportista ["distrito"]
			self.ecudoc ["05_MCI"]                = transportista ["MCI"]
			self.ecudoc ["06_Empresa"]            = transportista ["empresa"]

			#print ("\n>>> Identificación Permisos")
			permisos                              = self.getPermisosInfo ()
			self.ecudoc ["07_TipoPermiso_CI"]     = permisos ["tipoPermisoCI"]
			self.ecudoc ["08_TipoPermiso_PEOTP"]  = permisos ["tipoPermisoPEOTP"]
			self.ecudoc ["09_TipoPermiso_PO"]     = permisos ["tipoPermisoPO"]
			self.ecudoc ["10_PermisoOriginario"]  = permisos ["permisoOriginario"]
			self.ecudoc ["11_PermisoServicios1"]  = permisos ["permisoServicios1"]
			self.ecudoc ["12_PermisoServicios2"]  = None
			self.ecudoc ["13_PermisoServicios3"]  = None
			self.ecudoc ["14_PermisoServicios4"]  = None

			# Empresa
			self.ecudoc ["15_NombreTransportista"] = self.getNombreEmpresa ()
			self.ecudoc ["16_DirTransportista"]    = self.getDireccionEmpresa ()

			#print ("\n>>>>>> Identificacion de la Unidad de Carga (Remolque) <<<")
			remolque                             = self.extractVehiculoInfo ("REMOLQUE")
			self.ecudoc ["24_Marca_remolque"]    = remolque ["marca"]
			self.ecudoc ["25_Ano_Fabricacion"]   = remolque ["anho"]
			self.ecudoc ["26_Placa_remolque"]    = remolque ["placa"]
			self.ecudoc ["27_Pais_remolque"]     = remolque ["pais"]
			self.ecudoc ["28_Nro_Certificado"]   = remolque ["certificado"]
			self.ecudoc ["29_Otra_Unidad"]       = remolque ["chasis"]

			#print ("\n>>>>>> Identificacion del Vehículo Habilitado <<<")
			vehiculo                             = self.extractVehiculoInfo ("VEHICULO", remolque)
			self.ecudoc ["17_Marca_Vehiculo"]    = vehiculo ["marca"]
			self.ecudoc ["18_Ano_Fabricacion"]   = vehiculo ["anho"]
			self.ecudoc ["19_Pais_Vehiculo"]     = vehiculo ["pais"]
			self.ecudoc ["20_Placa_Vehiculo"]    = vehiculo ["placa"]
			self.ecudoc ["21_Nro_Chasis"]        = vehiculo ["chasis"]
			self.ecudoc ["22_Nro_Certificado"]   = vehiculo ["certificado"]
			self.ecudoc ["23_Tipo_Vehiculo"]     = vehiculo ["tipo"]

			#print ("\n>>>>>> Identificacion de la Tripulacion <<<")
			conductor                             = self.extractConductorInfo ()
			self.ecudoc ["30_Pais_Conductor"]     = conductor ["pais"]
			self.ecudoc ["31_TipoId_Conductor"]   = conductor ["tipoDoc"]
			self.ecudoc ["32_Id_Conductor"]       = conductor ["documento"]
			self.ecudoc ["33_Sexo_Conductor"]     = conductor ["sexo"]
			self.ecudoc ["34_Fecha_Conductor"]    = conductor ["fecha_nacimiento"]
			self.ecudoc ["35_Nombre_Conductor"]   = conductor ["nombre"]
			self.ecudoc ["36_Licencia_Conductor"] = conductor ["licencia"]
			self.ecudoc ["37_Libreta_Conductor"]  = None

			# Auxiliar
			self.ecudoc ["38_Pais_Auxiliar"]     = None
			self.ecudoc ["39_TipoId_Auxiliar"]   = None
			self.ecudoc ["40_Id_Auxiliar"]       = None
			self.ecudoc ["41_Sexo_Auxiliar"]     = None
			self.ecudoc ["42_Fecha_Auxiliar"]    = None
			self.ecudoc ["43_Nombre_Auxiliar"]   = None
			self.ecudoc ["44_Apellido_Auxiliar"] = None
			self.ecudoc ["45_Licencia_Auxiliar"] = None
			self.ecudoc ["46_Libreta_Auxiliar"]  = None

			#print ("\n>>>>>> Datos sobre la carga <<<")
			text                                 = Utils.getValue (self.fields, "23_Carga_CiudadPais")
			ciudad, pais                         = Extractor.getCiudadPais (text, self.resourcesPath)
			self.ecudoc ["47_Pais_Carga"]        = Utils.checkLow (pais)
			self.ecudoc ["48_Ciudad_Carga"]      = Utils.checkLow (ciudad)

			text                                 = Utils.getValue (self.fields, "24_Descarga_CiudadPais")
			ciudad, pais                         = Extractor.getCiudadPais (text, self.resourcesPath)
			self.ecudoc ["49_Pais_Descarga"]     = Utils.checkLow (pais)
			self.ecudoc ["50_Ciudad_Descarga"]   = Utils.checkLow (ciudad)

			#self.updateDistrito ("04_Distrito", descarga ["pais"]) # LOGITRANS: Update after knowing destination country

			cargaInfo                            = self.getCargaInfo ()
			self.ecudoc ["51_Tipo_Carga"]        = cargaInfo ["tipo"]
			self.ecudoc ["52_Descripcion_Carga"] = cargaInfo ["descripcion"]

			#print ("\n>>>>>> Datos sobre la mercancia (Incoterm) <<<")
			text                                 = Utils.getValue (self.fields, "34_Precio_Incoterm_Moneda")
			incoterm                             = self.getIncotermInfo (text)
			self.ecudoc ["53_Precio_Mercancias"] = incoterm ["precio"]
			self.ecudoc ["54_Incoterm"]          = incoterm ["incoterm"]
			self.ecudoc ["55_Moneda"]            = incoterm ["moneda"]
			self.ecudoc ["56_Pais"]       = incoterm ["pais"]
			self.ecudoc ["57_Ciudad"]     = incoterm ["ciudad"]

			#print ("\n>>>>>> Datos de las aduanas <<<")
			aduana                                = self.getAduanaInfo ()
			self.ecudoc ["58_AduanaDest_Pais"]    = aduana ["paisDestino"]
			self.ecudoc ["59_AduanaDest_Ciudad"]  = aduana ["ciudadDestino"]

			#print ("\n>>>>>> Datos sobre las unidades) <<<")
			unidades = self.getUnidadesMedidaInfo ()
			self.ecudoc ["60_Peso_NetoTotal"]     = unidades ["pesoNetoTotal"]
			self.ecudoc ["61_Peso_BrutoTotal"]    = unidades ["pesoBrutoTotal"]
			self.ecudoc ["62_Volumen"]            = None
			self.ecudoc ["63_OtraUnidad"]         = unidades ["otraUnidadTotal"]

			## Aduana Cruce
			self.ecudoc ["64_AduanaCruce_Pais"]   = aduana ["paisCruce"]
			self.ecudoc ["65_AduanaCruce_Ciudad"] = aduana ["ciudadCruce"]

			#print ("\n>>>>>> Detalles finales <<<")
			self.ecudoc ["66_Secuencia"]         = Utils.addLow (self.getSecuencia ())
			self.ecudoc ["67_MRN"]               = self.getMRN ()
			self.ecudoc ["68_MSN"]               = self.getMSN ()

			bultos                         = self.getBultosInfoManifiesto ()
			self.ecudoc ["69_CPIC"]        = Utils.checkLow (bultos ["cartaporte"])
			self.ecudoc ["70_TotalBultos"] = Utils.checkLow (bultos ["cantidad"])
			self.ecudoc ["71_Embalaje"]	   = Utils.checkLow (bultos ["embalaje"])
			self.ecudoc ["72_Marcas"]      = Utils.checkLow (bultos ["marcas"])

			# Unidades
			self.ecudoc ["73_Peso_Neto"]        = unidades ["pesoNetoTotal"]
			self.ecudoc ["74_Peso_Bruto"]       = unidades ["pesoBrutoTotal"]
			self.ecudoc ["75_Volumen"]          = None
			self.ecudoc ["76_OtraUnidad"]       = unidades ["otraUnidadTotal"]

			#print ("\n>>>>>> Detalles finales <<<")
			self.ecudoc ["77_Nro_UnidadCarga"]  = None
			self.ecudoc ["78_Tipo_UnidadCarga"] = None
			self.ecudoc ["79_Cond_UnidadCarga"] = None
			self.ecudoc ["80_Tara"]             = None
			self.ecudoc ["81_Descripcion"]      = bultos ['descripcion']
			self.ecudoc ["82_Precinto"]         = Utils.getValue (self.fields, "27_Carga_Precintos")

			# Update fields depending of other fields (or depending of # "empresa")
			self.updateExtractedEcuapassFields ()

		except:
			Utils.printx (f"ALERTA: Problemas extrayendo información del documento '{self.docFieldsPath}'")
			Utils.printx (traceback_format_exc())
			raise

		Utils.redirectOutput ("log-extraction-manifiesto.log", logFile, stdoutOrg)
		return (self.ecudoc)

	#------------------------------------------------------------------
	# Transportista information 
	#------------------------------------------------------------------
	def getTransportistaInfo (self):
		transportista = Utils.createEmptyDic (["procedimiento", "sector", "fechaEmision", "distrito", "MCI", "empresa"])
		try:	
			transportista ["procedimiento"]     = self.getTipoProcedimiento ()
			transportista ["sector"]            = "NORMAL||LOW"

			text                                = Utils.getValue (self.fields, "40_Fecha_Emision")
			transportista ["fechaEmision"]      = Extractor.getDate (text, self.resourcesPath)
			transportista ["distrito"]          = self.getDistrito ()
			transportista ["MCI"]               = self.getNumeroDocumento ()
			transportista ["empresa"]           = None    # Bot select the first option in BoxField
		except:
			Utils.printException ("Obteniendo información del transportista")
		return (transportista)

	#------------------------------------------------------------------
	# Permisos info: Overwritten in subclasses
	#------------------------------------------------------------------
	def getPermisosInfo (self):
		permisos = Utils.createEmptyDic (["tipoPermisoCI", "tipoPermisoPEOTP", 
									      "tipoPermisoPO", "permisoOriginario", "permisoServicios"])
		try:
			permisos ["permisoOriginario"] = self.getPermiso_PerEmpresa ("ORIGINARIO")
			permisos ["permisoServicios"]  = self.getPermiso_PerEmpresa ("SERVICIOS")
			#permisos ["permisoOriginario"] = self.getPermiso ("02_Permiso_Originario")
			#permisos ["permisoServicios"]  = self.getPermiso ("03_Permiso_Servicios").replace ("-","")

			tipoPermiso = permisos ["permisoOriginario"].split ("-")[0]
			tipoPermiso = re.sub (r"[^A-Za-z0-9]+", "", tipoPermiso).upper()  # re for removing symbols
			if (tipoPermiso == "CI"):
				permisos ["tipoPermisoCI"]     = "1"
			elif (tipoPermiso == "POETP"):
				permisos ["tipoPermisoPOETP"]  = "1"
			elif (tipoPermiso == "PO"):
				permisos ["tipoPermisoPO"]     = "1"
			else:
				Utils.printException (f"Tipo permiso desconocido en el texto: '{text}'")
		except:
			Utils.printException ("Obteniendo información de permisos")

		return (permisos)

	#------------------------------------------------------------------
	# 'Servicios" permission is None for BYZA
	#------------------------------------------------------------------
	def getPermiso_PerEmpresa (self, tipoPermiso):
		outPermiso = None
		#----------------------------------------------------------
		def getPermiso (key):
			"""May contain one or two numbers. First is returned"""
			permiso = self.fields [key]
			return permiso.split ("\n")[0]
		#----------------------------------------------------
		if tipoPermiso == "ORIGINARIO":
			outPermiso =  getPermiso ("02_Permiso_Originario")
		elif tipoPermiso == "SERVICIOS":
			if self.empresa["id"] == "BYZA":
				outPermiso = None
			else:
				outPermiso = getPermiso ("03_Permiso_Servicios").replace ("-","")

		return outPermiso
		
	#------------------------------------------------------------------
	# Get Vehiculo/Remolque information 
	#------------------------------------------------------------------
	def extractVehiculoInfo (self, type="VEHICULO", remolque=None):
		vehiculo = {key:None for key in ["marca","anho","pais","placa","chasis","certificado","tipo"]}
		keys     = None
		if type == "VEHICULO":
			keys = {"marca":"04_Camion_Marca", "anho":"05_Camion_AnoFabricacion", "placaPais":"06_Camion_PlacaPais", 
		   			"chasis":"07_Camion_Chasis", "certificado":"08_Certificado_Habilitacion"}
		elif type == "REMOLQUE":
			keys = {"marca":"09_Remolque_Marca", "anho":"10_Remolque_AnoFabricacion", "placaPais":"11_Remolque_PlacaPais", 
					"chasis": "12_Remolque_Otro", "certificado": "08_Certificado_Habilitacion"}
		else:
			print (f"ERROR: Tipo de vehiculo desconocido: '{type}'")
			return vehiculo
 
		try:
			text = self.fields [keys ["placaPais"]]
			placaPaisText            = Extractor.getValidValue (self.fields [keys ["placaPais"]])
			if placaPaisText:
				placaPais            = Extractor.getPlacaPais (placaPaisText, self.resourcesPath) 
				vehiculo ["placa"]   = Extractor.getValidValue (placaPais ["placa"])
				vehiculo ["pais"]    = Extractor.getValidValue (placaPais ["pais"])
				vehiculo ["marca"]   = Extractor.getValidValue (self.fields [keys ["marca"]])
				vehiculo ["anho"]    = Extractor.getValidValue (self.fields [keys ["anho"]])

				if type == "VEHICULO":
					vehiculo ["chasis"]  = Extractor.getValidValue (self.fields [keys ["chasis"]])

				vehiculo ["certificado"] = Extractor.getValidValue (self.getCheckCertificado (type, keys ["certificado"]))
				vehiculo ["tipo"]        = self.getTipoVehiculo (type, remolque)
		except Exception as e:
			Utils.printException (f"Extrayendo información del vehículo", e)

		print ("+++ Vehiculo:", vehiculo)
		return vehiculo

	#-- Get ECUAPASS tipo vehículo for 'empresa'
	def getTipoVehiculo  (self, tipo, remolque=None):
		transportNTA     = {"camion": "CAMION", "tractocamion": "SEMIRREMOLQUE"}
		transportOTHERS  = {"camion": "CAMION", "tractocamion": "TRACTOCAMION"}

		empresa   = self.empresa["id"]
		transport = transportNTA if empresa == "NTA" else transportOTHERS
		if tipo == "VEHICULO" and not remolque: 
			return transport ["camion"]
		elif tipo == "VEHICULO" and remolque:
			return transport ["tractocamion"] 
		elif tipo == "REMOLQUE":
			return "REMOLQUE"

	#-- Return certificadoString if it is valid (e.g. CH-CO-XXXX-YY, RUC-CO-XXX-YY), else None
	def getCheckCertificado (self, vehicleType, key):
		try:
			textCertificado  = Utils.getValue (self.fields, key)
			if vehicleType == "VEHICULO":
				text    = Extractor.getFirstString (textCertificado)
				pattern = re.compile (r'^CH-(CO|EC)-\d{4,5}-\d{2}')
			elif vehicleType == "REMOLQUE":
				text    = Extractor.getLastString (textCertificado)
				pattern = re.compile (r'^(CRU|CR)-(CO|EC)-\d{4,5}-\d{2}')

			if (text == None): 
				return "||LOW" if vehicleType == "VEHICULO" else None

			certificadoString = self.formatCertificadoString (text, vehicleType)
			if bool (pattern.match (certificadoString)) == False:
				Utils.printx (f"Error validando certificado de <{vehicleType}> en texto: '{certificadoString}'")
				certificadoString = "||LOW"
		except:
			Utils.printException (f"Obteniendo/Verificando certificado '{certificadoString}' para '{vehicleType}'")

		return certificadoString;

	#-- Try to convert certificado text to valid certificado string
	#-- Overwriten in LOGITRANS (CR-->CRU)
	def formatCertificadoString (self, text, vehicleType):
		try:
			if (text in [None, ""]):
				return None

			text = text.replace ("-","") 
			text = text.replace (".", "") 
 
			if vehicleType == "VEHICULO":
				first  = text [0:2]; text = text [2:]   # CH
			elif vehicleType == "REMOLQUE":
				if text [0:3] == "CRU":
					first  = "CRU"; text = text [3:]   # CRU
				elif text [0:2] == "CR":
					first  = "CR"; text = text [2:]   # CR

			second = text [0:2]; text = text [2:]       # CO|EC
			last   = text [-2:]; text = text [:-2]      # 23|23|XX
			middle = text                               # XXXX|YYYYY

			certificadoString = f"{first}-{second}-{middle}-{last}"
		except:
			Utils.printException (f"Excepción formateando certificado para '{vehicleType}' desde el texto '{text}'")
			certificadoString = ""

		return certificadoString
		
	#------------------------------------------------------------------
	# Extract conductor/Auxiliar informacion
	#------------------------------------------------------------------
	def extractConductorInfo (self, type="CONDUCTOR"):
		keysAll = {
			"CONDUCTOR":{"nombreFecha":"13_Conductor_Nombre", "documento":"14_Conductor_Id", 
					   "pais":"15_Conductor_Nacionalidad", "licencia":"16_Conductor_Licencia"},
		  	"AUXILIAR" :{"nombreFecha":"18_Auxiliar_Nombre", "documento":"19_Auxiliar_Id",  
					   "pais":"20_Auxiliar_Nacionalidad", "licencia":"21_Auxiliar_Licencia"}
		}
		conductor = Utils.createEmptyDic (["pais", "tipoDoc", "documento", "sexo", "fecha_nacimiento", "nombre", "licencia"])
		keys      = keysAll [type]
		try:
			documento = Utils.getValue (self.fields, keys ["documento"])
			if Extractor.getValidValue (documento):
				conductor ["documento"]        = documento
				conductor ["pais"]             = Extractor.getPaisFromPrefix (Utils.getValue (self.fields, keys ["pais"]))  
				conductor ["tipoDoc"]          = "CEDULA DE IDENTIDAD"
				conductor ["sexo"]             = "Hombre"
				text                           = Utils.getValue (self.fields, keys ["nombreFecha"])
				fecha_nacimiento               = Extractor.getDate (text, self.resourcesPath)
				conductor ["fecha_nacimiento"] = fecha_nacimiento if fecha_nacimiento else "06-01-1980"
				conductor ["nombre"]           = Extractor.extractNames (text)
				conductor ["licencia"]         = Utils.getValue (self.fields, keys ["licencia"])
		except:
			Utils.printException ("Obteniendo informacion del conductor")
		print (f"+++ Conductor '{conductor}'")
		return conductor

	#------------------------------------------------------------------
	# Info carga: type and descripcion
	#------------------------------------------------------------------
	def getCargaInfo (self):
		info = {"tipo": None, "descripcion": None}
		try:
			info ["tipo"]           = "CARGA SUELTA||LOW"
			info ["descripcion"]    = self.getCargaDescripcion ()
		except:
			Utils.printException ("Obteniendo inforamcion de la carga en texto:")
		return info

	#-- Overwritten in companies (BYZA:None)
	def getCargaDescripcion (self):
		return Utils.getValue (self.fields, "25e_Carga_TipoDescripcion")

	#--------------------------------------------------------------------
	#-- Search "pais" for "ciudad" in previous document boxes
	#--------------------------------------------------------------------
	def searchPaisPreviousBoxes (self, ciudad, pais):
		try:
			if (ciudad != None and pais == None):
				if self.ecudoc ["48_Ciudad_Carga"] and ciudad in self.ecudoc ["48_Ciudad_Carga"]:
					pais	 = self.ecudoc ["47_Pais_Carga"]
				elif self.ecudoc ["50_Ciudad_Descarga"] and ciudad in self.ecudoc ["50_Ciudad_Descarga"]:
					pais	 = self.ecudoc ["49_Pais_Descarga"]

		except Exception as e:
			Utils.printException (f"Obteniendo informacion de 'mercancía' en texto: '{text}'", e)
		return ciudad, pais

	#-----------------------------------------------------------
	# Get info from unidades de medida:"peso neto, volumente, otras
	#-----------------------------------------------------------
	def getUnidadesMedidaInfo (self):
		info = {"pesoNetoTotal":None, "pesoBrutoTotal":None, "otraUnidadTotal":None}
		try:
			info ["pesoBrutoTotal"]  = Extractor.getNumber (self.fields ["32a_Peso_BrutoTotal"])
			info ["pesoNetoTotal"]   = Extractor.getNumber (self.fields ["32b_Peso_NetoTotal"])
			info ["otraUnidadTotal"] = Extractor.getNumber (self.fields ["33_Otra_MedidaTotal"])
		except:
			Utils.printException ("'Unidades de Medida'")

		return info

	#--------------------------------------------------------------------
	# Aduana info: extract ciudad and pais for "cruce" and "destino" aduanas
	#--------------------------------------------------------------------
	def getAduanaInfo (self):
		info = {"paisCruce":"||NEEDED", "ciudadCruce":"||NEEDED", "paisDestino":"||NEEDED", "ciudadDestino":"||NEEDED"}
		#info = Utils.createEmptyDic (["paisCruce", "ciudadCruce", "paisDestino", "ciudadDestino"])
		text = ""
		try:
			aduanas = {}
			aduanas ["37_Aduana_Cruce"]   = {"ciudad":"ciudadCruce", "pais": "paisCruce"}
			aduanas ["38_Aduana_Destino"] = {"ciudad":"ciudadDestino", "pais": "paisDestino"}

			for key in ["37_Aduana_Cruce", "38_Aduana_Destino"]:
				text = Utils.getValue (self.fields, key)
				ciudad, pais = Extractor.getCiudadPais (text, self.resourcesPath)
				info [aduanas [key]["ciudad"]] = ciudad if Utils.isValidText (ciudad) else "||NEEDED"
				info [aduanas [key]["pais"]]   = pais if Utils.isValidText (pais) else "||NEEDED"

		except Exception as e:
			Utils.printException (f"Extrayendo pais-ciudad desde aduanas en texto: '{text}'", e)
		return info


#	def getAduanaInfoWithREs (self):
#		info = {"paisCruce":"||NEEDED", "ciudadCruce":"||NEEDED", "paisDestino":"||NEEDED", "ciudadDestino":"||NEEDED"}
#		#info = Utils.createEmptyDic (["paisCruce", "ciudadCruce", "paisDestino", "ciudadDestino"])
#		text = ""
#		try:
#			#reWithSeparador = r'(\b\w+[\s\w]*\b)\s*?[-.,]?\s*(\w+)'
#			reWithSeparador = r"(?P<city>[A-Za-z\s]+)\s*[-,\.]\s*(?P<country>[A-Za-z\s]+)"
#			reWithParentesis = r'(\b\w+[\s\w]*\b)\s*?\s*[(](\w+)[)]'
#
#			aduanas = {}
#			aduanas ["37_Aduana_Cruce"]   = {"ciudad":"ciudadCruce", "pais": "paisCruce"}
#			aduanas ["38_Aduana_Destino"] = {"ciudad":"ciudadDestino", "pais": "paisDestino"}
#
#			for key in ["37_Aduana_Cruce", "38_Aduana_Destino"]:
#				text = Utils.getValue (self.fields, key)
#				results = [re.search (x, text) for x in [reWithSeparador, reWithParentesis]]
#				print ("+++ Aduana resultados:", results)
#
#				if results [0] or results [1]:
#					result = results [0] if results [0] else results [1]
#					ciudad = result.group (1).strip()
#					info [aduanas [key]["ciudad"]] = ciudad if Utils.isValidText (ciudad) else "||NEEDED"
#					pais = Extractor.getPaisFromPrefix (result.group (2)).strip()
#					info [aduanas [key]["pais"]]   = pais if Utils.isValidText (pais) else "||NEEDED"
#
#		except Exception as e:
#			Utils.printException (f"Extrayendo pais-ciudad desde aduanas en texto: '{text}'", e)
#		return info
	#------------------------------------------------------------------
	# Secuencia, MRN, MSN, NumeroCPIC for BOTERO-SOTO
	#------------------------------------------------------------------
	def getSecuencia (self):
		return "1"

	def getMSN (self):
		return "0001" + "||LOW"

	#-----------------------------------------------------------
	#-- Get bultos info: cantidad, embalaje, marcas
	#-----------------------------------------------------------
	def getBultosInfoManifiesto (self):
		ecuapassFields = {"cantidad": "30_Mercancia_Bultos", "marcas":
			   "31_Mercancia_Embalaje", "descripcion": "29_Mercancia_Descripcion"}

		bultosInfo = self.getBultosInfo (ecuapassFields)
		bultosInfo ["cartaporte"] = self.getNumeroCartaporte ()
		return bultosInfo

	#-----------------------------------------------------------
	#-----------------------------------------------------------
	# Basic functions
	#-----------------------------------------------------------
	#-----------------------------------------------------------
	def getPaisDestinoDocumento (self):
		try:
			paisDestino = self.ecudoc ["49_Pais_Descarga"]
			if not paisDestino:
				paisDestino = self.ecudoc ["58_AduanaDest_Pais"]
			return paisDestino
		except:
			return None

	#-- Extract numero cartaprote from doc fields
	def getNumeroCartaporte (self):
		docKey = "28_Mercancia_Cartaporte"
		text    = Utils.getValue (self.fields, docKey)
		numero  = Extractor.getNumeroDocumento (text.replace ("\n", ""))
		return numero
		
#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

