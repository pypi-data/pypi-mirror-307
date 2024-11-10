import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt
import gc

#读图像文件
def read_img(filename):
    dataset = gdal.Open(filename) #打开文件
    im_width = dataset.RasterXSize  #栅格矩阵的列数
    im_height = dataset.RasterYSize  #栅格矩阵的行数
    im_bands = dataset.RasterCount   #波段数
    im_geotrans = dataset.GetGeoTransform()  #仿射矩阵，左上角像素的大地坐标和像素分辨率
    im_proj = dataset.GetProjection() #地图投影信息，字符串表示
    im_data = dataset.ReadAsArray(0,0,im_width,im_height).astype('float')

    del dataset

    return im_width, im_height, im_bands, im_geotrans, im_proj, im_data

#写GeoTiff文件
def write_img(filename, im_proj, im_geotrans, im_data):

    #判断栅格数据的数据类型
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    #判读数组维数
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    else:
       im_bands, (im_height, im_width) = 1, im_data.shape

    #创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

    dataset.SetGeoTransform(im_geotrans)       #写入仿射变换参数
    dataset.SetProjection(im_proj)          #写入投影

    if im_bands == 1:
        dataset.GetRasterBand(1).WriteArray(im_data) #写入数组数据
    else:
        for i in range(im_bands):
            dataset.GetRasterBand(i+1).WriteArray(im_data[i])

    del dataset

def math_landsat8_VI(input_filename, output_prefix):
    im_width, im_height, im_bands, im_proj, im_geotrans, im_data = read_img(input_filename)

    # 获取波段数据
    B, G, R, NIR = im_data[1], im_data[2], im_data[3], im_data[4]

    # 指数计算及保存
    indices = {
        'NDVI': (NIR - R) / (NIR + R),
        'NDWI': (G - NIR) / (G + NIR),
        'DVI': NIR - R,
        'EVI': 2.5 * (NIR - R) / (NIR + 6 * R - 7.5 * B + 1.0),
        'CRI': 1 / B - 1 / G,
        'GDVI': NIR - G,
        'GNDVI': (NIR - G) / (NIR + G),
        'GRVI': NIR / G,
        'NLI': (NIR * NIR - R) / (NIR * NIR + R),
        'RGRI': R / G,
        'SRI': NIR / R,
        'CIgreen': (NIR / G) - 1,
        'SAVI': 1.5 * (NIR - R) / (NIR + R + 0.5)
    }

    for name, data in indices.items():
        write_img(f"{output_prefix}/{name}.tif", im_proj, im_geotrans, data)
        fig = plt.figure(dpi=100)
        plt.imshow(data, vmin=np.nanpercentile(data, 2), vmax=np.nanpercentile(data, 98), cmap=plt.cm.gray)
        plt.colorbar()
        plt.title(name)
        plt.axis('off')
        plt.show()
        del data
        gc.collect()
