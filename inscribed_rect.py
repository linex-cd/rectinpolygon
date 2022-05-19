
import cv2
import numpy as np



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

#线段求交
def get_line_intersection(line1, line2):

	p0, p1 = line1
	p2, p3 = line2

	p0_x, p0_y = p0
	p1_x, p1_y = p1
	p2_x, p2_y = p2
	p3_x, p3_y = p3


	s1_x = p1_x - p0_x
	s1_y = p1_y - p0_y
	s2_x = p3_x - p2_x
	s2_y = p3_y - p2_y

	intersection = None
	
	
	if -s2_x * s1_y + s1_x * s2_y == 0:
		return intersection;
	#endif
	
	if -s2_x * s1_y + s1_x * s2_y == 0:
		return intersection;
	#endif
	
	s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-s2_x * s1_y + s1_x * s2_y)
	t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-s2_x * s1_y + s1_x * s2_y)

	

	if s >= 0 and s <= 1 and t >= 0 and t <= 1:
		
		i_x = p0_x + (t * s1_x);
		i_y = p0_y + (t * s1_y);
		
		intersection = (i_x, i_y)
	#endif

	return intersection;
#enddef


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


#判断子矩形是否在多边形之内
def is_subarea_in_polygon(polygon, subarea):
	
	pt1 = subarea[0]
	pt2 = subarea[1]
	
	pt3 = [pt2[0], pt1[1]]
	pt4 = [pt1[0], pt2[1]]
	
	if pt_is_in_poly(pt1, polygon) and pt_is_in_poly(pt2, polygon) and pt_is_in_poly(pt3, polygon) and pt_is_in_poly(pt4, polygon):
		return True
	#endif

	return False
	
#enddef
			
