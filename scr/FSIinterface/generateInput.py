# generate input file for openfoam
import os
import workPath
import numpy as np

cwd = os.getcwd()
with open('./asterinput/meshinfomation.txt', 'r') as f:
    content = f.read()
    meshinfo = eval(content)

posiInfo = np.load("posi.npy")
fhInfo = np.load("Fh.npy")


def CR_posi():
    # step 1 the head
    output_file = open(cwd + '/posi', 'w+')
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
            the_file.write('p' + str(i) + ' ( ' + str(posiInfo[i][0]) + '\t' + str(
                posiInfo[i][1]) + '\t' + str(posiInfo[i][2]) + ' );\n')
    # step the tail
    output_file = open(cwd + '/posi', 'a')
    output_file.write('''
}
// ************************************************************************* //
\n''')
    output_file.write('\n')
    output_file.close()


def CR_fh():
    # step 1 the head
    output_file = open(cwd + '/Fh', 'w+')
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
    object      Fh;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
{
numOfFh   ''' + str(meshinfo['numberOfSurfaces'] * 4) + ''' ;''')
    # step 2 the nodes
    output_file.write('\n')
    output_file.close()
    with open(cwd + '/Fh', 'a') as the_file:
        for i in range(meshinfo['numberOfSurfaces'] * 4):
            the_file.write('fh' + str(i) + ' ( ' + str(fhInfo[i][0]) + '\t' + str(
                fhInfo[i][1]) + '\t' + str(fhInfo[i][2]) + ' );\n')

    # step the tail
    output_file = open(cwd + '/Fh', 'a')
    output_file.write('''
}
// ************************************************************************* //
\n''')
    output_file.write('\n')
    output_file.close()


CR_posi()
CR_fh()
