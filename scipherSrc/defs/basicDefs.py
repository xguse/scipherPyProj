def slidingWindow(sequence,winSize,step=1):
    # verification code 
    if not type(sequence) == type(''):
        raise Exception("**ERROR** type(sequence) must be str.")
    if not ((type(winSize) == type(0)) and (type(step) == type(0))):
        raise Exception("**ERROR** type(winSize) and type(step) must be int.")
    if step > winSize:
        raise Exception("**ERROR** step must not be larger than winSize.")
    if winSize > len(sequence):
        raise Exception("**ERROR** winSize must not be larger than sequence length.")

    for i in range(0,len(sequence),step):
        chunk = sequence[i:i+winSize]
        if len(chunk) == winSize:
            yield chunk
        else:
            break