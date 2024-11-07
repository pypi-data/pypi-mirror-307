from matplotlib import pyplot as plt
import numpy as np

def plot_distance_matrix(city_positions:dict, distance_matrix:np.ndarray,best_path:list)->None:
    plt.figure(figsize=(8, 6))
    for i, (x1, y1) in city_positions.items():
        for j, (x2, y2) in city_positions.items():
            if i != j:
                plt.plot([x1, x2], [y1, y2], 'gray', linestyle='--', alpha=0.3)
                plt.text((x1 + x2) / 2, (y1 + y2) / 2, f"{distance_matrix[i][j]:.1f}",
                         ha='center', va='center', fontsize=8, color='blue')

    for city, (x, y) in city_positions.items():
        plt.scatter(x, y, s=100)
        plt.text(x, y, f"City {city}", ha='center', va='center', fontsize=12, color='red')

    path_x = [city_positions[city][0] for city in best_path]
    path_y = [city_positions[city][1] for city in best_path]
    path_x.append(path_x[0])  
    path_y.append(path_y[0])
    plt.plot(path_x, path_y, 'b-', marker='o', markersize=10, linewidth=2)

    plt.title("Distance Matrix Visualization")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.show()