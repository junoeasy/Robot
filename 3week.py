import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

#링크 길이
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
    det_J = np.linalg.det(J)
    return abs(det_J) < 1e-6, det_J  # 행렬식이 0에 가까운 경우




def plot_robot(ax, positions):
    ax.cla()  # Clear the axes for new plotting
    if positions:  # Check if positions list is not empty
        # Start plotting the robot arm
        ax.plot([0, positions[0][0]], [0, positions[0][1]], 'ro-',label='link1')  # 0,0 에서 첫번째 점 까지 연결
        ax.plot([positions[0][0], positions[1][0]],[positions[0][1], positions[1][1]],'bo-',label="link2") #첫번째 점에서 두번째 점 까지 연결결
        # Plot the end effector position
        end_effector_position = positions[-1]
        ax.scatter(end_effector_position[0], end_effector_position[1], color='green',label="End effector" ,zorder=3)
        ax.legend()
        
    # Set limits and labels
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_xticks(np.arange(-2, 2.1, 0.5))  # X축 눈금 간격을 0.5로 설정
    ax.set_yticks(np.arange(-2, 2.1, 0.5))  # Y축 눈금 간격을 0.5로 설정
    ax.grid(True)
    plt.draw()  # Redraw the plot
    
    
    
def plot_bar_chart(ax_bar,theta):
    #초기화
    ax_bar.cla()
    #가운데 검은색 줄 추가
    ax2.axhline(0, color='black', linewidth=1.5, linestyle='-')
    labels = ["det(J)"]
    values = [check_singularity(jacobian(theta[0],theta[1]))[1]]  # 초기값
    ax_bar.bar(labels, values, color=['green'],label=f'det(jacobian): {check_singularity(jacobian(theta[0],theta[1]))[1]:.2f}') #자코비안 값 설정 및 라벨 설정
    if check_singularity(jacobian(theta[0],theta[1]))[0]: 
        ax2.text(0.5, 0.6, 'singularity', fontsize=14, color='red', ha='center', va='center', transform=ax2.transAxes)
    ax_bar.set_ylim([-1, 1]) #y축 범위위
    ax_bar.set_ylabel("det_Jacobian")
    ax_bar.set_title("Singularity Determinant")
    ax2.legend()
    
    
    
def update(val):
    """Update the robot plot based on the slider values."""
    for i in range(2):
        theta_degrees[i] = sliders[i].val  
    theta = np.radians(theta_degrees)
    positions = forward_kinematics(theta[0],theta[1])
    plot_robot(ax, positions)
    plot_bar_chart(ax2,theta)


#초기 각도
theta_degrees = [0, 0]
theta = np.radians(theta_degrees) 
positions = forward_kinematics(theta[0],theta[1])  
fig = plt.figure(figsize=(5, 8)) 
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)  # 2D 서브플롯 추가
# Initial plotting
plot_robot(ax, positions)
plot_bar_chart(ax2,theta)

#슬라이더 추가가
sliders = []  
slider_ax = [plt.axes([0.45, 0.6 - i * 0.05, 0.4, 0.03]) for i in range(2)]  
for i in range(2):
    slider = Slider(slider_ax[i], f'Theta{i + 1}(degree)', -180, 180, valinit=theta_degrees[i])
    sliders.append(slider) 
    slider.on_changed(update) #슬라이더 값 조절시 실시간 변경
    
plt.legend()
plt.tight_layout()
plt.show()


