# spot_diff.py

import cv2
import time
from skimage.metrics import structural_similarity
from datetime import datetime
from alert import send_all_alerts  # ✅ IMPORT ALERT SYSTEM

def spot_diff(frame1, frame2):

    frame1 = frame1[1]
    frame2 = frame2[1]

    g1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    g1 = cv2.blur(g1, (2,2))
    g2 = cv2.blur(g2, (2,2))

    (score, diff) = structural_similarity(g2, g1, full=True)

    print("Image similarity:", score)

    diff = (diff * 255).astype("uint8")
    thresh = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY_INV)[1]

    contors = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contors = [c for c in contors if cv2.contourArea(c) > 50]

    if len(contors):
        for c in contors:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 2)

        # ✅ Send notification if something is detected
        send_all_alerts("🚨 Theft or motion detected in the surveillance area!")

    else:
        print("Nothing stolen")
        return 0

    cv2.imshow("diff", thresh)
    cv2.imshow("win1", frame1)
    cv2.imwrite("stolen/"+datetime.now().strftime("%d-%m-%y-%H-%M-%S")+".jpg", frame1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return 1
