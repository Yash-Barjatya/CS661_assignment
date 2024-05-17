# Import the required modules
from vtk import *


def prompt_user_for_phong_shading():
    """
    Prompt the user for Phong shading preference.
    Returns:
        bool: True if Phong shading is enabled, False otherwise.
    """
    while True:
        use_phong = input("Enable Phong shading (0 for no, 1 for yes)? ")
        if use_phong in ("0", "1"):
            return bool(int(use_phong))
        else:
            print("Invalid input. Please enter 0 or 1.")


def create_reader(file_name):
    """
    Create and configure the reader for the data.
    Args:
        file_name (str): Name of the file to read.
    Returns:
        vtkXMLImageDataReader: Configured reader object.
    """
    reader = vtkXMLImageDataReader()
    reader.SetFileName(file_name)
    reader.Update()
    return reader.GetOutput()


def create_transfer_functions():
    """
    Create color and opacity transfer functions.
    Returns:
        vtkColorTransferFunction: Color transfer function.
        vtkPiecewiseFunction: Opacity transfer function.
    """
    # Color transfer function
    color_function = vtkColorTransferFunction()
    color_function.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)
    color_function.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)
    color_function.AddRGBPoint(-1873.9, 0.0, 0.0, 0.5)
    color_function.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)
    color_function.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)
    color_function.AddRGBPoint(2594.97, 1.0, 1.0, 0.0)

    # Opacity transfer function
    opacity_function = vtkPiecewiseFunction()
    opacity_function.AddPoint(-4931.54, 1.0)
    opacity_function.AddPoint(101.815, 0.002)
    opacity_function.AddPoint(2594.97, 0.0)

    return color_function, opacity_function


def create_volume_property(color_function, opacity_function, phong_shading):
    """
    Create and configure volume property.
    Args:
        color_function (vtkColorTransferFunction): Color transfer function.
        opacity_function (vtkPiecewiseFunction): Opacity transfer function.
        phong_shading (bool): Whether to enable Phong shading.
    Returns:
        vtkVolumeProperty: Volume property object.
    """
    volume_property = vtkVolumeProperty()
    volume_property.SetColor(color_function)
    volume_property.SetScalarOpacity(opacity_function)
    volume_property.SetAmbient(0.5)
    volume_property.SetDiffuse(0.5)
    volume_property.SetSpecular(0.5)
    if phong_shading:
        volume_property.ShadeOn()
    else:
        volume_property.ShadeOff()
    volume_property.SetInterpolationTypeToLinear()
    return volume_property


def create_volume_actor(volume_mapper, volume_property):
    """
    Create volume actor.
    Args:
        volume_mapper (vtkSmartVolumeMapper): Volume mapper object.
        volume_property (vtkVolumeProperty): Volume property object.
    Returns:
        vtkVolume: Volume actor object.
    """
    volume_actor = vtkVolume()
    volume_actor.SetMapper(volume_mapper)
    volume_actor.SetProperty(volume_property)
    return volume_actor


def create_outline_actor(data):
    """
    Create outline actor.
    Args:
        data (vtkImageData): Input data object.
    Returns:
        vtkActor: Outline actor object.
    """
    outline_filter = vtkOutlineFilter()
    outline_filter.SetInputData(data)

    outline_mapper = vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

    outline_property = vtkProperty()
    outline_property.SetColor(0, 0, 0)

    outline_actor = vtkActor()
    outline_actor.SetMapper(outline_mapper)
    outline_actor.SetProperty(outline_property)

    return outline_actor


def setup_renderer(volume_actor, outline_actor):
    """
    Setup renderer, render window, and interactor.
    Args:
        volume_actor (vtkVolume): Volume actor object.
        outline_actor (vtkActor): Outline actor object.
    """
    renderer = vtkRenderer()
    renderer.SetBackground(1, 1, 1)

    render_window = vtkRenderWindow()
    render_window.SetSize(1000, 1000)
    render_window.AddRenderer(renderer)

    render_window_interactor = vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    renderer.AddActor(volume_actor)
    renderer.AddActor(outline_actor)
    renderer.ResetCamera()

    render_window.Render()
    render_window_interactor.Start()


def main():
    """
    Main function to execute the volume rendering.

    """
    file_name = 'Data/Isabel_3D.vti'
    phong_shading = prompt_user_for_phong_shading()
    data = create_reader(file_name)
    color_function, opacity_function = create_transfer_functions()
    volume_property = create_volume_property(
        color_function, opacity_function, phong_shading)
    volume_mapper = vtkSmartVolumeMapper()
    volume_mapper.SetInputData(data)
    volume_actor = create_volume_actor(volume_mapper, volume_property)
    outline_actor = create_outline_actor(data)
    setup_renderer(volume_actor, outline_actor)


if __name__ == "__main__":
    main()
