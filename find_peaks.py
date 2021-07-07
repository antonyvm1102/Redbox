def find_peaks(times, values, threshold_value = 0.0, t_start = None, t_end = None):

    """
        
        Arguments: 
        
        times: list 
        values: list
        threshold_value: minimum absolute value to be consider as a peak. Default is 0.0
        t_start: time to start considering peaks
        t_end: time to end considering peaks
        
        Return:
        
        timePeaks: list of times at which peaks occur
        local_peaks: list of peaks
        peak: maximum absolute peak value
        
        
    """

    timesPeaks = []
    local_peaks = []
    directionOfMovement = "flat"
    #default values
    input_times = np.array(times)
    input_values = np.array(values)
    if not t_start:
        t_start = input_times[0]
    if not t_end:
        t_end = input_times[-1]
    times = input_times[(input_times >= t_start) & (input_times <= t_end)]
    #print(times)
    values = input_values[(input_times >= t_start) & (input_times <= t_end)]
    #compute peaks
    for i in range(len(times)-1):
        previousDirectionOfMovement = directionOfMovement
        if values[i+1] > values[i]:
            directionOfMovement = "increasing"
        elif values[i+1] < values[i]:
            directionOfMovement = "decreasing"
        else:
            directionOfMovement = previousDirectionOfMovement  #keep holding the same direction
        if directionOfMovement != previousDirectionOfMovement:
            if i > 0 and abs(values[i]) >= threshold_value:
                timesPeaks.append(times[i])
                local_peaks.append(values[i])
    peak = np.max([np.max(local_peaks), -np.min(local_peaks)])
    return timesPeaks, local_peaks, peak