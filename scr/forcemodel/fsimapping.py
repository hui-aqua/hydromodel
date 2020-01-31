"""
/--------------------------------\
|    University of Stavanger     |
|           Hui Cheng            |
\--------------------------------/
Any questions about this code, please email: hui.cheng@uis.no

"""
import pickle
import os
import time


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


def write_element(hydro_element, cwd):
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


def write_fh(hydro_force, timeFE,cwd):
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
timeInFE  ''' + str(timeFE) + ''' ;
numOfFh   ''' + str(len(hydro_force)) + ''' ;''')
    output_file.write('\n')
    output_file.close()
    # step 2 the nodes

    with open(cwd + '/Fh', 'a') as the_file:
        for i in range(len(hydro_force)):
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

# here we assume Code_aster is much faster than OpenFoam, thus OpenFOAM do not need to wait .
def get_velocity(cwd, length_velocity, time_aster):
    cwd_foam_root = "/".join(cwd.split("/")[0:-2])
    velocity_file, time_foam = read_velocity(cwd_foam_root, length_velocity)
    while float(time_aster) > float(time_foam) or time_foam == 0:
        time.sleep(2)
        velocity_file, time_foam = read_velocity(cwd_foam_root, length_velocity)
    else:
        return velocity_file["velocities_at_" + str(time_foam)]


def read_velocity(cwd_foam_root, length_velocity):
    velocity_dict = {}
    while not os.path.isfile(cwd_foam_root + "/velocity_on_elements.txt"):
        print("Wait for velocity from OpenFoam")
        time.sleep(10)
    else:
        f = open(cwd_foam_root + "/velocity_on_elements.txt", "r")
        lines = f.readlines()
        velocity_dict['time_slice'] = []
        time_foam = 0
        for line in lines:
            if "The velocities at" in line:
                time_foam = line.split(" ")[-3][:-1]
                velocity_dict['time_slice'].append(time_foam)
                start_line = lines.index(line) + 3
                velocity_dict["velocities_at_" + str(time_foam)] = []
                for element in lines[start_line:start_line + length_velocity]:
                    velocity_dict["velocities_at_" + str(time_foam)].append(
                        [float(element.split()[0][1:]), float(element.split()[1]), float(element.split()[2][:-1])])
    return velocity_dict, time_foam