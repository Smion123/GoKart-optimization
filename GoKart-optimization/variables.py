import pygame

t = 0

number_of_improvements_accepted = 0

ticks_offset = 0


max_accel_multiple = 0
detected_collision = 0

x = 0
y = 0

velocity_x = 0
velocity_y = 0

acceleration_x = 0
acceleration_y = 0

current_acceleration_squared_for_total = 0
max_accel_delta_recorded = 0
current_accel_delta = 0
t_at_worst_smoothness = 0
total_accel_delta_for_smoothness_eval = 0
t_at_least_velocity = 0
smallest_velocity_measured = 0
total_distance = 0
t_at_smallest_accel = 0
smallest_accel = 999999

previous_x = 0
previous_y = 0


car_rot_rect = pygame.Rect(0,0,0,0)

best_run_value = 0

t_at_last_collision = 0
t_at_last_max_accel = 0

rotation_angles = []

total_penalty_accel = 0
total_penalty_smoothness = 0
total_penalty_min_speed = 0
total_penalty_distance = 0

stop_and_write = 0
stop = 0

approximate_collision_detected = 0

show_trajectory_flag = 1

repetitions_since_last_accept = 0

accel_modifier = 2
smoothness_modifier = 1
min_speed_modifier = 0.5
distance_modifier = 0.05
approximate_collisions_modifier = 1
progress_done = 0

control_points_at_start = 0

adding_more_points_allowed = 1

showmode_on = 1

victory_tune = pygame.mixer.init()
victory_tune = pygame.mixer.Sound("tune.mp3")