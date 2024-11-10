import xarray as xr
import rasterio
from rasterio.transform import from_bounds
import os
from pathlib import Path
import glob

def nc_to_tiffs(nc_file, output_dir):
    # 创建输出目录(如果不存在)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 打开nc文件
    ds = xr.open_dataset(nc_file)
    
    # 获取变量列表
    variables = list(ds.data_vars)
    
    for var in variables:
        data = ds[var].values
        
        # 获取经纬度信息
        if 'lon' in ds.coords and 'lat' in ds.coords:
            lons = ds.lon.values
            lats = ds.lat.values
            
            # 计算转换参数
            transform = from_bounds(
                lons.min(), lats.min(),
                lons.max(), lats.max(),
                len(lons), len(lats)
            )
            
            # 设置输出文件路径
            output_file = os.path.join(output_dir, f"{var}.tif")
            
            # 写入GeoTIFF
            with rasterio.open(
                output_file,
                'w',
                driver='GTiff',
                height=data.shape[0],
                width=data.shape[1],
                count=1,
                dtype=data.dtype,
                crs='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs',
                transform=transform
            ) as dst:
                dst.write(data, 1)
    
    ds.close()
    print(f"文件处理完成: {nc_file}")

def batch_process_nc_files(input_dir, output_base_dir):
    # 获取所有.nc文件
    nc_files = glob.glob(os.path.join(input_dir, "*.nc"))
    
    if not nc_files:
        print(f"在 {input_dir} 中没有找到.nc文件")
        return
    
    print(f"找到 {len(nc_files)} 个.nc文件")
    
    # 处理每个文件
    for nc_file in nc_files:
        # 获取文件名（不含扩展名）作为子文件夹名
        file_name = Path(nc_file).stem
        
        # 创建对应的输出子文件夹
        output_dir = os.path.join(output_base_dir, file_name)
        
        print(f"正在处理: {file_name}")
        try:
            nc_to_tiffs(nc_file, output_dir)
        except Exception as e:
            print(f"处理文件 {file_name} 时出错: {str(e)}")

# # 使用示例
# input_dir = "输入文件夹路径"  # 包含.nc文件的文件夹路径
# output_base_dir = "输出文件夹路径"  # 存放结果的基础路径

# batch_process_nc_files(input_dir, output_base_dir)