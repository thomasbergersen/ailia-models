import sys
import time

import matplotlib.pyplot as plt
import cv2

import ailia
from hrnet_utils import save_pred, gen_preds_img, smooth_output

# import original modules
sys.path.append('../../util')
from utils import get_base_parser, update_parser  # noqa: E402
from model_utils import check_and_download_models  # noqa: E402
from image_utils import load_image  # noqa: E402
import webcamera_utils  # noqa: E402


# ======================
# Parameters 1
# ======================
MODEL_NAMES = ['HRNetV2-W48', 'HRNetV2-W18-Small-v1', 'HRNetV2-W18-Small-v2']
IMAGE_PATH = 'test.png'
SAVE_IMAGE_PATH = 'result.png'
IMAGE_HEIGHT = 512
IMAGE_WIDTH = 1024


# ======================
# Arguemnt Parser Config
# ======================
parser = get_base_parser(
    'High-Resolution networks for semantic segmentations.',
    IMAGE_PATH,
    SAVE_IMAGE_PATH,
)
parser.add_argument(
    '-a', '--arch', metavar="ARCH",
    default='HRNetV2-W18-Small-v2',
    choices=MODEL_NAMES,
    help='model architecture:  ' + ' | '.join(MODEL_NAMES) +
         ' (default: HRNetV2-W18-Small-v2)'
)
parser.add_argument(
    '--smooth',  # '-s' has already been reserved for '--savepath'
    action='store_true',
    help='result image will be smoother by applying bilinear upsampling'
)
args = update_parser(parser)


# ======================
# Parameters 2
# ======================
MODEL_NAME = args.arch
WEIGHT_PATH = MODEL_NAME + ".onnx"
MODEL_PATH = WEIGHT_PATH + ".prototxt"
REMOTE_PATH = 'https://storage.googleapis.com/ailia-models/hrnet/'


# ======================
# Main functions
# ======================
def recognize_from_image():
    # prepare input data
    input_data = load_image(
        args.input,
        (IMAGE_HEIGHT, IMAGE_WIDTH),
        gen_input_ailia=True
    )

    # net initialize
    net = ailia.Net(MODEL_PATH, WEIGHT_PATH, env_id=args.env_id)

    # inference
    print('Start inference...')
    if args.benchmark:
        print('BENCHMARK mode')
        for i in range(5):
            start = int(round(time.time() * 1000))
            preds_ailia = net.predict(input_data)
            end = int(round(time.time() * 1000))
            print(f'\tailia processing time {end - start} ms')
    else:
        preds_ailia = net.predict(input_data)

    # postprocessing
    if args.smooth:
        preds_ailia = smooth_output(preds_ailia)

    save_pred(preds_ailia, args.savepath, IMAGE_HEIGHT, IMAGE_WIDTH)
    print('Script finished successfully.')


def recognize_from_video():
    # net initialize
    net = ailia.Net(MODEL_PATH, WEIGHT_PATH, env_id=args.env_id)

    capture = webcamera_utils.get_capture(args.video)

    # create video writer if savepath is specified as video format
    if args.savepath != SAVE_IMAGE_PATH:
        print(
            '[WARNING] currently, video results cannot be output correctly...'
        )
        f_h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        f_w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        writer = webcamera_utils.get_writer(args.savepath, f_h, f_w)
    else:
        writer = None

    while(True):
        ret, frame = capture.read()
        if (cv2.waitKey(1) & 0xFF == ord('q')) or not ret:
            break

        input_image, input_data = webcamera_utils.preprocess_frame(
            frame, IMAGE_HEIGHT, IMAGE_WIDTH,
        )

        # inference
        preds_ailia = net.predict(input_data)

        # postprocessing
        if args.smooth:
            preds_ailia = smooth_output(preds_ailia)
        gen_img = gen_preds_img(preds_ailia, IMAGE_HEIGHT, IMAGE_WIDTH)
        plt.imshow(gen_img)
        plt.pause(.01)
        if not plt.get_fignums():
            break

        # # save results
        # if writer is not None:
        #     writer.write(res_img)

    capture.release()
    cv2.destroyAllWindows()
    if writer is not None:
        writer.release()
    print('Script finished successfully.')


def main():
    # model files check and download
    check_and_download_models(WEIGHT_PATH, MODEL_PATH, REMOTE_PATH)

    if args.video is not None:
        # video mode
        recognize_from_video()
    else:
        # image mode
        recognize_from_image()


if __name__ == '__main__':
    main()