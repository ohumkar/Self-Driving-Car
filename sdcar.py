import RPi.GPIO as gpio
import time
#import numpy as np
import cv2
from scipy.stats import itemfreq

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(12, gpio.OUT)
gpio.setup(16, gpio.IN)
gpio.output(7,False)
gpio.output(11,False)
gpio.output(13,False)
gpio.output(15,False)
gpio.output(12,False)



def reverse(tf):
    gpio.output(7,False)
    gpio.output(11,True)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    
     
    
def forward(tf):
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(tf)
  
  
def turn_right(tf):
    gpio.output(11,True)
    gpio.output(7,False)
    gpio.output(13,True)
    gpio.output(15, False)
    time.sleep(tf)
    
    
    
def turn_left(tf):
    time.sleep(0.1)
    gpio.output(11, False)
    gpio.output(7,True)
    gpio.output(13, False)
    gpio.output(15,True)
    time.sleep(tf)
  

def stop(tf):
    gpio.output(7, False)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, False)
    time.sleep(tf)


#making point using slope and intercept of lines
def make_points(image, line):
    slope, intercept = line
    y1 = int(image.shape[0])# bottom of the image
    y2 = int(y1*3/5)         # slightly lower than the middle
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return [[x1, y1, x2, y2]]

#sensor code for distance calculation
def distance(measure='cm'):
    
    gpio.output(12, True)
    time.sleep(0.00001)
    
    gpio.output(12, False)
    while gpio.input(16) == 0 :
        nosig = time.time()
    while gpio.input(16) == 1:
        sig = time.time()
    
    tl = sig - nosig
    
    if measure == 'cm':
        distance = tl / 0.000058
    elif measure == 'in':
        distance = tl / 0.000148
    else:
        print('Improper choice of measurement: in or cm')
        distance = None

    return distance

#taking average of slope and intercept of left and right line
def average_slope_intercept(image, lines):
    left_fit    = []
    right_fit   = []
    if lines is None:
        return None
    for line in lines:
        for x1, y1, x2, y2 in line:
            fit = np.polyfit((x1,x2), (y1,y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0: # y is reversed in image
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
    # add more weight to longer lines
    if left_fit!=[]:#if left fit not empty
        left_fit_average  = np.average(left_fit, axis=0)
        left_line  = make_points(image, left_fit_average)
    else:#if left fit is empty
        left_line=[[1,1,1,1]]
    if right_fit!=[]:  
        right_fit_average = np.average(right_fit, axis=0)
        right_line = make_points(image, right_fit_average)
    else:
        right_line=[[1,1,1,1]]
    
    #taking the average of upper and lower point of left and right line to find middle line     
    middle_line=[[int((left_line[0][0]+right_line[0][0])/2),int((left_line[0][1]+right_line[0][1])/2),int((left_line[0][2]+right_line[0][2])/2),int((left_line[0][3]+right_line[0][3])/2)]]
    #central line of image is camera line
    camera_line=[[int(image.shape[1]/2),0,int(image.shape[1]/2),int(image.shape[0])]]
    averaged_lines = [left_line, right_line,middle_line,camera_line]
    return averaged_lines

#appling canny edge algorithum to find edges in the image
def canny(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)#to reduce the complexity
    kernel = 5
    blur = cv2.GaussianBlur(gray,(kernel, kernel),0)#to reduse noise 
    canny = cv2.Canny(gray, 180, 200)
    return canny

#formation of lines on the the completly black image 
def display_lines(img,lines):
    line_image = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image,(x1,y1+int(img.shape[0]/2)),(x2,y2+int(img.shape[0]/2)),(255,0,0),10) #addition of half of image height is due to masking of image
    return line_image



#sign detection

def obj(success,frame):
    #function to get dominant colour in region
    def get_dominant_color(image, n_colors):
        pixels = np.float32(image).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        flags, labels, centroids = cv2.kmeans(
            pixels, n_colors, None, criteria, 10, flags)
        palette = np.uint8(centroids)
        return palette[np.argmax(itemfreq(labels)[:, -1])]


    clicked = False
    #mouse event intereption
    def onMouse(event, x, y, flags, param):
        global clicked
        if event == cv2.EVENT_LBUTTONUP:
            clicked = True


    cameraCapture = frame 
    cv2.namedWindow('camera')
    cv2.setMouseCallback('camera', onMouse)

    while success and not clicked:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(gray, 37)
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,
                                  1, 50, param1=120, param2=40)

        if not circles is None:
            circles = np.uint16(np.around(circles))
            #find the circle with maximum radius in image
            max_r, max_i = 0, 0
            for i in range(len(circles[:, :, 2][0])):
                if circles[:, :, 2][0][i] > 50 and circles[:, :, 2][0][i] > max_r:
                    max_i = i
                    max_r = circles[:, :, 2][0][i]
            x, y, r = circles[:, :, :][0][max_i]
            if y > r and x > r:
                #formation square region around the circle
                square = frame[y-r:y+r, x-r:x+r]

                dominant_color = get_dominant_color(square, 2)
                if dominant_color[2] > 100:#if dominant colour is red sign is stop
                    return('Stop')
                else: 
                    return('n/a')
    
            for i in circles[0, :]:#making circle on the image
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
        return('n')
    cv2.imshow('camera', frame)
    return('n')

