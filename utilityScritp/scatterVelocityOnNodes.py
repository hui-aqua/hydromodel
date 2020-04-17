"""
-------------------------------------------\n
-         University of Stavanger          \n
-         Hui Cheng (PhD student)          \n
-          Lin Li (Medveileder)            \n
-      Prof. Muk Chen Ong (Supervisor)     \n
-------------------------------------------\n
Any questions about this code,
please email: hui.cheng@uis.no \n
"""

norm = matplotlib.colors.Normalize(vmin=0.00, vmax=1)


def geoFigure(file_folder, time):
    positions = ps.read_positions(file_folder + "posi" + str(time) + ".txt")
    hydro_element = ps.read_surf(file_folder + "hydro_elements.txt")
    position_probe = np.zeros((len(hydro_element), 3))
    for index, one in enumerate(hydro_element):
        center = positions[int(one[0])] + positions[int(one[1])] + positions[int(one[2])]
        position_probe[index] = center / 3.0
    U, Umean = ps.read_velocity_dict(time)
    print("Here is " + str(U[0]))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    p = ax.scatter(position_probe[:, 0],
                   position_probe[:, 1],
                   position_probe[:, 2],
                   # U[0],
                   # s=50,
                   color=U[0], cmap=cm.jet, norm=norm)
    fig.colorbar(p)
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    plt.xlim([-1, 1])
    plt.ylim([-1, 1])

    plt.show()
