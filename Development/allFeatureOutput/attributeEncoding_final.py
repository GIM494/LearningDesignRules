import xml.etree.ElementTree as ET

# This has the nameSpaces for srcML code; additional namespaces
# may need to be added for languages other than java
nameSpace = { 'src': 'http://www.srcML.org/srcML/src'}

## Comment the following code out before testing with other file ##
#classFilename = "MicrotaskCommand.xml"
#classTree = ET.parse(classFilename)
#classRoot = classTree.getroot()
####################################################################

# List of attributes generated from base class
attributeList = {}

def generateAttributes(classRootNode, id_start):
    id_no = id_start

    # Extract attributes from a single class.
    # Got an error with one of the test files when the .// was removed, so
    # I added it back in. It shouldn't make a difference in the output.
    classRoot = classRootNode.find(".//src:class", nameSpace)


    #classRoot = classRootNode


    # Output all annotations on class
    clsAnnotCandidate = classRoot.findall("src:annotation", nameSpace)
    if clsAnnotCandidate is not None:
        for clsAnnot in clsAnnotCandidate:

            annotArgs = clsAnnot.findall(".//src:argument/src:expr", nameSpace)
            clsAnnotName = "class with annotation @" + (clsAnnot.find('src:name', nameSpace)).text

            if len(annotArgs) > 0:
                clsAnnotName += " with \n"
                for node in annotArgs:
                    for ch in list(node):
                        if ch.text != None:
                            clsAnnotName += ch.text
                        else:
                            for c in list(ch):
                                if c.text != None:
                                    clsAnnotName += c.text
                        clsAnnotName += " "
                    clsAnnotName += "\n"
                #Removes trailing newline
                clsAnnotName = clsAnnotName[0:len(clsAnnotName)-1]

            if clsAnnotName not in attributeList:
                attributeList[clsAnnotName] = id_no
                id_no += 1

    # What kind of constructor the class has
    # Choose last constructor because sometimes a default is defined first
    # and then redefined by another constructor (see Microtask.java)
    constructor = classRoot.findall("src:block/src:constructor", nameSpace)
    if len(constructor) > 0:
        for constr in constructor:
            # Constructor body empty or not
            constructorBody = constr.find("src:block", nameSpace)
            # Initialize arrays for use later
            memVarsSet = []
            setTo = []

            if constructorBody.find(".*", nameSpace) != None:
                name = "class has non-empty-body constructor"
                if name not in attributeList:
                    attributeList[name] = id_no
                    id_no += 1
                # Constructor sets member variables
                constructorExpr = constructorBody.findall("src:expr_stmt/src:expr", nameSpace)
                # If member variables are set:
                for expr in constructorExpr:
                    name = expr.find("src:name/src:name", nameSpace)
                    op = expr.find("src:operator", nameSpace)
                    # If there exists some expr of the form this.field = ____
                    if ((name != None) and (name.text == "this")) and ((op != None) and (op.text == "=")):
                        #Store names of mem vars that are set
                        memVar = expr.find("src:name/src:name[2]", nameSpace)
                        memVarsSet.append(memVar.text)
                        # Store names of things that member variables are set to
                        setToName = expr.find("src:name[2]", nameSpace)
                        # Check if set to null instead of some name
                        if setToName == None:
                            setToName = expr.find("src:literal", nameSpace)
                        if setToName == None:
                            setTo.append("something other than null or variable name")
                        else:
                            setTo.append(setToName.text)
                # Output something like "constructor sets member variables x, y z"
                if len(memVarsSet) != 0:
                    memVarsSet.sort()
                    memVarNames = ", ".join(memVarsSet)
                    name = "constructor sets member variables " + memVarNames
                    if name not in attributeList:
                        attributeList[name] = id_no
                        id_no += 1

                # Check for calls to constructors
                allExpr = constructorBody.findall(".//src:expr", nameSpace)
                for expr in allExpr:
                    op = expr.find("src:operator", nameSpace)
                    call = expr.find("src:call/src:name", nameSpace)
                    if ((op != None) and (op.text == "new")) and ((call != None) and (call.text != None)):
                        name = "call to constructor of " + call.text + " is made in class constructor"
                        if name not in attributeList:
                            attributeList[name] = id_no
                            id_no += 1
            else:
                name = "class has empty-body constructor"
                if name not in attributeList:
                    attributeList[name] = id_no
                    id_no += 1

            # Assume all params stored as member variables
            allParamsStored = True

            paramsList = constr.findall("src:parameter_list/src:parameter/src:decl", nameSpace)
            # If the constructor has parameters
            for p in paramsList:
                # Find name of parameter
                paramName = p.find("src:name", nameSpace)
                # Check if stored as member variable
                if paramName.text != None and paramName.text not in setTo:
                    allParamsStored = False
                # What kind of parameters are in constructor
                paramType = p.find("src:type/src:name", nameSpace)
                # Check for nesting
                if paramType.text == None:
                    paramType = paramType.find("src:name", nameSpace)
                name = "class defines constructor with parameter of type " + paramType.text
                if name not in attributeList:
                    attributeList[name] = id_no
                    id_no += 1

            # If the constructor does not have parameters
            if len(paramsList) == 0:
                name = "class defines constructor with no parameters"
                if name not in attributeList:
                    attributeList[name] = id_no
                    id_no += 1
            else:
                # If the constructor has parameters and all of them were stored
                if allParamsStored == True:
                    name = "constructor stores all parameters as member variables"
                    if name not in attributeList:
                        attributeList[name] = id_no
                        id_no += 1

    # Class does not have a constructor
    else:
        name = "class does not define constructor"
        if name not in attributeList:
            attributeList[name] = id_no
            id_no += 1

    # Output all member fields of a particular type
    # The way we output information about member variables here impacts the
    # interpretations of associated attributes. If there is a member field
    # that has an annotation, two attributes will be output. For example,
    # both class has member field called projectId AND
    # class has member field called projectId with annotation @Index
    # are output for a member field projectId that has annotation @Index.
    # However, if the member field does not have an annotation, only the
    # attribute class has member field called projectId will be output.
    # Later, when attributes are output for other related classes, if both
    # attributes are associated together, then it is the case that the class
    # has a member field with that name and annotation. On the other hand,
    # if only the member field without annotation version of the attribute
    # is frequently associated, then we know that that member field was
    # frequent but not the annotation itself.
    declarations = classRoot.findall("src:block/src:decl_stmt/src:decl", nameSpace)
    if declarations != None:
        for decl in declarations:
            # Generate feature for all member variable names
            memberVarName = decl.find("src:name", nameSpace)
            memberVarNameAttr = "class has member field called " + memberVarName.text
            if memberVarNameAttr not in attributeList:
                attributeList[memberVarNameAttr] = id_no
                id_no += 1
            # Generate feature for all member variable names with annotations
            memberVarAnnotations = decl.findall("src:annotation", nameSpace)
            if memberVarAnnotations != None:
                for annot in memberVarAnnotations:
                    annotName = annot.find("src:name", nameSpace)
                    memberVarAnnotAttr = "class has member field called " + memberVarName.text + " with annotation @" + annotName.text
                    annotArgs = annot.findall(".//src:argument/src:expr", nameSpace)

                    if len(annotArgs) > 0:
                        memberVarAnnotAttr += " with \n"
                        for node in annotArgs:
                            for ch in list(node):
                                if ch.text != None:
                                    memberVarAnnotAttr = memberVarAnnotAttr + ch.text
                                else:
                                    for c in list(ch):
                                        if c.text != None:
                                            memberVarAnnotAttr = memberVarAnnotAttr + c.text
                                memberVarAnnotAttr += " "
                            memberVarAnnotAttr += "\n"

                        # Remove trailing newline
                        memberVarAnnotAttr = memberVarAnnotAttr[0:len(memberVarAnnotAttr)-1]

                    if memberVarAnnotAttr not in attributeList:
                        attributeList[memberVarAnnotAttr] = id_no
                        id_no += 1

            # Generate feature for all member variable types
            memberVarType = decl.find("src:type/src:name", nameSpace)
            # Check for nesting
            if memberVarType.text == None:
                memberVarType = memberVarType.find("src:name", nameSpace)
            memberVarTypeAttr = "class has member field of type " + memberVarType.text
            if memberVarTypeAttr not in attributeList:
                attributeList[memberVarTypeAttr] = id_no
                id_no += 1
            # Generate feature for all member variable names with types
            if memberVarName.text != None and memberVarType.text != None:
                memberVarNameAndType = "class has member field " + memberVarName.text + " of type " + memberVarType.text
                if memberVarNameAndType not in attributeList:
                    attributeList[memberVarNameAndType] = id_no
                    id_no += 1

    # What a class extends
    classExtends = classRoot.find("src:super/src:extends", nameSpace)
    if classExtends != None:
        classExtendsName = "class extends class " + (classExtends.find('src:name', nameSpace)).text
        if classExtendsName not in attributeList:
            attributeList[classExtendsName] = id_no
            id_no += 1

    # What a class implements
    classImplements = classRoot.find("src:super/src:implements", nameSpace)
    if classImplements != None:
        classImplementsName = "class implements " + (classImplements.find("src:name", nameSpace)).text
        if classImplementsName not in attributeList:
            attributeList[classImplementsName] = id_no
            id_no += 1

    # Get class visibility specifier
    clSpecificity = classRoot.find("src:specifier", nameSpace)
    # If the class does not have an explicit visibility specifier
    # then it is public by default
    if clSpecificity == None:
        clSpecificity = "public"
    else:
        clSpecificity = clSpecificity.text

    classSpecName = "is " + clSpecificity + " class"
    if classSpecName not in attributeList:
        attributeList[classSpecName] = id_no
        id_no += 1

    # NOTE: This database is generated by first finding all classes (subclasses,
	# inner classes, outer classes), then finding all top-level functions in each
	# class. We do so to avoid generating duplicate functions/transactions, but
	# one consideration to note is that we may want to know that a function is in
	# a class that is a subclass of X, or that it is in a class that extends Y, etc.

    for fnc in classRoot.findall("src:block/src:function", nameSpace):
        # Get the function name
        fncName = fnc.find("src:name", nameSpace)
        # Get visibility specifiers for the functions
        ## This will capture visibility specifiers, static, and abstract
        # functions
        fncSpec = fnc.findall("src:specifier", nameSpace)
        fncSpecType = " "
        # If the function didn't have a visibility specifier, then we
        # default to the class' visibility
        if len(fncSpec) == 0:
            fncSpecType = clSpecificity

        elif len(fncSpec) > 0:
            # If the function had some kind of specifier (public, private, protected,
            # abstract, or static) then we need to check that at least one is
            # a visibility specifier; visibility specifiers will be listed/found
            # first
            if fncSpec[0].text != "public" and fncSpec[0].text != "private" and fncSpec[0].text != "protected":
                fncSpecType = clSpecificity
            # If the visibility specifier is listed for this function that
            # is what we use
            else:
                fncSpecType = fncSpec[0].text
            # check for other keywords such as abstract or static
            for spec in fncSpec:
                # If statement here to avoid adding the visibility specifier twice
                if spec.text != fncSpecType:
                    fncSpecType = fncSpecType + " " + spec.text

        fncNamePresence = "has " + fncSpecType + " function " + fncName.text + "()"
        fncSpectype = ""
        if fncNamePresence not in attributeList:
            attributeList[fncNamePresence]= id_no
            id_no += 1

        allExpr = fnc.findall(".//src:expr", nameSpace)
        for expr in allExpr:
            op = expr.find("src:operator", nameSpace)
            call = expr.find("src:call/src:name", nameSpace)
            if ((op != None) and (op.text == "new")) and ((call != None) and (call.text != None)):
                name = "call to constructor of " + call.text + " is made in " + fncName.text + "()"
                if name not in attributeList:
                    attributeList[name] = id_no
                    id_no += 1

		# Combine searches for (1) constructor call and (2) function call in return
		# statement (combined for efficiency).
        fncReturnInfo = fnc.find(".//src:block/src:return/src:expr", nameSpace)
        # Function return info exists: search for constructor or call
        if fncReturnInfo is not None:
            # (1) Calls constructor (expandable)
            constructorCall = fncReturnInfo.find("src:operator", nameSpace)
            if constructorCall is not None and constructorCall.text == "new":
                name = fncName.text + "() function calls constructor in return statement"
                # Check whether attribute has been seen globally
                if name not in attributeList:
                    attributeList[name] = id_no
                    id_no += 1
			# (2) Returns output from function call (expandable)
            retOutputFromFncCall = fncReturnInfo.find("src:call", nameSpace)
            if retOutputFromFncCall is not None:
                name = fncName.text +  "() function returns output from function call"
                #### ALSO SEE IF WE CAN GET THE EXACT TYPE FOR THIS ####
                if name not in attributeList:
                    attributeList[name] = id_no
                    id_no += 1
                callName = retOutputFromFncCall.find("src:name", nameSpace)
                # added condition for callName.text != None but not sure why
                if callName is not None and callName.text is not None:
                    name = fncName.text +  "() function returns output from function call to " + callName.text
                    if name not in attributeList:
                        attributeList[name] = id_no
                        id_no += 1

		# Has parameters (expandable)
        fncParams = fnc.findall("src:parameter_list/src:parameter", nameSpace)
        if fncParams == None:
            name = fncName.text + "() function has no parameters"
            # Check whether attribute has been seen globally
            if name not in attributeList:
                attributeList[name] = id_no
                id_no += 1
        else:
            for p in fncParams:
                paramType = p.find("src:decl/src:type/src:name", nameSpace)
                # Check for nesting
                if paramType.text == None:
                    paramType = paramType.find("src:name", nameSpace)
                name = fncName.text + "() function has parameter of type " + paramType.text
                # Check whether attribute has been seen globally
                if name not in attributeList:
                    attributeList[name] = id_no
                    id_no += 1

		# Modifies member variable with specific name
        modifiesMemberVar = fnc.findall("src:block/src:expr_stmt/src:expr", nameSpace)
        if modifiesMemberVar is not None:
            for mod in modifiesMemberVar:
                name = mod.find("src:name/src:name", nameSpace)
                op =  mod.find("src:operator", nameSpace)
                call = mod.find("src:call/src:name/src:name", nameSpace)
                if (name is not None) and (name.text == "this") and (op is not None) and (op.text == "="):
                    attrName = fncName.text + "() function modifies member variable" + name.text
					# Check whether attribute has been seen globally
                    if attrName not in attributeList:
                        attributeList[attrName] = id_no
                        id_no += 1

		# Combine searches for (1) is void and (2) returns type ... (combined for efficiency).
        returnType = fnc.find("src:type/src:name", nameSpace)
        if returnType is not None:
			# Check for list: when the return type is a list, the function's type
    		# nests the list name with other arguments.
            if returnType.text == None:
                returnType = returnType.find("src:name", nameSpace)
    		# (1) Is void
            if returnType.text == "void":
                name = "class has void function " + fncName.text + "()"
				# Check whether attribute has been seen globally
                if name not in attributeList:
                    attributeList[name] = id_no
                    id_no += 1
			# (2) Returns type ...
            else:
                retAttr = fncName.text + "() function returns type " + returnType.text
				# Check whether attribute has been seen globally
                if retAttr not in attributeList:
                    attributeList[retAttr] = id_no
                    id_no += 1


		# Has annotation
        fncAnnotCandidate = fnc.findall("src:annotation", nameSpace)
        if fncAnnotCandidate is not None:
            for fncAnnot in fncAnnotCandidate:
                name = "function " + fncName.text + "() has annotation @" + (fncAnnot.find('src:name', nameSpace)).text
                annotArgs = fncAnnot.findall(".//src:argument/src:expr", nameSpace)

                if len(annotArgs) > 0:
                    name += " with \n"
                    for node in annotArgs:
                        for ch in list(node):
                            if ch.text is not None:
                                name += ch.text
                            else:
                                for c in list(ch):
                                    if c.text != None:
                                        name += c.text
                            name += " "
                        name += "\n"

                    # Remove trailing newline
                    name = name[0:len(name)-1]

			    # Check whether attribute has been seen globally
                if name not in attributeList:
                    attributeList[name] = id_no
                    id_no += 1

    return id_no, attributeList





