import pygame
import math
import derivations
import constants_and_points
import spline
import variables
import track
import random
import time
import cProfile
import re
from sys import exit

# px = dm

'''
kontrola zrychleni i kdyz se zataci (bacha na rotaci)
zkusit manualne trajektorii a ohodnotit jestli optimalizuju spravny veci

upresneni jednotek? ted je to chaos
'''

#run_main(1) == sim speed slow # variable speed, equal gaps (presentation purposes???)
#run_main(2) == sim speed
#run_main(3) == sim speed faster
#run_main(4) == real speed # constant speed, weird gaps

def space_points():
    
    variables.control_points_at_start = len(constants_and_points.control_points)
    variables.repetitions_since_last_accept = 0
    variables.number_of_improvements_accepted = 0

    variables.best_run_value = evaluate_run()
    if variables.best_run_value > 1000:
        variables.best_run_value = 999
    print("best_run_value init as: ", variables.best_run_value)

    '''
    for k in range(20):
        translation_optimization()
        positional_optimization()
        check_for_exit_cue(0)
        check_for_weighting_changes_and_point_additions()
    '''
#optimalizace trajektorie jen pro jeden segment!!!
   list get_accel_for_segment
   m = max(get_accel_for_segment)
   i = get_accel_for_segment.index(m)
   random.randint(0,1)


def draw_points():
    for x in range(len(constants_and_points.control_points)):
        for y in range(3):
            if (y == 0):
                draw_control_point_circle(constants_and_points.control_points[x][y], y)
            if (y == 1):
                draw_control_point_circle(get_relative_speed(constants_and_points.control_points[x][y], constants_and_points.control_points[x][0]), y)
            if (y == 2):
                draw_control_point_circle(get_relative_acceleration(constants_and_points.control_points[x][y], constants_and_points.control_points[x][0]), y)

def draw_track():
    for i in range(len(track.track_limits)):
        pygame.draw.rect(screen, (255, 0, 0), track.track_limits[i])

def get_relative_speed(control_point, pos_point):
    x = control_point[0] / 10 + pos_point[0]
    y = control_point[1] / 10 + pos_point[1]
    result = [x, y]
    return result

def get_relative_acceleration(control_point, pos_point):
    x = control_point[0] / 10 + pos_point[0]
    y = control_point[1] / 10 + pos_point[1]
    result = [x, y]
    return result

def get_car_alfa_rot():
    input = derivations.get_derivation(variables.t)

    hypotenuse = math.sqrt(input[0]**2 + input[1]**2)
    
    if (check_positive(input[0]) == 1):
        quadrantX = [1, 4]
    elif (check_positive(input[0]) == -1):
        quadrantX = [2, 3]
    else:
        quadrantX = [0, 0]


    if (check_positive(input[1]) == 1):
        quadrantY = [1, 2]
    elif (check_positive(input[1]) == -1):
        quadrantY = [3, 4]
    else:
        quadrantY = [0, 0]

    combined = quadrantX + quadrantY

    if 0 in combined:
        return 0

    doubled = []

    for i in range(len(combined)):
        if combined[i] not in doubled:
            doubled.append(combined[i])
        else:
            finalQuadrant = combined[i]

    if finalQuadrant == 1:
        return math.degrees(math.acos(input[0]/hypotenuse))
    elif finalQuadrant == 2:
        return math.degrees(math.acos(input[0]/hypotenuse))
    elif finalQuadrant == 3:
        return math.degrees(math.asin(input[0]/hypotenuse)) - 90
    elif finalQuadrant == 4:
        return math.degrees(math.asin(input[0]/hypotenuse)) - 90
    else:
        raise Exception("quadrant out of range")

def truncate_num(n, decimals=0):
    multiplier = 10**decimals
    return int(n * multiplier) / multiplier



def check_positive(a):
    if (a > 0):
        return 1
    
    elif (a < 0):
        return -1
    
    elif (a == 0):
        return 0
    
    else:
        return -2


def reset_ticks():
    variables.ticks_offset = pygame.time.get_ticks()

def read_ticks():
    return pygame.time.get_ticks() - variables.ticks_offset

