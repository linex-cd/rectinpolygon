
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



#检索每个点的所有矩形
def get_rect_of_point(i, j, max_w, max_h, matrix_bool):

	r_array = []
	#每个宽度都尝试一次
	for z in range(1,max_w+1):
		#扫描每列
		for x in range(1,max_h+1):

			#如果下移遇到0，则保存一个矩形，并减小一次宽度
			p=i+x

			#扫描下一行
			for y in range(z):

				q=j+y

				w=matrix_bool[p][q]
				
				if w == 0:
					
					#x=0, w=1
					#x=1, w=0
					
					r = p-1
					s = j+z-1
					
					#判断上面所有行是否存在矩形
					flag = 1
					for u in range(i, r+1):
						if matrix_bool[u][s] == 0:
							flag = 0
							break
						#endif
					#endfor
					if flag == 1:
						r = [i,j,r,s]
						if r not in r_array:
							r_array.append(r)
						#endif
					#endif

					
				#endif

			
			#endfor
		#endfor
	#endfor
	return r_array
#enddef


#计算面积
def get_rect_size_of_matrix(matrix_vertex, r):
	
	[i, j, r, s] = r
	
	[pt1, pt2] = matrix_vertex[i][j]
	x1 = pt1[0]
	y1 = pt1[1]

	[pt3, pt4] = matrix_vertex[r][s]
	x2 = pt4[0]
	y2 = pt4[1]
	
	size = (x2-x1) * (y2-y1)
	
	return size

#enddef

#寻找矩阵内标记的最大矩形区域
def get_rects_in_matrix(matrix_vertex, matrix_bool):
	rects = []
	
	v_size = len(matrix_bool)
	h_size = len(matrix_bool[0])
	

	for i in range(v_size):
				
		for j in range(h_size):
			
			#当前矩形
			v = matrix_bool[i][j]

			rect = matrix_vertex[i][j]
			
			pt1 = rect[0]
			pt2 = rect[1]
			
			
			
			#跳过空值
			if v == 0:
				continue
			#endif
			
			#找最大宽度和高度
			max_w = 1
			max_h = 1
			
			#横向查找,最远的矩形跨度w赋值为max_w，如果这个w<max_w，则更新max_w
			
			w = 1
			for m in range(j+1, h_size):
				if matrix_bool[i][m] == 1:
					w = w + 1
				else:
					break
				#endif
			#endfor
			if w > max_w:
				max_w = w
			#endif
			print("row i(%d) , col j(%d) max_w=%d" % (i, j, max_w))
			
			
			#纵向查找,最远的矩形跨度h赋值为max_h，如果这个h<max_h，则更新max_h
			
			h = 1
			for n in range(i+1, v_size):
				if matrix_bool[n][j] == 1:
					h = h + 1
				else:
					break
				#endif
			#endfor
			if h > max_h:
				max_h = h
			#endif
			print("row i(%d) , col j(%d) max_h=%d" % (i, j, max_h))
			
			'''
			[0, 0, 0, 0, 0, 0, 0, 0]
			[0, 0, 1, 0, 0, 0, 0, 0]
			[0, 0, 1, 1, 0, 0, 0, 0]
			[0, 1, 1, 1, 1, 0, 0, 0]
			[0, 1, 1, 1, 1, 1, 0, 0]
			[0, 0, 1, 1, 1, 1, 1, 0]
			[0, 0, 0, 1, 1, 1, 0, 0]
			[0, 0, 0, 0, 0, 0, 0, 0]
			'''
		
			r_array = get_rect_of_point(i, j, max_w, max_h, matrix_bool)
			
			
			rects.append(r_array)
			
			
			
		#endfor
		
	#endfor
	
	return rects
#endif
			
