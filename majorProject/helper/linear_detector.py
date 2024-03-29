import cv2 as cv
import tensorflow as tf
import numpy as np

DEBUG_LOGS = []
class_names = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "+",
    ".",
    "/",
    "=",
    "*",
    "-",
    "x",
    "y",
    "z",
]


# model = tf.keras.models.load_model("../models/19_class.h5")

lite = tf.lite.Interpreter(model_path='./models/tflite_quant_model.tflite')
input_details = lite.get_input_details()
output_details = lite.get_output_details()
lite.resize_tensor_input(input_details[0]['index'], (1, 100, 100, 3))
lite.resize_tensor_input(output_details[0]['index'], (1, 19))
lite.allocate_tensors()


def get_contour(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    edged = cv.adaptiveThreshold(
        gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 4)
    (contours, _) = cv.findContours(
        edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return contours


def get_char_bb(contours):
    chars_bb = []
    for contour in contours:
        contour = contour.reshape((contour.shape[0], contour.shape[2]))
        left_tc = np.amin(contour, axis=0)
        right_bc = np.amax(contour, axis=0)
        min_x = left_tc[0]
        max_x = right_bc[0]
        min_y = left_tc[1]
        max_y = right_bc[1]
        chars_bb.append([min_x, min_y, max_x, max_y])
    return chars_bb


def remove_equals(chars_bb):
    chars_bb.sort()
    for i, box in enumerate(chars_bb):
        try:
            next_box = chars_bb[i+1]
        except IndexError:
            break

        if abs(box[0] - next_box[0]) <= 30:
            min_x = min(box[0], next_box[0])
            min_y = min(box[1], next_box[1])
            max_x = max(box[2], next_box[2])
            max_y = max(box[3], next_box[3])
            new_box = [min_x, min_y, max_x, max_y]
            chars_bb[i] = new_box
            chars_bb.remove(next_box)
    return chars_bb


def get_cropped_images(image, chars_bb):
    croped_images = []
    copy = image.copy()
    for box in chars_bb:
        x_min = box[0]
        y_min = box[1]
        height = abs(box[0]-box[2])
        width = abs(box[1]-box[3])
        character = copy[y_min:y_min+width, x_min:x_min+height]
        croped_images.append(character)
    return croped_images


def extra_padding(img, padding=50):
    return cv.copyMakeBorder(img, top=padding, bottom=padding, left=padding, right=padding, borderType=cv.BORDER_CONSTANT, value=(255, 255, 255))


def get_padded_images(croped_images):
    padded_images = []
    for img in croped_images:
        padded_img = extra_padding(img)
        padded_images.append(padded_img)
    return padded_images


def get_resized_images(padded_images):
    resized_images = []
    for img in padded_images:
        resized_img = cv.resize(img, (100, 100), interpolation=cv.INTER_LINEAR)
        resized_images.append(resized_img)
    return resized_images


# def get_prediction(images):
#     predictions = []
#     for image in images:
#         image = np.expand_dims(image, axis=0)
#         image = image.astype('float32')/255
#         prediction = model.predict(image)
#         label = class_names[np.argmax(prediction)]
#         confidence = np.max(prediction)*100
#         confidence = str(confidence)[:2]
#         predictions.append((label, confidence))
#     return predictions


def show_prediction_lite(images):
    predictions_lst = []
    for image in images:
        image = np.expand_dims(image, axis=0)
        image = image.astype('float32')/255
        lite.set_tensor(input_details[0]['index'], image)
        lite.invoke()
        prediction = lite.get_tensor(output_details[0]['index'])
        label = class_names[np.argmax(prediction)]
        confidence = np.max(prediction)*100
        confidence = str(confidence)[:2]
        predictions_lst.append((label, confidence))

    return predictions_lst


def buld_lin_eqn(predictions):
    eqn = ""
    for prediction in predictions:
        eqn += prediction[0]
    return eqn


def handle_alpha_channel(image):
    '''
    Input: Image with alpha channel
    Output: Image without alpha channel
    '''
    try:
        alpha = image[:, :, 3]
        alpha = cv.bitwise_not(alpha)
        new_image = cv.merge([alpha, alpha, alpha])
        image = new_image
    except:
        pass
    finally:
        return image


def get_lin_equation(image):
    DEBUG_LOGS = []
    image = cv.imdecode(np.fromstring(
        image.read(), np.uint8), cv.IMREAD_UNCHANGED)
    image = handle_alpha_channel(image)
    contours = get_contour(image)
    chars_bb = get_char_bb(contours)
    chars_bb = remove_equals(chars_bb)
    croped_images = get_cropped_images(image, chars_bb)
    padded_images = get_padded_images(croped_images)
    resized_images = get_resized_images(padded_images)

    predictions = show_prediction_lite(resized_images)

    DEBUG_LOGS.append(predictions)

    eqn = buld_lin_eqn(predictions)
    return eqn, DEBUG_LOGS
