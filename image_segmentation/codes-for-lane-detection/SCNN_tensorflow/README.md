# SCNN-Tensorflow

## Input

![Input](00000.jpg)

Ailia input shape : (1, 288, 800, 3)

Range : [0., 255.]

## Output

![Output](output.jpg)

Ailia output shape : [(1, 288, 800, 5), (1,4)] 
 
Range : [0., 1.0]

## Usage
Automatically downloads the onnx and prototxt files on the first run.
It is necessary to be connected to the Internet while downloading.

For the sample image,
``` bash
$ python3 SCNN.py
```

If you want to specify the input image, put the image path after the `--input` option.  
You can use `--savepath` option to change the name of the output file to save.
```bash
$ python3 SCNN.py --input IMAGE_PATH --savepath SAVE_IMAGE_PATH
```

By adding the `--video` option, you can input the video.   
If you pass `0` as an argument to VIDEO_PATH, you can use the webcam input instead of the video file.

```bash
$ python3 SCNN.py --video VIDEO_PATH
```

The default setting is to use the optimized model and weights, but you can also switch to the normal model by using the `--normal` option.

## Reference

[Codes-for-Lane-Detection](https://github.com/cardwing/Codes-for-Lane-Detection/)

[Spatial As Deep: Spatial CNN for Traffic Scene Understanding](https://github.com/cardwing/Codes-for-Lane-Detection/tree/master/SCNN-Tensorflow)

## Framework

Tensorflow 1.13.2

## Model Format

ONNX opset = 11

## Netron

[SCNN.onnx.prototxt](https://storage.googleapis.com/ailia-models/codes-for-lane-detection/SCNN_tensorflow.onnx.prototxt)

[SCNN.opt.onnx.prototxt](https://storage.googleapis.com/ailia-models/codes-for-lane-detection/SCNN_tensorflow.opt.onnx.prototxt)