import numpy as np

"""
This file contains a set of methods that can be used to calculate the magnetic field using Biot-Savart and some methods that allows to calculation of the inductance of circuits.
"""

def mutual_inductance_matrix_2D(line_elements, D = 1e-3):
    """
    Calculates the mutual inductance matrix that allows for rotation around in the XY plane, not in the XZ and YZ planes.
    Note that the length of the elements matters a lot, so if the length is to long, it will not give the right value.

    :param line_elements: [x, y, z, length, angle]
    :param D: Thickness of the wire [m].
    :return: L (Mutual inductance matrix)
    """

    L = np.zeros((len(line_elements), len(line_elements)))

    for i in range(len(line_elements)):
        for j in range(len(line_elements)):
            if j == 0:
                # Self inductance (Link doesn't work anymore)
                L11 = 1e-9 * 2 * line_elements[j][3] * 100 * (
                            np.log(2 * line_elements[j][3] / D * (1 + (1 + (D / (2 * line_elements[j][3])) ** 2) ** 0.5)) - (
                                1 + (D / (2 * line_elements[j][3])) ** 2) ** 0.5 + 1 / 4 + D / (2 * line_elements[j][3]))
            else:
                # Mutual inductance: double integral Neumann formula https://en.wikipedia.org/wiki/Inductance
                # M = u0/4pi * dx_m dot dx_n / |x_m-x_n|
                L11 = 1e-7 * line_elements[i][3] * line_elements[j][3] * np.cos(line_elements[i][4] - line_elements[j][4]) / (
                            (line_elements[i][0] - line_elements[j][0]) ** 2 + (line_elements[i][1] - line_elements[j][1]) ** 2 + (
                                line_elements[i][2] - line_elements[j][2]) ** 2) ** 0.5
            L[i, j] = L11

    print('Inductance: ' + str(round(np.sum(L)*1e3, 2)) + ' mH' )
    return L

def mutual_inductance_matrix_3D(line_elements, D = 1e-3):
    """
    Calculates the mutual inductance matrix that allows for rotation around in the XY plane, not in the XZ and YZ planes.
    Note that the length of the elements matters a lot, so if the length is to long, it will not give the right value.

    The line_elements variable comtains an array of all line elements, each comprising its position, current direction vector and length.
    The position of the element in the center of the line element.
    The vector points in to the direction of the current, used for calculating the angle between two line elements.
    The length of the element is the length of the element of course.

    :param line_elements: [position, vector, element length]
    :param D: Thickness of the wire [m], optional.
    :return: L (Mutual inductance matrix)
    """

    L = np.zeros((len(line_elements), len(line_elements)))

    line_elements = [[np.array(line_elements[i][0]), np.array(line_elements[i][1]), line_elements[i][2]] for i in range(len(line_elements))]

    for i in range(len(line_elements)):
        if np.mod(i, 10) == 0:
            print(i, 'out of', len(line_elements), flush=True)
        for j in np.arange(i, len(line_elements)):
            a = line_elements[i][2]
            b = line_elements[j][2]
            if j == i:
                # Self inductance (Link doesn't work anymore)
                L11 = 1e-9 * 2 * b * 100 * (
                            np.log(2 * b / D * (1 + (1 + (D / (2 * b)) ** 2) ** 0.5)) - (
                                1 + (D / (2 * b)) ** 2) ** 0.5 + 1 / 4 + D / (2 * b))
            else:
                # Mutual inductance: double integral Neumann formula https://en.wikipedia.org/wiki/Inductance
                # M = u0/4pi * dx_m dot dx_n / |x_m-x_n|
                # Dxyz = ((line_elements[i][0][0] - line_elements[j][0][0]) ** 2 + (line_elements[i][0][1] - line_elements[j][0][1]) ** 2 + (line_elements[i][0][2] - line_elements[j][0][2]) ** 2) ** 0.5
                Dxyz = np.linalg.norm(line_elements[i][0]-line_elements[j][0])
                ab = np.dot(line_elements[i][1],line_elements[j][1])
                abab = ab/(a*b)
                abab = 1.0 if abab > 1.0 else abab
                abab = -1.0 if abab < -1.0 else abab
                angle = np.arccos(abab)
                L11 = 1e-7 * a * b * np.cos(angle) / Dxyz
            L[i, j] = L11
            L[j, i] = L11

    print('Inductance: ' + str(round(np.sum(L)*1e3, 2)) + ' mH' )
    return L