def get_inscribed_rect(points):

	rect = None
	
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
	
	## *遍历角度组合
	
	
	## *遍历矩形组合
	
	## 计算所有网格线
	lines = []
	lines_h = []
	lines_v = []
	for index in range(count):
		
		pt = points[index]
		pt = list(pt)
		
		pt1 = (pt[0], 0)
		pt2 = (pt[0], bound[3] + bound[1])
		lines_v.append([pt1, pt2])
		lines.append([pt1, pt2])
		
		cv2.line(canvas, pt1, pt2, (100, 100, 100), 1)
		
		pt1 = (0, pt[1])
		pt2 = (bound[2] + bound[0], pt[1])
		lines_h.append([pt1, pt2])
		lines.append([pt1, pt2])
		
		cv2.line(canvas, pt1, pt2, (100, 100, 100), 1)
		
	#endfor
	cv2.imshow('get_inscribed_rect', canvas)
	cv2.waitKey(0)
	
	## 网格线和边求交
	vertexs = []

	for edge in edges:
		for line in lines:
			print("edge, line:", edge, line)
			
			cv2.line(canvas, edge[0], edge[1], (0, 255, 255), 2)
			cv2.line(canvas, line[0], line[1], (0, 255, 255), 1)
			
			intersection = get_line_intersection(edge, line)
			if intersection is not None:
			
				print('intersection:', intersection)
				v = list(intersection)
				v = (int(v[0]), int(v[1]))

				vertexs.append(v)
				
				cv2.circle(canvas, v, 5, color=(255, 0, 0), thickness=-1)
				
				cv2.imshow('get_inscribed_rect', canvas)
				cv2.waitKey(0)
				
			#endif
			
			cv2.line(canvas, edge[0], edge[1], (0, 0, 255), 2)
			cv2.line(canvas, line[0], line[1], (100, 100, 100), 1)
			
		#endfor
	
	#endfor
	cv2.imshow('get_inscribed_rect', canvas)
	cv2.waitKey(0)
	
	## 计算顶点网格
	for index in range(len(vertexs)):
		
		pt = vertexs[index]
		
		#忽略原始顶点
		if pt in points:
			continue
		#endif
		
		pt = list(pt)
		
		pt1 = (pt[0], 0)
		pt2 = (pt[0], bound[3] + bound[1])
		lines_v.append([pt1, pt2])
		lines.append([pt1, pt2])
		
		cv2.line(canvas, pt1, pt2, (100, 100, 0), 1)
		
		pt1 = (0, pt[1])
		pt2 = (bound[2] + bound[0], pt[1])
		lines_h.append([pt1, pt2])
		lines.append([pt1, pt2])
		
		cv2.line(canvas, pt1, pt2, (100, 100, 0), 1)
		
	#endfor
	cv2.imshow('get_inscribed_rect', canvas)
	cv2.waitKey(0)
	
	
	## 网格去重
	tmp_lines_h = []
	for line_h in lines_h:
		if line_h not in tmp_lines_h:
			tmp_lines_h.append(line_h)
		#endif
	#endfor
	lines_h = tmp_lines_h
	
	tmp_lines_v = []
	for line_v in lines_v:
		if line_v not in tmp_lines_v:
			tmp_lines_v.append(line_v)
		#endif
	#endfor
	lines_v = tmp_lines_v
	
	## 网格排序
	lines_h = sorted(lines_h, key=lambda x: x[0][1])
	lines_v = sorted(lines_v, key=lambda x: x[0][0])
	
	
	## 所有网格求交得到子矩形集合，并判断子矩形是否在多边形之内，生成判断集合矩阵
	matrix_bool = []
	matrix_vertex = []
	
	count_lines_h = len(lines_h)
	count_lines_v = len(lines_v)
	
	#扫描行,忽略边框
	for i in range(1, count_lines_h):
		line_h = lines_h[i]
		print('line_h:', line_h)
		cv2.line(canvas, line_h[0], line_h[1], (0, 100, 100), 1)
		
		y1 = lines_h[i-1][1][1]
		y2 = lines_h[i][1][1]
		
		matrix_vertex.append([])
		matrix_bool.append([])
		
		#扫描列,忽略边框
		for j in range(1, count_lines_v):
			line_v = lines_v[j]
			print('line_v:', line_v)
			
			cv2.line(canvas, line_v[0], line_v[1], (0, 100, 100), 1)
			
			x1 = lines_v[j-1][0][0]
			x2 = lines_v[j][0][0]
			
			
			#左上角位置
			pt1 = (x1, y1)
			print('pt1', pt1)
			cv2.circle(canvas, pt1, 2, color=(0, 255, 0), thickness=-1)
			
			#右下角位置
			pt2 = (x2, y2)
			print('pt2', pt2)
			cv2.circle(canvas, pt2, 2, color=(0, 255, 0), thickness=-1)
			
			cv2.imshow('get_inscribed_rect', canvas)
			cv2.waitKey(0)
			
			#保存子矩形
			subarea = [pt1, pt2]
			matrix_vertex[i-1].append(subarea)

			## 判断子矩形是否在多边形之内，生成判断集合矩阵
			
			check = is_subarea_in_polygon(polygon = points, subarea = subarea)
			if check:
				
				matrix_bool[i-1].append(1)
				
				#cv2.rectangle(canvas, pt1, pt2, (0, 200, 0), -1)
				cv2.rectangle(canvas, (pt1[0]+1, pt1[1]+1), (pt2[0]-1, pt2[1]-1), (0, 200, 0), -1)
				cv2.imshow('get_inscribed_rect', canvas)
				cv2.waitKey(0)
				
			else:
				matrix_bool[i-1].append(0)
			#endif

			
			
			cv2.line(canvas, line_v[0], line_v[1], (100, 0, 100), 1)
		#endfor
		
		
		cv2.line(canvas, line_h[0], line_h[1], (100, 0, 100), 1)
	#endfor
	
	## 扫描连通图
	print('matrix_bool')
	for m in matrix_bool:
		print(m)
	
	#endfor
	
	#矩形数组[左上角矩形左上角顶点xy, 右下角矩形右下角顶点, 面积]
	# R =[ [x1,y1,x2,y2,s], [x1,y1,x2,y2,s], [x1,y1,x2,y2,s] ... ]
	R = []
	
	'''
	
	h_size = len(matrix_bool)
	v_size = len(matrix_bool[0])
	
	print('matrix_bool')
	for i in range(h_size-1):
		
		for j in range(v_size-1):
			
			#当前矩形
			v = matrix_bool[i][j]
			
			#横向寻找
			#纵向寻找
			v_right = matrix_bool[i][j+1]
			v_down = matrix_bool[i+1][j]
			
			rect = matrix_vertex[i][j]
			
			pt1 = rect[0]
			pt2 = rect[1]
			
			if v == 1 and v_right == 1 and v_down == 1: 
			
				cv2.rectangle(canvas, (pt1[0]+2, pt1[1]+2), (pt2[0]-2, pt2[1]-2), (50, 150, 1000), -1)
			
			else:
				cv2.rectangle(canvas, (pt1[0]+2, pt1[1]+2), (pt2[0]-2, pt2[1]-2), (50, 50, 50), -1)
			#endif
			cv2.imshow('get_inscribed_rect', canvas)
			cv2.waitKey(0)
		#endfor
		
	#endfor
	'''


	cv2.destroyAllWindows()
	
	return rect
#enddef


points = [(100,300), (200,200), (500, 350), (500, 600), (350, 700), (200, 600), (150, 500)]

print(points)
r = get_inscribed_rect(points)