#movement is based on the distance between middle and camera lines top most point
def move(a,b,c):
    t=(a[0][0]-b)*(a[0][0]-c)
    print(t)
    if t<-8000 and t>-26000:
        print("turn right")
        #turn_right(abs(t)/1000000)
        #stop(0.1)
        turn_right(0.05)
        stop(0.3)
    elif t>8000 and t<26000:
        print("turn left")
        #turn_left(abs(t)/1000000)
        #stop(0.1)
        turn_left(0.05)
        stop(0.3)
    elif t>-8000 and t<8000:
        print("keep going")
        if t<3000 or t>-3000:
            forward(0.3)
        else:
            forward(0.15)
        stop(0.25)
    else:
        print('reverse')
        reverse(0.2)
        stop(0.25)
        if t<0:
            turn_right(0.1)
        else:
            turn_left(0.1)
        stop(0.3)
            
    return

# image = cv2.imread('test_image.jpg')
# lane_image = np.copy(image)
# lane_canny = canny(lane_image)
# cropped_canny = region_of_interest(lane_canny)
# lines = cv2.HoughLinesP(cropped_canny, 2, np.pi/180, 100, np.array([]), minLineLength=40,maxLineGap=5)
# averaged_lines = average_slope_intercept(image, lines)
# line_image = display_lines(lane_image, averaged_lines)
# combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 0)

cap = cv2.VideoCapture(0)
i=0
while (cap.isOpened()):
    if i%5==0:
        try:
            try:
                try:
                    ret, frame = cap.read()
                    
                    if obj(ret, frame)=='Stop':
                        print("STOP")
                        stop(0.1)
                
                    #elif distance('cm')<10:
                        #print("ultra stop")
                        #stop(0.1)
                    
                    else:
                        frame1=frame[int(frame.shape[0]/2):int(frame.shape[0]),0:frame.shape[1]]
                        canny_image = canny(frame1)
                        lines = cv2.HoughLinesP(canny_image, 1, np.pi/180, 50, np.array([]), minLineLength=20,maxLineGap=5)
                        averaged_lines = average_slope_intercept(frame1, lines)
                        line_image = display_lines(frame, averaged_lines)
                        combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
                        move(averaged_lines[2],averaged_lines[1][0][0],averaged_lines[3][0][0])
                        cv2.imshow("result", combo_image)
                        if cv2.waitKey(10)& 0xFF == ord('q'):
                            break
                except TypeError:
                    pass
            except IndexError:
                pass
        except OverflowError:
            pass
    if i>100000:
        i=0
    i=i+1
    
stop(0.1)
cap.release()
cv2.destroyAllWindows()
gpio.cleanup()

