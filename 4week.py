import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Load data from CSV
data = pd.read_csv('data/IMU_GPS_sensor_data.csv')
time = data['time'].values
gps_x = data['gps_x'].values
gps_y = data['gps_y'].values
absolute_x = data['absolute_x'].values
absolute_y = data['absolute_y'].values
imu_acceleration_x = data['imu_acceleration_x'].values
imu_acceleration_y = data['imu_acceleration_y'].values

class KalmanFilter:
    def __init__(self, process_variance, measurement_variance):
        self.x = np.array([[0], [0], [0], [0]]) #현재 상태 (위치 + 속도)
        self.P = np.eye(4) #오차 공분산 (추정의 신뢰도)
        self.F = np.array([[1, 0, 1, 0],
                           [0, 1, 0, 1],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]]) #상태 전이 행렬 (현재 상태에서 다음 상태로 어떻게 변하는지)
        self.H = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0]]) #측정 행렬 (센서 값과 상태 변수 간의 관계)
        self.Q = np.eye(4) * process_variance #프로세스 노이즈 (모델의 불확실성)
        self.R = np.eye(2) * measurement_variance #측정 노이즈 (센서 오차)
        
    def predict(self, dt, imu_acceleration):
        self.F[0, 2] = dt
        self.F[1, 3] = dt
        acceleration = np.array([[0.5 * imu_acceleration[0] * dt**2], 
                                [0.5 * imu_acceleration[1] * dt**2],
                                [imu_acceleration[0] * dt],
                                [imu_acceleration[1] * dt]])
        self.x = self.F @ self.x + acceleration
        self.P = self.F @ self.P @ self.F.T + self.Q
    
    def update(self, gps_measurement):
        y = gps_measurement - (self.H @ self.x)
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (np.eye(4) - K @ self.H) @ self.P
        
            
# Create a function to run the Kalman Filter and update the plot
def run_kalman_filter(process_variance, measurement_variance):
    kf = KalmanFilter(process_variance, measurement_variance)
    estimates_x = []
    estimates_y = []

    for i in range(1, len(time)):
        dt = time[i] - time[i - 1]
        imu_acceleration = [imu_acceleration_x[i], imu_acceleration_y[i]]
        gps_measurement = np.array([[gps_x[i]], [gps_y[i]]])

        kf.predict(dt, imu_acceleration)
        kf.update(gps_measurement)

        estimates_x.append(float(kf.x[0, 0]))
        estimates_y.append(float(kf.x[1, 0]))
    print("x",estimates_x)
    print("gps",gps_x)
    return estimates_x,estimates_y
        
        
        
fig, ax1 = plt.subplots(1, 1, figsize=(10, 5))
ax1.set_xlim(-2, 25)
ax1.set_ylim(-7, 7)
ax1.grid()
ax1.set_title("Robot Arm")
ax1.set_xlabel("X-axis")
ax1.set_ylabel("Y-axis")

# 슬라이더를 위한 축 설정
slider_ax1 = plt.axes([0.3, 0.58, 0.5, 0.03])  # 슬라이더 1 (theta1)
slider_ax2 = plt.axes([0.3, 0.55, 0.5, 0.03])  # 슬라이더 2 (theta2)

Measure_slider = Slider(slider_ax1, 'Measurement Variance', 0.1, 10, valinit=1.0)
Process_slider = Slider(slider_ax2, 'Process Variance', 0.0001, 0.1, valinit=0.0001)

def draw(measurement,process):
    ax1.clear()
    ax1.set_xlim(-2, 25)
    ax1.set_ylim(-7, 7)
    x,y=run_kalman_filter(measurement,process)
    ax1.scatter(x,y,color='blue',s=1,label='Kalman Filter predicted(GPS+IMU)')
    ax1.scatter(gps_x,gps_y,color='green',s=1,label='GPS measured')
    ax1.scatter(absolute_x,absolute_y,color='red',s=1,label='absolute_path(GT)')
    ax1.legend()
    ax1.grid()
    
def update(val):
    measurement = Measure_slider.val
    process = Process_slider.val
    draw(measurement, process)

measurement = Measure_slider.val
process = Process_slider.val
draw(measurement, process)
Measure_slider.on_changed(update)
Process_slider.on_changed(update)
plt.show()