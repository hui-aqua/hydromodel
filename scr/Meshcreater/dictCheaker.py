"""
this is to check if the components are intact
"""
def errormess(ite):
    print("Error! '" + ite + "' is not in cagedict")

listOfInput1 = ['cageType',
                'elementOverCir',
                'elementOverDepth',
                'cageDiameter',
                'cageHeight',
                'weightType',
                'NumOfSinker',
                'sinkerWeight'
                ]

listOfInput2 = ['cageType',
                'elementOverCir',
                'elementOverDepth',
                'cageDiameter',
                'cageHeight',
                'centerTipHeight'
                'weightType',
                'bottomringR',
                'bottomringRho',
                'bottomringYoungmodule',
                'centerWeight',
                ]


def check(cage, meshType):
    if meshType == "fishcagewithoutbottom":
        for i in listOfInput1:
            if i not in list(cage):
                errormess(i)
                exit()
        if not float(cage['elementOverCir'] / cage['NumOfSinker']).is_integer():
            print("\nAlarm! The sinkers cannot be evenly distributed in the bottom.\n"
                  "\nYou have to set the sinkers in the mesh file manually through GUI.\n")

    if meshType == "fishcagewithbottom":
        for i in listOfInput2:
            if i not in list(cage):
                errormess(i)
                exit()
