import xml.etree.ElementTree as ET
import allFeatureOutput_abstrctAdd as AE
import parentChildRelations as PCR

# Import data for reading
# This is the name of a srcML document that only has
classFilename = "eclipse.xml"
classTree = ET.parse(classFilename)
classRoot = classTree.getroot()

peripheralClassFile = "eclipse_compatibilityAll.xml"
peripheralClassTree = ET.parse(peripheralClassFile)
peripheralClassRoot = peripheralClassTree.getroot()

outputFile = "attributeMETAdata_eclipseCompat_All.txt"


analysisFileName = "AE_eclipseCompat_All.txt"

id_start = 1

nameSpace = { 'src': 'http://www.srcML.org/srcML/src'}
allAttributes = {}
parentClassList = {}

# The basic idea of the algorithm is to extract all the attributes from a
# single base class, and then look for those attributes in a set of classes
# that are related to the base class in some way. Only attributes found in
# both the base class and the related (peripheral) classes are output to
# the database that is fed to the FP Growth algorithm.

for clRoot in classRoot.findall(".//src:class", nameSpace):
    #if clRoot.find("src:name", nameSpace) != None:
    #    print((clRoot.find("src:name", nameSpace)).text)
    result = AE.generateAttributes(clRoot, id_start)
    allAttributes.update(result[1])
    id_start = result[0]
    parentClassList = result[2]

output = PCR.addParentChildRelations(classTree, id_start, allAttributes, parentClassList)
allAttributes.update(output[1])
id_start = result[0]


AE.outputDatabase(peripheralClassRoot, allAttributes, analysisFileName)

AE.outputMetaData(allAttributes, outputFile)
