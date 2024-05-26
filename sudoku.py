from PIL import Image, ImageDraw
import cv2 as cv
import numpy as np

# Sudoku resmini yükle
sudoku_image = Image.open("sudoku_image.jpg")
draw = ImageDraw.Draw(sudoku_image)
zero_count = 0
box_size = sudoku_image.width // 9
detected_circles = None
box_images = [[0 for _ in range(9)] for _ in range(9)]
box_dot_counts = [[0 for _ in range(9)] for _ in range(9)]
for i in range(9):
    for j in range(9):
        x1 = j * box_size
        y1 = i * box_size
        x2 = x1 + box_size
        y2 = y1 + box_size
        draw.rectangle([(x1, y1), (x2, y2)], outline ="red")

        # Kutunun içindeki siyah yuvarlakları say
        box_image = sudoku_image.crop((x1, y1, x2, y2))
        box_pixels = box_image.load()
        box = np.array(box_image)
        box_images[i][j] = box
        gray = cv.cvtColor(box_images[i][j], cv.COLOR_BGR2GRAY) 
        gray_blurred = cv.blur(gray, (3, 3)) 
        detected_circles = cv.HoughCircles(gray_blurred,  
                   cv.HOUGH_GRADIENT, 1, 20, param1 = 50, 
               param2 = 30, minRadius = 1, maxRadius = 40)
        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))
            box_dot_counts[i][j] = len(detected_circles[0, :])

for row in box_dot_counts:
    for column in row:
        if column == 0:
            zero_count += 1
            
print(box_dot_counts)
print(zero_count)
print("Total Finished : %"+str(round((zero_count/81)*100)))
sudoku_image.save("sudoku_image_boxes.jpg")