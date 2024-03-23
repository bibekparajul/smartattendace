# import dlib
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt


# face_detector = dlib.get_frontal_face_detector()
# landmark_detector = dlib.shape_predictor("data/data_dlib/shape_predictor_68_face_landmarks.dat")

# img_path = "D:\smart-attendance-project\pythonProject\data\data_faces_from_camera\person_8_Bibek_parajulibbek11@gmail.com\img_face_1.jpg"
 
# #read with dlib
# img = dlib.load_rgb_image(img_path)

# faces = face_detector(img, 1)

# landmark_tuple = []
# for k, d in enumerate(faces):
#    landmarks = landmark_detector(img, d)
#    for n in range(0, 27):
#       x = landmarks.part(n).x
#       y = landmarks.part(n).y
#       landmark_tuple.append((x, y))
#       cv2.circle(img, (x, y), 2, (255, 255, 0), -1)

# routes = []
 
# for i in range(15, -1, -1):
#    from_coordinate = landmark_tuple[i+1]
#    to_coordinate = landmark_tuple[i]
#    routes.append(from_coordinate)
 
# from_coordinate = landmark_tuple[0]
# to_coordinate = landmark_tuple[17]
# routes.append(from_coordinate)
 
# for i in range(17, 20):
#    from_coordinate = landmark_tuple[i]
#    to_coordinate = landmark_tuple[i+1]
#    routes.append(from_coordinate)
 
# from_coordinate = landmark_tuple[19]
# to_coordinate = landmark_tuple[24]
# routes.append(from_coordinate)
 
# for i in range(24, 26):
#    from_coordinate = landmark_tuple[i]
#    to_coordinate = landmark_tuple[i+1]
#    routes.append(from_coordinate)
 
# from_coordinate = landmark_tuple[26]
# to_coordinate = landmark_tuple[16]
# routes.append(from_coordinate)
# routes.append(to_coordinate)


# for i in range(0, len(routes)-1):
#    from_coordinate = routes[i]
#    to_coordinate = routes[i+1]
#    img = cv2.line(img, from_coordinate, to_coordinate, (255, 255, 0), 1)

# # mask = np.zeros((img.shape[0], img.shape[1]))
# # mask = cv2.fillConvexPoly(mask, np.array(routes), 1)
 
# # out = np.zeros_like(img)
# # out[mask] = img[mask]
# print(img.shape)
# plt.imshow(img)
# plt.show()




import dlib
import cv2
import numpy as np
import matplotlib.pyplot as plt


face_detector = dlib.get_frontal_face_detector()
landmark_detector = dlib.shape_predictor("data/data_dlib/shape_predictor_68_face_landmarks.dat")

img_path = "D:\smart-attendance-project\pythonProject\data\data_faces_from_camera\person_8_Bibek_parajulibbek11@gmail.com\img_face_1.jpg"
 
#read with dlib
img = dlib.load_rgb_image(img_path)

faces = face_detector(img, 1)

landmark_tuple = []
for k, d in enumerate(faces):
   landmarks = landmark_detector(img, d)
   for n in range(0, 67):
      x = landmarks.part(n).x
      y = landmarks.part(n).y
      landmark_tuple.append((x, y))
      cv2.circle(img, (x, y), 2, (255, 255, 0), -1)

# Uncomment the following lines if you want to draw routes
# routes = []
# for i in range(15, -1, -1):
#    from_coordinate = landmark_tuple[i+1]
#    to_coordinate = landmark_tuple[i]
#    routes.append(from_coordinate)
# for i in range(17, 20):
#    from_coordinate = landmark_tuple[i]
#    to_coordinate = landmark_tuple[i+1]
#    routes.append(from_coordinate)
# for i in range(24, 26):
#    from_coordinate = landmark_tuple[i]
#    to_coordinate = landmark_tuple[i+1]
#    routes.append(from_coordinate)
# from_coordinate = landmark_tuple[26]
# to_coordinate = landmark_tuple[16]
# routes.append(from_coordinate)
# routes.append(to_coordinate)
# for i in range(0, len(routes)-1):
#    from_coordinate = routes[i]
#    to_coordinate = routes[i+1]
#    img = cv2.line(img, from_coordinate, to_coordinate, (255, 255, 0), 1)

print(img.shape)
plt.imshow(img)
plt.show()
