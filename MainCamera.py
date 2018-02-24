import cv2
import time
import threading
import Tkinter
from PIL import Image, ImageTk

class MainCamera:
	IsCameraAlive = False
	face_cascade = None
	eye_cascade = None
	
	def __init__(self):
		self.camera = cv2.VideoCapture(0) #use for to initialize camera; 0=> default camera
		MainCamera.face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
		MainCamera.eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')
		
	def StartCaptureImage(self, RawImage, MaskImage):	
		MainCamera.IsCameraAlive = True
		cam = threading.Thread(target = self.TryCaptureImage, args = (self.camera, RawImage, MaskImage))
		cam.start()
		
	def TryCaptureImage(self, camera, RawImage, MaskImage):
		while MainCamera.IsCameraAlive:
			try:
				rc, frame = camera.read()
				if not rc:
					continue
				
				grayimage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)	
				faces = MainCamera.face_cascade.detectMultiScale(grayimage, 1.3, 5) #search for faces
				for (x,y,w,h) in faces:
					cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
					RegionOfImage_Gray = grayimage[y:y+h, x:x+w]
					RegionOfImage_color = frame[y:y+h, x:x+w]
					
					eyes = MainCamera.eye_cascade.detectMultiScale(RegionOfImage_Gray)
					for(EX, EY, EW, EH) in eyes:
						cv2.rectangle(RegionOfImage_color, (EX, EY), (EX+ EW, EY +EH), (0,255,0), 2)
				
				#CONVERTING FRAME IMAGE TO RGB COLOR TO IMAGE OBJECT TO TKINTER
				raw_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				raw_image = Image.fromarray(raw_image)
				raw_image = ImageTk.PhotoImage(image = raw_image)
				
				#CONVERTING GRAY IMAGE TO IMAGE OBJECT TO TKINTER
				raw_image_gray = Image.fromarray(grayimage)
				raw_image_gray = ImageTk.PhotoImage(image = raw_image_gray)
				
				try:
					RawImage.configure(image = raw_image)
					RawImage._image_cache = raw_image
					
					MaskImage.configure(image = raw_image_gray)
					MaskImage._image_cache = raw_image_gray	
				except Exception, ex:
					print "Error-1: {0}".format(ex)
			except Exception, ex:
				print "Error-2: {0}".format(ex)
	
	def StopCaptureImage(self):
		MainCamera.IsCameraAlive = False
		self.camera.release()
		time.sleep(0.1)

	def __del__(self):
		self.StopCaptureImage()