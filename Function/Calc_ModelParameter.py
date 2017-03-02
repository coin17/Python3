#!/usr/bin/env python
# encoding=utf-8

"""
高斯大气扩散模型中参数计算

"""

import math

#定义方法，默认参数
def calculateY(pointX,pointY,windAngle):
	pointLocation = pointX * pointY

	pointAngle_Y = math.degrees(math.atan(abs(pointX) / abs(pointY)))
	print("目标点位与Y轴夹角："+str(pointAngle_Y))

	pointLength = math.sqrt(math.pow(pointX, 2) + math.pow(pointY, 2))
	print("目标点位与原点距离："+str(pointLength))

	if windAngle == 90 or windAngle == 270:
		return abs(pointX), abs(pointY)
	elif windAngle == 180 or windAngle == 360 or windAngle == 0:
		return abs(pointY), abs(pointX)
		
	elif windAngle > 90 and windAngle < 180:
		windAngle_Y = 180 - windAngle
	elif windAngle > 180 and windAngle < 270:
		windAngle_Y = 270 - windAngle
	elif windAngle > 270 and windAngle < 360:
		windAngle_Y = 360 - windAngle
	else:
		windAngle_Y = windAngle
		
	print("风向与Y轴夹角：" + str(windAngle_Y))

	if (pointLocation > 0 and (windAngle < 90 or (windAngle > 180 and windAngle < 270))) or (pointLocation < 0 and ((windAngle > 90 and windAngle < 180) or (windAngle > 270 and windAngle < 360))):
		print("点位、风向在同一象限")
		includedAngle = abs(pointAngle_Y - windAngle_Y)
	else:
		print("点位、风向在相邻象限")
		includedAngle = pointAngle_Y + windAngle_Y
		if(includedAngle > 90):
			includedAngle = abs(includedAngle - 180)

	print("点位与风向夹角为：" + str(includedAngle))

	if math.sin(math.radians(includedAngle)) == 0:
		return 0,0
	else:
		if windAngle < 90:
			windAngle_Y = windAngle
		elif windAngle > 90 and windAngle < 180:
			windAngle_Y = 180 - windAngle
		elif windAngle > 180 and windAngle < 270:
			windAngle_Y = 270 - windAngle
		elif windAngle > 270 and windAngle < 360:
			windAngle_Y = 360 - windAngle
		else:
			windAngle_Y = windAngle
		dy = pointLength * math.sin(math.radians(includedAngle)) 
		dx = math.sqrt(math.pow(pointLength, 2) - math.pow(dy, 2))
		return dx, dy


if __name__ == '__main__':
    dx, dy = calculateY(4, 4, 90)
    print("完成计算，垂线长度为："+str(dx) + " " + str(dy))