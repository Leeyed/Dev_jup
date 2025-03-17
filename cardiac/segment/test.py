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
    
    # Azimuth angle (theta) [0, 2π]
    theta = np.arctan2(dy, dx) + np.pi +dz*0 # Shift to range [0, 2π]
    
    # Elevation angle (phi) [0, π/2] 
    phi = np.arccos(dz / (distance2center + 1e-6))
    phi[distance2center == 0] = 0  # Handle division by zero
    
    # Create sector masks based on r, theta, phi ranges
    sector_masks = np.zeros_like(img3d, dtype=int)
    
    # Only include points within radius and upper hemisphere
    hemisphere_mask = (distance2center <= radius) & (dz <= 0)

    # Define theta and phi bins
    theta_bins = np.linspace(0, 2*np.pi, 41)  # 9-degree steps
    phi_bins = np.linspace(0, np.pi/2, 9)  # 12-degree steps

    # Flatten to ensure proper broadcasting
    theta_indices = np.digitize(theta.flatten(), theta_bins) - 1
    phi_indices = np.digitize(phi.flatten(), phi_bins) - 1

    # Reshape back to 3D
    theta_indices = theta_indices.reshape(img3d.shape)
    phi_indices = phi_indices.reshape(img3d.shape)

    # Valid indices mask
    valid_mask = (theta_indices >= 0) & (theta_indices < len(theta_bins)-1) & \
                 (phi_indices >= 0) & (phi_indices < len(phi_bins)-1) & \
                 hemisphere_mask

    # Assign sector values
    sector_masks[valid_mask] = theta_indices[valid_mask] * (len(phi_bins)-1) + phi_indices[valid_mask] + 1

    return sector_masks


# 示例调用
center = (20, 26, 28)  # 示例中心坐标  
radius = 16  # 示例半径
img3d = np.zeros((50, 50, 50))  # 示例 3D 图像大小
sector_masks = get_sector_masks_by_spherical_coords(img3d, center, radius)

plot_sector_masks_3d(sector_masks)