def get_inscribed_rect(points):

	inscribed_rect = None
	
	## 获取边界
	bound = get_bound(points)
	
	
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

		
	#endfor

	
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
		
		
		pt1 = (0, pt[1])
		pt2 = (bound[2] + bound[0], pt[1])
		lines_h.append([pt1, pt2])
		lines.append([pt1, pt2])
		
		
	#endfor

	
	## 网格线和边求交
	vertexs = []

	for edge in edges:
		for line in lines:

			intersection = get_line_intersection(edge, line)
			if intersection is not None:
			
				v = list(intersection)
				v = (int(v[0]), int(v[1]))

				vertexs.append(v)
				
				
			#endif
			
			
		#endfor
	
	#endfor

	
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

		pt1 = (0, pt[1])
		pt2 = (bound[2] + bound[0], pt[1])
		lines_h.append([pt1, pt2])
		lines.append([pt1, pt2])
		
		
	#endfor

	
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
	matrix_bool = [] #是否在多边形内
	matrix_vertex = [] #矩形的顶点
	
	
	count_lines_h = len(lines_h)
	count_lines_v = len(lines_v)
	
	#扫描行,忽略边框
	for i in range(1, count_lines_h):
		line_h = lines_h[i]

		y1 = lines_h[i-1][1][1]
		y2 = lines_h[i][1][1]
		
		matrix_vertex.append([])
		matrix_bool.append([])
		
		#扫描列,忽略边框
		for j in range(1, count_lines_v):
			line_v = lines_v[j]

			x1 = lines_v[j-1][0][0]
			x2 = lines_v[j][0][0]
			
			
			#左上角位置
			pt1 = (x1, y1)

			#右下角位置
			pt2 = (x2, y2)

			
			#保存子矩形
			subarea = [pt1, pt2]
			matrix_vertex[i-1].append(subarea)

			## 判断子矩形是否在多边形之内，生成判断集合矩阵
			
			check = is_subarea_in_polygon(polygon = points, subarea = subarea)
			if check:
				matrix_bool[i-1].append(1)
				
			else:
				matrix_bool[i-1].append(0)
				
			#endif

		#endfor
		

	#endfor
	
	## 扫描连通图
	print('matrix_bool:')
	for m in matrix_bool:
		print(m)
	
	#endfor
	
	#求矩形数组
	#矩形数组[左上角矩形左上角顶点xy, 右下角矩形右下角顶点, 面积]
	#矩形为左上角的最大矩形
	# array_rects =[ [[i,j,r,s], [i,j,r,s],] [[i,j,r,s],] ]
	array_rects = get_rects_in_matrix(matrix_vertex, matrix_bool)
	
	#寻找每个子矩形的扩张最大矩形面积
	max_size = 0
	max_size_rect = None
	for rects in array_rects:
		for rect in rects:
			size = get_rect_size_of_matrix(matrix_vertex, rect)
			if size > max_size:
				max_size = size
				max_size_rect = rect
			#endif
		#endfor
	
	#endfor

	[i,j,r,s] = max_size_rect
	
	[pt1, pt2] = matrix_vertex[i][j]
	[pt3, pt4] = matrix_vertex[r][s]

	inscribed_rect = [matrix_vertex[i][j], matrix_vertex[r][s], max_size]
	

	return inscribed_rect
#enddef

			
def get_inscribed_rect_test(points):

	inscribed_rect = None
	
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
	matrix_bool = [] #是否在多边形内
	matrix_vertex = [] #矩形的顶点
	
	
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
	print('matrix_bool:')
	for m in matrix_bool:
		print(m)
	
	#endfor
	
	
	#求矩形数组
	#矩形数组[左上角矩形左上角顶点xy, 右下角矩形右下角顶点, 面积]
	#矩形为左上角的最大矩形
	# array_rects =[ [[i,j,r,s], [i,j,r,s],] [[i,j,r,s],] ]
	array_rects = get_rects_in_matrix(matrix_vertex, matrix_bool)
	
	#寻找每个子矩形的扩张最大矩形面积
	max_size = 0
	max_size_rect = None
	for rects in array_rects:
		for rect in rects:
			size = get_rect_size_of_matrix(matrix_vertex, rect)
			if size > max_size:
				max_size = size
				max_size_rect = rect
			#endif
		#endfor
	
	#endfor

	print(max_size)
	print(max_size_rect)
	[i,j,r,s] = max_size_rect
	
	[pt1, pt2] = matrix_vertex[i][j]
	[pt3, pt4] = matrix_vertex[r][s]
	cv2.rectangle(canvas, (pt1[0]+1, pt1[1]+1), (pt4[0]-1, pt4[1]-1), (200, 200, 200), 2)
	
	inscribed_rect = [matrix_vertex[i][j], matrix_vertex[r][s], max_size]
	
	cv2.imshow('get_inscribed_rect', canvas)
	while(True):
		c = cv2.waitKey(0)
		if c == 27:#ESC
			break
		
	cv2.destroyAllWindows()
	
	return inscribed_rect
#enddef

if __name__ == "__main__":

	pass

	points = [(100,300), (200,200), (500, 350), (450, 600), (350, 700), (200, 600), (150, 500)] #凸
	points = [(100,300), (200,200), (500, 350), (400, 450), (450, 600), (350, 700), (200, 600), (150, 500)] #凹
	points = [(100,300), (200,200), (500, 350), (400, 350), (450, 600), (350, 700), (200, 600), (150, 500)] #水平边
	points = [(100,300), (200,200), (500, 350), (400, 350), (400, 600), (450, 600), (350, 700), (200, 600), (150, 500)] #垂直边
	points = [(100,300), (200,200), (500, 350), (400, 370), (430, 600), (450, 600), (350, 700), (200, 600), (150, 500)] #

	print(points)
	r = get_inscribed_rect_test(points)
	print(r)

