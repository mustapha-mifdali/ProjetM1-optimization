# data_loader.py
import math
import os

def load_tsplib_data(filepath):
    """
    Reads a standard TSPLIB file and extracts the X, Y coordinates of the cities.
    Assumes the file has a 'NODE_COORD_SECTION' followed by 'id x y'.
    """
    coordinates = []
    
    with open(filepath, 'r') as file:
        lines = file.readlines()
        
        reading_nodes = False
        for line in lines:
            line = line.strip()
            # Start reading coordinates when we hit this line
            if line == "NODE_COORD_SECTION":
                reading_nodes = True
                continue
            # Stop reading when we hit EOF (End Of File)
            if line == "EOF":
                break
                
            if reading_nodes:
                parts = line.split()
                # Ensure the line actually contains an ID, X, and Y
                if len(parts) >= 3:
                    x = float(parts[1])
                    y = float(parts[2])
                    coordinates.append((x, y))
                    
    return coordinates

def calculate_distance_matrix_from_coords(coordinates):
    """
    Creates a 2D matrix where matrix[i][j] is the Euclidean distance 
    between city i and city j, rounded to the nearest integer.
    """
    n = len(coordinates)
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i != j:
                x1, y1 = coordinates[i]
                x2, y2 = coordinates[j]
                
                # Standard Euclidean distance formula
                distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                
                # Round to the nearest integer (standard TSPLIB practice)
                matrix[i][j] = round(distance)
                
    return matrix