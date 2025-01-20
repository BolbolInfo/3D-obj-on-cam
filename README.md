BolbolInfo: create a readme file for this project

Workspace: Collecting workspace information

Still building the workspace index, response may be less accurate.

# 3D Object QR Code Detection and Rendering

This project detects QR codes using a webcam and renders corresponding 3D objects on the video feed. The 3D objects are loaded from `.obj` files and can be manipulated (rotated, scaled, translated) based on user input.

## Project Structure

```
camobj.py
obj/
    AWP.obj
    ball.obj
    cone.obj
    cube.obj
    ELBOLBOLTEXT.obj
    fish.obj
    monkey.obj
    torus.obj
objectONQr.py
```

### Files

- 

camobj.py

: Contains the main logic for loading 3D objects, detecting QR codes, and rendering the objects on the video feed.
- 

objectONQr.py

: Contains additional logic for handling QR code detection and object manipulation.
- 

obj

: Directory containing the `.obj` files for the 3D objects.

## Dependencies

- OpenCV
- NumPy

Install the dependencies using pip:

```sh
pip install opencv-python numpy
```

## Usage

1. Ensure your `.obj` files are placed in the 

obj

 directory.
2. Run the main script:

```sh
python camobj.py
```

### Controls

- `t`: Rotate the selected object around the X-axis (positive direction)
- 

y

: Rotate the selected object around the Y-axis (positive direction)
- `u`: Rotate the selected object around the Z-axis (positive direction)
- `g`: Rotate the selected object around the X-axis (negative direction)
- `a`: Exit the application

## Classes and Functions

### 

Shape3D

 Class

- 

__init__(self, filename: str, face_color: tuple[int, int, int], scale: float = 0.5, translate_x: float = 0, translate_y: float = 0, rotation_x: float = 0, rotation_y: float = 0, rotation_z: float = 0, rotation_speed: float = 0.05, scale_speed: float = 0.05, move_screen_value: float = 0.1)

: Initializes a 3D shape object.
- 

load_obj(self, filename)

: Loads vertices and faces from an `.obj` file.
- 

rotate_x(self, vertices, angle)

: Rotates vertices around the X-axis.
- 

rotate_y(self, vertices, angle)

: Rotates vertices around the Y-axis.
- 

rotate_z(self, vertices, angle)

: Rotates vertices around the Z-axis.
- 

Rotate_around_X_axis_UP(self)

: Rotates the object around the X-axis in the positive direction.
- 

Rotate_around_Y_axis_UP(self)

: Rotates the object around the Y-axis in the positive direction.
- 

Rotate_around_Z_axis_UP(self)

: Rotates the object around the Z-axis in the positive direction.
- 

Rotate_around_X_axis_DOWN(self)

: Rotates the object around the X-axis in the negative direction.

### Functions

- 

average_depth(vertices, face)

: Calculates the average depth of a face.
- 

draw_object_on_frame(frame, vertices, faces, shape_color, line_color, scale=0.5, translate_x=0, translate_y=0)

: Draws the 3D object on the video frame with scaling, translation, and depth sorting.

## License

This project is licensed under the MIT License. See the LICENSE file for details.