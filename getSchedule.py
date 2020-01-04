from selenium import webdriver
import json
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re
scheduleURL="http://www.ahslyy.com.cn/mz/index_1252.aspx?lcid=3"
baseURL="http://www.ahslyy.com.cn/mz/Department/info_41.aspx?itemid=29495"
def get_cookies():
    wd=webdriver.Chrome(r'.\chromedriver_win32\chromedriver.exe')
    wd.get(baseURL)
    #wd.refresh()
    cookie=""
    temp=""
    for i in wd.get_cookies():
        print(i)
        cookies=temp+i["name"]+"="+i["value"]
        temp=cookies
        temp=temp+";"

    #print(cookies)
    with open(r".\cookies.txt","w") as f:
        f.write(cookies)
        f.close()
    return cookies
def get_HTMLText(url,cookies):
    #with open(r"C:\Users\dell\Desktop\cookies.txt","r") as f:
    #    cookies = f.read()
    #print(cookies)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    Cookie={}
    Cookie["Cookie"]=cookies
    #print(Cookie)
    headers.update(Cookie)
    #session = requests.session()
    try:
        r=requests.get(url,headers=headers,timeout=30,allow_redirects=True)
        r.raise_for_status()# if status!=200,raise HTTPError exception
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return "产生异常"
def getDoctorTable(physician):
    DoctorNames=[]
    for grid in physician:
        soup1 = BeautifulSoup(str(grid), 'html.parser')
        hrefSet=soup1.find_all(name='a')
        subsetName=[]
        for doctor in hrefSet:
            name=doctor.get_text().replace(' ' , '' )
            subsetName.append(name)
        DoctorNames.append(subsetName)
    #print(DoctorNames)
    return DoctorNames
#def collectDoctorUrls():
departmentPrefix='http://www.ahslyy.com.cn/mz/index_13.aspx?pid='
departmentId=['20','21','555','1272','1273',
              '1930','2689','2795','2850','2858',
              '1525','2935','2936']
#departmentId=['2935']
departmentSuffix='&page='

cookieOverdue=False
cookieFlag='请开启JavaScript并刷新该页.'

webBase='http://www.ahslyy.com.cn/'
websites=['/mz/index_17.aspx?lcid=1&type=1', #s=1 b 0
'/mz/index_17.aspx?lcid=1&type=2', #s=2 b1
'/mz/index_17.aspx?lcid=1&type=3', #s=3 b2
'/mz/index_17.aspx?lcid=1&type=4', #s=4 b3
'/mz/index_1270.aspx',#c4
'/mz/index_1252.aspx',#a5
'/mz/index_17.aspx?lcid=2&type=0',#b6
'/mz/index_1252.aspx?lcid=2',#a7
'/mz/index_17.aspx?lcid=3&type=0',#b8
'/mz/index_1252.aspx?lcid=3']#a9
TypeA=[5,7,9]
TypeB=[0,1,2,3,6,8]
TypeC=[4]
department=['总院','总院','总院','总院','总院','总院','南区','南区','西区','西区']
def getScheduleTable1(scheduleURL,savePath,d,department,cookies):
    #cookies=get_cookies()
    HTMLText=get_HTMLText(scheduleURL,cookies)
    soup = BeautifulSoup(HTMLText, 'html.parser')
    #get name_ID_pairs
    fin=open(r'.\name_ID_pairs.txt','r',encoding='UTF-8')
    name_ID_pairs={}
    allLines=fin.readlines()
    for i in range(len(allLines)):#len(allLines)
        entry=allLines[i]
        entry=eval(entry)
        name_ID_pairs.update(entry)
    fin.close()
    #get 分区
    department=department[d]
    print(department)
    #get date 日期
    date=[]
    embed1=soup.find(attrs={'width':'100%','border':'0'})
    soup1 = BeautifulSoup(str(embed1), 'html.parser')
    embed2=soup1.find_all(attrs={'width':'12%'},name='th')
    for i in range(1,len(embed2)):
        date.append(embed2[i].get_text())
    #print(len(date))
    #get 门诊类型
    embed1=soup.find(name='a',attrs={'class':'on',})
    outpatient=embed1.get_text()
    print(outpatient)
    #get 科室，时间，医师
    embed1=soup.find_all(name='thead')
    soup1 = BeautifulSoup(str(embed1), 'html.parser')
    embed2=soup1.find_all(name='tr')#table entry的数量
    fout=open(savePath,'a+',encoding='utf-8')
    for i in range(1,len(embed2)):#每一行
        soup2=BeautifulSoup(str(embed2[i]), 'html.parser')
        sectionTemp=soup2.find(name='td',attrs={'rowspan':'2',})
        if sectionTemp!=None:
            section=sectionTemp.get_text()
        #print(soup2)
        time=soup2.find(name='td',attrs={'width':'6%',}).get_text()
        physician=soup2.find_all(name='td',attrs={'width':'12%','rowspan':False})
        DoctorNames=getDoctorTable(physician)
        for j in range(len(date)):
            entry={}
            entry['分区']=department
            entry['门诊类型']=outpatient
            entry['科室']=section
            entry['日期']=date[j]
            entry['时间']=time
            DocList=[]
            for k in DoctorNames[j]:
                if k in name_ID_pairs.keys():
                    k=k+str(name_ID_pairs[k])
                DocList.append(k)
            entry['医师']=DocList
            fout.write(str(entry)+'\n')
            #print(entry)
    fout.close()
