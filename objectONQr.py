import cv2
import numpy as np
import math
import os


#       B    G   R
BLUE = (255 , 0 , 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)

CYAN = (255,255,0)
YELLOW = (0,255,255)
MAGENTA = (255,0,255)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)




AVAILABLE_FILES=os.listdir(os.path.join("obj"))
AVAILABLE_OBJ=[]
for file in AVAILABLE_FILES:
    if ".obj" in file:
        AVAILABLE_OBJ.append(file)





class Shape3D():
    def __init__(self,filename:str,face_color:tuple[int,int,int],scale:float=0.5,translate_x:float=0,translate_y:float=0,rotation_x:float=0,rotation_y:float=0,rotation_z:float=0,rotation_speed:float=0.05,scale_speed:float=0.05,move_screen_value:float=0.1,opacity:float=0):
        self.filename = filename
        self.vertices,self.faces =self.load_obj(filename)
        self.face_color = face_color
        self.scale = scale
        self.translate_x = translate_x #to move on screen x
        self.translate_y = translate_y #to move on screen y
        self.rotation_x = rotation_x #to rotate the object on the axe x
        self.rotation_y = rotation_y #to rotate the object on the axe y
        self.rotation_z = rotation_z #to rotate the object on the axe z
        self.rotation_speed = rotation_speed #the speed of object rotation
        self.scale_speed = scale_speed #the resize scale speed 
        self.move_screen_value = move_screen_value #the amount the object move on the screen
        self.opacity = opacity #object opacity


    def load_obj(self,filename):
        vertices = []
        faces = []

        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('v '):  # Vertex data
                    parts = line.split()
                    vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
                elif line.startswith('f '):  # Face data
                    parts = line.split()
                    face = [int(p.split('/')[0]) - 1 for p in parts[1:]]  # Convert to 0-based index
                    faces.append(face)

        return vertices, faces

    # Function to apply rotation on X axis
    def rotate_x(self,vertices, angle):
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, math.cos(angle), -math.sin(angle)],
            [0, math.sin(angle), math.cos(angle)]
        ])
        
        rotated_vertices = []
        for vertex in vertices:
            rotated_vertex = np.dot(rotation_matrix, vertex)
            rotated_vertices.append(tuple(rotated_vertex))
        
        return rotated_vertices

    # Function to apply rotation on Y axis
    def rotate_y(self,vertices, angle):
        rotation_matrix = np.array([
            [math.cos(angle), 0, math.sin(angle)],
            [0, 1, 0],
            [-math.sin(angle), 0, math.cos(angle)]
        ])
        
        rotated_vertices = []
        for vertex in vertices:
            rotated_vertex = np.dot(rotation_matrix, vertex)
            rotated_vertices.append(tuple(rotated_vertex))
        
        return rotated_vertices

    # Function to apply rotation on Z axis
    def rotate_z(self,vertices, angle):
        rotation_matrix = np.array([
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [0, 0, 1]
        ])
        
        rotated_vertices = []
        for vertex in vertices:
            rotated_vertex = np.dot(rotation_matrix, vertex)
            rotated_vertices.append(tuple(rotated_vertex))
        
        return rotated_vertices


    def Rotate_around_X_axis_UP(self):
        self.rotation_x += self.rotation_speed
        self.vertices = self.rotate_x(self.vertices, self.rotation_speed)
    def Rotate_around_Y_axis_UP(self):
        self.rotation_y += self.rotation_speed
        self.vertices = self.rotate_y(self.vertices, self.rotation_speed)
    def Rotate_around_Z_axis_UP(self):
        self.rotation_z += self.rotation_speed
        self.vertices = self.rotate_z(self.vertices, self.rotation_speed)
    def Rotate_around_X_axis_DOWN(self):
        self.rotation_x += self.rotation_speed
        self.vertices = self.rotate_x(self.vertices, -self.rotation_speed)
    def Rotate_around_Y_axis_DOWN(self):
        self.rotation_y += self.rotation_speed
        self.vertices = self.rotate_y(self.vertices, -self.rotation_speed)
    def Rotate_around_Z_axis_DOWN(self):
        self.rotation_z += self.rotation_speed
        self.vertices = self.rotate_z(self.vertices, -self.rotation_speed)
    
    def Move_UP(self):
        self.translate_y -= self.move_screen_value
    def Move_DOWN(self):
        self.translate_y += self.move_screen_value
    def Move_RIGHT(self):
        self.translate_x += self.move_screen_value
    def Move_LEFT(self):
        self.translate_x -= self.move_screen_value 
    
    def Increase_scale(self):
        self.scale += self.scale_speed  
    def Decrease_scale(self):
        self.scale -= self.scale_speed  



