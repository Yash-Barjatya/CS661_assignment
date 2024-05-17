# Import the required modules
from vtk import *


def get_user_isovalue():
    """
    Prompt the user for an isovalue within the range of (-1438, 630).
    Returns:
        float: User-entered isovalue.
    """
    while True:
        user_isoval = float(
            input("Enter any Isovalue (between -1438 and 630): "))
        if -1438 <= user_isoval <= 630:
            return user_isoval
        else:
            print("Invalid input. Please enter an isovalue within the range.")


def create_reader(file_name):
    """
    Create and configure the reader for the data.
    Args:
        file_name (str): Name of the file to read.
    Returns:
        vtkXMLImageDataReader: Configured reader object.
    """
    data_reader = vtkXMLImageDataReader()
    data_reader.SetFileName(file_name)
    data_reader.Update()
    return data_reader.GetOutput()


def add_polyline_segment(contour_lines, contour_points, intersection_points):
    """
    Add polyline segment to contour lines and corresponding points to contour points.
    Args:
        contour_lines (vtkCellArray): Cell array for polyline segments.
        contour_points (vtkPoints): Points array for contour points.
        intersection_points (list): List of intersection points.
    """
    num_points_before = contour_points.GetNumberOfPoints()
    for point in intersection_points:
        contour_points.InsertNextPoint(point)
    num_points_after = contour_points.GetNumberOfPoints()

    polyline = vtkPolyLine()
    polyline.GetPointIds().SetNumberOfIds(len(intersection_points))
    for i in range(len(intersection_points)):
        polyline.GetPointIds().SetId(i, num_points_before + i)
    contour_lines.InsertNextCell(polyline)


def extract_isocontour(data_object, user_isoval):
    """
    Extract isocontour from the input data.
    Args:
        data_object (vtkImageData): Input data object.
        user_isoval (float): User-specified isovalue.
    Returns:
        vtkPolyData: Polydata containing isocontour.
    """
    # Get the pressure array
    pressure_array = data_object.GetPointData().GetArray('Pressure')
    num_cells = data_object.GetNumberOfCells()
    contour_lines = vtkCellArray()
    contour_points = vtkPoints()

    # Loop through each cell in the data
    for i in range(num_cells):
        cell = data_object.GetCell(i)
        point_ids = [cell.GetPointId(0), cell.GetPointId(
            1), cell.GetPointId(3), cell.GetPointId(2)]
        point_values = [pressure_array.GetTuple1(pid) for pid in point_ids]
        point_coordinates = [data_object.GetPoint(pid) for pid in point_ids]

        # Check if the cell is completely inside or outside the isosurface
        if all(val < user_isoval for val in point_values) or all(val > user_isoval for val in point_values):
            # Skip the cell if it's completely outside or inside the isosurface
            continue
        else:
            # Initialize intersection count and list to store intersection points
            intersection_count = 0
            intersection_points = []

            # Check for intersections between cell edges and isosurface
            for j in range(4):
                next_j = (j + 1) % 4
                if (point_values[j] <= user_isoval and point_values[next_j] > user_isoval) or \
                        (point_values[j] >= user_isoval and point_values[next_j] < user_isoval):
                    px = ((point_values[j] - user_isoval) / (point_values[j] - point_values[next_j])) * \
                        (point_coordinates[next_j][0] -
                         point_coordinates[j][0]) + point_coordinates[j][0]
                    py = ((point_values[j] - user_isoval) / (point_values[j] - point_values[next_j])) * \
                        (point_coordinates[next_j][1] -
                         point_coordinates[j][1]) + point_coordinates[j][1]
                    pz = 25  # Constant z-coordinate assumption
                    intersection_point = (px, py, pz)
                    intersection_points.append(intersection_point)
                    intersection_count += 1

            # Create polyline segments for each intersection case
            if intersection_count == 2:
                add_polyline_segment(
                    contour_lines, contour_points, intersection_points[:2])
            elif intersection_count == 4:
                add_polyline_segment(
                    contour_lines, contour_points, intersection_points[0:2])
                add_polyline_segment(
                    contour_lines, contour_points, intersection_points[2:])

    poly_data = vtkPolyData()
    poly_data.SetPoints(contour_points)
    poly_data.SetLines(contour_lines)

    return poly_data


def write_isocontour_to_file(poly_data, output_file):
    """
    Write the isocontour data to a VTP file.
    Args:
        poly_data (vtkPolyData): Polydata containing isocontour.
        output_file (str): Output file name.
    """
    output_writer = vtkXMLPolyDataWriter()
    output_writer.SetInputData(poly_data)
    output_writer.SetFileName(output_file)
    output_writer.Write()


def main():
    """
    Main function to execute isocontour extraction and writing to file.
    """
    file_name = 'Data/Isabel_2D.vti'
    user_isoval = get_user_isovalue()
    data_object = create_reader(file_name)
    isocontour_polydata = extract_isocontour(data_object, user_isoval)
    write_isocontour_to_file(isocontour_polydata, 'isocontour.vtp')


if __name__ == "__main__":
    main()