def outputDatabase(peripheralClassRoot, allAttributes, fileName):

    # This is the file we will be outputting to
    open(fileName,"w").close()


    # Output all attributes in all classes found in this srcML file that are
    # also found in the allAttributes list
    for cl in peripheralClassRoot.findall("src:unit/src:class", nameSpace):

        attributes = []
        # Output all annotations on class
        clsAnnotCandidate = cl.findall("src:annotation", nameSpace)
        if clsAnnotCandidate is not None:
            for clsAnnot in clsAnnotCandidate:

                annotArgs = clsAnnot.findall(".//src:argument/src:expr", nameSpace)
                clsAnnotName = "class with annotation @" + (clsAnnot.find('src:name', nameSpace)).text

                if len(annotArgs) > 0:
                    clsAnnotName += " with \n"
                    for node in annotArgs:
                        for ch in list(node):
                            if ch.text != None:
                                clsAnnotName += ch.text
                            else:
                                for c in list(ch):
                                    if c.text != None:
                                        clsAnnotName += c.text
                            clsAnnotName += " "
                        clsAnnotName += "\n"

                    # Removes trailing newline
                    clsAnnotName = clsAnnotName[0:len(clsAnnotName)-1]

                if clsAnnotName in allAttributes:
                    attributes.append(allAttributes[clsAnnotName])

        # What kind of constructor the class has
        # Choose last constructor because sometimes a default is defined first
        # and then redefined by another constructor (see Microtask.java)
        constructor = cl.findall("src:block/src:constructor", nameSpace)
        if len(constructor) > 0:
            for constr in constructor:
                # Constructor body empty or not
                constructorBody = constr.find("src:block", nameSpace)
                # Initialize arrays for use later
                memVarsSet = []
                setTo = []
                if constructorBody.find(".*", nameSpace) != None:
                    name = "class has non-empty-body constructor"
                    if name in allAttributes:
                        attributes.append(allAttributes[name])

                    # Constructor sets member variables
                    constructorExpr = constructorBody.findall("src:expr_stmt/src:expr", nameSpace)
                    # If member variables are set:
                    for expr in constructorExpr:
                        name = expr.find("src:name/src:name", nameSpace)
                        op = expr.find("src:operator", nameSpace)
                        # If there exists some expr of the form this.field = ____
                        if ((name != None) and (name.text == "this")) and ((op != None) and (op.text == "=")):
                            #Store names of mem vars that are set
                            memVar = expr.find("src:name/src:name[2]", nameSpace)
                            memVarsSet.append(memVar.text)
                            # Store names of things that member variables are set to
                            setToName = expr.find("src:name[2]", nameSpace)
                            # Check if set to null instead of some name
                            if setToName == None:
                                setToName = expr.find("src:literal", nameSpace)
                            if setToName == None:
                                setTo.append("something other than null or variable name")
                            else:
                                setTo.append(setToName.text)

                    # Output something like "constructor sets member variables x, y z"
                    if len(memVarsSet) != 0:
                        memVarsSet.sort()
                        memVarNames = ", ".join(memVarsSet)
                        name = "constructor sets member variables " + memVarNames
                        if name in allAttributes:
                            attributes.append(allAttributes[name])

                    # Check for calls to constructors
                    allExpr = constructorBody.findall(".//src:expr", nameSpace)
                    for expr in allExpr:
                        op = expr.find("src:operator", nameSpace)
                        call = expr.find("src:call/src:name", nameSpace)
                        if ((op != None) and (op.text == "new")) and ((call != None) and (call.text != None)):
                            name = "call to constructor of " + call.text + " is made in class constructor"
                            if name in allAttributes:
                                attributes.append(allAttributes[name])
                else:
                    name = "class has empty-body constructor"
                    if name in allAttributes:
                        attributes.append(allAttributes[name])

                # Assume all params stored as member variables
                allParamsStored = True

                paramsList = constr.findall("src:parameter_list/src:parameter/src:decl", nameSpace)
                # If the constructor has parameters
                for p in paramsList:
                    # Find name of parameter
                    paramName = p.find("src:name", nameSpace)
                    # Check if stored as member variable
                    if paramName.text != None and paramName.text not in setTo:
                        allParamsStored = False
                    # What kind of parameters are in constructor
                    paramType = p.find("src:type/src:name", nameSpace)
                    # Check for nesting
                    if paramType.text == None:
                        paramType = paramType.find("src:name", nameSpace)
                    name = "class defines constructor with parameter of type " + paramType.text
                    if name in allAttributes:
                        attributes.append(allAttributes[name])

                # If the constructor does not have parameters
                if len(paramsList) == 0:
                    name = "class defines constructor with no parameters"
                    if name in allAttributes:
                        attributes.append(allAttributes[name])
                else:
                    # Check if the constructor has parameters and all of them were stored
                    if allParamsStored == True:
                        name = "constructor stores all parameters as member variables"
                        if name in allAttributes:
                            attributes.append(allAttributes[name])
        # Constructor not defined
        else:
            name = "class does not define constructor"
            if name in allAttributes:
                attributes.append(allAttributes[name])


        # Output all member fields of a particular type
        declarations = cl.findall("src:block/src:decl_stmt/src:decl", nameSpace)
        if declarations != None:
            for decl in declarations:
                # Generate feature for all member variable names
                memberVarName = decl.find("src:name", nameSpace)
                memberVarNameAttr = "class has member field called " + memberVarName.text
                if memberVarNameAttr in allAttributes:
                    attributes.append(allAttributes[memberVarNameAttr])
                # Generate feature for all member variable names with annotations
                memberVarAnnotations = decl.findall("src:annotation", nameSpace)
                if memberVarAnnotations != None:
                    for annot in memberVarAnnotations:
                        annotName = annot.find("src:name", nameSpace)
                        memberVarAnnotAttr = "class has member field called " + memberVarName.text + " with annotation @" + annotName.text
                        annotArgs = annot.findall(".//src:argument/src:expr", nameSpace)

                        if len(annotArgs) > 0:
                            memberVarAnnotAttr += " with \n"
                            for node in annotArgs:
                                for ch in list(node):
                                    if ch.text != None:
                                        memberVarAnnotAttr = memberVarAnnotAttr + ch.text
                                    else:
                                        for c in list(ch):
                                            if c.text != None:
                                                memberVarAnnotAttr = memberVarAnnotAttr + c.text
                                    memberVarAnnotAttr += " "
                                memberVarAnnotAttr += "\n"

                            # Remove trailing newline
                            memberVarAnnotAttr = memberVarAnnotAttr[0:len(memberVarAnnotAttr)-1]

                        if memberVarAnnotAttr in allAttributes:
                            attributes.append(allAttributes[memberVarAnnotAttr])

                # Generate feature for all member variable types
                memberVarType = decl.find("src:type/src:name", nameSpace)
                # Check for nesting
                if memberVarType.text == None:
                    memberVarType = memberVarType.find("src:name", nameSpace)
                memberVarTypeAttr = "class has member field of type " + memberVarType.text
                if memberVarTypeAttr in allAttributes:
                    attributes.append(allAttributes[memberVarTypeAttr])
                # Generate feature for all member variable names with types
                if memberVarName.text != None and memberVarType.text != None:
                    memberVarNameAndType = "class has member field " + memberVarName.text + " of type " + memberVarType.text
                    if memberVarNameAndType in allAttributes:
                        attributes.append(allAttributes[memberVarNameAndType])

        # What a class extends
        classExtends = cl.find("src:super/src:extends", nameSpace)
        if classExtends != None:
            classExtendsName = "class extends class " + (classExtends.find('src:name', nameSpace)).text
            if classExtendsName in allAttributes:
                attributes.append(allAttributes[classExtendsName])

        # What a class implements
        classImplements = cl.find("src:super/src:implements", nameSpace)
        if classImplements != None:
            classImplementsName = "class implements " + (classImplements.find("src:name", nameSpace)).text
            if classImplementsName in allAttributes:
                attributes.append(allAttributes[classImplementsName])

        # Get class visibility specifier
        clSpecificity = cl.find("src:specifier", nameSpace)
        # If the class does not have an explicit visibility specifier
        # then it is public by default
        if clSpecificity == None:
            clSpecificity = "public"
        else:
            clSpecificity = clSpecificity.text

        classSpecName = "is " + clSpecificity + " class"
        if classSpecName in allAttributes:
            attributes.append(allAttributes[classSpecName])


        # NOTE: This database is generated by first finding all classes (subclasses,
    	# inner classes, outer classes), then finding all top-level functions in each
    	# class. We do so to avoid generating duplicate functions/transactions, but
    	# one consideration to note is that we may want to know that a function is in
    	# a class that is a subclass of X, or that it is in a class that extends Y, etc.

        for fnc in cl.findall("src:block/src:function", nameSpace):
            # Get the function name
            fncName = fnc.find("src:name", nameSpace)
            # Get visibility specifiers for the functions
            ## This will capture visibility specifiers, static, and abstract
            # functions
            fncSpec = fnc.findall("src:specifier", nameSpace)
            fncSpecType = " "
            # If the function didn't have a visibility specifier, then we
            # default to the class' visibility
            if len(fncSpec) == 0:
                fncSpecType = clSpecificity

            elif len(fncSpec) > 0:
                # If the function had some kind of specifier (public, private, protected,
                # abstract, or static) then we need to check that at least one is
                # a visibility specifier; visibility specifiers will be listed/found
                # first
                if fncSpec[0].text != "public" and fncSpec[0].text != "private" and fncSpec[0].text != "protected":
                    fncSpecType = clSpecificity
                # If the visibility specifier is listed for this function that
                # is what we use
                else:
                    fncSpecType = fncSpec[0].text
                # check for other keywords such as abstract or static
                for spec in fncSpec:
                    # If statement here to avoid adding the visibility specifier twice
                    if spec.text != fncSpecType:
                        fncSpecType = fncSpecType + " " + spec.text

            fncNamePresence = "has " + fncSpecType + " function " + fncName.text + "()"
            fncSpectype = ""

            if fncNamePresence in allAttributes:
                attributes.append(allAttributes[fncNamePresence])

            # Check for call to constructor
            allExpr = fnc.findall(".//src:expr", nameSpace)
            for expr in allExpr:
                op = expr.find("src:operator", nameSpace)
                call = expr.find("src:call/src:name", nameSpace)
                if ((op != None) and (op.text == "new")) and ((call != None) and (call.text != None)):
                    name = "call to constructor of " + call.text + " is made in " + fncName.text + "()"
                    if name in allAttributes:
                        attributes.append(allAttributes[name])

    		# Combine searches for (1) constructor call and (2) function call in return
    		# statement (combined for efficiency).
            fncReturnInfo = fnc.find(".//src:block/src:return/src:expr", nameSpace)
            # Function return info exists: search for constructor or call
            if fncReturnInfo is not None:
                # (1) Calls constructor (expandable)
                constructorCall = fncReturnInfo.find("src:operator", nameSpace)
                if constructorCall is not None and constructorCall.text == "new":
                    name = fncName.text + "() function calls constructor in return statement"
                    # Check whether attribute has been seen globally
                    if name in allAttributes:
                        attributes.append(allAttributes[name])

    			# (2) Returns output from function call (expandable)
                retOutputFromFncCall = fncReturnInfo.find("src:call", nameSpace)
                if retOutputFromFncCall is not None:
                    name = fncName.text +  "() function returns output from function call"
                    #### ALSO SEE IF WE CAN GET THE EXACT TYPE FOR THIS ####
                    if name in allAttributes:
                        attributes.append(allAttributes[name])
                    callName = retOutputFromFncCall.find("src:name", nameSpace)
                    # added callName.text != None to fix bug
                    if callName is not None and callName.text is not None:
                        name = fncName.text +  "() function returns output from function call to " + callName.text
                        if name in allAttributes:
                            attributes.append(allAttributes[name])

    		# Has parameters (expandable)
            fncParams = fnc.findall("src:parameter_list/src:parameter", nameSpace)
            if fncParams == None:
                name = fncName.text + "() function has no parameters"
                # Check whether attribute has been seen globally
                if name in allAttributes:
                    attributes.append(allAttributes[name])
            else:
                for p in fncParams:
                    paramType = p.find("src:decl/src:type/src:name", nameSpace)
                    # Check for nesting
                    if paramType.text == None:
                        paramType = paramType.find("src:name", nameSpace)
                    name = fncName.text + "() function has parameter of type " + paramType.text
                    # Check whether attribute has been seen globally
                    if name in allAttributes:
                        attributes.append(allAttributes[name])

    		# Modifies member variable with specific name
            modifiesMemberVar = fnc.findall("src:block/src:expr_stmt/src:expr", nameSpace)
            if modifiesMemberVar is not None:
                for mod in modifiesMemberVar:
                    name = mod.find("src:name/src:name", nameSpace)
                    op =  mod.find("src:operator", nameSpace)
                    if ((name != None) and (name.text == "this")) and ((op is not None) and (op.text == "=")):
                        attrName = fncName.text + "() function modifies member variable" + name.text
    					# Check whether attribute has been seen globally
                        if attrName in allAttributes:
                            attributes.append(allAttributes[attrName])

    		# Combine searches for (1) is void and (2) returns type ... (combined for efficiency).
            returnType = fnc.find("src:type/src:name", nameSpace)
            if returnType is not None:
    			# Check for list: when the return type is a list, the function's type
        		# nests the list name with other arguments.
                if returnType.text == None:
                    returnType = returnType.find("src:name", nameSpace)
        		# (1) Is void
                if returnType.text == "void":
                    name = "class has void function " + fncName.text + "()"
    				# Check whether attribute has been seen globally
                    if name in allAttributes:
                        attributes.append(allAttributes[name])
    			# (2) Returns type ...
                else:
                    retAttr = fncName.text + "() function returns type " + returnType.text
    				# Check whether attribute has been seen globally
                    if retAttr in allAttributes:
                        attributes.append(allAttributes[retAttr])


            # Has annotation
            fncAnnotCandidate = fnc.findall("src:annotation", nameSpace)
            if fncAnnotCandidate is not None:
                for fncAnnot in fncAnnotCandidate:
                    name = "function " + fncName.text + "() has annotation @" + (fncAnnot.find('src:name', nameSpace)).text
                    annotArgs = fncAnnot.findall(".//src:argument/src:expr", nameSpace)

                    if len(annotArgs) > 0:
                        name += " with \n"
                        for node in annotArgs:
                            for ch in list(node):
                                if ch.text is not None:
                                    name += ch.text
                                else:
                                    for c in list(ch):
                                        if c.text != None:
                                            name += c.text
                                name += " "
                            name += "\n"
                        # Remove trailing newline
                        name = name[0:len(name)-1]

                # Check whether attribute has been seen globally
                if name in allAttributes:
                    attributes.append(allAttributes[name])

        # Remove duplicates in attributes list

        # From stackoverflow: In Python 3.7, the regular dict is guaranteed
        # to be bothe ordered and unique across all implementations.

        # We don't care about order here (we will sort them anyway),
        # but it is the most elegant solution
        attributes = list(dict.fromkeys(attributes))
        # Sort attribute values in ascending order
        attributes.sort()


        # This is the file we will be outputting to
        file = open(fileName,"a+")
        # Output attributes found to database
        # Current FP Growth implementation will stop when it reads a newline
        # so we don't want it to output newlines when attributes is empty
        if len(attributes) > 0:
            file.write(' '.join(str(attr) for attr in attributes))
            file.write('\n')

        attributes.clear()
        file.close()




def outputMetaData(allAttributes, outputFile):

    file = open(outputFile, "w")

    for m in allAttributes:
        file.write(str(allAttributes[m]) + " " + str(m) + "\n")

    file.close()