# Function to calculate the average depth of a face
def average_depth(vertices, face):
    depth = 0
    for vertex in face:
        _, _, z = vertices[vertex]  # Get the z-coordinate of the vertex
        depth += z
    return depth / len(face)  # Return the average depth of the face

# Function to draw the 3D object on frame with scaling, translation, and depth sorting
def draw_object_on_frame(frame, vertices, faces,shape_color,line_color, scale=0.5, translate_x=0, translate_y=0):
    height, width, _ = frame.shape
    # Create an overlay to draw the polygons with opacity
    # overlay = frame.copy()
    # opacity = 0  # Opacity level (0.0 to 1.0)
    # Sort faces by their average depth (descending order: farther faces come first)
    faces_sorted = sorted(faces, key=lambda face: average_depth(vertices, face), reverse=True)

    for face in faces_sorted:
        pts = []
        for vertex in face:
            # Get the vertex coordinates
            x, y, z = vertices[vertex]
            
            # Apply scaling
            x *= scale
            y *= scale
            
            # Apply translation
            x += translate_x
            y += translate_y
            
            # Project 3D to 2D (simple orthographic projection for simplicity)
            projected_x = int((x + 1) * width / 2)
            projected_y = int((y + 1) * height / 2)
            pts.append([projected_x, projected_y])

        pts = np.array(pts, dtype=np.int32)
        pts = pts.reshape((-1, 1, 2))
        
        # Fill the faces with a color (e.g., green)
        cv2.fillPoly(frame, [pts], color=shape_color)  # Fill with green
        
        # Draw the outline of the faces (optional)
        cv2.polylines(frame, [pts], isClosed=True, color=line_color, thickness=1)  # Black outline
    # cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)
    return frame


def getShapeIndex(name:str,allshapes:list[Shape3D])->int:
    for i in range(len(allshapes)):
        if allshapes[i].filename.split("/")[1][:-4]==name:
            return i
    return None


def updateShapesList(new:list,allshapes:list[Shape3D],allshapes_name:list):
    remList=[]
    for i in range(len(allshapes)):
        name = allshapes[i].filename.split("/")[1][:-4]
        Found = False
        for newName in new:
            if name==newName:
                Found=True
                break
        if Found==False:
            remList.append(name)
    for remName in remList:
        index=getShapeIndex(remName,allshapes)
        # allshapes.pop(index)
        # allshapes_name.remove(remName)
        allshapes[index].opacity=1#clear the object



# TODO:make the object transperent instead of removing it if the qr code desnt detect it

