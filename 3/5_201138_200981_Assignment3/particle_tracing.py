import vtk
import numpy as np


class VectorFieldInterpolator:
    """
    Interpolates the vector field at a given position using VTKProbeFilter.
    """

    def __init__(self, vector_field):
        self.vector_field = vector_field

    def interpolate(self, position):
        """
        Interpolates the vector field at a given position.

        Args:
            position (np.ndarray): The 3D position to interpolate at.

        Returns:
            np.ndarray: The interpolated vector at the specified position.

        Raises:
            ValueError: If the position is outside the data bounds.
        """
        point = vtk.vtkPoints()
        point.SetNumberOfPoints(1)
        point.SetPoint(0, position[0], position[1], position[2])

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(point)

        probe_filter = vtk.vtkProbeFilter()
        probe_filter.SetInputData(polydata)
        probe_filter.SetSourceData(self.vector_field)
        probe_filter.Update()

        # Attempt to get the vector at the specified point
        if probe_filter.GetOutput().GetPointData().GetVectors() is not None:
            return probe_filter.GetOutput().GetPointData().GetVectors().GetTuple3(0)
        else:
            raise ValueError(
                "The specified position is outside the data bounds.")


class RK4Integrator:
    """
    Performs RK4 integration using a vector field.
    """

    def __init__(self, vector_field):
        self.vector_field = vector_field

    def step(self, x, y, z, step_size):
        """
        Perform a single RK4 step using the vector field at position (x, y, z).

        Args:
            x (float): X coordinate of the starting position.
            y (float): Y coordinate of the starting position.
            z (float): Z coordinate of the starting position.
            step_size (float): The step size for integration.

        Returns:
            Tuple[float, float, float]: The new position after RK4 integration.
        """
        def get_vector(xi, yi, zi):
            interpolator = VectorFieldInterpolator(self.vector_field)
            vector = interpolator.interpolate(np.array([xi, yi, zi]))
            # Return a zero vector if out of bounds
            return np.array(vector) if vector is not None else np.array([0, 0, 0])

        k1 = get_vector(x, y, z)
        k2 = get_vector(x + 0.5 * step_size *
                        k1[0], y + 0.5 * step_size * k1[1], z + 0.5 * step_size * k1[2])
        k3 = get_vector(x + 0.5 * step_size *
                        k2[0], y + 0.5 * step_size * k2[1], z + 0.5 * step_size * k2[2])
        k4 = get_vector(x + step_size * k3[0], y +
                        step_size * k3[1], z + step_size * k3[2])

        delta = (k1 + 2 * k2 + 2 * k3 + k4) / 6
        return x + step_size * delta[0], y + step_size * delta[1], z + step_size * delta[2]


class StreamlineGenerator:
    """
    Generates a streamline using RK4 integration.
    """

    def __init__(self, vector_field):
        self.vector_field = vector_field

    def generate(self, seed, step_size, max_steps):
        """
        Generate a streamline using RK4 integration.

        Args:
            seed (Tuple[float, float, float]): The starting seed point.
            step_size (float): The step size for integration.
            max_steps (int): The maximum number of integration steps.

        Returns:
            List[Tuple[float, float, float]]: List of points comprising the streamline.
        """
        integrator = RK4Integrator(self.vector_field)
        x, y, z = seed
        streamline_points = [seed]

        # Forward integration
        for _ in range(max_steps):
            x, y, z = integrator.step(x, y, z, step_size)
            streamline_points.append((x, y, z))

        # Backward integration
        x, y, z = seed
        for _ in range(max_steps):
            x, y, z = integrator.step(x, y, z, -step_size)
            streamline_points.insert(0, (x, y, z))

        return streamline_points


class StreamlineWriter:
    """
    Writes a streamline to a VTKPolyData file.
    """

    def write(self, streamline_points, filename):
        """
        Write the streamline to a VTKPolyData file.

        Args:
            streamline_points (List[Tuple[float, float, float]]): List of points comprising the streamline.
            filename (str): The output filename.
        """
        points = vtk.vtkPoints()
        lines = vtk.vtkCellArray()

        for i, point in enumerate(streamline_points):
            points.InsertPoint(i, point)
        for i in range(len(streamline_points) - 1):
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, i)
            line.GetPointIds().SetId(1, i + 1)
            lines.InsertNextCell(line)

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)
        polydata.SetLines(lines)

        writer = vtk.vtkXMLPolyDataWriter()
        writer.SetFileName(filename)
        writer.SetInputData(polydata)
        writer.Write()


def main():
    # Load vector field data
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName("tornado3d_vector.vti")
    reader.Update()
    vector_field = reader.GetOutput()

    # Get the seed location from the user
    seed_x = float(input("Seed X coordinate: "))
    seed_y = float(input("Seed Y coordinate: "))
    seed_z = float(input("Seed Z coordinate: "))
    seed = (seed_x, seed_y, seed_z)

    # Define parameters
    step_size = 0.05
    max_steps = 1000

    # Generate streamline
    generator = StreamlineGenerator(vector_field)
    streamline_points = generator.generate(seed, step_size, max_steps)

    # Write the streamline to a VTKPolyData file
    writer = StreamlineWriter()
    writer.write(streamline_points, "tornado.vtp")


if __name__ == "__main__":
    main()
