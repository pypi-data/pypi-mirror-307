

#!/usr/bin/python3
# coding=utf-8
###################################################################
#           ____     _     _ __  __                 
#          / __/__  (_)___(_) /_/ /  ___  ___  ___ _
#         _\ \/ _ \/ / __/ / __/ /__/ _ \/ _ \/ _ `/
#        /___/ .__/_/_/ /_/\__/____/\___/_//_/\_, / 
#           /_/                              /___/  
# Copyright (c) 2024 Chongqing Spiritlong Technology Co., Ltd.
# All rights reserved.  
# @author	arthuryang
# @brief	excel工具集
#
###################################################################  

import sys
def export(_function):
	# 动态地将函数添加到导出的模块中
	setattr(sys.modules[globals()['__name__']], _function.__name__, _function)

from	SpiritLong_excel.excel	import	alignment_center
from	SpiritLong_excel.excel	import	alignment_left
from	SpiritLong_excel.excel	import	alignment_right
from	SpiritLong_excel.excel	import	style_title