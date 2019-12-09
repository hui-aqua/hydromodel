import os

cwd = os.getcwd()
with open('meshinfomation.txt', 'r') as f:
    content = f.read()
    meshinfo = eval(content)


# D = float(input("\nInput your cage diameter [m] \n"))

def CR_posi():
    # step 1 the head
    output_file = open(cwd + 'posi', 'w')
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
    with open(cwd + 'posi', 'a') as the_file:
        for i in range(meshinfo['numberOfNodes']):
            the_file.write('p' + str(i) + ' ( ' + str(meshinfo['netNodes'][i][0]) + '\t' + str(
                meshinfo['netNodes'][i][1]) + '\t' + str(meshinfo['netNodes'][i][2]) + ' );\n')
    # step the tail
    output_file = open(cwd + 'posi', 'a')
    output_file.write('''
}
// ************************************************************************* //
\n''')
    output_file.write('\n')
    output_file.close()


def CR_surc():
    # step 1 the head
    output_file = open(cwd + 'surc', 'w')
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
numOfSurc   ''' + str(meshinfo['numberOfSurfaces'] * 2) + ''' ;''')

    # step 2 the surface
    output_file.write('\n')
    output_file.close()
    with open(cwd + 'surc', 'a') as the_file:
        for i in range(meshinfo['numberOfSurfaces']):
            the_file.write('e' + str(i) + ' ( ' + str(meshinfo['netSurfaces'][i][0]) + '\t' + str(
                meshinfo['netSurfaces'][i][1]) + '\t' + str(meshinfo['netSurfaces'][i][2]) + ' );\n')
            the_file.write(
                'e' + str(meshinfo['numberOfSurfaces'] + i) + ' ( ' + str(meshinfo['netSurfaces'][i][1]) + '\t' + str(
                    meshinfo['netSurfaces'][i][3]) + '\t' + str(meshinfo['netSurfaces'][i][2]) + ' );\n')

    # step the tail
    output_file = open(cwd + 'surc', 'a')
    output_file.write('''
}
// ************************************************************************* //
\n''')
    output_file.write('\n')
    output_file.close()


CR_posi()
CR_surc()
