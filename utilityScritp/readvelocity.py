"""
----------------------------------------------
--         University of Stavanger          --
--         Hui Cheng (PhD student)          --
--          Lin Li (Medveileder)            --
--      Prof. Muk Chen Ong (Supervisor)     --
----------------------------------------------
Any questions about this code,
please email: hui.cheng@uis.no
"""
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
import matplotlib.gridspec as gc
import sys
import ast

def getData(time):
    Ux = []
    Uy = []
    Uz = []
    for item in velocity_dict["velocities_at_" + str(time)]:
        Ux.append(item[0])
        Uy.append(item[1])
        Uz.append(item[2])
    U = [Ux, Uy, Uz]
    Umean = [sum(Ux) / len(Ux), sum(Uy) / len(Uy), sum(Uz) / len(Uz)]
    return U, Umean


def oneFigure(time):
    points = [i for i in range(len(velocity_dict["velocities_at_" +  str(time)]))]
    U,Umean=getData(time)
    titles=['U_x','U_y','U_z']
    colors=['r','g','b']
    gs = gc.GridSpec(1, 3)
    for i in range(3):
        ax = plt.subplot(gs[i])
        plt.title(titles[i]+" at " + str(time) + "s")
        ax.scatter(points, U[i], color=colors[i], marker='.')
        ax.plot([0, len(points)], [Umean[i], Umean[i]], color='k')
        plt.ylabel("velocity (m/s)")
        plt.xlabel("mean velocity =" + str(Umean[i]) + "(m/s)")

    plt.tight_layout()
    plt.show()


def ani(velocity_dict):
    for record in velocity_dict['time_record'][1:]:
        print("record is " +str(record))
        plt.figure(figsize=(16, 5))
        oneFigure(record)
# main()

with open(sys.argv[1], 'r') as f:
    content = f.read()
    velocity_dict = ast.literal_eval(content)

print("The recorded velocities are" + str(velocity_dict["time_record"]) + "\n")

time_selected = str(input("Please choose a time slice: \n"))

print("Plotting the velocity statistics at " + str(time_selected) + " s \n")
plt.figure(figsize=(16, 5))
oneFigure(time_selected)

# playAni = str(input("Do you want to play a animation? \n"))
#
# if playAni == "yes":
#
#     fig = plt.figure(figsize=(16, 5))
#     anim = animation.FuncAnimation(fig, ani(velocity_dict),
#                                    frames=200, interval=20, blit=True)
