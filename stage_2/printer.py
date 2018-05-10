import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator


def plot_probability_and_time(k, number_of_clauses, prob, time):

    x = np.asarray([[val] * len(number_of_clauses) for val in k])

    # projection of n_o_f on k
    y = np.asarray([number_of_clauses] * len(k))

    z = np.asarray(prob)

    z_t = np.asarray(time)

    # call plot for prob
    plot(x, y, z, "Length of Clauses", "Number of Clauses", "Probability_of_Sat", "Proability of Satistiability for randomly generated formula N = 150")

    #call plot for time
    plot(x, y, z_t, "Length of Clauses", "Number of Clauses", "CPU_Time", "CPU_TIME for randomly generated formula N = 150")


def plot(x, y, z, xlabel, y_label, z_label, title):
    font = {'family': 'helvet',
            'weight': 'bold',
            'size': 75}

    mpl.rc('font', **font)

    fig = plt.figure(0, figsize=(70, 90))
    ax = Axes3D(fig)

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.xlabel(xlabel, fontsize=120.0, labelpad=150.0)
    plt.ylabel(y_label, fontsize=120.0, labelpad=150.0)
    ax.set_zlabel(z_label, fontsize=120.0, labelpad=150.0)

    plt.title(title,
              fontsize=150.0, weight="bold")

    # Plot the surface.
    surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    angle = 45
    ax.view_init(14, angle)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)

    fig.savefig(title + ".png")