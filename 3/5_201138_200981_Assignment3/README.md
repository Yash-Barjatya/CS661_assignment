# Particle Tracing Program

This program generates streamlines from a 3D vector field dataset using Runge-Kutta 4 (RK4) integration technique. It allows users to specify a seed location and performs RK4 integration in both forward and backward directions to trace streamlines. The output is saved as a VTKPolyData file (*.vtp).

## Instructions

### Prerequisites
- Python 3.6 or higher
- VTK (Visualization Toolkit) library

### Running the Program
1. Place the Python script file (`particle_tracing.py`) and the VTK data file (`tornado3d_vector.vti`) in the same directory.
2. Open a terminal or command prompt.
3. Navigate to the directory where the files are located.
4. Run the Python script with the following command: 'python particle_tracing.py'
5. Enter the X, Y, and Z coordinates for the seed point when prompted.
6. Once the execution is complete, a file named `tornado.vtp` will be generated in the same directory.
