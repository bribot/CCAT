import cv2
import numpy as np

c = cv2.VideoCapture(-1)
roiPnt = [(0,0), (10,10)]
roiSet = False
roiDrag = False

def nothing(i):
	pass

def main():
	print("hack the planet")
	
	global roiSet
	minH = 22
	maxH = 37
	minS = 109
	maxS = 255
	minV = 115
	maxV = 255
	
	alpha=1.0
	
	win1 = 'Trackbars'
	cv2.namedWindow(win1,0)
	cv2.resizeWindow(win1,700,50)
	cv2.createTrackbar('Max H',win1,maxH,255,nothing)
	cv2.createTrackbar('Min H',win1,minH,255,nothing)
	cv2.createTrackbar('Max S',win1,maxS,255,nothing)
	cv2.createTrackbar('Min S',win1,minS,255,nothing)
	cv2.createTrackbar('Max V',win1,maxV,255,nothing)
	cv2.createTrackbar('Min V',win1,minV,255,nothing)
	cv2.createTrackbar("alpha",win1,int(alpha*100),100,nothing)
	
	win2 = 'Final'
	cv2.namedWindow(win2)
	cv2.setMouseCallback(win2,clickr)
	hsv=[0,0,0]
	while(1):
		ret, frame = c.read()
		img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		
		
		maxH = cv2.getTrackbarPos('Max H', win1)
		minH = cv2.getTrackbarPos('Min H', win1)
		maxS = cv2.getTrackbarPos('Max S', win1)
		minS = cv2.getTrackbarPos('Min S', win1)
		maxV = cv2.getTrackbarPos('Max V', win1)
		minV = cv2.getTrackbarPos('Min V', win1)
		hsvMax = np.array((maxH, maxS, maxV))
		hsvMin = np.array((minH, minS, minV))
		
		img_hsv = cv2.GaussianBlur(img,(11,11),0)
		img = cv2.inRange(img_hsv, hsvMin, hsvMax)
		#cv2.imshow("before",img)
		img = noiseCleaner(img)
		
		
		alpha = cv2.getTrackbarPos("alpha", win1) * 0.01
		beta = 1.0
		img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
		img2 = cv2.addWeighted(frame, alpha, img, beta, 0.0)
		if roiSet | roiDrag:
			cv2.rectangle(img2, roiPnt[0], roiPnt[1], (0,255,0), 2)
		
		
		tSize=0.4
		cv2.putText(img2,'H = %i, %i (%i)' %(minH,maxH,hsv[0]), (10,20),cv2.FONT_HERSHEY_SIMPLEX, tSize, (255,255,255))
		cv2.putText(img2,'S = %i, %i (%i)'%(minS,maxS,hsv[1]), (10,35),cv2.FONT_HERSHEY_SIMPLEX, tSize, (255,255,255))
		cv2.putText(img2,'V = %i, %i (%i)'%(minV,maxV,hsv[2]), (10,50),cv2.FONT_HERSHEY_SIMPLEX, tSize, (255,255,255))
		#cv2.imshow("camera feed", frame)
		#cv2.imshow("bin", img)
		cv2.imshow(win2, img2)
		
		
		
		
		if cv2.waitKey(1)&0xFF==ord('q'):
			break
		if roiSet:
			tmPnt=np.sort(roiPnt,axis=0)
			hsv=setHSV(img_hsv[tmPnt[0][1]:tmPnt[1][1],tmPnt[0][0]:tmPnt[1][0]])
			#cv2.imshow("test",img_hsv[roiPnt[0][1]:roiPnt[1][1],roiPnt[0][0]:roiPnt[1][0]])
			print hsv
			var = 15
			if hsv[0] < var:
				var = 5
			cv2.setTrackbarPos('Max H', win1, np.uint8(hsv[0])+var)
			cv2.setTrackbarPos('Min H', win1, np.uint8(hsv[0]-var))
			#cv2.setTrackbarPos('Max S', win1, int(hsv[1]+5))
			cv2.setTrackbarPos('Min S', win1, np.uint8(hsv[1]-15))
			#cv2.setTrackbarPos('Max V', win1, int(hsv[2]+15))
			cv2.setTrackbarPos('Min V', win1, np.uint8(hsv[2]-15))
			roiSet = False
		
		
	c.release()
	
def setHSV(img):
	hsv=[]
	img= cv2.split(img)
	hsv.append(np.mean(img[0]))
	hsv.append(np.mean(img[1]))
	hsv.append(np.mean(img[2]))
	return hsv
	

def noiseCleaner(img):
	disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
	img = cv2.erode(img, disk, iterations = 3)
	img = cv2.dilate(img, disk, iterations = 3)
	
	img1 = cv2.erode(img,disk,iterations = 1)
	img1 = cv2.bitwise_not(img1)
	img = cv2.bitwise_and(img,img1)
	return img
	
def clickr(event, x, y, flags, img):
	global roiSet, roiDrag
	if (event == cv2.EVENT_MOUSEMOVE) & roiDrag:
		roiPnt[1] = (x,y)
		#print "what a drag"
		
	if (event == cv2.EVENT_LBUTTONDOWN) & (not(roiSet)):
		roiPnt[0]=(x,y)
		roiPnt[1] = (x,y)
		roiDrag = True
		print(roiPnt)
		
	elif (event == cv2.EVENT_LBUTTONUP) & (not(roiSet)):
		if (x,y) == roiPnt[0]:
			roiPnt[1]=(x+1,y+1)
		else:
			roiPnt[1]=(x,y)
		
		print(roiPnt)
		roiDrag = False
		roiSet=True
		
	

if __name__ == '__main__':
	main()