def display_stats():
    total_width = 7
    total_width_for_t = 4
    variables.velocity_x = derivations.get_derivation(variables.t)[0]
    variables.velocity_y = derivations.get_derivation(variables.t)[1]
    variables.acceleration_x = derivations.get_second_derivation(variables.t)[0]
    variables.acceleration_y = derivations.get_second_derivation(variables.t)[1]
    #print(math.sqrt(variables.velocity_x**2 + variables.velocity_y**2))
    text_surface = data.render("velocity X " + f"{variables.velocity_x :0{total_width}.2f}" + "   velocity Y " + f"{variables.velocity_y :0{total_width}.2f}" + "   acceleration X " + f"{variables.acceleration_x :0{total_width}.2f}" + "   acceleration Y " + f"{variables.acceleration_y :0{total_width}.2f}" + "   t: " + f"{variables.t:0{total_width_for_t}.2f}", False, "White", (64, 64, 64))
    #text_surface = data.render("velocity X " + str(truncate_num(variables.velocity_x * 10, 2)) + "   velocity Y " + str(truncate_num(variables.velocity_y * 10, 2)) + "   acceleration X " + str(truncate_num(variables.acceleration_x * 10, 2)) + "   acceleration Y " + str(truncate_num(variables.acceleration_y * 10, 2)) + "   t: " + str(truncate_num(variables.t, 2)), False, "White", (64, 64, 64))
    text_rect = text_surface.get_rect(center = (constants_and_points.data_x_offset, constants_and_points.data_y_offset))
    text_rect_unchanged = text_surface.get_rect(center = (constants_and_points.data_x_offset, constants_and_points.data_y_offset))
    width = text_surface.get_width()
    height = text_surface.get_height()
    black_surface = pygame.Surface((width + 200, height))
    text_rect = text_rect.inflate(200, 0)
    if variables.showmode_on == 1:
        screen.blit(black_surface, text_rect)
        screen.blit(text_surface, text_rect_unchanged)

def clean_screen():
    screen.fill((0,0,0), None)


def organize_control_points():
    done = False
    j = 0
    while (not done):
        try:
            eval(f"constants_and_points.point_{j}_pos")
        except:
            constants_and_points.num_points = j
            done = True
            print("num of control points counted to be: ", j)
        j = j + 1

        


    control_points = []
    
    for i in range(constants_and_points.num_points):
        pos = eval(f"constants_and_points.point_{i}_pos")
        speed = eval(f"constants_and_points.point_{i}_actual_speed")
        accel = eval(f"constants_and_points.point_{i}_actual_acceleration")
        control_points.append([pos, speed, accel])
    
    return control_points

def organize_track():
    done = False
    j = 0
    while (not done):
        try:
            eval(f"track.track_limit_{j}")
        except:
            track.num_of_track_limits = j
            done = True
            print("num of track limits counted to be: ", j)
        j = j + 1


    track_limits = []

    for i in range(track.num_of_track_limits):
        track_limits.append(eval(f"track.track_limit_{i}"))
    return track_limits
    


def  display_car(pos, display_bool):
    car_rotated = pygame.transform.rotate(pygame.transform.scale(car_sufrace, (constants_and_points.car_x_len, constants_and_points.car_y_len)), get_car_alfa_rot())

    '''
    if variables.showmode_on == 1:
        car_rotated = pygame.transform.rotate(pygame.transform.smoothscale(car_sufrace, (constants_and_points.car_x_len, constants_and_points.car_y_len)), get_car_alfa_rot()) #probleem
    else:
        car_rotated = pygame.transform.rotate(pygame.transform.scale(car_sufrace, (constants_and_points.car_x_len, constants_and_points.car_y_len)), get_car_alfa_rot())
    '''
    variables.car_rot_rect = car_rotated.get_rect(center = pos)
    if variables.show_trajectory_flag == 1 and variables.showmode_on == 1:
        screen.blit(car_rotated, variables.car_rot_rect)

def draw_control_point_circle(pos, color):
    if (color == 0):
        pygame.draw.circle(screen, (0, 255, 255), pos, 5)
    if (color == 1):
        pygame.draw.circle(screen, (255, 0, 255), pos, 5)
    if (color == 2):
        pygame.draw.circle(screen, (255, 255, 0), pos, 5)

def load_control_points():
    constants_and_points

pygame.init()
pygame.mixer.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h - 2))

pygame.display.set_caption('Trajectory')
clock = pygame.time.Clock()

data = pygame.font.Font(constants_and_points.font_path, constants_and_points.font_size)

car_sufrace = pygame.image.load('grafika/auto.png')


constants_and_points.control_points = organize_control_points()
track.track_limits = organize_track()


def detect_collisions():
    deflated_car = variables.car_rot_rect.scale_by(0.5)
    inflated_car = variables.car_rot_rect.scale_by(4)

    for i in track.track_limits:
        if deflated_car.colliderect(i):
            variables.detected_collision = 1
            variables.t_at_last_collision = variables.t
            print("track limit collided with: " + str(i)) 
            print("t at collision: " + str(variables.t_at_last_collision))
            car_sufrace.set_alpha(100)
        if inflated_car.colliderect(i):
            variables.approximate_collision_detected = variables.approximate_collision_detected + 1

def detect_worst_speed():
    total_current_speed = math.sqrt(variables.velocity_x**2 + variables.velocity_y**2)
    if variables.smallest_velocity_measured > total_current_speed:
        variables.smallest_velocity_measured = total_current_speed
        variables.t_at_least_velocity = variables.t

