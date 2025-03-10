import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

a1=1
a2=1

def forward_kinematics(theta1, theta2):
    """끝단의 위치 계산"""
    x1 = a1 * np.cos(theta1)        # 첫 번째 링크 끝 위치
    y1 = a1 * np.sin(theta1)
    x2 = x1 + a2 * np.cos(theta1 + theta2)  # 두 번째 링크 끝 위치
    y2 = y1 + a2 * np.sin(theta1 + theta2)
    return [np.array([x1, y1]),np.array([x2,y2])]


def jacobian(theta1, theta2):
    """자코비안 계산"""
    j11 = -a1 * np.sin(theta1) - a2 * np.sin(theta1 + theta2)
    j12 = -a2 * np.sin(theta1 + theta2)
    j21 = a1 * np.cos(theta1) + a2 * np.cos(theta1 + theta2)
    j22 = a2 * np.cos(theta1 + theta2)
    return np.array([[j11, j12], [j21, j22]])

def check_singularity(J):
    """특이점 확인"""
    det_J = np.linalg.det(J)
    return abs(det_J) < 1e-6, det_J  # 행렬식이 0에 가까운 경우






def plot_robot(ax, positions):
    """Plot the robot arm based on the given positions."""
    ax.cla()  # Clear the axes for new plotting
    
    
    if positions:  # Check if positions list is not empty
        # Start plotting the robot arm
        ax.plot([0, positions[0][0]], [0, positions[0][1]], 'ro-')  # 0,0 에서 첫번째 점 까지 연결
        ax.plot([positions[0][0], positions[1][0]],[positions[0][1], positions[1][1]],'bo-')
        #print(positions)
        # Plot the end effector position
        #end_effector_position = positions[-1]
        #ax.scatter(end_effector_position[0], end_effector_position[1], end_effector_position[2], color='green',  
        #           label=f'Pos : ({end_effector_position[0]:.2f}, {end_effector_position[1]:.2f},{end_effector_position[2]:.2f})\nOri : ({Orientaion[2]:.2f},{Orientaion[0]:.2f},{Orientaion[1]:.2f})')  # End effector position
        ax.legend()
    # Set limits and labels
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('3D Visualization of Robotic Arm')
    
    ax.grid(True)
    plt.draw()  # Redraw the plot
    
    
    
def plot_bar_chart(ax_bar,theta):
    """막대 그래프를 그리는 함수"""
    ax_bar.cla()
    labels = ["det(J)"]
    values = [check_singularity(jacobian(theta[0],theta[1]))[1]]  # 초기값
    print("jaco",check_singularity(jacobian(theta[0],theta[1]))[1])
    ax_bar.bar(labels, values, color=['green'])
    ax_bar.set_ylim([-1, 1])
    ax_bar.set_ylabel("det_Jacobian")
    ax_bar.set_title("Joint Angles")
    
def update(val):
    """Update the robot plot based on the slider values."""
    # Update joint angles from sliders
    for i in range(2):
        theta_degrees[i] = sliders[i].val  # Access each slider's value from the list

    # Convert degrees to radians for calculations
    theta = np.radians(theta_degrees)

    # Calculate Forward Kinematics
    positions = forward_kinematics(theta[0],theta[1])
    print(positions)
    # Update the plot
    plot_robot(ax, positions)
    plot_bar_chart(ax2,theta)



theta_degrees = [0, 0]
# Create initial plot
theta = np.radians(theta_degrees)  # Ensure the initial angles are in radians
positions = forward_kinematics(theta[0],theta[1])  # Calculate initial positions
print(positions)
fig = plt.figure(figsize=(6, 8))  # Adjust figure size
ax = fig.add_subplot(211)
ax.set_aspect('equal',adjustable='box')

# Initial plotting
plot_robot(ax, positions)


ax2 = fig.add_subplot(212)  # 2D 서브플롯 추가
plot_bar_chart(ax2,theta)

# ax = fig.add_subplot(212)
# Create sliders for each joint angle
sliders = []  # List to hold slider objects 
slider_ax = [plt.axes([0.32, 0.52 + i * 0.05, 0.4, 0.03]) for i in range(2)]  # [left, bottom, width, height]Adjusted positioning of sliders
for i in range(2):
    slider = Slider(slider_ax[i], f'Theta {i + 1}', -180, 180, valinit=theta_degrees[i])
    sliders.append(slider)  # Store slider in the list
    slider.on_changed(update)  # Attach update function to slider changes
plt.legend()
plt.tight_layout()
plt.show()
#####################################


