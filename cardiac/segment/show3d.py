'''
Author: LiuSheng
Date: 2025-03-14 15:38:30
LastEditTime: 2025-03-14 16:13:40
Description: 
'''
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_sector_masks_3d(sector_masks):
    """
    Visualize the sector masks in 3D
    """
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Get nonzero points (masked regions)
    z, y, x = np.where(sector_masks > 0)
    c = sector_masks[z, y, x]  # Color by sector index
    
    ax.scatter(x, y, z, c=c, cmap='jet', marker='o', alpha=0.6)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Visualization of Sector Masks')
    
    plt.show()


def get_sector_masks_by_spherical_coords(img3d, center, radius):
    """
    Create masks for sectors based on spherical coordinates (r, theta, phi)
    
    Args:
        img3d: 3D numpy array
        center: (cz, cy, cx) center coordinates 
        radius: radius of hemisphere
        
    Returns:
        sector_masks: 3D array with sector index values
    """
    cz, cy, cx = center
    
    # Create coordinate grids
    Z, Y, X = np.ogrid[:img3d.shape[0], :img3d.shape[1], :img3d.shape[2]]
    
    # Calculate distances and angles from center for each point
    dz = Z - cz + 0.5 
    dy = Y - cy + 0.5
    dx = X - cx + 0.5
    
    # Distance (r)
    distance2center = np.sqrt(dz**2 + dy**2 + dx**2)
    
    # Azimuth angle (theta) [-pi, pi]
    theta = np.arctan2(dy, dx)+np.pi + dz*0
    
    # Elevation angle (phi) [0, pi/2] 
    phi = np.arccos(dz/(distance2center+1e-6))
    phi[distance2center == 0] = 0 # Handle division by zero
    
    # Create sector masks based on r, theta, phi ranges
    sector_masks = np.zeros_like(img3d)
    
    # Only include points within radius and upper hemisphere (changed from lower to upper)
    hemisphere_mask = (distance2center <= radius) & (dz <= 0)  # Changed from dz >= 0 to dz <= 0

    
    theta_unit = 9/180*np.pi
    theta_bins = np.array(range(41))*theta_unit # 9 degree steps
    
    phi_unit = 12/180*np.pi
    phi_bins = np.array(range(9))* phi_unit
    
    
    for i, (start_theta, end_theta) in enumerate(zip(theta_bins[:-1], theta_bins[1:])):
        for j, (start_phi, end_phi) in enumerate(zip(phi_bins[:-1], phi_bins[1:])):
            sector_mask = hemisphere_mask & (theta >= start_theta) & (theta < end_theta) & \
                         (phi >= start_phi) & (phi < end_phi)
            sector_masks[sector_mask] = i * len(phi_bins[:-1]) + j + 1
            
        
    
            
    return sector_masks


import plotly.graph_objects as go
import numpy as np

def plot_sector_masks_plotly(sector_masks):
    """ 使用 Plotly 进行 3D 可视化 """
    z, y, x = np.where(sector_masks > 0)
    c = sector_masks[z, y, x]  # 颜色映射

    fig = go.Figure(data=[go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=3,
            color=c,
            colorscale='Jet',
            opacity=0.5
        )
    )])

    fig.update_layout(title="3D Visualization of Sector Masks (Plotly)")
    fig.show()

# 示例调用
# plot_sector_masks_plotly(sector_masks)

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyvista as pv

# def plot_sector_masks_3d(sector_masks):
#     """
#     Visualize the sector masks in 3D using PyVista
#     """
#     grid = pv.UniformGrid()
#     grid.dimensions = np.array(sector_masks.shape) + 1
#     grid.spacing = (1, 1, 1)
#     grid.cell_data['values'] = sector_masks.flatten(order='F')
    
#     plotter = pv.Plotter()
#     plotter.add_mesh(grid.threshold(0.5), cmap='jet')
#     plotter.show()

from skimage.measure import marching_cubes
import trimesh

def plot_sector_isosurface(sector_masks):
    verts, faces, _, _ = marching_cubes(sector_masks, level=0)
    mesh = trimesh.Trimesh(vertices=verts, faces=faces)
    mesh.show()

# plot_sector_isosurface(sector_masks)


# 示例调用
center = (20, 26, 28)  # 示例中心坐标  
radius = 16  # 示例半径
img3d = np.zeros((50, 50, 50))  # 示例 3D 图像大小
sector_masks = get_sector_masks_by_spherical_coords(img3d, center, radius)

plot_sector_masks_3d(sector_masks)