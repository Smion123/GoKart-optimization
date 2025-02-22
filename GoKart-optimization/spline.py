import math
import variables
import constants_and_points
"""
def compute_spline_point(t, control_points):
    result = [0, 0]
    
    #result[0] = math.sin(t/29) *700 +800
    #result[1] = math.sin(t/2) *100 +300


    num_of_spline_segments = len(control_points) -1
    i = math.floor(t)
    if i < num_of_spline_segments:
        start_points = control_points[i]
        end_points_flipped = control_points[i+1]
        end_points = [end_points_flipped[2], end_points_flipped[1], end_points_flipped[0]]
        modified_start_points = [[modify_m1(start_points[0][0], start_points[1][0], start_points[2][0]), modify_m1(start_points[0][1], start_points[1][1], start_points[2][1])], [modify_m2(start_points[0][0], start_points[1][0], start_points[2][0]), modify_m2(start_points[0][1], start_points[1][1], start_points[2][1])], [modify_m3(start_points[0][0], start_points[1][0], start_points[2][0]), modify_m3(start_points[0][1], start_points[1][1], start_points[2][1])]]
        modified_end_points = [[modify_m4(end_points[0][0], end_points[1][0], end_points[2][0]), modify_m4(end_points[0][1], end_points[1][1], end_points[2][1])], [modify_m5(end_points[0][0], end_points[1][0], end_points[2][0]), modify_m5(end_points[0][1], end_points[1][1], end_points[2][1])], [modify_m6(end_points[0][0], end_points[1][0], end_points[2][0]), modify_m6(end_points[0][1], end_points[1][1], end_points[2][1])]]
        print("start point x", start_points[0][0])
        print("end point x", end_points[0][0])
        x = (1-t)**5 * modified_start_points[0][0] + 5 * (1-t)**4 * t * modified_start_points[1][0] + 10 * (1-t)**3 * t**2 * modified_start_points[2][0] + 10 * (1-t)**2 * t**3 * modified_end_points[0][0] + 5 * (1-t) * t**4 * modified_end_points[1][0] + t**5 * modified_end_points[2][0]
        y = (1-t)**5 * modified_start_points[0][1] + 5 * (1-t)**4 * t * modified_start_points[1][1] + 10 * (1-t)**3 * t**2 * modified_start_points[2][1] + 10 * (1-t)**2 * t**3 * modified_end_points[0][1] + 5 * (1-t) * t**4 * modified_end_points[1][1] + t**5 * modified_end_points[2][1]
        result = [x, y]

    return result
"""

"""
def compute_current_spline_point():
    current_segment_num = math.floor(variables.t)
    result = compute_spline_point(variables.t - current_segment_num, constants_and_points.control_points)
    return result

def compute_current_spline_point_offset_for_derivation():
    current_segment_num = math.floor(variables.t + 0.001)
    result = compute_spline_point(variables.t + 0.001 - current_segment_num, constants_and_points.control_points)
    return result
"""

'''
def compute_spline_point(t, starting_control_point, ending_control_point_):
    result = [0, 0]

    end_points = [ending_control_point_[2], ending_control_point_[1], ending_control_point_[0]]
    modified_start_points = [[modify_m1(starting_control_point[0][0], starting_control_point[1][0], starting_control_point[2][0]), modify_m1(starting_control_point[0][1], starting_control_point[1][1], starting_control_point[2][1])], [modify_m2(starting_control_point[0][0], starting_control_point[1][0], starting_control_point[2][0]), modify_m2(starting_control_point[0][1], starting_control_point[1][1], starting_control_point[2][1])], [modify_m3(starting_control_point[0][0], starting_control_point[1][0], starting_control_point[2][0]), modify_m3(starting_control_point[0][1], starting_control_point[1][1], starting_control_point[2][1])]]
    modified_end_points = [[modify_m4(end_points[0][0], end_points[1][0], end_points[2][0]), modify_m4(end_points[0][1], end_points[1][1], end_points[2][1])], [modify_m5(end_points[0][0], end_points[1][0], end_points[2][0]), modify_m5(end_points[0][1], end_points[1][1], end_points[2][1])], [modify_m6(end_points[0][0], end_points[1][0], end_points[2][0]), modify_m6(end_points[0][1], end_points[1][1], end_points[2][1])]]
    x = (1-t)**5 * modified_start_points[0][0] + 5 * (1-t)**4 * t * modified_start_points[1][0] + 10 * (1-t)**3 * t**2 * modified_start_points[2][0] + 10 * (1-t)**2 * t**3 * modified_end_points[0][0] + 5 * (1-t) * t**4 * modified_end_points[1][0] + t**5 * modified_end_points[2][0]
    y = (1-t)**5 * modified_start_points[0][1] + 5 * (1-t)**4 * t * modified_start_points[1][1] + 10 * (1-t)**3 * t**2 * modified_start_points[2][1] + 10 * (1-t)**2 * t**3 * modified_end_points[0][1] + 5 * (1-t) * t**4 * modified_end_points[1][1] + t**5 * modified_end_points[2][1]
    result = [x, y]

    return result
'''