def compute_smoothness_dependant_on_speed():
    last_total_acceleration = variables.current_acceleration_squared_for_total
    variables.current_acceleration_squared_for_total = math.sqrt(variables.acceleration_x**2 + variables.acceleration_y**2)
    accel_delta = abs(last_total_acceleration - variables.current_acceleration_squared_for_total)
    if accel_delta > variables.max_accel_delta_recorded:
        variables.max_accel_delta_recorded = accel_delta
        variables.t_at_worst_smoothness = math.floor(variables.t)
    variables.current_accel_delta = accel_delta
    variables.total_accel_delta_for_smoothness_eval = variables.total_accel_delta_for_smoothness_eval + (accel_delta)
    return accel_delta

def detect_distance():
    last_x = variables.previous_x
    last_y = variables.previous_y
    current_point = [variables.x, variables.y]
    variables.previous_x = current_point[0]
    variables.previous_y = current_point[1]
    distance_x = abs(last_x - variables.previous_x)
    distance_y = abs(last_y - variables.previous_y)
    total_distance_local = math.sqrt(distance_x**2 + distance_y**2)
    variables.total_distance = variables.total_distance + total_distance_local

def drawing_displaying_updating():
    spline_points = spline.compute_spline_point(variables.t, constants_and_points.control_points)
    display_stats()
    
    if variables.showmode_on == 1:
        display_car([spline_points[0], spline_points[1]], 1)
        pygame.display.flip() #maybe update()
    elif variables.repetitions_since_last_accept % 50000 == 0:
        variables.showmode_on = 1
        display_car([spline_points[0], spline_points[1]], 1)
        variables.adding_more_points_allowed = 1
        pygame.display.flip() #maybe update()
        variables.showmode_on = 0
    else:
        display_car([spline_points[0], spline_points[1]], 1)


    derivations.get_max_accel_rotated_multiple(variables.acceleration_x, variables.acceleration_y, variables.t)
    variables.rotation_angles.append(get_car_alfa_rot())

    compute_smoothness_dependant_on_speed()

    detect_collisions()

    detect_worst_speed()

    detect_distance()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                variables.stop_and_write = 1



def drawing_displaying_updating_for_elimination():
    spline_points = spline.compute_spline_point(variables.t, constants_and_points.control_points)
    display_stats()
    

    variables.showmode_on = 1
    display_car([spline_points[0], spline_points[1]], 1)
    variables.adding_more_points_allowed = 1
    pygame.display.flip() #maybe update()
    variables.showmode_on = 0

    derivations.get_min_accel_rotated_multiple(variables.acceleration_x, variables.acceleration_y, variables.t)
    variables.rotation_angles.append(get_car_alfa_rot())



def drawing_displaying_updating_with_resets():
    spline_points = spline.compute_spline_point(variables.t, constants_and_points.control_points)
    display_stats()
    draw_track()
    draw_points()
    
    if variables.showmode_on == 1:
        display_car([spline_points[0], spline_points[1]], 1)
        pygame.display.flip() #maybe update()
        variables.showmode_on = 0
    elif variables.repetitions_since_last_accept % 50000 == 0:
        variables.showmode_on = 1
        display_car([spline_points[0], spline_points[1]], 1)
        variables.adding_more_points_allowed = 1
        pygame.display.flip() #maybe update()
        variables.showmode_on = 0
    else:
        display_car([spline_points[0], spline_points[1]], 1)


    derivations.get_max_accel_rotated_multiple(variables.acceleration_x, variables.acceleration_y, variables.t)
    variables.rotation_angles.append(get_car_alfa_rot())

    compute_smoothness_dependant_on_speed()

    detect_collisions()

    detect_worst_speed()

    detect_distance()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                variables.stop_and_write = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            variables.stop = 1



