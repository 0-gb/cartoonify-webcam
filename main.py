import cv2

cap = cv2.VideoCapture(0)
save_to_file = True
vid_filename = 'cartooned_you.mp4'
out = cv2.VideoWriter(vid_filename, -1, 20.0, (640, 480))

if not cap.isOpened():
    raise IOError("Error opening webcam")


def get_image_edges(frame_local):
    frame_local = cv2.cvtColor(frame_local, cv2.COLOR_BGR2GRAY)
    frame_local = cv2.medianBlur(frame_local, 5)
    frame_local = cv2.adaptiveThreshold(frame_local, 255,
                                        cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY, 3, 3)
    return frame_local


def get_colour_image(frame_local):
    return cv2.bilateralFilter(frame_local, 5, 300, 300)


while True:

    ret, frame = cap.read()

    image_edges = get_image_edges(frame)
    colour_image = get_colour_image(frame)

    cartoon_image = cv2.bitwise_and(colour_image, colour_image, mask=image_edges)

    if save_to_file:
        out.write(cartoon_image)

    cv2.imshow('Cartooned image', cartoon_image)
    cv2.imshow('Original image', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