def getScheduleTable2(scheduleURL,savePath,serialNum,d,department,cookies):
    #cookies=get_cookies()
    HTMLText=get_HTMLText(scheduleURL,cookies)
    soup = BeautifulSoup(HTMLText, 'html.parser')
    #print(soup)
    #get name_ID_pairs
    fin=open(r'.\name_ID_pairs.txt','r',encoding='UTF-8')
    name_ID_pairs={}
    allLines=fin.readlines()
    for i in range(len(allLines)):#len(allLines)
        entry=allLines[i]
        entry=eval(entry)
        name_ID_pairs.update(entry)
    fin.close()

    #get 分区
    department=department[d]
    print(department)
    #get date 日期
    date=[]
    embed1=soup.find(attrs={'width':'100%','border':'0'})
    soup1 = BeautifulSoup(str(embed1), 'html.parser')
    embed2=soup1.find_all(attrs={'width':'12%'},name='th')
    for i in range(1,len(embed2)):
        date.append(embed2[i].get_text())
    #print(len(date))
    #get 门诊类型
    embed1=soup.find(name='a',attrs={'class':'on',})
    if embed1==None:
        embed1=soup.find(name='a',attrs={'id':'type'+str(serialNum),})
    outpatient=embed1.get_text()
    print(outpatient)

    #get 科室，时间，医师
    embed1=soup.find_all(name='tbody')
    soup1 = BeautifulSoup(str(embed1), 'html.parser')
    embed2=soup1.find_all(name='tr')#table entry的数量
    fout=open(savePath,'a+',encoding='utf-8')
    for i in range(0,len(embed2)):#每一行
        soup2=BeautifulSoup(str(embed2[i]), 'html.parser')
        sectionTemp=soup2.find(name='td',attrs={'rowspan':'2',})
        if sectionTemp!=None:
            section=sectionTemp.get_text()
        #print(soup2)
        time=soup2.find(name='td',attrs={'width':'6%',}).get_text()
        physician=soup2.find_all(name='td',attrs={'width':'12%','rowspan':False})
        DoctorNames=getDoctorTable(physician)
        for j in range(len(date)):
            entry={}
            entry['分区']=department
            entry['门诊类型']=outpatient
            entry['科室']=section
            entry['日期']=date[j]
            entry['时间']=time
            DocList=[]
            for k in DoctorNames[j]:
                if k in name_ID_pairs.keys():
                    k=k+str(name_ID_pairs[k])
                DocList.append(k)
                #print(DocList)
            entry['医师']=DocList
            fout.write(str(entry)+'\n')
            #print(entry)
    fout.close()


def getAll():
    departmentId=['20','21','555','1272','1273',
                  '1930','2689','2795','2850','2858',
                  '1525','2935','2936']
    departmentSuffix='&page='

    cookieOverdue=False
    cookieFlag='请开启JavaScript并刷新该页.'

    webBase='http://www.ahslyy.com.cn/'
    websites=['/mz/index_17.aspx?lcid=1&type=1', #s=1 b 0
    '/mz/index_17.aspx?lcid=1&type=2', #s=2 b1
    '/mz/index_17.aspx?lcid=1&type=3', #s=3 b2
    '/mz/index_17.aspx?lcid=1&type=4', #s=4 b3
    '/mz/index_1270.aspx',#c4
    '/mz/index_1252.aspx',#a5
    '/mz/index_17.aspx?lcid=2&type=0',#b6
    '/mz/index_1252.aspx?lcid=2',#a7
    '/mz/index_17.aspx?lcid=3&type=0',#b8
    '/mz/index_1252.aspx?lcid=3']#a9
    TypeA=[5,7,9]
    TypeB=[0,1,2,3,6,8]
    TypeC=[4]
    department=['总院','总院','总院','总院','总院','总院','南区','南区','西区','西区']
    cookies=get_cookies()
    savePath='.\Table.json'
    for i in TypeB:
        print(str(i)+webBase+websites[i])
        getScheduleTable2(webBase+websites[i],savePath,i+1,i,department,cookies)

    for i in TypeA:
        print(str(i)+webBase+websites[i])
        getScheduleTable1(webBase+websites[i],savePath,i,department,cookies)