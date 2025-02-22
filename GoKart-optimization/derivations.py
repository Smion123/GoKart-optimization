import spline
import constants_and_points
import variables
import math


'''
def get_derivation(t):

    current = spline.compute_spline_point(t, constants.control_points)
    after = spline.compute_spline_point(t + 0.001, constants.control_points)

    current = spline.compute_current_spline_point()
    after = spline.compute_current_spline_point_offset_for_derivation()
    print("der after", after[0])
    print("der current", current[0])

    velocity_x = (after[0] - current[0])
    velocity_y = (after[1] - current[1])
    result = [velocity_x, -velocity_y]

    return result
'''
def get_derivation(t):
    delta = 0.001
    current = spline.compute_spline_point(t, constants_and_points.control_points)
    after = spline.compute_spline_point(t + delta, constants_and_points.control_points)
    velocity_x = (after[0] - current[0])
    velocity_y = (after[1] - current[1])
    result = [velocity_x / delta, -velocity_y / delta]

    return result

def get_second_derivation(t):
    delta = 0.001
    current = get_derivation(t)
    after = get_derivation(t+delta)
    acceleration_x = (after[0] - current[0])
    acceleration_y = (after[1] - current[1])
    result = [acceleration_x / delta, acceleration_y / delta]

    return result

def get_max_accel_rotated_multiple(accel_x, accel_y, deg_rot):
    total_accel = math.sqrt(accel_x**2 + accel_y**2)
    #print(str(total_accel))
    if (total_accel > variables.max_accel_multiple):
        variables.max_accel_multiple = total_accel
        variables.t_at_last_max_accel = variables.t

def get_min_accel_rotated_multiple(accel_x, accel_y, deg_rot):
    total_accel = math.sqrt(accel_x**2 + accel_y**2)
    #print(str(total_accel))
    if (total_accel < variables.smallest_accel):
        variables.smallest_accel = total_accel
        variables.t_at_smallest_accel = variables.t