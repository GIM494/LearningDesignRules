import xml.etree.ElementTree as ET
import attributeEncoding_outputAllAttr as AE

# Import data for reading
# This is the name of a srcML document that only has
classFilename = "cc_commands_Package.xml"
classTree = ET.parse(classFilename)
classRoot = classTree.getroot()

peripheralClassFile = "cc_commands_Package.xml"
peripheralClassTree = ET.parse(peripheralClassFile)
peripheralClassRoot = peripheralClassTree.getroot()

outputFile = "attributeMETAdata_cc_commands_Package.txt"


analysisFileName = "AE_cc_commands_Package.txt"

id_start = 1

nameSpace = { 'src': 'http://www.srcML.org/srcML/src'}
allAttributes = {}

# The basic idea of the algorithm is to extract all the attributes from a
# single base class, and then look for those attributes in a set of classes
# that are related to the base class in some way. Only attributes found in
# both the base class and the related (peripheral) classes are output to
# the database that is fed to the FP Growth algorithm.


for clRoot in classTree.findall(".//src:class", nameSpace):
    #if clRoot.find("src:name", nameSpace) != None:
    #    print((clRoot.find("src:name", nameSpace)).text)
    result = AE.generateAttributes(clRoot, id_start)
    allAttributes.update(result[1])
    id_start = result[0]


AE.outputDatabase(peripheralClassRoot, allAttributes, analysisFileName)

AE.outputMetaData(allAttributes, outputFile)
