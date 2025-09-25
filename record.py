import cv2
from datetime import datetime
from logger import surveillance_logger

def record():
    cap = cv2.VideoCapture(0)
    start_time = datetime.now()
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    filename = f'recordings/{start_time.strftime("%d-%m-%y-%H-%M-%S")}.avi'
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640,480))
    
    # Log recording start
    surveillance_logger.log_recording(
        action="recording_started",
        file_path=filename,
        resolution="640x480",
        status="in_progress"
    )

    while True:
        _, frame = cap.read()

        cv2.putText(frame, f'{datetime.now().strftime("%D-%H-%M-%S")}', (50,50), cv2.FONT_HERSHEY_COMPLEX,
                        0.6, (255,255,255), 2)

        out.write(frame)
        
        cv2.imshow("esc. to stop", frame)

        if cv2.waitKey(1) == 27:
            break
    
    # Calculate duration and log recording end
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    surveillance_logger.log_recording(
        action="recording_stopped",
        file_path=filename,
        duration=duration,
        resolution="640x480",
        status="completed"
    ) 