def main():



    allshapes:list[Shape3D]=[]
    allshapes_name=[]



    cap = cv2.VideoCapture(0) 
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read from the webcam.")
            break

        # data, bbox, _ = qr_detector.detectAndDecode(frame)
        retval, decoded_infoL, pointsL, _ = cv2.QRCodeDetectorAruco().detectAndDecodeMulti(frame)
        updateShapesList(decoded_infoL,allshapes,allshapes_name)
        if retval:

            for data,points in zip(decoded_infoL,pointsL):
                if data in allshapes_name:
                    x_min, y_min = np.min(points[:, 0]), np.min(points[:, 1])
                    x_max, y_max = np.max(points[:, 0]), np.max(points[:, 1])

                    qr_width = x_max - x_min
                    qr_height = y_max - y_min

                    # Set the scale to fit the QR code size
                    scale = min(qr_width, qr_height) / 300  # Assume the object is ~300 units wide in OBJ file
                    translate_x = (x_min + qr_width / 2) / frame.shape[1] * 2 - 1  # Center X in normalized space
                    translate_y = (y_min + qr_height / 2) / frame.shape[0] * 2 - 1  # Center Y in normalized space
                    Shape_index=getShapeIndex(data,allshapes)
                    if Shape_index!=None:
                        allshapes[Shape_index].translate_x = translate_x
                        allshapes[Shape_index].translate_y = translate_y
                        allshapes[Shape_index].opacity = 0 #color object
                        allshapes[Shape_index].scale=scale



                else:
                    if f"{data}.obj" in AVAILABLE_OBJ:

                        # Compute scale and translation based on QR code size
                        x_min, y_min = np.min(points[:, 0]), np.min(points[:, 1])
                        x_max, y_max = np.max(points[:, 0]), np.max(points[:, 1])

                        qr_width = x_max - x_min
                        qr_height = y_max - y_min

                        # Set the scale to fit the QR code size
                        scale = min(qr_width, qr_height) / 300  # Assume the object is ~300 units wide in OBJ file
                        translate_x = (x_min + qr_width / 2) / frame.shape[1] * 2 - 1  # Center X in normalized space
                        translate_y = (y_min + qr_height / 2) / frame.shape[0] * 2 - 1  # Center Y in normalized space




                        shape = Shape3D(f"obj/{data}.obj",MAGENTA,translate_x=translate_x,translate_y=translate_y,scale=scale)

                        allshapes.append(shape)
                        allshapes_name.append(data)
                        index = len(allshapes)-1
                    else:
                        if data!='':
                            print(f"object not found ! {data}")




        if len(allshapes)!=0 and index>len(allshapes)-1:
            index=0
        
        if len(allshapes)!=0:
            i=0
            for shpe3D in allshapes:
                if i== index:
                    pass
                else:
                    if shpe3D.opacity != 1:
                        shape_color = shpe3D.face_color
                        line_color= BLACK
                        frame = draw_object_on_frame(frame, shpe3D.vertices, shpe3D.faces, shape_color,line_color,shpe3D.scale, shpe3D.translate_x, shpe3D.translate_y)
                i+=1
            if allshapes[index].opacity!=1:
                shpe3D=allshapes[index]
                shape_color = shpe3D.face_color
                line_color= WHITE

                frame = draw_object_on_frame(frame, shpe3D.vertices, shpe3D.faces, shape_color,line_color,shpe3D.scale, shpe3D.translate_x, shpe3D.translate_y)
                
            

        cv2.imshow('Camera Feed with 3D Object', frame)

        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('a'):
            break
        
        elif key == ord('t') and 0<=index<len(allshapes):  # Rotate around X-axis +
            allshapes[index].Rotate_around_X_axis_UP()
        elif key == ord('y') and 0<=index<len(allshapes):  # Rotate around Y-axis +
            allshapes[index].Rotate_around_Y_axis_UP()
        elif key == ord('u') and 0<=index<len(allshapes):  # Rotate around Z-axis +
            allshapes[index].Rotate_around_Z_axis_UP()
        
        elif key == ord('g') and 0<=index<len(allshapes):  # Rotate around X-axis -
            allshapes[index].Rotate_around_X_axis_DOWN()
        elif key == ord('h') and 0<=index<len(allshapes):  # Rotate around Y-axis -
            allshapes[index].Rotate_around_Y_axis_DOWN()
            
        elif key == ord('j') and 0<=index<len(allshapes):  # Rotate around Z-axis -
            allshapes[index].Rotate_around_Z_axis_DOWN()
            
        elif key == ord('z') and 0<=index<len(allshapes): 
            # Move up
            allshapes[index].Move_UP()
        elif key == ord('s') and 0<=index<len(allshapes):
            # Move down
            allshapes[index].Move_DOWN()
        elif key == ord('q') and 0<=index<len(allshapes):
            # Move left
            allshapes[index].Move_LEFT()
        elif key == ord('d') and 0<=index<len(allshapes):
            # Move right
            allshapes[index].Move_RIGHT()

        elif key == ord('o') and 0<=index<len(allshapes):  
            # Increase scale
            allshapes[index].Increase_scale()
        elif key == ord('p') and 0<=index<len(allshapes):  
            # Decrease scale
            allshapes[index].Decrease_scale()
        elif key == ord('m') and 0<=index<len(allshapes):# next shape index 
            index+=1
            if index==len(allshapes):
                index = 0
        elif key == ord('l') and 0<=index<len(allshapes):# previus shape index
            index-=1
            if index==-1:
                index = len(allshapes)-1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":    
    main()
