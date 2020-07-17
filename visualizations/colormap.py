#import the needed packages
import numpy as np
import mahotas as mh
import pandas as pd
import cv2
import glob
import seaborn as sns

# Helper Functions
def avg_pixel_intensity(img_src):
    image = mh.imread(img_src)
    return (int(np.mean(image)))

def create_measurement_df(img_dir, threshold, channel_selection):
    img_src = img_dir + "/*.tif"
    files = glob.glob(img_src)
    data = []
    x = []
    y = []
    img_names = []
    avg_intensity = []
    pct_threshold = []
    channel = []
    for f1 in files:
        img = cv2.imread(f1)
        val1 = f1.split('/')
        val2 = val1[3].split('-')
        val3 = val2[1].split('_')
        val4 = val3[3].split('.')
        if(val4[0] == channel_selection):
            channel.append(val4[0])
            x.append(int(val3[1]))
            y.append(int(val3[2]))
            data.append(img)
            img_names.append(f1)
            avg_intensity.append(avg_pixel_intensity(f1))
            pct_threshold.append(calculate_threshold_intensity_pct(img, threshold))
    d = {'x':x, 'y':y, 'file_name': img_names, 'avgintensity': avg_intensity, 'channel': channel, 'pct_above_threshold': pct_threshold}
    coordinates = pd.DataFrame(d)
    return coordinates

def calculate_threshold_intensity_pct(img, threshold):
    total = 0
    calc = 0
    rows = img.shape[0]
    cols = img.shape[1]
    for x in range(rows):
        for y in range(cols):
            if(img[x][y][0] >= threshold):
                calc += 1
            total += 1
    print(calc, total)
    intensity_pct = (100 * calc) / total
    return round(intensity_pct)
    
def plot_intensity_colormap(df, channel):
    df_ch3 = df[df['channel'] == channel]
    uniform_data = df_ch3.pivot('x', 'y', 'avgintensity')
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    ax = sns.heatmap(uniform_data, annot=True, fmt = "d", cmap="YlGnBu_r")
    ax.xaxis.tick_top()
    ax.yaxis.tick_left()
    fig = ax.get_figure()
    dir = '../output/'
    fig.savefig(dir + "intensity.png")
    fig.clf()


def plot_threshold_colormap(df, channel):
    df_ch3 = df[df['channel'] == channel]
    uniform_data = df_ch3.pivot('x', 'y', 'pct_above_threshold')
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    ax = sns.heatmap(uniform_data, annot=True, fmt = "f", cmap="YlGnBu_r")
    ax.xaxis.tick_top()
    ax.yaxis.tick_left()
    fig = ax.get_figure()
    dir = '../output/'
    fig.savefig(dir + "threshold.png")
    fig.clf()

measurements = create_measurement_df("../resources/Images", 4, "ch3")
#measurements.head()

plot_intensity_colormap(measurements, 'ch3')

plot_threshold_colormap(measurements, 'ch3')
