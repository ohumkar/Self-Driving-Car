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
