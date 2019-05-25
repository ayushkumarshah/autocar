
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math
#import serial


# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
stop_cascade = cv2.CascadeClassifier('stop_sign.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
traffic_cascade = cv2.CascadeClassifier('traffic_light.xml')

#serial_port = serial.Serial('/dev/ttyACM0', 9600, timeout=1)


def region_of_interest(img, vertices):
    # Define a blank matrix that matches the image height/width.
    mask = np.zeros_like(img)
    # Retrieve the number of color channels of the image.
    #channel_count = img.shape[2]
    channel_count =3;
    #print(channel_count)
    # Create a match color with the same color channel counts.
    match_mask_color = (255,) * channel_count
      
    # Fill inside the polygon
    cv2.fillPoly(mask, vertices, match_mask_color)
    
    # Returning the image only where mask pixels match
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image
def draw_lines(img, lines, color=[255, 0, 0], thickness=3):
    # If there are no lines to draw, exit.
    if lines is None:
        return
    # Make a copy of the original image.
    img = np.copy(img)
    # Create a blank image that matches the original in size.
    line_img = np.zeros(
        (
            img.shape[0],
            img.shape[1],
            3
        ),
        dtype=np.uint8,
    ) 
    # Loop over all lines and draw them on the blank image.
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
    #return line_img
    
    # Merge the image with the lines onto the original.
    img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)
    # Return the modified image.
    return img

def pipeline(image):
    """
    An image processing pipeline which will output
    an image with the lane lines annotated.
    """
    height = image.shape[0]
    width = image.shape[1]
    region_of_interest_vertices = [
        (0, height),
        (float(width / 3), float(height / 3)),
	(2*float(width / 3), float(height / 3)),
	(width, height),
    ]
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    cannyed_image = cv2.Canny(gray_image, 100, 200)
 
    cropped_image = region_of_interest(
        cannyed_image,
        np.array(
            [region_of_interest_vertices],
            np.int32
        ),
    )
    plt.imshow(cropped_image)
    lines = cv2.HoughLinesP(
        cropped_image,
        rho=6,
        theta=np.pi / 180,
        threshold=160,
        lines=np.array([]),
        minLineLength=40,
        maxLineGap=25
    )
    #print(lines)
    left_line_x = []
    left_line_y = []
    right_line_x = []
    right_line_y = []
    left_x_start=[]
    right_x_start=[]
    
    if not lines is None:
        for line in lines:
	    for x1,y1,x2,y2 in line:
		slope = (y2-y1)/float(x2-x1) 
		if math.fabs(slope) < 0.5: 
		    continue
	   	if slope <= 0: 
		    left_line_x.extend([x1, x2])
		    left_line_y.extend([y1, y2])
		else: 
		    right_line_x.extend([x1, x2])
		    right_line_y.extend([y1, y2])

    min_y = int(image.shape[0] * (3 / 5))
    #print(min_y)
    max_y = int(image.shape[0])
    if left_line_x and left_line_y:
	left=np.polyfit(
	left_line_y,
	left_line_x,
	deg=1
	)
	poly_left = np.poly1d(left) 

	y=image.shape[0]-10
	x=float(y-left[1])/left[0]







	#print(x,y)
	#print("poly_left")
	#print(left)
	left_x_start = int(poly_left(max_y))
	#print(left_x_start)
	left_x_end = int(poly_left(min_y))

	   

    if right_line_x and right_line_y:
	poly_right = np.poly1d(np.polyfit(
	right_line_y,
	right_line_x,
	deg=1
	))

	right_x_start = int(poly_right(max_y))
	right_x_end = int(poly_right(min_y))
    if left_line_x and right_line_x and left_line_y and right_line_y:
	line_image = draw_lines(
	image,
	[[
	    [left_x_start, max_y, left_x_end, min_y],
	    [right_x_start, max_y, right_x_end, min_y],
	]],
	thickness=5,
	)
    else:
	line_image = draw_lines(
	image,
	[[
	   
	]],
	thickness=5,
	)
    
    if right_x_start and left_x_start:
	cv2.line(
		line_image,

		    (left_x_start, y-10),( right_x_start, y-10)
		,
		(255,0,0),5,
	    )


	centre=(right_x_start-left_x_start)/2+left_x_start
	cv2.circle(line_image,(centre,y-10), 5, (0,0,255), -1) 
	distance= centre-left_x_start
	#print(distance) 
	#if distance<220:
	    #print("turn")



    return line_image


cap = cv2.VideoCapture(0)


while 1:
    ret, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    line_image=pipeline(image)

    stops = stop_cascade.detectMultiScale(gray, 1.3, 5)
    traffics = traffic_cascade.detectMultiScale(gray, 1.3, 5)

    #data=serial_port.readline()
    if data:
	#print data
	cv2.putText(line_image, data, (400,23), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    #print stops;
    if (stops!=()):
        #serial_port.write(chr(0))
        print("Stop")
    '''else:
	#serial_port.write(chr(1))
        print("Go")
'''

    for (x,y,w,h) in stops:
        #print ("stopppp")
        #print(x,y,x+w,y+h)
       	cv2.rectangle(line_image,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = line_image[y:y+h, x:x+w]

    '''for (x,y,w,h) in traffics:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]''' 
	
    for (x_pos, y_pos, width, height) in traffics:
        cv2.rectangle(line_image, (x_pos, y_pos), (x_pos+width, y_pos+height), (255, 255, 255), 2)
        v = y_pos + height - 5   
	
	gray_image = cv2.cvtColor(line_image, cv2.COLOR_RGB2GRAY)
	roi = gray_image[y_pos+10:y_pos + height-10, x_pos+10:x_pos + width-10]
        mask = cv2.GaussianBlur(roi, (25, 25), 0)
	
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)
                
        threshold = 150
        print(maxVal - minVal)          # check if light is on
        if maxVal - minVal > threshold:
            cv2.circle(roi, maxLoc, 5, (255, 0, 0), 2)
                    
                    # Red light
            if 1.0/8*(height-30) < maxLoc[1] < 4.0/8*(height-30):
                cv2.putText(line_image, 'Red', (x_pos+5, y_pos-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		#serial_port.write(chr(0))
                #self.traffic_cascade.red_light = True
                    
                    # Green light
            elif 5.9/8*(height-30) < maxLoc[1] < height-30:
                cv2.putText(line_image, 'Green', (x_pos+5, y_pos - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                #self.traffic_cascade.green_light = True
		#serial_port.write(chr(0))
    
                    # yellow light
                    #elif 4.0/8*(height-30) < maxLoc[1] < 5.5/8*(height-30):
                    #    cv2.putText(image, 'Yellow', (x_pos+5, y_pos - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                    #    self.yellow_light = True

    #cv2.imshow('mask',roi)
    cv2.imshow('img',line_image)
    k = cv2.waitKey(10) 
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
