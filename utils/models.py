def model(type): 
    if type == 'lightning':
        return 'models/movenet_lightning.tflite', 192
    elif type == 'thunder':
        return 'models/movenet_thunder.tflite', 256