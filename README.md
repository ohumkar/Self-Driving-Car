### A scaled down version of the self-driving system using  OpenCV
This was my first ever project developed as a part of Srishti '19 (Technical exhibtion at IIT Roorkee) </br>

The system comprises of -    
- Raspberry Pi with a webcam and an ultrasonic sensor as inputs,
  - Steering using move in sdcar.py        
  - Stop sign detection using houghcircles and colour intensities         
  - Front collision avoidance using an ultrasonic sensor     
- l298N motor controller                   

### Project Structure:              
- sdcar.py is a combination of all the following               
- lane_lines.py:                  
  - step1.take the webcam feed and apply the  canny  edge                 
  algorithm to detect the edges                 
  - step2. detect the lines in an edged image using  houghlines                  
  - step3. average the lines according to the slope                 
  - step4.making points using slope                  
  - step5. return right, left, camera and central line               
- sensor.py: distance measurement using input and output pins               
- sign.py:                  
  - detection of circles in image using hough circles                   
  - if the dominant colour in a square region around the circle is red then it is                    
  stop sign.                  
  - if the dominant colour in a square region around the circle is blue then there are 5 cases left, right, forward, forward and right or forward and left for this:     
    - make the 3 zones of square regions the right , left, upper(for forward)    
    - if the right zone is white and the other two are blue then the sum of RGB colour intensities in the right zone will be obviously greater than the other two zones then the sign is right similarly for others.  

### Challenges faced :
- Given that a deep learning based approach was not used, quite a few heuristics and manual tweaks were performed
- There was quite a noticable lag from the webcam while reading images which resulted in a low framerate
- The resulting low frame rate caused an offset where a new frame was read while the processing was previous frame was still going. This caused a delay in the decisions of the car often causing it to deviate from the track
- We tried to address this problem temporarily by shifting to a move and stop driving, where the car would drive in steps instead of a continous manner
- 
Working Model : https://drive.google.com/drive/u/0/folders/1f9eJIs4ksZifZLUeAl-CM_1WS04smbpB
    
       
