from selenium import webdriver
import json
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
def get_cookies():
    baseURL = "http://www.ahslyy.com.cn/mz/index_13.aspx?pid=20"
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


def collectDoctorUrls():
    departmentPrefix='http://www.ahslyy.com.cn/mz/index_13.aspx?pid='
    departmentId=['20','21','555','1272','1273',
                  '1930','2689','2795','2850','2858',
                  '1525','2935','2936']
    #departmentId=['2935']
    departmentSuffix='&page='

    cookieOverdue=False
    cookieFlag='请开启JavaScript并刷新该页.'
    doctorURLs=[]
    cookies=get_cookies()
    for ID in departmentId:# traverse departments
        print('departmentID:',ID)
        PageNum=1
        notLastPage=True
        while (notLastPage):# traverse pages
            print('Page:',PageNum)
            departmentURL=departmentPrefix+ID+departmentSuffix+str(PageNum)
            HTMLText=get_HTMLText(departmentURL,cookies)
            soup = BeautifulSoup(HTMLText, 'html.parser')
            # check the weather the cookies is overdue
            flag=soup.find('strong')
            if flag!=None:#update cookies
                print("cookies overdue!!!")
                cookies=get_cookies()
                HTMLText=get_HTMLText(departmentURL,cookies)
                soup = BeautifulSoup(HTMLText, 'html.parser')
            # find all DoctorURL and push into doctorURLs
            DoctorURL=soup.find_all(class_=re.compile("zpic"))
            if DoctorURL==[]:
                print('!!!!!!!!!!!!!!!!!')
            for i in DoctorURL:
                DoctorHref=i.get('href')
                doctorURLs.append(DoctorHref)
            # get next page
            nextHref=soup.find(class_=re.compile("a_next")).get('href')
            print('nextHref:',nextHref)
            if 'javascript' in nextHref:# reach the trailer page
                notLastPage=False;
                print('LastPage:',PageNum)
            PageNum=PageNum+1# next page
            with open('.\DocURLs.txt', 'w') as fout:
                for site in doctorURLs:
                    fout.write(site+'\n')

def getDocInfo():
    tempPath='.\DocURLs.txt'
    docURLPrefix='http://www.ahslyy.com.cn/'
    Doctors=[]
    cookies=get_cookies()
    with open(tempPath, "r", encoding="utf-8") as fin:
        i=1
        allLines=fin.readlines()
        for lineNum in range(len(allLines)):

            line=allLines[lineNum]
            doctor={}
            line=line.strip()
            docURL=docURLPrefix+line
            print(docURL)
            HTMLText=get_HTMLText(docURL,cookies)
            soup = BeautifulSoup(HTMLText, 'html.parser')
            # check the weather the cookies is overdue
            flag=soup.find('strong')
            while (flag!=None):#update cookies
                if '开启JavaScript并刷新该页' in soup.find('strong').get_text():
                    print("cookies overdue!!!")
                    cookies=get_cookies()
                    time.sleep(8)
                    HTMLText=get_HTMLText(docURL,cookies)
                    soup = BeautifulSoup(HTMLText, 'html.parser')
                    flag=soup.find('strong')
                else:
                    break
            #
            print('i=',i,'lineNum=',lineNum)
            doctor['id']=i
            Doctorinfo=soup.find(class_=re.compile("Doctorinfo")).get_text()
            Doctorinfo=Doctorinfo.strip()
            Doctorinfo=Doctorinfo.split('\n')
            doctor[Doctorinfo[0].split('：')[0]]=Doctorinfo[0].split('：')[1]
            doctor[Doctorinfo[1].split('：')[0]]=Doctorinfo[1].split('：')[1]
            doctor[Doctorinfo[2].split('：')[0]]=Doctorinfo[2].split('：')[1]
            Doctorinfo=soup.find(class_=re.compile("place")).get_text()
            Doctorinfo=Doctorinfo.split('>>')
            doctor['所属科室']=Doctorinfo[4]
            types=['专业特长']
            entries=soup.find_all(class_=re.compile("SinglePage"))
            doctor['专业特长']=entries[0].get_text().strip()
            doctor['详细介绍']=entries[1].get_text().strip()
            #print(doctor)
            Doctors.append(doctor)
            i=i+1

    with open (r".\DoctorInfo.json",'w',encoding='utf-8') as file:
        for line in Doctors:
            file.write(str(line)+'\n')


def get_name_ID_pairs():
    fin1=open('.\DocURLs.txt')
    fin2=open(r".\DoctorInfo.json",'r',encoding='UTF-8')
    allLines1=fin1.readlines()
    allLines2=fin2.readlines()
    name_ID_pairs=[]
    for i in range(len(allLines1)):
        entry1=allLines1[i]
        entry2=allLines2[i]
        entry2 = json.dumps(entry2,ensure_ascii=False)
        print(entry2)
        entry2_dict=eval(eval(entry2))

        print(entry2_dict)
        print(type(entry2_dict))
        name=entry2_dict['姓名'].replace( ' ' , '' )
        name_ID={}
        name_ID[name]=i
        name_ID_pairs.append(name_ID)

    with open (r".\name_ID_pairs.txt",'w',encoding='utf-8') as file:
        for line in name_ID_pairs:
            file.write(str(line)+'\n')

    fin1.close()
    fin2.close()