import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_save_plot(attribute, xlab, plotname, logscale, logxval): #logscale is for log scale not log of value;
    # logxval is for x axis value
    attribute = pd.Series(attribute)
    if logxval == 'yes':
        attribute = np.log10(attribute)
        # plt.xscale('log')
    plt.hist(attribute, bins='auto', histtype='bar', color='purple')
    plt.xlim(min(attribute), max(attribute))
    if logscale == 'yes':
        plt.cla()
        plt.delaxes()
        MIN, MAX = 0.001, 0.1
        plt.hist(attribute, bins = 10 ** np.linspace(np.log10(MIN), np.log10(MAX), 250))
        plt.gca().set_xscale('log')
    plt.xlabel(xlab, fontsize=8)
    plt.ylabel('Frequency', fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.title('Distribution Histogram', fontsize=8)
    plt.axvline(attribute.mean(), color='cyan', linestyle='dashed', linewidth=1)
    dir = '../output/'
    plt.savefig(dir + plotname)
    plt.cla()
    plt.delaxes()

cell = pd.read_csv("../resources/u26a_ar014d_analysisCells.csv")
image = pd.read_csv("../resources/u26a_ar014d_analysisImage.csv")
cellcount = image['Count_Cells']
cellarea = cell['AreaShape_Area']
integratedmch = cell['Intensity_IntegratedIntensity_CorrmCh']
meanmch = cell['Intensity_MeanIntensity_CorrmCh']

create_save_plot(cellarea, 'Cell Area', 'Cell Area', 'no', 'no')
create_save_plot(integratedmch, 'Total (or integrated) mCh intensity', 'Total(Integrated) mCherry', 'no', 'no')
create_save_plot(meanmch, 'Average mCh intensity', 'Average mCherry on Linear Scale', 'no', 'no')
create_save_plot(meanmch, 'Average mCh intensity', 'Average mCherry on Logarithmic Scale', 'yes', 'no')
create_save_plot(meanmch, 'Log(Average mCherry)', 'Log of Average mCh intensity on Linear Scale','no', 'yes')
create_save_plot(cellcount, 'Number of cells per FOV', 'Cell per FOV', 'no', 'no')