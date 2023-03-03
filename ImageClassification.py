
from tensorflow.keras.applications import ResNet50, ResNet101, VGG16, VGG19, Xception
#https://keras.io/api/applications/#extract-features-with-vgg16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import cv2

def FindTheImage(image_path):
    im_path = image_path

    im = cv2.imread(im_path)
    # im_shape = im.shape

    model_VGG19 = VGG19(weights='imagenet', pooling='avg', classifier_activation="softmax")
    model_VGG16 = VGG16(weights='imagenet', pooling='avg', classifier_activation="softmax")
    model_ResNet50 = ResNet50(weights='imagenet', pooling='avg', classifier_activation="softmax")
    model_ResNet101 = ResNet101(weights='imagenet', pooling='avg', classifier_activation="softmax")

    # model.summary()
    try:
        img = image.load_img(im_path, target_size=(224, 224, 3))
    except:
        print("path not valid")
        return
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds_VGG19 = model_VGG19.predict(x)
    preds_VGG16 = model_VGG16.predict(x)
    preds_ResNet50 = model_ResNet50.predict(x)
    preds_ResNet101 = model_ResNet101.predict(x)
    # decode the results into a list of tuples (class, description, probability)
    # (one such list for each sample in the batch)

    pred_list = [preds_VGG19, preds_VGG16, preds_ResNet50, preds_ResNet101]

    all_dec_pred = []
    for pred in pred_list:
        all_dec_pred.append(decode_predictions(pred, top=1)[0])

    np_all_dec_pred = np.array(all_dec_pred)

    for i in range(len(np_all_dec_pred[:, :, 2])):
        np_all_dec_pred[i, :, 2] = float(np_all_dec_pred[i, :, 2])

    best_pred = np_all_dec_pred[np.argmax(np_all_dec_pred[:, :, 2]), :, :]

    pred_count = np.argmax(np_all_dec_pred[:, :, 2])
    if pred_count == 0:
        best_model = "VGG19"
    elif pred_count == 1:
        best_model = "VGG16"
    elif pred_count == 2:
        best_model = "RestNet50"
    elif pred_count == 3:
        best_model = "RestNet101"
    else:
        best_model = "Unkown"

    print("Best prediction is: ", best_pred[:, 1], "with a", float(best_pred[:, 2]) * 100, "confidence.")
    print("Predicted by: ", best_model)

    # print(np.argmax(all_dec_pred))

    # print('Predicted by VGG19:', decode_predictions(preds_VGG19, top=1)[0])
    # print('Predicted by VGG16:', decode_predictions(preds_VGG19, top=1)[0])
    # print('Predicted by ResNet50:', decode_predictions(preds_ResNet50, top=1)[0])
    # print('Predicted by ResNet101:', decode_predictions(preds_ResNet101, top=1)[0])


#FindTheImage('images/elephant.jpg')