def evaluate_run():
    check_for_exit_cue(0)

    result = 0
    run_main(3)  # Get rotation angles from simulation

    # Collision Penalty
    if (variables.detected_collision == 1):
        result += 1000

    # Add max acceleration penalty
    variables.total_penalty_accel = (variables.max_accel_multiple / 300) * variables.accel_modifier ## here change max accel multiple for optimalization
    result += variables.total_penalty_accel
    print("total base penalty for accel: " + str(variables.total_penalty_accel))
    print("t at last max accel: " + str(variables.t_at_last_max_accel))
    print("accel at worst point: " + str(math.sqrt(derivations.get_second_derivation(variables.t_at_last_max_accel)[0]**2 + derivations.get_second_derivation(variables.t_at_last_max_accel)[1]**2)))
    
    # Smoothness Penalty
    '''
    variables.total_penalty_smoothness = (variables.total_accel_delta_for_smoothness_eval / 10000) * variables.smoothness_modifier * 2 #here change accel optimalization multiplier
    result += variables.total_penalty_smoothness
    print("total base penalty for smoothness: " + str(variables.total_accel_delta_for_smoothness_eval / 10000))
    '''
    #print("approx collision detected??? "  + str(variables.approximate_collision_detected))

    collision_penalty = variables.approximate_collision_detected * 0.07 * variables.approximate_collisions_modifier

    if (variables.approximate_collision_detected > 0):
        result += collision_penalty
    print("total base penalty for approximate collisions: " + str(collision_penalty))
    #else:
        #print("collision not detected")

    '''
    #have this twice??
    #not working correctly - inverted?
    variables.total_penalty_distance = (variables.total_distance / 1000) * variables.distance_modifier ##here change distance penalty
    result += variables.total_penalty_distance
    print("total penalty distance: " + str(variables.total_distance / 1000))
    '''
    
    '''
    # not working correctly???
    variables.total_penalty_min_speed = ((0.1 / (variables.smallest_velocity_measured + 0.000001)) * 1000) * variables.min_speed_modifier #change here for velocity penalty multiplier
    if variables.total_penalty_min_speed > 20:
        variables.total_penalty_min_speed = 20
    result += variables.total_penalty_min_speed
    print("total penalty for min speed: " + str(variables.total_penalty_min_speed))
    # Total Distance Penalty (if applicable)
    '''
    '''
    total_distance = 0
    for i in range(1, len(constants_and_points.control_points)):
        dist = math.sqrt(
            (constants_and_points.control_points[i][0][0] - constants_and_points.control_points[i-1][0][0]) ** 2 +
            (constants_and_points.control_points[i][0][1] - constants_and_points.control_points[i-1][0][1]) ** 2
        )
        total_distance += dist


    variables.total_penalty_distance = total_distance / 2000
    result += variables.total_penalty_distance
    print("total base distance penalty " + str(variables.total_penalty_distance))
    '''

    print("current run evaluation: " + str(result))
    print("best run evaluation:" + str(variables.best_run_value))
    return result

def positional_optimization_try():
    '''
    random_var = random.randint(0, 3)
    if random_var == 3:
        lower_point = random.randint(0, len(constants_and_points.control_points))
    elif variables.detected_collision:
        lower_point = math.floor(variables.t_at_last_collision)
        print("collision detected, t: " + str(variables.t_at_last_collision))
    elif variables.total_penalty_smoothness > variables.total_penalty_accel and variables.total_penalty_smoothness > variables.total_penalty_min_speed:
        lower_point = math.floor(variables.t_at_worst_smoothness)
    elif variables.total_penalty_accel > variables.total_penalty_smoothness and variables.total_penalty_accel > variables.total_penalty_min_speed:
        lower_point = math.floor(variables.t_at_last_max_accel)
    else:
        lower_point = math.floor(variables.t_at_least_velocity)

    variables.start_of_problematic_segment = lower_point

    random_num_for_different_point_pick = random.randint(0, 1)

    lower_point = lower_point + random_num_for_different_point_pick

    if (len(constants_and_points.control_points) - 3) < lower_point:
            lower_point = len(constants_and_points.control_points) - 3
    if lower_point < 1:
        lower_point = 1
    '''

    random_var = random.randint(0, 3)
    if random_var == 3:
        lower_point = random.randint(0, len(constants_and_points.control_points))
        #print("choosing this point randomly: " + str(lower_point))
    else:
        lower_point = math.floor(variables.t_at_last_max_accel)

    point_chosen = lower_point + random.randint(0, 1)

    if (len(constants_and_points.control_points) - 2) < point_chosen:
            point_chosen = len(constants_and_points.control_points) - 2
    if point_chosen < 1:
        point_chosen = 1

    print("point chosen to be changed: " + str(point_chosen))


    previous_position_x = constants_and_points.control_points[point_chosen][0][0]
    previous_position_y = constants_and_points.control_points[point_chosen][0][1]
    previous_velocity_x = constants_and_points.control_points[point_chosen][1][0]
    previous_velocity_y = constants_and_points.control_points[point_chosen][1][1]
    previous_acceleration_x = constants_and_points.control_points[point_chosen][2][0]
    previous_acceleration_y = constants_and_points.control_points[point_chosen][2][1]


    constants_and_points.control_points[point_chosen][0][0] = constants_and_points.control_points[point_chosen][0][0] + random.uniform(-5, 5)
    constants_and_points.control_points[point_chosen][0][1] = constants_and_points.control_points[point_chosen][0][1] + random.uniform(-5, 5)
    constants_and_points.control_points[point_chosen][1][0] = constants_and_points.control_points[point_chosen][1][0] + random.uniform(-5, 5)
    constants_and_points.control_points[point_chosen][1][1] = constants_and_points.control_points[point_chosen][1][1] + random.uniform(-5, 5)
    constants_and_points.control_points[point_chosen][2][0] = constants_and_points.control_points[point_chosen][2][0] + random.uniform(-5, 5)
    constants_and_points.control_points[point_chosen][2][1] = constants_and_points.control_points[point_chosen][2][1] + random.uniform(-5, 5)

    data_for_reverting = (point_chosen, previous_position_x, previous_position_y, previous_velocity_x, previous_velocity_y, previous_acceleration_x, previous_acceleration_y)

    # Change the control point and store the previous state
    return (data_for_reverting)


