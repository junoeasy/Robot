import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

# 링크의 길이
a1 = 1.0  # 첫 번째 링크 길이
a2 = 1.0  # 두 번째 링크 길이

def forward_kinematics(theta1, theta2):
    """엔드 이펙터의 위치 계산"""
    x1 = a1 * np.cos(theta1)        # 첫 번째 링크 끝 위치
    y1 = a1 * np.sin(theta1)
    x2 = x1 + a2 * np.cos(theta1 + theta2)  # 두 번째 링크 끝 위치
    y2 = y1 + a2 * np.sin(theta1 + theta2)
    return np.array([x1, y1]), np.array([x2, y2])  # 첫 번째 조인트와 엔드 이펙터 위치 반환

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

# 시뮬레이션을 위한 초기 설정
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 10))
ax1.set_xlim(-2, 2)
ax1.set_ylim(-2, 2)
ax1.set_aspect('equal')
ax1.grid()
ax1.set_title("Robot Arm")
ax1.set_xlabel("X-axis")
ax1.set_ylabel("Y-axis")

# 슬라이더를 위한 축 설정
slider_ax1 = plt.axes([0.3, 0.58, 0.5, 0.03])  # 슬라이더 1 (theta1)
slider_ax2 = plt.axes([0.3, 0.55, 0.5, 0.03])  # 슬라이더 2 (theta2)

# 슬라이더 초기화
theta1_slider = Slider(slider_ax1, 'Theta 1', -np.pi, np.pi, valinit=0.0)
theta2_slider = Slider(slider_ax2, 'Theta 2', -np.pi, np.pi, valinit=0.0)

def draw_robot(theta1, theta2):
    """로봇 팔 그리기"""
    ax1.clear()
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax1.set_aspect('equal')
    ax1.grid()
    
    joint1 = np.array([0, 0])
    joint2, end_effector = forward_kinematics(theta1, theta2)

    # 링크를 그리기
    ax1.plot([joint1[0], joint2[0]], [joint1[1], joint2[1]], 'ro-', label='Link 1')  # 첫 번째 링크
    ax1.plot([joint2[0], end_effector[0]], [joint2[1], end_effector[1]], 'bo-', label='Link 2')  # 두 번째 링크
    ax1.plot(end_effector[0], end_effector[1], 'go', label='End Effector')  # 엔드 이펙터
    ax1.legend()

    # 자코비안 계산
    J = jacobian(theta1, theta2)
    singular, det_J = check_singularity(J)
    
    # 행렬식 값 시각화
    ax2.clear()
    ax2.bar(['det(J)'], [det_J], color='red' if singular else 'green')
    ax2.set_title("Singularity Determinant")
    ax2.set_ylabel("det_Jacobian")
    ax2.set_ylim(-1, 1)  # 행렬식의 범위 설정
    ax2.axhline(0, color='black', lw=1)  # y=0 선 추가

    # 특이점 여부 출력
    if singular:
        ax2.text(0, det_J + 0.1, 'Singularity!', color='red', ha='center')

# 슬라이더 값 변경 시 로봇을 업데이트하는 함수
def update(val):
    theta1 = theta1_slider.val
    theta2 = theta2_slider.val
    draw_robot(theta1, theta2)

# 슬라이더 이벤트 연결
theta1_slider.on_changed(update)
theta2_slider.on_changed(update)

# 초기 로봇 그림
draw_robot(0.0, 0.0)

plt.tight_layout()
plt.show()

