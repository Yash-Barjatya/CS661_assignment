INSTRUCTIONS FOR RUNNING THE PYTHON SCRIPT
-----------------------------------

PART 1 : Isocontour Extraction Script 
-----------------------------------

1. Place your 2D scalar data file (in VTI format) in a folder named 'Data' within the same directory as the script.
2. Run the script using Python 3.
3. When prompted, enter the isovalue for which you want to extract the isocontour.
4. The script will write the extracted contour to a file named 'isocontour.vtp'.
5. You can visualize the contour using ParaView by loading the above output file.

Part 2: Volume Rendering Script 
-------------------------------

1. Place your 3D data file (in VTI format) in a folder named 'Data' within the same directory as the script.
2. Run the script using Python 3.
3. When prompted, enter "1" if you want to use Phong shading, or "0" if you don't.
4. The script will render the 3D data and display the result in a new window.