def translational_optimization_try():
    random_var = random.randint(0, 3)
    '''
    if variables.total_penalty_distance > variables.total_penalty_accel and variables.total_penalty_distance > variables.total_penalty_min_speed and variables.total_distance > variables.total_penalty_smoothness or random_var == 3:
        lower_point = random.randint(0, len(constants_and_points.control_points))
        print("too much distance detected, choosing this point randomly: " + str(lower_point))
    elif variables.detected_collision:
        lower_point = math.floor(variables.t_at_last_collision)
        print("collision detected, t: " + str(variables.t_at_last_collision))
    elif variables.total_penalty_smoothness > variables.total_penalty_accel and variables.total_penalty_smoothness > variables.total_penalty_min_speed:
        lower_point = math.floor(variables.t_at_worst_smoothness)
    elif variables.total_penalty_accel > variables.total_penalty_smoothness and variables.total_penalty_accel > variables.total_penalty_min_speed:
        lower_point = math.floor(variables.t_at_last_max_accel)
    else:
        lower_point = math.floor(variables.t_at_least_velocity)
    '''

    if random_var == 3:
        lower_point = random.randint(0, len(constants_and_points.control_points))
        #print("choosing this point randomly: " + str(lower_point))
    else:
        lower_point = math.floor(variables.t_at_last_max_accel)

    point_chosen = lower_point + random.randint(0, 1)

    if (len(constants_and_points.control_points) - 2) < point_chosen:
            point_chosen = len(constants_and_points.control_points) - 2
    if point_chosen < 1:
        point_chosen = 1

    print("transopt point chosen: " + str(point_chosen))


    target_t = point_chosen + (random.randint(-100, 100) / 1000)

    previous_position_x = constants_and_points.control_points[point_chosen][0][0]
    previous_position_y = constants_and_points.control_points[point_chosen][0][1]
    previous_velocity_x = constants_and_points.control_points[point_chosen][1][0]
    previous_velocity_y = constants_and_points.control_points[point_chosen][1][1]
    previous_acceleration_x = constants_and_points.control_points[point_chosen][2][0]
    previous_acceleration_y = constants_and_points.control_points[point_chosen][2][1]

    spline_pos = spline.compute_spline_point(target_t, constants_and_points.control_points)
    spline_speed = derivations.get_derivation(target_t)
    spline_accel = derivations.get_second_derivation(target_t)
    position_x = spline_pos[0]
    position_y = spline_pos[1]
    velocity_x = spline_speed[0]
    velocity_y = spline_speed[1]
    acceleration_x = spline_accel[0]
    acceleration_y = spline_accel[1]

    constants_and_points.control_points[point_chosen][0][0] = position_x
    constants_and_points.control_points[point_chosen][0][1] = position_y
    constants_and_points.control_points[point_chosen][1][0] = velocity_x
    constants_and_points.control_points[point_chosen][1][1] = -velocity_y
    constants_and_points.control_points[point_chosen][2][0] = acceleration_x
    constants_and_points.control_points[point_chosen][2][1] = -acceleration_y

    data_for_reverting = (point_chosen, previous_position_x, previous_position_y, previous_velocity_x, previous_velocity_y, previous_acceleration_x, previous_acceleration_y)

    return data_for_reverting

def revert_optimization_try(optimization_result):
    point_chosen = optimization_result[0]

    constants_and_points.control_points[point_chosen][0][0] = optimization_result[1]
    constants_and_points.control_points[point_chosen][0][1] = optimization_result[2]
    constants_and_points.control_points[point_chosen][1][0] = optimization_result[3]
    constants_and_points.control_points[point_chosen][1][1] = optimization_result[4]
    constants_and_points.control_points[point_chosen][2][0] = optimization_result[5]
    constants_and_points.control_points[point_chosen][2][1] = optimization_result[6]

def positional_optimization():
    positional_optimization_try_result = positional_optimization_try()
    
    last_run = evaluate_run()
    #print(f"best run: {variables.best_run_value}    last run: {last_run}")
    #print(f"contents of returned list: {local_list[0]} {local_list[1]} part: {local_list[2]}")

    if (variables.best_run_value > last_run) and (variables.detected_collision == 0):
        variables.best_run_value = last_run
        print("just changed best run value to1: " + str(last_run))
        print("Positional improvement detected; accepted!")
        variables.number_of_improvements_accepted = variables.number_of_improvements_accepted + 1
        variables.repetitions_since_last_accept = 0
    else:
        revert_optimization_try(positional_optimization_try_result)
        variables.repetitions_since_last_accept = variables.repetitions_since_last_accept + 1

