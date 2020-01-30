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


def write_fh(hydro_force, cwd):
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


def read_velocity(cwd, length_velocity,time_aster):
    velocitydict = {}
    cwd_foam_root = "/".join(cwd.split("/")[0:-2])
    control_file = open(cwd_foam_root + '/system/controlDict', 'r')
    lines = control_file.readlines()
    for line in lines:
        if "deltaT" in line:
            dt_foam = float(line.split(" ")[-1])

    while os.path.isfile(cwd_foam_root + "/velocityOnNetpanels.dat"):
        f = open(cwd_foam_root + "/velocityOnNetpanels.dat", "r")
        lines = f.readlines()
        velocitydict['Numoflist'] = 0
        for line in lines:
            if str() + "\n" in line:
                velocitydict['Numoflist'] += 1
                velocitydict['time_foam'] += 1*dt_foam

        for time_foam in range(velocitydict['Numoflist']):
            data_velocity = lines[3 + time_foam * 1157:1155 + time_foam * 1157]
            velocity = []
            for item in data_velocity:
                vector = item.split()
                velocity.append([float(vector[0][1:]), float(vector[1]), float(vector[2][:-1])])
            velocitydict['velocityinsurfaceAt' + str(time_foam + 1)] = velocity
        f.close()
    else:
        print("Wait for velocity from OpenFoam")
        time.sleep(10)

    output = open(cwd + 'velocityfile.pkl', 'wb')
    pickle.dump(velocitydict, output)
    output.close()

    pkfile = open(cwd + 'velocityfile.pkl', 'rb')
    re = pickle.load(pkfile)
    pkfile.close()

    T = re['Numoflist'] * dt_foam
    Velo = re['velocityinsurfaceAt' + str(re['Numoflist'])]
    data = {'Time': T,
            'velo': Velo}
    while float(time_aster) > float(data['Time']):
        time.sleep(10)
        print("Now, the time in Openfoam solver is " + str(re['Time']) +
              "\nThe time in Code_Aster is " + str(time_aster))

    else:
        return data['velo']
