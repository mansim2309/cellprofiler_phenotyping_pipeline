import pandas as pd
import matplotlib.pyplot as plt


def draw_signal_by_metadata(image, y_temp, imgtitle):
    x = image['Time']
    y = image[y_temp]
    data = {'time': x, y_temp: y}
    df = pd.DataFrame(data)
    df1 = df.sort_values(by = 'time', ascending = True).copy()
    min_time = min(df1['time'])
    max_time = max(df1['time'])
    plt.xlim(min_time, max_time)
    plt.ylabel('Frequency', fontsize=8)
    plt.xlabel(y_temp, fontsize = 8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.title('Fluorescence signal by movement', fontsize=8)
    plt.plot(df1['time'], df1[y_temp])
    dir = '../output/'
    plt.savefig(dir + imgtitle)
    plt.cla()
    plt.delaxes()

img = pd.read_csv("../resources/u26a_ar014d_analysisImage.csv")

draw_signal_by_metadata(img, 'Mean_Cells_Intensity_MeanIntensity_CorrActin', 'Mean Cell Mean Intensity Actin')
draw_signal_by_metadata(img, 'Mean_Cells_Intensity_MedianIntensity_CorrActin', 'Mean Cell Median Intensity Actin')
# draw_signal_by_metadata(img, 'Median_Cells_Intensity_MeanIntensity_CorrActin', 'Median Cell Mean Intensity Actin')
# draw_signal_by_metadata(img, 'Median_Cells_Intensity_MedianIntensity_CorrActin', 'Median Cell Median Intensity Actin')
draw_signal_by_metadata(img, 'Mean_Cells_Intensity_IntegratedIntensity_CorrActin', 'Mean Cell Integrated Intensity Actin')
# draw_signal_by_metadata(img, 'Median_Cells_Intensity_IntegratedIntensity_CorrActin', 'Median Cell Integrated Intensity Actin')

#Nucleus doesn't have much actin
draw_signal_by_metadata(img, 'Mean_Cytoplasm_Intensity_MeanIntensity_CorrActin', 'Mean Cytoplasm Mean Intensity Actin')
draw_signal_by_metadata(img, 'Mean_Cytoplasm_Intensity_MedianIntensity_CorrActin', 'Mean Cytoplasm Median Intensity Actin')
# draw_signal_by_metadata(img, 'Median_Cytoplasm_Intensity_MeanIntensity_CorrActin', 'Median Cytoplasm Mean Intensity Actin')
# draw_signal_by_metadata(img, 'Median_Cytoplasm_Intensity_MedianIntensity_CorrActin', 'Median Cytoplasm Median Intensity Actin')
draw_signal_by_metadata(img, 'Mean_Cytoplasm_Intensity_IntegratedIntensity_CorrActin', 'Mean Cytoplasm Integrated Intensity Actin')
# draw_signal_by_metadata(img, 'Median_Cytoplasm_Intensity_IntegratedIntensity_CorrActin', 'Median Cytoplasm Integrated Intensity Actin')

draw_signal_by_metadata(img, 'Mean_Cells_Intensity_MeanIntensity_CorrmCh', 'Mean Cell Mean Intensity mCh')
draw_signal_by_metadata(img, 'Mean_Cells_Intensity_MedianIntensity_CorrmCh', 'Mean Cell Median Intensity mCh')
# draw_signal_by_metadata(img, 'Median_Cells_Intensity_MeanIntensity_CorrmCh', 'Median Cell Mean Intensity mCh')
# draw_signal_by_metadata(img, 'Median_Cells_Intensity_MedianIntensity_CorrmCh', 'Median Cell Median Intensity mCh')
draw_signal_by_metadata(img, 'Mean_Cells_Intensity_IntegratedIntensity_CorrmCh', 'Mean Cell Integrated Intensity mCh')
# draw_signal_by_metadata(img, 'Median_Cells_Intensity_IntegratedIntensity_CorrmCh', 'Median Cell Integrated Intensity mCh')

draw_signal_by_metadata(img, 'Mean_Cytoplasm_Intensity_MeanIntensity_CorrmCh', 'Mean Cytoplasm Mean Intensity mCh')
draw_signal_by_metadata(img, 'Mean_Cytoplasm_Intensity_MedianIntensity_CorrmCh', 'Mean Cytoplasm Median Intensity mCh')
# draw_signal_by_metadata(img, 'Median_Cytoplasm_Intensity_MeanIntensity_CorrmCh', 'Median Cytoplasm Mean Intensity mCh')
# draw_signal_by_metadata(img, 'Median_Cytoplasm_Intensity_MedianIntensity_CorrmCh', 'Median Cytoplasm Median Intensity mCh')
draw_signal_by_metadata(img, 'Mean_Cytoplasm_Intensity_IntegratedIntensity_CorrmCh', 'Mean Cytoplasm Integrated Intensity mCh')
# draw_signal_by_metadata(img, 'Median_Cytoplasm_Intensity_IntegratedIntensity_CorrmCh', 'Median Cytoplasm Integrated Intensity mCh')

draw_signal_by_metadata(img, 'Mean_FilteredNuclei_Intensity_MeanIntensity_CorrDNA', 'Mean Fil Nuc Mean Intensity DNA')
draw_signal_by_metadata(img, 'Mean_FilteredNuclei_Intensity_MedianIntensity_CorrDNA', 'Mean Fil Nuc Median Intensity DNA')