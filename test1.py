

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def dh_transform(theta, d, a, alpha):
    """Create the transformation matrix based on DH parameters."""
    return np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha),  np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta),  np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0,              np.sin(alpha),                   np.cos(alpha),                  d],
        [0,              0,                                  0,                             1]
    ])

def forward_kinematics(theta_list, a, d, alpha):
    """Calculate the forward kinematics to get end effector position."""
    T = np.eye(4)
    positions = []
    for i in range(len(theta_list)):
        T_i = dh_transform(theta_list[i], d[i], a[i], alpha[i])
        T = T @ T_i  # Combine transformations
        positions.append(T[:3, 3])  # Append the position of the end effector
    return T, positions

def rotation_matrix_to_euler_angles(R):
    # (pitch, y축 회전)
    pitch = np.arctan2(-R[2, 0], np.sqrt(R[0, 0]**2 + R[1, 0]**2))
    # (yaw, z축 회전)
    yaw = np.arctan2(R[1, 0], R[0, 0])
    # (roll, x축 회전)
    roll = np.arctan2(R[2, 1], R[2, 2])
    return np.degrees(pitch), np.degrees(yaw), np.degrees(roll)

def plot_robot(ax, positions,T):
    """Plot the robot arm based on the given positions."""
    ax.cla()  # Clear the axes for new plotting
    
    R=T[:3,:3]
    Orientaion=rotation_matrix_to_euler_angles(R)
    
    if positions:  # Check if positions list is not empty
        # Start plotting the robot arm
        ax.plot([0, positions[0][0]], [0, positions[0][1]], [0, positions[0][2]], 'ro-')  # Joint 0
        for i in range(len(positions) - 1):
            ax.plot([positions[i][0], positions[i + 1][0]], 
                    [positions[i][1], positions[i + 1][1]], 
                    [positions[i][2], positions[i + 1][2]], 'bo-')  # Links between joints
        
        # Plot the end effector position
        end_effector_position = positions[-1]
        ax.scatter(end_effector_position[0], end_effector_position[1], end_effector_position[2], color='green',  
                   label=f'Pos : ({end_effector_position[0]:.2f}, {end_effector_position[1]:.2f},{end_effector_position[2]:.2f})\nOri : ({Orientaion[2]:.2f},{Orientaion[0]:.2f},{Orientaion[1]:.2f})')  # End effector position
        ax.legend()
    # Set limits and labels
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([0, 1.5])
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('3D Visualization of Robotic Arm')
    
    plt.grid()
    plt.draw()  # Redraw the plot

    
def update(val):
    """Update the robot plot based on the slider values."""
    # Update joint angles from sliders
    for i in range(6):
        theta_degrees[i] = sliders[i].val  # Access each slider's value from the list

    # Convert degrees to radians for calculations
    theta = np.radians(theta_degrees)

    # Calculate Forward Kinematics
    T, positions = forward_kinematics(theta, a, d, alpha)
    print(positions)
    # Update the plot
    plot_robot(ax, positions,T)

# UR5 DH Parameters
theta_degrees = np.array([0, 0, 0, 0, 0, 0])  # Joint angles (initially set to 0 in degrees)
a = np.array([0, -0.425, -0.392, 0, 0, 0])  # Length of the common normal (a values)
d = np.array([0.089, 0, 0, 0.109, 0.095, 0.082])  # Offset along the z-axis (d values)
alpha = np.array([np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2, 0])  # Link twist angles (alpha values)

# Create initial plot
theta = np.radians(theta_degrees)  # Ensure the initial angles are in radians
T, positions = forward_kinematics(theta, a, d, alpha)  # Calculate initial positions
fig = plt.figure(figsize=(8, 8))  # Adjust figure size
ax = fig.add_subplot(211, projection='3d')

# Initial plotting
plot_robot(ax, positions,T)

# ax = fig.add_subplot(212)
# Create sliders for each joint angle
sliders = []  # List to hold slider objects 
slider_ax = [plt.axes([0.3, 0.2 + i * 0.05, 0.4, 0.03]) for i in range(6)]  # [left, bottom, width, height]Adjusted positioning of sliders
for i in range(6):
    slider = Slider(slider_ax[i], f'Theta {i + 1}', -180, 180, valinit=theta_degrees[i])
    sliders.append(slider)  # Store slider in the list
    slider.on_changed(update)  # Attach update function to slider changes
plt.legend()
plt.tight_layout()
plt.show()