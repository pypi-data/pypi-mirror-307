# dynamicDQNet/core.py
import pandas as pd
import numpy as np
def find_path(MPT_matrix,distance_matrix,roads_matrix,speed_matrix, EVs_mapped,EVs_50,vehicle_index,w1, w2, w3):
    # 初始节点和目标节点


    # 初始化汇总和调度详情表格
    current_node = EVs_mapped[vehicle_index][0]
    destination_node = EVs_mapped[vehicle_index][1]
    remaining_battery = EVs_50[vehicle_index][0]
    time_left = EVs_50[vehicle_index][2]
    path = [current_node]

    while current_node != destination_node:
        candidates = list(range(len(distance_matrix)))
        best_node, best_score = None, float("-inf")
        best_battery, best_time_left = float("inf"), float("inf")

        for next_node in candidates:
            if next_node in path or current_node == next_node:
                continue

            distance = distance_matrix[current_node][next_node]
            speed = speed_matrix[current_node][next_node]
            if distance == 0 or speed == 0:
                continue

            travel_time = distance / speed
            energy_consumption = (EVs_50[vehicle_index][3] / 100) * distance
            energy_charged = MPT_matrix[current_node][next_node] * travel_time if roads_matrix[current_node][next_node] == 1 else 0
            new_battery = min(remaining_battery - energy_consumption + energy_charged, EVs_50[vehicle_index][1])
            new_battery, new_time_left = max(new_battery, 0), time_left - travel_time

            if new_battery <= 0 or new_time_left <= 0:
                continue

            distance_to_destination = distance_matrix[next_node][destination_node]
            estimated_energy_to_destination = (EVs_50[vehicle_index][3] / 100) * distance_to_destination
            speed_to_destination = speed_matrix[next_node][destination_node]
            estimated_time_to_destination = 0 if speed_to_destination == 0 else distance_to_destination / speed_to_destination

            if estimated_time_to_destination > new_time_left:
                continue

            total_time_used = travel_time + estimated_time_to_destination
            score = (w1 * new_battery - w2 * estimated_energy_to_destination - w3 * total_time_used)

            if score > best_score:
                best_score, best_node = score, next_node
                best_battery, best_time_left = new_battery, new_time_left

        if best_node is None:
            path = []
            break
        path.append(best_node)
        current_node, remaining_battery, time_left = best_node, best_battery, best_time_left

    return path, remaining_battery, time_left
