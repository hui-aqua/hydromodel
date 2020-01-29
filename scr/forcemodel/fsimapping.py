"""
/--------------------------------\
|    University of Stavanger     |
|           Hui Cheng            |
\--------------------------------/
Any questions about this code, please email: hui.cheng@uis.no

"""


def write_position(position, cwd):
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
numOfPoint   ''' + str(len(position)) + ''' ;''')
    output_file.write('\n')
    output_file.close()
    # step 2 the nodes
    with open(cwd + 'posi', 'a') as the_file:
        for i in range(len(position)):
            the_file.write('p' + str(i) + ' ( ' + str(position[i][0]) + '\t' + str(
                position[i][1]) + '\t' + str(position[i][2]) + ' );\n')

    # step the tail
    output_file = open(cwd + 'posi', 'a')
    output_file.write('''
}
// ************************************************************************* //
\n''')
    output_file.write('\n')
    output_file.close()


def write_element(hydro_element,cwd):
    # step 1 the head
    output_file = open(cwd + 'surf', 'w')
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
numOfSurf   ''' + str(len(hydro_element)) + ''' ;''')
    output_file.write('\n')
    output_file.close()
    # step 2 the surface
    with open(cwd + 'surf', 'a') as the_file:
        for ele in hydro_element:
            the_file.write('e' + str(hydro_element.index(ele)) + ' ( ' + str(ele[0]) + '\t' + str(ele[1]) + '\t' + str(
                ele[2]) + ' );\n')
    # step the tail
    output_file = open(cwd + 'surf', 'a')
    output_file.write('''
}
// ************************************************************************* //
\n''')
    output_file.write('\n')
    output_file.close()


def write_fh(hydro_force,cwd):
    # step 1 the head
    output_file = open(cwd + 'Fh', 'w+')
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
numOfFh   ''' + str(len(hydro_force)) + ''' ;''')
    output_file.write('\n')
    output_file.close()
    # step 2 the nodes

    with open(cwd + '/Fh', 'a') as the_file:
        for i in range(hydro_force):
            the_file.write('fh' + str(i) + ' ( ' + str(hydro_force[i][0]) + '\t' + str(
                hydro_force[i][1]) + '\t' + str(hydro_force[i][2]) + ' );\n')

    # step the tail
    output_file = open(cwd + 'Fh', 'a')
    output_file.write('''
}
// ************************************************************************* //
\n''')
    output_file.write('\n')
    output_file.close()
