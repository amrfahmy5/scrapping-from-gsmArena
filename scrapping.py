from urllib.error import URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle
import sys
sys.setrecursionlimit(10000)

#to save object in file
def saveObject(name,Object):
    name = str(name) + '.pkl'
    with open(name, 'wb') as f:
        pickle.dump(Object, f, pickle.HIGHEST_PROTOCOL)
#to load object with run code again
def loadObject(name):
    name = str(name) + '.pkl'
    with open(name, 'rb') as f:
        return pickle.load(f)               



#get all categories
def caeateCategories():
    categories = []
    url = "https://www.gsmarena.com/makers.php3"
    try:
        html = urlopen(url)
    except URLError as e:
            print(e.reason)
    soup = BeautifulSoup(html, 'lxml')
    outDiv = soup.find("div", {"class", "st-text"})
    all_links = outDiv.find_all("td")
    for link in all_links: 
        sub = link.find("a").get("href")
        url = "https://www.gsmarena.com/" + str(sub)  # category link
        category = ''.join([i for i in link.text[0:-8] if not i.isdigit()])  # file name
        print(category)
        categories.append({'url':url,'category':category})
    return categories


#get links for phone for its data
def phone_links(categories):
    categories_phone=[]
    for link in categories:
        try:
            phones = urlopen(link['url'])
            soupPhones = BeautifulSoup(phones, 'lxml')
            divPhones = soupPhones.find("div", {"class", "makers"})
            try:
              ulPhones=divPhones.find("ul")
            except AttributeError:
              continue
            phone_links = ulPhones.find_all("li")
            
            navDiv = soupPhones.find("div", {"class": "nav-pages"})
            if navDiv:
                AnotherPages = navDiv.find_all("a")
                for page in AnotherPages:
                    url = "https://www.gsmarena.com/" + str(page.get('href'))
                    print(url)
                    try:
                      Morephones = urlopen(url)
                      MoresoupPhones = BeautifulSoup(Morephones, 'lxml')
                      MoredivPhones = MoresoupPhones.find("div", {"class", "makers"})
                      try:
                        MoreulPhones=MoredivPhones.find("ul")
                      except AttributeError:
                        continue
                      Morephone_links = MoreulPhones.find_all("li")
                      for i in Morephone_links:
                          phone_links.append(i)
                    except :
                          continue
            tempArr=[]  
            for Phone_link in phone_links:
                
                sub = Phone_link.find("a").get("href")
                Name=Phone_link.find("a").find('strong').find('span').string
                tempArr.append({'phoneName':Name,'phoneLinks':sub})
            categories_phone.append({'category':link['category'],'phones':tempArr})
        except URLError as e:
            print(e.reason)
    return categories_phone

#get data for each mobile in each category
def PholeData(categories_phone):
    MobileInfo=[]
    for i in categories_phone:
        CategoryName = i['category']
        Category = i['phones']
        for j in Category:
            try:
                MobileName,Mobile = j['phoneName'],j['phoneLinks']
                url= "https://www.gsmarena.com/"+str(Mobile)
                #print(url)
                mobileHTML=urlopen(url)
                soupMobile = BeautifulSoup(mobileHTML, 'lxml')
                divPhones = soupMobile.find("div", {"id": "specs-list"})
                tablePhones = divPhones.find_all('table')
                phoneData=[]
                for table in tablePhones:
                    tr=table.find_all('tr')
                    thGlobal=''
                    
                    for tableData in tr:
                        if thGlobal == '':
                            th=tableData.find('th').string
                            thGlobal=th
                        else:
                            th=thGlobal
                        try:
                            tdtitleTemp=tableData.find('td',{'class':'ttl'}).find('a')
                        except:
                            continue
                        if(tdtitleTemp is None):
                            continue
                        
                        tdtitle=tdtitleTemp.string
                        #tdinfoTemp =tableData.find('td',{'class':'nfo'}).find('a')
                        tdinfoTemp =tableData.find('td',{'class':'nfo'})
                        if(tdinfoTemp is None):
                            continue
                        tdinfo=tdinfoTemp.string
                        phoneData.append({'th':th,'tdtitle':tdtitle,'tdinfo':tdinfo})
                MobileInfo.append({'Category':CategoryName,'Name':MobileName,'data':phoneData})
                #break
            except URLError as e:
                print(e.reason)
    return MobileInfo

categories = []
categories = caeateCategories()
saveObject('categories',categories)
#categories=loadObject('categories') 

           



categories_phone=[]
categories_phone=phone_links(categories)
saveObject('categories_phone',categories_phone)
#categories_phone=loadObject('categories_phone') 


MobileInfo=[]
MobileInfo=PholeData(categories_phone)
saveObject('MobileInfo',MobileInfo)
#MobileInfo=loadObject('MobileInfo') 
