import xml.etree.ElementTree as ET
nameSpace = { 'src': 'http://www.srcML.org/srcML/src'}

parentFncs = []
subCLfncs = []

def addParentChildRelations(classTree, id_no, attributeList, parentClassList):

    # First we're going to gather all of the information about the parent
    # classes; in this case, we're just wanting all of the functions
    # in the parent class
    for clsRoot in classTree.findall(".//src:class", nameSpace):

        clsName = clsRoot.find("src:name", nameSpace)
        if clsName is not None:
            if clsName.text is not None:
                clsName = clsName.text
        else:
            continue

        #print(clsName)

        # If the class is a parent class, then we want to make a list of all of
        # the functions that it has
        if clsName in parentClassList:

            for fnc in clsRoot.findall("src:block/src:function", nameSpace):
                # Get the function name
                fncName = (fnc.find("src:name", nameSpace)).text
                parentFncs.append(fncName)


            # Sort for easy comparison
            parentFncs.sort()

            #print("parentFunctions: ", parentFncs)

            # Then, we're going to see if this child class overrides
            # the functions in the parent class


            # This array is to keep track of what functions are overridden in
            # the child class; we assume they are overridden, but once
            # we find a class that doesn't override a parent function we
            # set that element to Falsee
            parentFncsOverridden = [True] * len(parentFncs)

            for subCL in classTree.findall(".//src:class", nameSpace):

                classExtends = subCL.find("src:super/src:extends", nameSpace)
                if classExtends != None:
                    clsN = (classExtends.find('src:name', nameSpace))
                    if clsN.text is None:
                        clsN = (clsN.find('src:name', nameSpace)).text
                    else:
                        clsN = clsN.text
                    # If this class extends the parent class, then we want to
                    # see if it overrides all the functions in the parent class;
                    if clsN is not None and clsN == clsName:

                        # First get a list of all the child functions
                        for fnc in subCL.findall("src:block/src:function", nameSpace):
                            # Get the function name
                            fncName = (fnc.find("src:name", nameSpace)).text
                            subCLfncs.append(fncName)

                        subCLfncs.sort()

                        #print(subCLfncs)

                        # Then see what functions are in common between the
                        # two lists
                        matchingFunctions = list(set(parentFncs).intersection(subCLfncs))


                        #print("matching functions:", matchingFunctions)


                        # This index is true then I need to have found the function
                        # at the corresponding parent index, otherwise I set that element to
                        # false
                        for m in range(0, len(parentFncsOverridden)):

                            # If the element at this index is True, then I must also
                            # have found corresponding function in the child class;
                            # otherwise I change this elements value to False
                            if parentFncsOverridden[m]:
                                # If we can't find this parent function in the
                                # child class, we change its value to False
                                if parentFncs[m] not in matchingFunctions:
                                    parentFncsOverridden[m] = False


                        for f in parentFncsOverridden[m]:
                            if f:

                                attr = "All children classes override function " + parentFncs[f] + "() in parent class"

                                if attr not in attributeList:
                                    attributeList[attr] = id_no
                                    id_no += 1    


            # After processing all of the children classes see which ones have
            # all overridden the same functions in the parent class
            for f in range(0, len(parentFncsOverridden)):
                if parentFncsOverridden[f]:

                        #print(attr)

            parentFncs.clear()


    return id_no, attributeList



def findParentChildRelations(peripheralClassRoot, allAttributes, attributes, parentClassList):

    #print("Here.")

    # First we're going to gather all of the information about the parent
    # classes; in this case, we're just wanting all of the functions
    # in the parent class


    for clsRoot in peripheralClassRoot.findall(".//src:class", nameSpace):

        clsName = clsRoot.find("src:name", nameSpace)
        if clsName is not None:
            if clsName.text is not None:
                clsName = clsName.text
        else:
            continue

        #print(clsName)

        # If the class is a parent class, then we want to make a list of all of
        # the functions that it has
        if clsName in parentClassList:

            for fnc in clsRoot.findall("src:block/src:function", nameSpace):
                # Get the function name
                fncName = (fnc.find("src:name", nameSpace)).text
                parentFncs.append(fncName)


            # Sort for easy comparison
            parentFncs.sort()

            #print("parentFunctions: ", parentFncs)

            # Then, we're going to see if all classes that extend the parent
            # class override the functions in that clas


            # This array is to keep track of what functions are overridden in
            # the child classes; we assume they are overridden, but once
            # we find a class that doesn't override a parent function we
            # set that element to Falsee
            parentFncsOverridden = [True] * len(parentFncs)

            for subCL in peripheralClassRoot.findall(".//src:class", nameSpace):

                classExtends = subCL.find("src:super/src:extends", nameSpace)
                if classExtends != None:
                    clsN = (classExtends.find('src:name', nameSpace))
                    if clsN.text is None:
                        clsN = (clsN.find('src:name', nameSpace)).text
                    else:
                        clsN = clsN.text
                    # If this class extends the parent class, then we want to
                    # see if it overrides all the functions in the parent class;
                    if clsN is not None and clsN == clsName:

                        # First get a list of all the child functions
                        for fnc in subCL.findall("src:block/src:function", nameSpace):
                            # Get the function name
                            fncName = (fnc.find("src:name", nameSpace)).text
                            subCLfncs.append(fncName)

                        subCLfncs.sort()

                        #print(subCLfncs)

                        # Then see what functions are in common between the
                        # two lists
                        matchingFunctions = list(set(parentFncs).intersection(subCLfncs))


                        #print("matching functions:", matchingFunctions)


                        # this index is true then I need to have found the function
                        # at the corresponding parent index, otherwise I set that element to
                        # false
                        for m in range(0, len(parentFncsOverridden)):

                            # If the element at this index is True, then I must also
                            # have found corresponding function in the child class;
                            # otherwise I change this elements value to False
                            if parentFncsOverridden[m]:
                                # If we can't find this parent function in the
                                # child class, we change its value to False
                                if parentFncs[m] not in matchingFunctions:
                                    parentFncsOverridden[m] = False

                        #for m in range(0, len(parentFncsOverridden)):
                        #    print(parentFncs[m] + ": " + str(parentFncsOverridden[m]))

                        subCLfncs.clear()


            # After processing all of the children classes see which ones have
            # all overridden the same functions in the parent class
            for f in range(0, len(parentFncsOverridden)):
                if parentFncsOverridden[f]:
                    attr = "All children classes override function " + parentFncs[f] + "() in parent class"

                    #print(attr)

                    if attr in allAttributes:
                        attributes.append(allAttributes[attr])
                        #print(allAttributes[attr])


            parentFncs.clear()


    return attributes
