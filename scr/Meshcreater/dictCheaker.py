"""
this is to check if the components are intact
todo need to update
"""
def errormess(ite):
    print("Error! '" + ite + "' is not in CageShape")


cylindricalNoBottom = ['shape',
                       'elementOverCir',
                       'elementOverHeight',
                       'cageDiameter',
                       'cageHeight',
                       ]
cylindricalWithBottom = ['shape',
                'elementOverCir',
                         'elementOverHeight',
                'cageDiameter',
                'cageHeight',
                         'cageCenterTip',
                         ]



def check(cage, meshType):
    if meshType == "cylindricalNoBottom":
        for i in cylindricalNoBottom:
            if i not in list(cage['CageShape']):
                errormess(i)
                exit()

    if meshType == "cylindricalWithBottom":
        for i in cylindricalWithBottom:
            if i not in list(cage['CageShape']):
                errormess(i)
                exit()

        # if not float(cage['elementOverCir'] / cage['NumOfSinker']).is_integer():
        #     print("\nAlarm! The sinkers cannot be evenly distributed in the bottom.\n"
        #           "\nYou have to set the sinkers in the mesh file manually through GUI.\n")