def compute_spline_point(t, control_points):
    result = [0, 0]

    t_floored = math.floor(t)
    t_changed = t - t_floored

    starting_control_point = control_points[t_floored]
    ending_control_point = control_points[t_floored + 1]

    end_points = [ending_control_point[2], ending_control_point[1], ending_control_point[0]]
    modified_start_points = [[modify_m1(starting_control_point[0][0], starting_control_point[1][0], starting_control_point[2][0], 1), modify_m1(starting_control_point[0][1], starting_control_point[1][1], starting_control_point[2][1], 1)], [modify_m2(starting_control_point[0][0], starting_control_point[1][0], starting_control_point[2][0], t_changed + 1), modify_m2(starting_control_point[0][1], starting_control_point[1][1], starting_control_point[2][1], t_changed + 1)], [modify_m3(starting_control_point[0][0], starting_control_point[1][0], starting_control_point[2][0], t_changed + 1), modify_m3(starting_control_point[0][1], starting_control_point[1][1], starting_control_point[2][1], t_changed + 1)]]
    modified_end_points = [[modify_m4(end_points[0][0], end_points[1][0], end_points[2][0], t_changed), modify_m4(end_points[0][1], end_points[1][1], end_points[2][1], t_changed)], [modify_m5(end_points[0][0], end_points[1][0], end_points[2][0], t_changed), modify_m5(end_points[0][1], end_points[1][1], end_points[2][1], t_changed)], [modify_m6(end_points[0][0], end_points[1][0], end_points[2][0], t_changed), modify_m6(end_points[0][1], end_points[1][1], end_points[2][1], t_changed)]]
    x = (1-t_changed)**5 * modified_start_points[0][0] + 5 * (1-t_changed)**4 * t_changed * modified_start_points[1][0] + 10 * (1-t_changed)**3 * t_changed**2 * modified_start_points[2][0] + 10 * (1-t_changed)**2 * t_changed**3 * modified_end_points[0][0] + 5 * (1-t_changed) * t_changed**4 * modified_end_points[1][0] + t_changed**5 * modified_end_points[2][0]
    y = (1-t_changed)**5 * modified_start_points[0][1] + 5 * (1-t_changed)**4 * t_changed * modified_start_points[1][1] + 10 * (1-t_changed)**3 * t_changed**2 * modified_start_points[2][1] + 10 * (1-t_changed)**2 * t_changed**3 * modified_end_points[0][1] + 5 * (1-t_changed) * t_changed**4 * modified_end_points[1][1] + t_changed**5 * modified_end_points[2][1]
    result = [x, y]

    variables.x = x
    variables.y = y

    return result

def modify_m1(point1, point2, point3, t):
    t = 1
    return point1

def modify_m2(point1, point2, point3, t):
    t = 1
    return point1 + point2*t/5

def modify_m3(point1, point2, point3, t):
    t = 1
    return point1 + 2 * point2*t/5 + (point3*(t**2))/20

def modify_m4(point4, point5, point6, t):
    t = 1
    return point6 - 2 * point5*t/5 + (point4*(t**2))/20

def modify_m5(point4, point5, point6, t):
    t = 1
    return point6 - point5*t/5

def modify_m6(point4, point5, point6, t):
    t = 1
    return point6
