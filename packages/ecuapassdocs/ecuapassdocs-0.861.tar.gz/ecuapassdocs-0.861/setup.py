from setuptools import setup, find_packages

setup(
    name='ecuapassdocs',  # Package name
    version='0.861',  # Package version
    url="https://github.com/lgarreta/ecuapassdocs",
    author='Luis Garreta',
    author_email='lgarreta@gmail.com',
    description='Utils for creating PDFs, loading resources and extracting info from fields in ECUAPASS docs: cartaportes, manifiestos, declaraciones',
    packages=find_packages(),  # Automatically finds packages within the directory
	include_package_data=True, 
	package_data={"ecuapassdocs": ["resources/images/*", 
	                               "resources/data_cartaportes/*",
	                               "resources/data_manifiestos/*",
	                               "resources/data_declaracion/*",
	                               "resources/data_common/*",
	                               "resources/docs/*"]},
	# List any dependencies here
    install_requires = [
		"PyPDF2==3.0.1",
		"reportlab==4.0.8",
		"Pillow==10.1.0"
	], 
	logs = {
		"0.861"  : "Nov/06 : Modifies extracting embalage (Nro)?(Embalaje)+",
		"0.860"  : "Nov/06 : Modified for Bot5: Aldia. Removed Azure fields structure",
		"0.858"  : "Oct/10 : Added getSortedFiles to Utils",
		"0.857"  : "Oct/09 : Fixed getSaveVehiculo with None",
		"0.856"  : "Oct/09 : Changed MCI: getTruckValue for new Extractor.getValidValue",
		"0.855"  : "Oct/06 : Restored getCartaporte in Manifiesto",
		"0.854"  : "Oct/06 : Removed default 'fecha_emision'",
		"0.852"  : "Sep/24 : break long lines function",
		"0.851"  : "Sep/23 : Logitrans load/save docs on web",
		"0.850"  : "11/Sep : Many improvements/fixes Docs and Bot",
		"0.79"   : "Search codebin form by NAME. Added settings for NTA",
		"0.78"   : "Improved infos:depositos, dates, vehiculo",
		"0.77"   : "Improved update (posprocessing) ECUAPASS file",
		"0.76"   : "Improved Utils, getCodebinValues",
		"0.75"   : "Simplified info classes (e.g. removed Gastos table)",
		"0.74"   : "Changed tipoProc (Byza === NTA)",
		"0.73"   : "Improved Byza's clean watermarks",
		"0.72"   : "Improved infos: embalaje",
		"0.71"   : "Improved assignation of vehicle type in Manifiestos",
		"0.70"   : "Added creation of ECUAPASSDOCS fields. Added numero to parameters",
		"0.63"   : "Added creation of CODEBIN fields",
		"0.60"   : "Changed resource names from 'data-XXX' to data_XXX'"
		},
)