def  translation_optimization():

    translational_optimization_result = translational_optimization_try()
    
    last_run = evaluate_run()
    #print(f"best run: {variables.best_run_value}    last run: {last_run}")
    #print(f"contents of returned list: {local_list[0]} {local_list[1]} part: {local_list[2]}")

    if (variables.best_run_value > last_run) and (variables.detected_collision == 0):
        variables.best_run_value = last_run
        print("just changed best run value to2: " + str(last_run))
        print("Translational optimization: Improvement detected; accepted!")
        variables.number_of_improvements_accepted = variables.number_of_improvements_accepted + 1
        variables.repetitions_since_last_accept = 0
    else:
        revert_optimization_try(translational_optimization_result)
        variables.repetitions_since_last_accept = variables.repetitions_since_last_accept + 1

def check_for_exit_cue(stop_and_write_anyways):
    if (variables.stop_and_write == 1 or stop_and_write_anyways == 1):
        print("")
        for i in range(len(constants_and_points.control_points)):
            position = constants_and_points.control_points[i][0]
            speed = constants_and_points.control_points[i][1]
            acceleration = constants_and_points.control_points[i][2]

            #getattr(constants_and_points, f'point_{i}_actual_acceleration')

            print(f"point_{i}_pos = [{position[0]}, {position[1]}]")
            print(f"point_{i}_actual_speed = [{speed[0]}, {speed[1]}]")
            print(f"point_{i}_actual_acceleration = [{acceleration[0]}, {acceleration[1]}]")
            print("")  # Blank line for better readability
        print("")  # Blank line for better readability
        print("total improvements accepted: " + str(variables.number_of_improvements_accepted))
        print("")  # Blank line for better readability
        print("control points added: " + str(len(constants_and_points.control_points) - variables.control_points_at_start))
        print("")  # Blank line for better readability
        pygame.quit
        exit()
    if (variables.stop == 1):
        print("total improvements accepted: " + str(variables.number_of_improvements_accepted))
        print("")  # Blank line for better readability
        print("control points added: " + str(len(constants_and_points.control_points) - variables.control_points_at_start))
        print("")  # Blank line for better readability
        pygame.quit
        exit()

