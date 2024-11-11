import os
from pymodis import convertmodis
import gdal
from osgeo import osr
from glob import glob

def modis_to_tif_batch(input_dir, output_dir, target_epsg=None, selected_bands=None, file_pattern="*.hdf"):
    """
    批量处理MODIS HDF文件并转换为GeoTIFF格式
    
    参数:
    input_dir: 输入文件夹路径
    output_dir: 输出文件夹路径
    target_epsg: 目标投影的EPSG代码(可选)
    selected_bands: 需要提取的波段列表(可选)
    file_pattern: 文件匹配模式，默认为"*.hdf"
    """
    
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有HDF文件
    hdf_files = glob(os.path.join(input_dir, file_pattern))
    
    if not hdf_files:
        print(f"在 {input_dir} 中没有找到匹配的HDF文件")
        return
    
    total_files = len(hdf_files)
    print(f"找到 {total_files} 个HDF文件待处理")
    
    for index, hdf_file in enumerate(hdf_files, 1):
        try:
            print(f"正在处理文件 {index}/{total_files}: {os.path.basename(hdf_file)}")
            
            # 生成输出文件名
            base_name = os.path.splitext(os.path.basename(hdf_file))[0]
            
            # 打开HDF文件
            hdf_ds = gdal.Open(hdf_file)
            
            if hdf_ds is None:
                print(f"无法打开文件: {hdf_file}")
                continue
            
            # 获取子数据集
            subdatasets = hdf_ds.GetSubDatasets()
            
            # 如果没有指定波段，则处理所有波段
            if selected_bands is None:
                selected_bands = range(len(subdatasets))
            
            for band_index in selected_bands:
                if band_index >= len(subdatasets):
                    print(f"波段 {band_index} 超出范围")
                    continue
                
                # 读取子数据集
                subdataset = gdal.Open(subdatasets[band_index][0])
                
                # 获取投影信息
                proj = subdataset.GetProjection()
                geotransform = subdataset.GetGeoTransform()
                
                # 读取数据
                data = subdataset.ReadAsArray()
                
                # 创建输出文件名
                output_file = os.path.join(output_dir, f"{base_name}_band_{band_index}.tif")
                
                # 创建输出数据集
                driver = gdal.GetDriverByName('GTiff')
                out_ds = driver.Create(output_file, 
                                     subdataset.RasterXSize, 
                                     subdataset.RasterYSize, 
                                     1, 
                                     gdal.GDT_Float32)
                
                # 设置投影和地理变换参数
                out_ds.SetProjection(proj)
                out_ds.SetGeoTransform(geotransform)
                
                # 写入数据
                out_ds.GetRasterBand(1).WriteArray(data)
                
                # 如果指定了目标投影，进行投影转换
                if target_epsg:
                    # 创建临时文件
                    temp_file = os.path.join(output_dir, f"{base_name}_temp.tif")
                    
                    # 设置目标空间参考
                    target_srs = osr.SpatialReference()
                    target_srs.ImportFromEPSG(target_epsg)
                    
                    # 进行投影转换
                    gdal.Warp(temp_file,
                             out_ds,
                             dstSRS=target_srs.ExportToWkt(),
                             resampleAlg=gdal.GRA_Bilinear)
                    
                    # 删除原文件，重命名临时文件
                    out_ds = None
                    os.remove(output_file)
                    os.rename(temp_file, output_file)
                
                # 清理
                out_ds = None
                subdataset = None
            
            hdf_ds = None
            print(f"完成文件 {index}/{total_files}")
            
        except Exception as e:
            print(f"处理文件 {hdf_file} 时出错: {str(e)}")
            continue
    
    print("所有文件处理完成！")

def process_with_error_handling(input_dir, output_dir, target_epsg=None, selected_bands=None):
    """
    带有错误处理的处理函数封装
    """
    try:
        # 验证输入目录是否存在
        if not os.path.exists(input_dir):
            raise ValueError(f"输入目录不存在: {input_dir}")
        
        # 确保输入路径是目录
        if not os.path.isdir(input_dir):
            raise ValueError(f"输入路径不是目录: {input_dir}")
        
        # 开始处理
        modis_to_tif_batch(input_dir, output_dir, target_epsg, selected_bands)
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        raise

# # 使用示例
# if __name__ == "__main__":
#     # 设置输入输出路径
#     input_directory = r"D:\modis_data\input"
#     output_directory = r"D:\modis_data\output"
    
#     # 示例1：基本批量转换
#     process_with_error_handling(input_directory, output_directory)
    
#     # 示例2：转换为WGS84投影并只处理特定波段
#     # process_with_error_handling(
#     #     input_directory, 
#     #     output_directory,
#     #     target_epsg=4326,
#     #     selected_bands=[0, 1]
#     # )