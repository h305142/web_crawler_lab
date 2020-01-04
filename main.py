import  getDoctorInfo
import getSchedule
import time
import datetime
def exeCrawler():
	#getDoctorInfo.collectDoctorUrls();
	#getDoctorInfo.getDocInfo();
	#getDoctorInfo.get_name_ID_pairs();
	getSchedule.getAll();
def time_ti(h=17,w=5):
	while True:
		now = datetime.datetime.now()
		week=now.weekday();
		# print(now.hour, now.minute)
		if now.hour == h and  week==w:
			exeCrawler()
# 每隔3600秒检测一次
		time.sleep(3600)
