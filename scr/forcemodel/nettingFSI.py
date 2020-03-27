""""""
"""
----------------------------------------------
--         University of Stavanger          --
--         Hui Cheng (PhD student)          --
--          Lin Li (Medveileder)            --
--      Prof. Muk Chen Ong (Supervisor)     --
----------------------------------------------
Any questions about this code,
please email: hui.cheng@uis.no
A module can be used to calculate the hydrodynamic forces on nets in Code_Aster.
To use this module, one should be import this into the input file for calculations.

"""
import os
import time
import numpy as np


# here we assume Code_aster is much faster than OpenFoam, thus OpenFOAM do not need to wait .

def start_flag(cwd, flag):
    if os.path.exists(cwd + str(flag)):
        os.remove(cwd + str(flag))


def finish_flag(cwd, flag):
    # print("in finish_flag, the cwd is "+cwd)
    os.mknod(cwd + str(flag))


def write_position(position, cwd):
    # print("Here>>>>>>>>>>>>>posi")
    start_flag(cwd, "/position_flag")
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
    finish_flag(cwd, "/position_flag")


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


def write_fh(hydro_force, timeFE, cwd):
    print("Here>>>>>>>>>>>>>Fh>>>  "+str(timeFE))
    start_flag(cwd, "/fh_flag")
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
    finish_flag(cwd, "/fh_flag")


velocity_dict = {'time_record': ['0']}


def get_velocity(cwd, length_velocity, time_aster):
    """
    :param cwd: working path for code aster
    :param length_velocity: the length of the list of element(or vlocity)
    :param time_aster:
    :return: a numpy array of velocity on elements
    """
    print("Here>>>>>>>>>>>>>velo>>>  "+str(time_aster))
    cwd_foam_root = "/".join(cwd.split("/")[0:-2])
    velocity_dict, time_foam = read_velocity(cwd_foam_root, length_velocity)
    time_foam = velocity_dict['time_record'][-1]
    while float(time_aster) > float(time_foam) or str(time_foam) == str(0):
        time.sleep(1)
        velocity_dict, time_foam = read_velocity(cwd_foam_root, length_velocity)
    else:
        # velocity_dict, time_foam = read_velocity(cwd_foam_root, length_velocity)
        # print("velocity from get_velocity i s "+str(np.array(velocity_dict["velocities_at_" + str(time_foam)])))
        f = open(cwd + "/velocity_on_element.txt", "w")
        f.write(str(velocity_dict))
        f.close()
        return np.array(velocity_dict["velocities_at_" + str(time_foam)])


def read_velocity(cwd_foam_root, length_velocity):
    while not os.path.isfile(cwd_foam_root + "/velocity_on_elements.txt"):
        print("Wait for velocity from OpenFoam......")
        time.sleep(10)
    else:
        f = open(cwd_foam_root + "/velocity_on_elements.txt", "r")
        lines = f.readlines()
        time_foam = str(0)
        for line in lines[-length_velocity * 5:]:
            if "The velocities at" in line:
                time_foam = line.split(" ")[3]
                if len(line.split()) == 6:
                    start_line = lines.index(line) + 3
                    end_line = lines.index(line) + 3 + length_velocity
                    if (end_line < len(lines)) and (str(time_foam) not in velocity_dict['time_record']):
                        velocity_dict['time_record'].append(str(time_foam))
                        velocity_dict["velocities_at_" + str(time_foam)] = []
                        for item in range(length_velocity):
                            try:
                                velocity_dict["velocities_at_" + str(time_foam)].append(
                                    [float(lines[item + start_line].split()[0][1:]),
                                     float(lines[item + start_line].split()[1]),
                                     float(lines[item + start_line].split()[2][:-1])])
                            except:
                                velocity_dict["velocities_at_" + str(time_foam)].append(
                                    [float(lines[start_line].split()[0][1:]),
                                     float(lines[start_line].split()[1]),
                                     float(lines[start_line].split()[2][:-1])])
    return velocity_dict, time_foam
