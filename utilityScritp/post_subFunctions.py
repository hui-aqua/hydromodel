"""
-------------------------------------------\n
-         University of Stavanger          \n
-         Hui Cheng (PhD student)          \n
-          Lin Li (Medveileder)            \n
-      Prof. Muk Chen Ong (Supervisor)     \n
-------------------------------------------\n
Any questions about this code,
please email: hui.cheng@uis.no \n
A repository to store all the function that might be used for plotting.
"""
import numpy as np


def read_force(file_name):
    """
    :param file_name: Give the full path and name of the file for total force on netting calculated by Code_Aster hydrodynamic module.
    :return: np.array([time,Fx,Fy,Fz])
    """
    force_str = open(file_name, "r").read().split("\n")
    force_array = np.zeros((len(force_str) - 1, 4))
    for index, one in enumerate(force_str[:-1]):
        force_array[index] = [float(one.split(",")[0][1:]),
                              float(one.split(",")[1]),
                              float(one.split(",")[2]),
                              float(one.split(",")[3][:-1])]
    return force_array


def read_velocity_dict(time, velocity_dict):
    """
    :param time: It has to be a value in "time_record"
    :param velocity_dict: The dictionary that is going to extract data.
    :return: [[u_mag],[ux],[uy],[uz]] and [mean([u_mag]),mean([ux]),mean([uy]),mean([uz])]
    """
    Ux = []
    Uy = []
    Uz = []
    umag = []
    for item in velocity_dict["velocities_at_" + str(time)]:
        Ux.append(float(item[0]))
        Uy.append(float(item[1]))
        Uz.append(float(item[2]))
        umag.append(np.linalg.norm(np.array([float(item[0]),
                                             float(item[1]),
                                             float(item[2])])))
    u = [umag, Ux, Uy, Uz]
    u_mean = [sum(umag) / len(umag),
              sum(Ux) / len(Ux),
              sum(Uy) / len(Uy),
              sum(Uz) / len(Uz)]
    return u, u_mean


def read_positions(file_name):
    """
    :param file_name: Give the full path and name of the file for the posotions of nodes, usually it is located at positionOutput and named as posi***.txt
    :return: np.array([px,py,pz]).size=(n,3) n is the number of points.
    """
    file = open(file_name, 'r')
    posi = file.read().split("\n")
    npposi = np.zeros((len(posi), 3))
    for index, one in enumerate(posi):
        try:
            npposi[index] = [float(one.split()[1]),
                             float(one.split()[2]),
                             float(one.split()[3][:-1])]
        except ValueError:
            npposi[index] = [float(one.split()[1]),
                             float(one.split()[2]),
                             float(one.split()[3][:-2])]
    return npposi


def read_surf(file_name):
    """
    :param file_name: Give the full path and name of the file hydrodynamic element. It is usually located at positionOutput and named as hydro_elements.txt
    :return:[[indexes of nodes]] a list of index of nodes.
    """
    file = open(file_name, 'r')
    elem = file.read().split("[")
    list_elem = []
    for one in elem[2:]:
        try:
            list_elem.append([int(one.split(",")[0]),
                              int(one.split(",")[1]),
                              int(one.split(",")[2][:-1])])
        except ValueError:
            list_elem.append([int(one.split(",")[0]),
                              int(one.split(",")[1]),
                              int(one.split(",")[2][:-2])])
    return list_elem


def read_pressureXY(file_name):
    return np.loadtxt(file_name)


def read_velocityXY(file_name):
    resu = np.loadtxt(file_name)
    u_mean = np.zeros((len(resu), 1))
    for i in range(len(resu)):
        u_mean[i] = np.linalg.norm(np.array(resu[i, 1:]))
    resu = np.hstack((resu, u_mean))
    return resu
