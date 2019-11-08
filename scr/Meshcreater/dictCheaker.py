def errormess(ite):
    print("Error! '" + ite + "' is not in cagedict")


listOfInput1 = ['cageType',
                'elementOverCir',
                'elementOverDepth',
                'cageDiameter',
                'cageHeight',
                'NumOfSinker',
                'sinkerWeight'
                ]

listOfInput2 = ['cageType',
                'elementOverCir',
                'elementOverDepth',
                'cageDiameter',
                'cageHeight',
                'bottomringR',
                'bottomringRho',
                'bottomringYoungmodule',
                'centerWeight'
                ]


def check(cage, meshname):
    if meshname == "fishcagewithoutbottom":
        for i in listOfInput1:
            if i not in list(cage):
                errormess(i)
                exit()

    if meshname == "fishcagewithbottom":
        for i in listOfInput2:
            if i not in list(cage):
                errormess(i)
                exit()
