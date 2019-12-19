import os

cwd = os.getcwd()
with open('meshinfomation.txt', 'r') as f:
    content = f.read()
    meshinfo = eval(content)


# D = float(input("\nInput your cage diameter [m] \n"))

def CR_posi():
    # step 1 the head
    output_file = open(cwd + '/posi', 'w')
    output_file.write('''
// Input for the nets in openfoam. 
// Author: Hui Cheng
// Email: hui.cheng@uis.no 
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "constant";
    object      posi;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
{
numOfPoint   ''' + str(meshinfo['numberOfNodes']) + ''' ;''')
    # step 2 the nodes
    output_file.write('\n')
    output_file.close()
    with open(cwd + '/posi', 'a') as the_file:
        for i in range(meshinfo['numberOfNodes']):
            the_file.write('p' + str(i) + ' ( ' + str(meshinfo['netNodes'][i][0]) + '\t' + str(
                meshinfo['netNodes'][i][1]) + '\t' + str(meshinfo['netNodes'][i][2]) + ' );\n')
    # step the tail
    output_file = open(cwd + '/posi', 'a')
    output_file.write('''
}
// ************************************************************************* //
\n''')
    output_file.write('\n')
    output_file.close()


def CR_surc():
    # step 1 the head
    output_file = open(cwd + '/surf', 'w')
    output_file.write('''
// Input for the nets in openfoam. 
// Author: Hui Cheng
// Email: hui.cheng@uis.no 
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "constant";
    object      surc;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
{
numOfSurf   ''' + str(meshinfo['numberOfSurfaces'] * 4) + ''' ;''')

    # step 2 the surface
    newHydroE = []
    output_file.write('\n')
    output_file.close()
    with open(cwd + '/surf', 'a') as the_file:
        for panel in meshinfo['netSurfaces']:
            if len([int(k) for k in set(panel)]) == 3:  # the hydrodynamic element is a triangle
                newHydroE.append([k for k in set([int(k) for k in set(panel)])])  # a list of the node sequence
            else:
                for i in range(len(panel)):  # loop 4 times to map the force
                    nodes = [int(k) for k in set(panel)]  # get the list of nodes [p1,p2,p3,p4]
                    nodes.pop(i)  # delete the i node to make the square to a triangle
                    newHydroE.append(nodes)  # delete the i node to make the square to a triangle
        for ele in newHydroE:
            the_file.write('e' + str(newHydroE.index(ele)) + ' ( ' + str(ele[0]) + '\t' + str(ele[1]) + '\t' + str(
                ele[2]) + ' );\n')
    # step the tail
    output_file = open(cwd + '/surf', 'a')
    output_file.write('''
}
// ************************************************************************* //
\n''')
    output_file.write('\n')
    output_file.close()


CR_posi()
CR_surc()
