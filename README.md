# web_crawler_lab
  [Orginal source](https://git.bdaa.pro/yxonic/data-specification/-/wikis/%E9%97%A8%E8%AF%8A%E4%B8%93%E5%AE%B6 "With a Title")
## Dpendencies
+  python dependencies  
python3,selenium,requests,bs4
+ webdriver  
 [Chrome Webdriver](http://npm.taobao.org/mirrors/chromedriver/)  
 省立医院网站间隔几十秒会返回JavaScript重新构造cookie，当cookie失效时，通过Webdriver解析获取新的cookie  
 
 ## 数据来源及格式
 
爬取数据来源:http://www.ahslyy.com.cn/mz/index_13.aspx?pid=20
 
医生信息：
 [
  {
    "id": 
    "姓名":
    "性别":
    "职称":
    "所属科室":
    "专业特长":
    "详细介绍":
  },
  ..
]

 
排班表：
[
  {
    "分区":
    "门诊类型":
    "科室":
    "日期":
    "时间":
    "医师": [医师id1, 医师id2, ...]
  }
]

## 功能
 getDoctorInfo.py：  
 从[门诊专家介绍](http://www.ahslyy.com.cn/mz/index_13.aspx?pid=20)处获取全体医师的信息  
 getSchedule.py：  
 从[门诊排班表](http://www.ahslyy.com.cn/mz/index_17.aspx?lcid=1&type=1)处获取全体排班信息   
 main.py：  
 每周调用getDoctorInfo,getSchedule更新排班表  
 
 
## 实验结果  
 医师信息表和排班表分别为result文件夹下DoctorInfo.json和Table.json
