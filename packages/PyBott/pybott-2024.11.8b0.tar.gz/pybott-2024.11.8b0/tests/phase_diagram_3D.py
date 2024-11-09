import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

import matplotlib.pyplot as plt

plt.rc("text", usetex=True)
plt.rc("font", family="serif", serif="Computer Modern")

def get_color_from_cmap(value, cmap_name="coolwarm"):
    cmap = plt.get_cmap(cmap_name)
    rgba = cmap(value)  
    hex_color = '#{:02x}{:02x}{:02x}'.format(int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255))
    return hex_color

def plot_phase_diagram_3d(filenames, xkey, ykey, delta_values, cmap='viridis', colorbar_label="Bott Index", 
                          xlabel="X-axis", ylabel="Y-axis", zlabel="Delta", fontsize=12, title=""):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    for idx, (filename, delta) in enumerate(zip(filenames, delta_values)):
        data = pd.read_csv(filename)
        phase_data = data.pivot(index=ykey, columns=xkey, values="Bott Index")
        
        x_min, x_max = data[xkey].min(), data[xkey].max()
        y_min, y_max = data[ykey].min(), data[ykey].max()
        
        x = np.linspace(x_min, x_max, phase_data.shape[1])
        y = np.linspace(y_min, y_max, phase_data.shape[0])
        X, Y = np.meshgrid(x, y)

        contour = ax.contour(X, Y, phase_data.values, levels=[0.5], colors=get_color_from_cmap(delta/max(delta_values)), 
                             linestyles='-', offset=delta)
    
    ax.set_xlabel(xlabel, fontsize=fontsize, labelpad=14)
    ax.set_ylabel(ylabel, fontsize=fontsize, labelpad=14)
    ax.set_zlabel(zlabel, fontsize=fontsize, labelpad=10)
    ax.tick_params(axis='both', labelsize=fontsize)
    ax.text(8,0.8,1,title,fontsize=fontsize)
    ax.view_init(elev=21, azim=-65)

    plt.savefig("phase_diagram_3D.pdf",format="pdf", bbox_inches='tight',  pad_inches=0.4)
    plt.show()


if __name__ == "__main__":
    filenames = ['pd_t2=0.2j_delta=1.1_n_side=16.csv',
                 'pd_t2=0.2j_delta=1_n_side=16.csv',
                 'pd_t2=0.2j_delta=0.9_n_side=16.csv',
                 'pd_t2=0.2j_delta=0.8_n_side=16.csv',
                 'pd_t2=0.2j_delta=0.7_n_side=16.csv',
                 'pd_t2=0.2j_delta=0.4_n_side=16.csv',
                 'pd_t2=0.2j_delta=0.2_n_side=16.csv',
                 'phase_diagram_disorder.csv']

    delta_values = [1.1, 1, 0.9, 0.8, 0.7, 0.4, 0.2, 0]
    xkey = "disorder"
    ykey = "energy"
    

    plot_phase_diagram_3d(filenames, xkey, ykey, delta_values, cmap='magma', colorbar_label="Bott Index", 
                          xlabel="Disorder $W$", ylabel="Energy $E$", zlabel=r"IS breaking $\delta$", fontsize=20,
                          title=r"$t_2=0.2i$")


