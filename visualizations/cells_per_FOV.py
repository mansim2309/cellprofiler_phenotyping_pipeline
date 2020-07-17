import pandas as pd
import seaborn as sns

def show_well(image, cellcount, cellnames):
    x = []
    y = []
    cellcount = image[cellcount]
    cellnames = image[cellnames]
    for f1 in cellnames:
        val1 = f1.split('_')
        val2 = val1[1].split('-')
        x.append(val2[1])
        y.append(val2[2])
    data = {'x': x, 'y': y, 'cellcount': cellcount}
    result = pd.DataFrame(data)
    uniform_data = result.pivot('x', 'y', 'cellcount')
    sns.set(rc={'figure.figsize': (100, 100)})
    ax = sns.heatmap(uniform_data, annot=True, fmt="f", cmap="YlGnBu_r")
    ax.xaxis.tick_top()
    ax.yaxis.tick_left()
    fig = ax.get_figure()
    dir = '../output/'
    fig.savefig(dir + "cellcount by FOV.png")
    fig.clf()

image = pd.read_csv("../resources/u26a_ar014d_analysisImage.csv")
show_well(image, 'Count_Cells', 'FileName_CellOutlines_overlayCorrActin')