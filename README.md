### A scaled down version of the self-driving system using  OpenCV

The system comprises of -    
• Raspberry Pi with a webcam and an ultrasonic sensor as inputs,
  -Steering using move in sdcar.py        
    ◦ Stop sign detection using houghcircles and colour intensities         
    ◦  Front collision avoidance using an ultrasonic sensor     
•   l298N motor controller                   
•  project structure:              
   *sdcar.py is a combination of all the following               
   *lane_lines.py:                  
     step1.take the webcam feed and apply the  canny  edge                 
     algorithm to detect the edges                 
     step2. detect the lines in an edged image using  houghlines                  
     step3. average the lines according to the slope                 
     step4.making points using slope                  
     step5. return right, left, camera and central line               
   *sensor.py:                 
     distance measurement using input and output pins               
   *sign.py:                  
     *detection of circles in image using hough circles                   
     *if the dominant colour in a square region around the circle is red then it is                    
     stop sign.                  
     *if the dominant colour in a square region around the circle is blue then                           
     there are 5 cases left, right, forward, forward and right or forward                    
     and left for this:     
       • make the 3 zones of square regions the right , left, upper(for forward)    
       • if the right zone is white and the other two are blue then the sum of RGB colour intensities in the right zone will be obviously greater than the other two zones then the sign is right similarly for others.                 
    
       