def check_for_weighting_changes_and_point_additions():
    print("reps since last accept: " + str(variables.repetitions_since_last_accept))
    '''
    if variables.repetitions_since_last_accept > 200:
        random1 = random.randint(0, 10000)
        random2 = random.randint(0, 10000)
        random3 = random.randint(0, 10000)
        random4 = random.randint(0, 10000)

        float1 = random1 / 1000
        float2 = random2 / 1000
        float3 = random3 / 1000
        float4 = random4 / 1000

        variables.accel_modifier = float1
        variables.distance_modifier = float2
        variables.smoothness_modifier = float3
        variables.min_speed_modifier = float4

        print("")
        print("evaluation weightings modified!!!")
        print("")

        variables.best_run_value = evaluate_run()
    '''
    #can be useful at the start of an optimization
    '''
    if (variables.repetitions_since_last_accept > 700):
        variables.approximate_collisions_modifier = random.uniform(0, 1.5)
        variables.best_run_value = evaluate_run()
    '''
    '''
    if (variables.repetitions_since_last_accept > 800 and (((variables.control_points_at_start) * 2) > len(constants_and_points.control_points)) and variables.adding_more_points_allowed == 1):
        lower_point = math.floor(variables.t_at_last_max_accel)

        if lower_point < 0:
            lower_point = 0

        if lower_point > (len(constants_and_points.control_points) - 2):
            lower_point = (len(constants_and_points.control_points) - 2)

        upper_point = lower_point + 1

        target_t = lower_point + 0.5

        x = spline.compute_spline_point(target_t, constants_and_points.control_points)[0] + random.randint(-80, 80)
        y = spline.compute_spline_point(target_t, constants_and_points.control_points)[1] + random.randint(-80, 80)
        x1 = derivations.get_derivation(target_t,)[0] / 2  + random.randint(-20, 20)
        y1 = derivations.get_derivation(target_t,)[1] / 2  + random.randint(-20, 20)
        x2 = derivations.get_second_derivation(target_t)[0] / 4  + random.randint(-30, 30)
        y2 = derivations.get_second_derivation(target_t)[1] / 4  + random.randint(-30, 30)


        previous1 = constants_and_points.control_points[lower_point][1][0]
        previous2 = constants_and_points.control_points[lower_point][1][1]
        previous3 = constants_and_points.control_points[lower_point][2][0]
        previous4 = constants_and_points.control_points[lower_point][2][0]

        previous5 = constants_and_points.control_points[upper_point][1][0]
        previous6 = constants_and_points.control_points[upper_point][1][1]
        previous7 = constants_and_points.control_points[upper_point][2][0]
        previous8 = constants_and_points.control_points[upper_point][2][1]

        constants_and_points.control_points[lower_point][1][0] = constants_and_points.control_points[lower_point][1][0] / 1.5
        constants_and_points.control_points[lower_point][1][1] = constants_and_points.control_points[lower_point][1][1] / 1.5
        constants_and_points.control_points[lower_point][2][0] = constants_and_points.control_points[lower_point][2][0] / 2
        constants_and_points.control_points[lower_point][2][1] = constants_and_points.control_points[lower_point][2][1] / 2

        constants_and_points.control_points[upper_point][1][0] = constants_and_points.control_points[upper_point][1][0] / 1.5
        constants_and_points.control_points[upper_point][1][1] = constants_and_points.control_points[upper_point][1][1] / 1.5
        constants_and_points.control_points[upper_point][2][0] = constants_and_points.control_points[upper_point][2][0] / 2
        constants_and_points.control_points[upper_point][2][1] = constants_and_points.control_points[upper_point][2][1] / 2


        point_pos = [x, y]
        point_actual_speed = [x1, y1]
        point_actual_acceleration = [x2, y2]
        new_control_point = [point_pos, point_actual_speed, point_actual_acceleration]
        # add handling for finalization! it crashes when more points are added, cely vyhodit a zacit s vic bodama/??
        constants_and_points.control_points.insert(lower_point + 1, new_control_point)

        #variables.adding_more_points_allowed = 0

        for i in range(len(constants_and_points.control_points)):
            position = constants_and_points.control_points[i][0]
            speed = constants_and_points.control_points[i][1]
            acceleration = constants_and_points.control_points[i][2]

            #getattr(constants_and_points, f'point_{i}_actual_acceleration')

            print(f"point_{i}_pos = [{position[0]}, {position[1]}]")
            print(f"point_{i}_actual_speed = [{speed[0]}, {speed[1]}]")
            print(f"point_{i}_actual_acceleration = [{acceleration[0]}, {acceleration[1]}]")
            print("")  # Blank line for better readability


        result = evaluate_run()

        #print("result: " + str(result))
        #print("bestrun + 3: " + str(variables.best_run_value + 0.5))
        #print("best run: " + str(variables.best_run_value))

        if (result > variables.best_run_value) or (variables.detected_collision == 1): #deleno pocet segmentu??
            constants_and_points.control_points.pop(lower_point + 1)

            constants_and_points.control_points[lower_point][1][0] = previous1
            constants_and_points.control_points[lower_point][1][1] = previous2
            constants_and_points.control_points[lower_point][2][0] = previous3
            constants_and_points.control_points[lower_point][2][1] = previous4

            constants_and_points.control_points[upper_point][1][0] = previous5
            constants_and_points.control_points[upper_point][1][1] = previous6
            constants_and_points.control_points[upper_point][2][0] = previous7
            constants_and_points.control_points[upper_point][2][1] = previous8
            print("removed attempted point addition")
        else:
            print("added new point")
            new_best = evaluate_run()
            variables.best_run_value = new_best
            print("just changed best run value to3: " + str(new_best))
        #variables.adding_more_points_allowed = 0
        #variables.repetitions_since_last_accept = 0
    '''
    if variables.repetitions_since_last_accept > 10000:
        print("found optimal solution ig???; very improbable (chime supposed to be played)")
        variables.victory_tune.play(1, 3, 0)
        check_for_exit_cue(1)



def optimization():
    space_points()

    variables.control_points_at_start = len(constants_and_points.control_points)
    variables.repetitions_since_last_accept = 0
    variables.number_of_improvements_accepted = 0

    variables.best_run_value = evaluate_run()
    if variables.best_run_value > 1000:
        variables.best_run_value = 999
    print("best_run_value init as: ", variables.best_run_value)

    for k in range(200):
        translation_optimization()
        positional_optimization()
        check_for_exit_cue(0)
        check_for_weighting_changes_and_point_additions()

    for i in range(100000):
        #variables.best_run_value = evaluate_run()
        for j in range(10):
            positional_optimization() #change
            if i % 10 == 0 and (j == 0):
                variables.show_trajectory_flag = 1
            else:
                variables.show_trajectory_flag = 0 #change
        translation_optimization() #change
        check_for_exit_cue(0)

        check_for_weighting_changes_and_point_additions()

        print("progress done: " + str(i))
        variables.progress_done = i
    variables.show_trajectory_flag = 1
    variables.showmode_on = 1

    run_main(1)

    for i in range(len(constants_and_points.control_points)):
        position = constants_and_points.control_points[i][0]
        speed = constants_and_points.control_points[i][1]
        acceleration = constants_and_points.control_points[i][2]
        
        print(f"point_{i}_pos = [{position[0]}, {position[1]}]")
        print(f"point_{i}_actual_speed = [{speed[0]}, {speed[1]}]")
        print(f"point_{i}_actual_acceleration = [{acceleration[0]}, {acceleration[1]}]")
        print("")  # Blank line for better readability

