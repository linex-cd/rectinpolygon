
polygon= [(100, 300), (200, 200), (500, 350), (400, 350), (450, 600), (350, 700), (200, 600), (150, 500)]
subarea =[(400, 350), (430, 500)]
import cv2
import numpy as np
def pt_is_in_poly(p, poly):

	px, py = p
	ret = False
	for i, corner in enumerate(poly):
		next_i = i + 1 if i + 1 < len(poly) else 0
		x1, y1 = corner
		x2, y2 = poly[next_i]
		if (x1 == px and y1 == py) or (x2 == px and y2 == py):  # 点在顶点上
			ret = True
			break
		#endif
		if min(y1, y2) < py <= max(y1, y2):  #找到多边形的水平边
			x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
			x = int(x) #转为整数，防止因为精度问题导致的判断错误
			if x == px:  # 点在边上
				ret = True
				break
			elif x > px:  #点在左侧，做一次发展
				ret = not ret
			#endif
		#endif
	
	#endfor
	
	return ret

#enddef
#初始化画布
def init_canvas(width, height, color=(255, 255, 255)):
	canvas = np.ones((height, width, 3), dtype="uint8")
	canvas[:] = color
	return canvas

#enddef

#获取边界
def get_bound(points):
	
	bound = None
	
	if len(points) == 0:
		
		return bound
	#endif
	pt = points[0]
	
	pt = list(pt)
	x1 = pt[0]
	x2 = pt[0]
	y1 = pt[1]
	y2 = pt[1]

	for pt in points:
		
		(x, y) = pt
		
		
		if x < x1:
			x1 = x
		#endif
		
		if x > x2:
			x2 = x
		#endif
		
		if y < y1:
			y1 = y
		#endif
		
		if y > y2:
			y2 = y
		#endif
	
	#endfor
	
	bound = [x1,y1,x2,y2]
	
	return bound
#enddef
points=[(100,300), (200,200), (500, 350), (400, 350), (450, 600), (350, 700), (200, 600), (150, 500)]
## 获取边界
bound = get_bound(points)
print("bound:", bound)


## 绘制画布
canvas = init_canvas(bound[2] + bound[0], bound[3] + bound[1], color=(0, 0, 0))

cv2.imshow('get_inscribed_rect', canvas)
cv2.waitKey(0)

## 求多边形边
edges = []
count = len(points)
for index in range(count):
	
	pt1 = points[index]
	
	if index == count -1:
		pt2 = points[0]
	else:
		pt2 = points[index+1]
	#endif
	
	edges.append([pt1, pt2])
	cv2.line(canvas, pt1, pt2, (0, 0, 255), 2)
	
#endfor
cv2.imshow('get_inscribed_rect', canvas)
cv2.waitKey(0)
pt3=(430,350)


#判断子矩形是否在多边形之内
def is_subarea_in_polygon(polygon, subarea):
	
	pts = []
	
	pt1 = subarea[0]
	pt2 = subarea[1]

	
	pt3 = [pt2[0], pt1[1]]
	pt4 = [pt1[0], pt2[1]]
	
	#因为对角线上的点可能都在矩形内，所以要判断边中点是否也都在多边形内
	pt5 = [int((pt1[0]+pt2[0])/2), pt1[1]]
	pt6 = [int((pt1[0]+pt2[0])/2), pt2[1]]
	
	pt7 = [pt1[0], int((pt1[1]+pt2[1])/2)]
	pt8 = [pt2[0], int((pt1[1]+pt2[1])/2)]
	
	pts.append(pt1)
	pts.append(pt2)
	pts.append(pt3)
	pts.append(pt4)
	pts.append(pt5)
	pts.append(pt6)
	pts.append(pt7)
	pts.append(pt8)
	
	for pt in pts:
		if pt_is_in_poly(pt, polygon) is False:
			return False
		#endif

	return True
	
#enddef


s=is_subarea_in_polygon(polygon, subarea)
print(s)














