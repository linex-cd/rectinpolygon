
#检索每个点的所有矩形-测试
def get_rect_of_point_test():
	#         *  
	#0  1  2  3  4  5  6  7 j/i
	matrix_bool=[
	[0, 0, 0, 0, 0, 0, 0, 0], #0
	[0, 0, 1, 0, 0, 0, 0, 0], #1
	[0, 0, 1, 1, 0, 0, 0, 0], #2
	[0, 1, 1, 1, 1, 0, 0, 0], #3
	[0, 1, 1, 1, 1, 1, 1, 0], #4*
	[0, 0, 1, 1, 1, 0, 0, 0], #5
	[0, 0, 0, 1, 1, 1, 0, 0], #6
	[0, 0, 0, 0, 1, 0, 0, 0], #7
	[0, 0, 0, 0, 0, 0, 0, 0]] #8	
	#5 4 5 6			
	#5 4 6 5			
	#5 4 6 4			
				
	#确认1矩形
	'''
	4, 3, 4, 6
	4, 3, 6, 3
    4, 3, 6, 4
	'''
	i=4
	j=3
	max_w=4
	max_h=3
	
	r_array = get_rect_of_point(i, j, max_w, max_h, matrix_bool)
	
	print(r_array)
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
get_rect_of_point_test()










