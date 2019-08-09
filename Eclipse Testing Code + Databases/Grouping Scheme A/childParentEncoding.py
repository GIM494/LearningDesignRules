import xml.etree.ElementTree as ET
import  childParentDatabase as CPD

# Import data for reading
# This is the name of a srcML document that only has
classFilename = "eclipse.xml"
classTree = ET.parse(classFilename)
classRoot = classTree.getroot()

peripheralClassFile = "eclipse.xml"
peripheralClassTree = ET.parse(peripheralClassFile)
peripheralClassRoot = peripheralClassTree.getroot()

outputFile = "attributeMETAdata_eclipse.xml.txt"

# For this version it should be some sort of "start" to a name since we want
# to output a different database for each set of children classes
analysisFileName = "AE_eclipse"

id_start = 1

nameSpace = { 'src': 'http://www.srcML.org/srcML/src'}
allAttributes = {}

# The basic idea of the algorithm is to extract all the attributes from a
# single base class, and then look for those attributes in a set of classes
# that are related to the base class in some way. Only attributes found in
# both the base class and the related (peripheral) classes are output to
# the database that is fed to the FP Growth algorithm.

parentClassList = CPD.makeParentList(peripheralClassRoot)

parentClassList.sort()
#print(parentClassList)

output = CPD.addParentChildRelations(classTree, id_start, parentClassList)
allAttributes.update(output[1])
id_start = output[0]

CPD.findParentChildRelations(peripheralClassRoot, allAttributes, parentClassList, analysisFileName)

CPD.outputMetaData(allAttributes, outputFile)
