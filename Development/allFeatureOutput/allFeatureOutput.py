import xml.etree.ElementTree as ET
import attributeEncoding_final as AE

# Import data for reading
# This is the name of a srcML document that only has
classFilename = "extendsMicrotask_base.xml"
classTree = ET.parse(classFilename)
classRoot = classTree.getroot()

peripheralClassFile = "extendsMicrotask_peripheral.xml"
peripheralClassTree = ET.parse(peripheralClassFile)
peripheralClassRoot = peripheralClassTree.getroot()


outputFile = "extendsMicrotask2_METAdata.txt"


analysisFileName = "attributeEncoding_extendsMicrotask2.txt"

id_start = 1

allAttributes = {}

# The basic idea of the algorithm is to extract all the attributes from a
# single base class, and then look for those attributes in a set of classes
# that are related to the base class in some way. Only attributes found in
# both the base class and the related (peripheral) classes are output to
# the database that is fed to the FP Growth algorithm.


allAttributes = AE.generateAttributes(classRoot, id_start)[1]

AE.outputDatabase(peripheralClassRoot, allAttributes, analysisFileName)

AE.outputMetaData(allAttributes, outputFile)
