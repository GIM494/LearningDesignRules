string fileName = "FPRules.txt"
targetAttrs = {1,2,3}

file = open(fileName, "r")

antecedent = {}
consequent = {}

for line in file.readlines():
    allParts = line.split(" ")
    foundArrow = False

    for p of allParts:
        if p == "==>":
            foundArrow = True

        if foundArrow:
            consequent.append(p)
        else:
            antecedent.append(p)

    matches = match(antecedent, targetAttrs)
    if !(all([v == 0 for v in matches])):
        print(line)

    else:
        matches = match(consrquent, targetAttrs)
        if !(all([v == 0 for v in matches])):
            print(line)