def mutual_inductance_matrix_solenoid(height, radius, turns, elements, sub_elements, D=1e-3):
    """
    Quick inductance calculator for a solenoid.
    :param height: coil height in [m]
    :param radius: coil radius in [m]
    :param turns: amount of turns
    :param elements: amount of elements per turn (in matrix)
    :param sub_elements: amount of elements per element (not in matrix), this number may need to be large depending on the other parameters.
    :param D: diameter of the wire [m]
    :return:
    """

    dphi = 2 * np.pi / (elements * sub_elements)
    dz = (height/turns) / (elements * sub_elements)
    dL = 2 * np.pi * radius / (elements * sub_elements)

    nodes = []
    for i in range(elements * turns * sub_elements):
        nodes.append([radius * np.cos(dphi * i), radius * np.sin(dphi * i), dz * i, dL, i * dphi])

    L = []
    for j in range(len(nodes)):
        if j == 0:
            # Self inductance (Link doesn't work anymore)
            L11 = 1e-9 * 2 * nodes[j][3] * 100 * (
                        np.log(2 * nodes[j][3] / D * (1 + (1 + (D / (2 * nodes[j][3])) ** 2) ** 0.5)) - (
                            1 + (D / (2 * nodes[j][3])) ** 2) ** 0.5 + 1 / 4 + D / (2 * nodes[j][3]))
        else:
            # Mutual inductance: double integral Neumann formula https://en.wikipedia.org/wiki/Inductance
            # M = u0/4pi * dx_m dot dx_n / |x_m-x_n|
            L11 = 1e-7 * nodes[0][3] * nodes[j][3] * np.cos(nodes[0][4] - nodes[j][4]) / (
                        (nodes[0][0] - nodes[j][0]) ** 2 + (nodes[0][1] - nodes[j][1]) ** 2 + (
                            nodes[0][2] - nodes[j][2]) ** 2) ** 0.5
        L.append(L11)

    L_list = L[::-1][:-1] + L
    L_list = np.add.reduceat(L_list, np.arange(0, len(L_list), sub_elements))

    n = turns * elements
    L_full = np.zeros((n, n))
    for i in range(n):
        L_full[i, :] = np.array(L_list[n - i - 1: n + n - i - 1]) * sub_elements

    print('Inductance: ' + str(round(np.sum(L_full) * 1e3, 2)) + ' mH')
    return L_full


def Mag_2D_XY(source, target, I):
    """ Calculates the Bx and By field given a current source pointing in the z direction.
    :param source: [x, y] The position of the source element.
    :param target: [x, y] The position of the target.
    :param I: The current.
    :return: Bx and By.
    """

    # Ampere's law: B = mu0I/2piR   for vectors  I*dL (current)  and   D  (element-center to XYZ)
    Dxy = np.array(target) - np.array(source)  # vector from element-center to XYZ
    D = np.dot(Dxy, Dxy)**0.5  # distance from element-center to XYZ
    if D > 0.0005:
        f = 2e-7 * I / D
        angle1 = np.arccos(Dxy[1]/D)
        angle2 = np.arccos(Dxy[0]/D)
        Bx =  np.cos(angle1) * f
        By = -np.cos(angle2) * f
        return Bx, By
    else:
        # It gives zeros if the distance between the target and the source is too small.
        return 0.0, 0.0

def Mag_3D_Quick(source, target, IdL=1.0):
    """ Calculates the Bx, By and Bz field given a small current source element using Biot Savart assuming no dz in the source elements.
    Since there is no dz and the directional sin/cos are calculated beforehand, this function is quite quick
    :param source: [x, y, z, sin(phi), cos(phi)] Position of the source element + the sin/cos giving the direction compared to the origin [0, 0, 0].
    :param target: [x, y, z]
    :param IdL: [Ampere * meter]
    :return:
    """
    # Biot-Savart: B = mu0/4pi * I*(dL x D)/|D|^3   for vectors  I*dL (current)  and   D  (element-center to XYZ)
    Dxyz = np.array(target[0:3])-np.array(source[0:3])  # vector from element-center to XYZ
    D = np.dot(Dxyz, Dxyz)**1.5                         # distance from element-center to XYZ
    if D > 0.0005**3:
        f = 1e-7 * IdL / D
        s1 = source[3]
        c1 = source[4]
        Bx = f * c1 * Dxyz[2]
        By = f * s1 * Dxyz[2]
        Bz = f * (-c1 * Dxyz[1] + s1 * Dxyz[0])
        return Bx, By, Bz
    else:
        return 0.0, 0.0, 0.0