import MainCamera
import Tkinter

class MainForm:
	def __init__(self):
		self.MCamera = None
	
		self.root = Tkinter.Tk()
		self.root.title("OPEN CV CAMERA Object Detection")
		self.root.geometry("816x450")
		
		self.StartCameraBtn = Tkinter.Button(self.root, text = "Start Camera", command = self.StartCameraBtn_Click)
		self.StartCameraBtn.place(x=5,y=5,width=100)
		
		self.StopCameraBtn = Tkinter.Button(self.root, text = "Stop Camera", command = self.StopCameraBtn_Click)
		self.StopCameraBtn.place(x=110,y=5,width=100)
		
		self.RawImage = Tkinter.Label(self.root, background="red")
		self.RawImage.place(x=5,y=40,width=400, height=400)
				
		self.MaskImage = Tkinter.Label(self.root, background="yellow")
		self.MaskImage.place(x=410, y=40, width=400, height=400)
		
		self.root.mainloop()
		
		#self.DestroyAll()
		
	def StartCameraBtn_Click(self):
		if self.MCamera == None:
			self.MCamera = MainCamera.MainCamera()
			self.MCamera.StartCaptureImage(self.RawImage, self.MaskImage)
	
	def StopCameraBtn_Click(self):
		if self.MCamera != None:
			self.MCamera.StopCaptureImage()
			self.MCamera = None
	def DestroyAll(self):
		self.StopCameraBtn_Click()