def double_control_points():

    for j in range(len(constants_and_points.control_points) - 1):
        x1 = constants_and_points.control_points[j * 2][0][0]
        y1 = constants_and_points.control_points[j * 2][0][1]
        x2 = constants_and_points.control_points[j * 2 + 1][0][0]
        y2 = constants_and_points.control_points[j * 2 + 1][0][1]
        x_avg = (x1 + x2)/2
        y_avg = (y1 + y2)/2
        new_point_pos = [x_avg, y_avg]
        new_point_accel = [0,0]
        new_point_speed = [0,0]
        new_point = [new_point_pos, new_point_accel, new_point_speed]
        constants_and_points.control_points.insert(j * 2 + 1, new_point)

def mid_optimization_point_elimination():
    double_control_points()
    double_control_points()
    optimization()
    print("got here")
    for i in range(math.floor(3/4 * len(constants_and_points.control_points))):
        variables.smallest_accel = 9999
        run_main(6)
        print("t at smallest accel: " + str(variables.t_at_smallest_accel))
        print("the smallest accel: " + str(variables.smallest_accel))
        del constants_and_points.control_points[math.floor(variables.t_at_smallest_accel) + random.randint(0, 1)]

    for i in range(len(constants_and_points.control_points)):
        position = constants_and_points.control_points[i][0]
        speed = constants_and_points.control_points[i][1]
        acceleration = constants_and_points.control_points[i][2]

        #getattr(constants_and_points, f'point_{i}_actual_acceleration')

        print(f"point_{i}_pos = [{position[0]}, {position[1]}]")
        print(f"point_{i}_actual_speed = [{speed[0]}, {speed[1]}]")
        print(f"point_{i}_actual_acceleration = [{acceleration[0]}, {acceleration[1]}]")
        print("")  # Blank line for better readability



def run_main(int):
    car_sufrace.set_alpha(200)
    variables.current_acceleration_squared_for_total = 0
    variables.max_accel_delta_recorded = 0
    variables.t_at_worst_smoothness = 0
    variables.total_accel_delta_for_smoothness_eval = 0
    variables.t_at_last_max_accel = 0
    variables.t_at_last_collision = 0
    variables.max_accel_multiple = 0
    variables.detected_collision = 0
    variables.rotation_angles = []
    variables.total_penalty_accel = 0
    variables.total_penalty_smoothness = 0
    variables.approximate_collision_detected = 0
    variables.t_at_least_velocity = 0
    variables.smallest_velocity_measured = 1000
    variables.total_distance = 0
    variables.total_penalty_distance = 0
    reset_ticks()
    variables.t = 0
    constants_and_points.num_points = len(constants_and_points.control_points)
    if variables.show_trajectory_flag == 1:
        clean_screen()

    draw_points()
    draw_track()
    variables.showmode_on = 1
    if int == 1:
        
        variables.t = 0
        while (variables.t + 0.006   < (constants_and_points.num_points - 1)):
            variables.showmode_on = 1
            variables.t = variables.t + 0.01 #0.002
            drawing_displaying_updating()
        time.sleep(3)

    if int == 2: #show
        variables.t = 0
        while (variables.t + 0.2 < (constants_and_points.num_points - 1)):
            variables.t = variables.t + ((math.pi / 70))
            drawing_displaying_updating()
        #time.sleep(5)

    if int == 3: #optimize
        variables.showmode_on = 0
        variables.t = 0
        while (variables.t + 0.2 < (constants_and_points.num_points - 1)):
            variables.t = variables.t + ((math.pi / 10)) #math.pi / 70 for short track
            drawing_displaying_updating()

    if int == 4:
        while (((read_ticks())/20000) + 0.0001 < (constants_and_points.num_points - 1)):
            variables.showmode_on = 1
            variables.t = (read_ticks()) / 1000
            variables.show_trajectory_flag = 1
            #clean_screen()
            drawing_displaying_updating_with_resets()
            clock.tick(165)

    if int == 5:
        variables.t = 0
        while (variables.t + 0.2 < (constants_and_points.num_points - 1)):
            variables.showmode_on = 1
            variables.show_trajectory_flag = 1
            #clean_screen()
            variables.t = variables.t + ((math.pi / 1500))
            drawing_displaying_updating_with_resets()
    
    if int == 6: #for point elimination
        variables.showmode_on = 0
        variables.t = 0.5
        while (variables.t + 0.2 < (constants_and_points.num_points - 1)):
            variables.showmode_on = 0
            variables.show_trajectory_flag = 0
            variables.t = variables.t + (1) #math.pi / 70 for short track
            drawing_displaying_updating_for_elimination()


cProfile.run('optimization()')

#evaluate_run()
#run_main(4)

#run_main(5)

#run_main(1)
#run_main(2)

#double_control_points()

#mid_optimization_point_elimination()