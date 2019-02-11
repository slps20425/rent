#Editor Evan Lee
def Rent():    
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
    import re
    import pandas as pd
    import time

    import django 
    django.setup()
    from rent.HereGoRent import EvanGoogle3D
    from rent.models import Room,Parameter
    import numpy as np

    chromedriver = "/Users/yi-hsuanlee/Desktop/Yi-Hsuan_Test/Django_project/lib/python3.6/site-packages/selenium/webdriver/chrome/chromedriver"

    def Addr_RoomType_Contact_list_Method(Addr_Data):
        ERList =[]
        RoomList=[]
        SpaceList=[]
        FloorList=[]

        for i in range(int(len(Addr_Data)/3)):
            t02 = Addr_Data[i*3+1]
            t03= Addr_Data[i*3+2] 
            tmp2 = [t02+t03]
            ERList.append(tmp2)

            t01 = Addr_Data[(i*3)].split('|')
            Room= Addr_Data[(i*3)].split('|')[0]
            Space=Addr_Data[(i*3)].split('|')[1]
            Floor=Addr_Data[(i*3)].split('|')[2]
            RoomList.append(Room)
            SpaceList.append(Space)
            FloorList.append(Floor)
        return(ERList,RoomList,SpaceList,FloorList)

    def closeWindow():
        AreaBox = driver.find_element_by_id('area-box-close')
        AllowBox = driver.find_element_by_xpath('/html/body/div[6]')
        LoginBox= driver.find_elements_by_xpath("/html/body/nav/div/div[4]/ul/li[1]/div/a[1]")[0]
        while AreaBox.is_displayed() ==True:
           AreaBox.click()
           time.sleep(15)
        while LoginBox.is_displayed() ==True:
           time.sleep(5)
           LoginBox.click()
           time.sleep(10)    
        while AllowBox.is_displayed() ==True:
           AllowBox.click() 
           time.sleep(10)       
        return

    # # 以下為 Custom item 
    # City= ['Taipei: 1','NewTaipei: 2','Taichung: 8','Tainan= 15', 'Taoyuan: 6', 'kaohsiung: 17']
    # whichCity = input('Please enter a number that which City\'s rent you are looking for:  '+str(City))
    # DefaultCityID = "[data-id='0']"
    # CityID = re.sub(r"[0-9]",whichCity,DefaultCityID)
    # whatType =  input('Please select what kind of rent option,any: 0, house: 1, 單人房: 2, 合租: 3, 雅房: 4, 車位: 8 ')
    # whatPrice = input('Please select Price Range, any:0 , under NT5,000 :1, NT5,000-NT10,000= 2, NT10,000-NT20,000: 3 ')
    # whatSpace = input('Please select how large Space you need, any = 0, under 10 = 1, 10- 20 = 2, 20-30: 3 , 30-40 : 4')
    # Keyword = input('If you have any additional request, please type it here: (Chinese or English are fine)  ')

    search=Parameter.objects.order_by('-pk')[0] 
    whichCity = search.City
    DefaultCityID = "[data-id='0']"
    CityID = re.sub(r"[0-9]",str(whichCity),DefaultCityID)
    Keyword= search.Keyword
    whatType=search.RoomType
    whatSpace=search.Space
    whatPrice=search.Price

    DefaultUrl = 'https://rent.591.com.tw/?kind=3&region=6&rentprice=3&area=10,20&shType=list' 
    driver=webdriver.Chrome(chromedriver)
    driver.get(DefaultUrl)

    ### To Close unnecessary Window ### 
    for i in range(len(DefaultUrl)):
        try:
            closeWindow()

        except Exception as e:
            pass
        break
        
    while driver.find_element_by_xpath('/html/body/div[6]').is_displayed() ==True:
        driver.find_element_by_xpath('/html/body/div[6]').click()
        while driver.find_elements_by_css_selector(CityID)[1].is_displayed() ==True:
            driver.find_elements_by_css_selector(CityID)[1].click() # Select City based on CityID which User provided
        else:
            driver.find_elements_by_css_selector("[data-ie='search-location-span']")[0].click()# expand the AreaTab
            driver.find_elements_by_css_selector(CityID)[1].click() # Select City based on CityID which User provided


    driver.find_elements_by_css_selector("[data-name='rentType']")[int(whatType)].click() #What kind of rentType
    driver.find_elements_by_css_selector("[data-name='rentPrice']")[int(whatPrice)].click() #What price 
    driver.find_elements_by_css_selector("[data-name='plain']")[int(whatSpace)].click()
    driver.find_element_by_id('keywords').send_keys(Keyword)   #Here's to type an keyWord, you can link your keyword from input()
    driver.find_elements_by_class_name('searchBtn')[1].click()  # << elments can found mutiple

    #Start catch data

    IndexList =[]
    SubURLList=[]
    TitleList=[]
    ImageList=[]
    PriceList=[]
    Addr_RoomType_Contact_List=[]     

    for i in range(6):       
        
        content = driver.page_source          
        soup = BeautifulSoup(content, 'html.parser')
        soup1 = soup.find_all(id="content")  
        soup2 =soup1[0].find_all('ul', class_="listInfo clearfix")
        print('This is xx round',i)
        print("----------Parsing {} Page---------".format(i))

        try:
            driver.find_element_by_xpath('//a [@class="pageNext"]/span[contains(text(), "下一頁")]').click()
        except Exception as e:
            pass
        time.sleep(15)
        while i ==1:
            DataFound = driver.find_element_by_xpath('//*[@id="container"]/section[5]/div/div[1]/div[3]/div[1]')  #Using Xpath to retrieve the tag text
            print('Heres\'s your result found\n',DataFound.text)
            break
        for index, article in enumerate(soup2):
          
            EachImage = soup2[index].find('img')['data-original'] 
            Price = soup2[index].find('div', class_='price').text
            EachPrice = re.sub('[\n\s\D]','',Price)
            index = i*30 +index 
            IndexList.append(index)
            newArt= article.find_all('li',class_='pull-left infoContent') 
            PriceList.append(EachPrice)
            ImageList.append(EachImage)
            #print(IndexList,ImageList)
            for index2,Art in enumerate(newArt):
                #print('-------Im-----------Index2-------watch out -----------------------',index2)
                SubURL = 'https:'+ newArt[index2].find('h3')('a')[0]['href'] 
                SubURL =re.sub('[\s]','',SubURL)
                MessTitle = newArt[index2].find('h3').text
                Title = re.sub('[^\u4e00-\u9fa5]','',MessTitle)
                newArt2 = newArt[0].find_all('p')
                SubURLList.append(SubURL)
                TitleList.append(Title)
                #print(SubURLList,TitleList)
                for index3, Art1 in enumerate(newArt2):
                    #print('-------Im-----------Index3-------watch out -----------------------',index3)
                    Mess_Addr_RoomType_Contact= newArt2[index3].text
                    Addr_RoomType_Contact = re.sub('[\n\xa0\s]','',Mess_Addr_RoomType_Contact)
                    Addr_RoomType_Contact_List.append(Addr_RoomType_Contact)
                    #print(Addr_RoomType_Contact_List)

    ## Sorting Data ##
    AddressList=Addr_RoomType_Contact_list_Method(Addr_RoomType_Contact_List)[0]
    RoomList= Addr_RoomType_Contact_list_Method(Addr_RoomType_Contact_List)[1]
    FloorList=Addr_RoomType_Contact_list_Method(Addr_RoomType_Contact_List)[3]
    SpaceList=Addr_RoomType_Contact_list_Method(Addr_RoomType_Contact_List)[2]

    for i,j in enumerate(SpaceList):
        j= re.sub('[\u4e00-\u9fa5]',"",j) #Chinese Unicode \u4e00-\u9fa5, Here using \u576a is a single chinese word
        print(j)
        SpaceList[i]=j

    DataToDict= {"Index":IndexList,"Title":TitleList,"SubURL":SubURLList,"Image":ImageList,'Price':PriceList,"Space":SpaceList,"RoomType":RoomList,"Floor":FloorList,"Address":AddressList}    
    DataDF=pd.DataFrame(DataToDict)
    DataDF.to_csv('Data_test.csv',index = False) 
    NewDataDF = pd.read_csv('Data_test.csv',sep=',',dtype={'Index':int,'Title':str,'SubURL':str,'Image':str,'Price':float,'Space':float,'RoomType':str,'Floor':str,'Address':str})
    NewDataDF =NewDataDF.drop_duplicates('SubURL') # remove duplicated items

    SpaceMeanValue=NewDataDF['Space'].mean() # Space mean value 
    NewDataDF2=NewDataDF.loc[NewDataDF['Price']>5000]   # sorting by price
    NewDataDF3=NewDataDF2.loc[(NewDataDF2['Price']<10000) & (NewDataDF2['Space']> SpaceMeanValue)] 

    ## Sorting ridiculious value from Space Column
    def RemoveSpaceIndex(SpaceValues):
        for i, j  in enumerate(SpaceValues):
            if SpaceValues[j] > SpaceMeanValue*3 :
                RemoveSpaceIndex = j
                return(RemoveSpaceIndex)
    RemoveSpaceIndex =RemoveSpaceIndex(NewDataDF3['Space'].to_dict())    
    if RemoveSpaceIndex ==True:
        NewDataDF3= NewDataDF3.drop(SpaceValues.index[RemoveSpaceIndex]) # SpaceValues.index[RemoveSpaceIndex] = Pending Removed Index Number
    else:
        print('There is no SpaceValue over 3*SpaceMean')

    NewDataDF3=NewDataDF3.sort_values(['Space','Price'],ascending=False)
    NewDataDF3=NewDataDF3.reset_index(drop=True)
    NewDataDF3['Index']= NewDataDF3.index.tolist() 
    NewDataDF3.head(20).to_csv('Data_test.csv',index = False)  # sorting again , reset index.

    NewDataDF3 = pd.read_csv('Data_test.csv',sep=',')



    #分析Address, 產出Real Address 等等要放盡Google Direction API
    def RealAddress(Data):
        ioo=Data.tolist()
        RealAddr = []    
        for i in range(len(ioo)):
            qq=str(ioo[i])
            kk=qq.split('/')[0]
            jj=re.sub('[\W]','',kk)
            PreAnswer0= re.sub('(\u5c4b\u4e3b)|(\u4ef2\u4ecb)|(\u4ee3\u7406\u4eba)',',',jj)   #屋主 :\u5c4b\u4e3b #仲介:(\u4ef2\u4ecb) #代理人 :(\u4ee3\u7406\u4eba))
            Answer0 = PreAnswer0.split(',')[0]  
            print(Answer0)
            RealAddr.append(Answer0)

        return RealAddr

    RealAddressList=RealAddress(NewDataDF3['Address']) 

    Google_List=EvanGoogle3D.Google3D(RealAddressList)
    D1=Google_List[0] #To_Office_Distance_List
    T1=Google_List[1] # To_Office_Duration_List

    D2=Google_List[2] #To_School_Distance_List
    T2=Google_List[3] #To_School_Duration_List

    D1=np.array(D1,dtype=np.float) # there is bug here
    D2=np.array(D2,dtype=np.float) # there is bug here
    T1=np.array(T1,dtype=np.float)
    T2=np.array(T2,dtype=np.float) 



    Distance = np.nansum(np.dstack((D1,D2)),2) 
    Duration = np.nansum(np.dstack((T1,T2)),2)

    NewDataDF3 =NewDataDF3.assign(Distance=pd.DataFrame(data=Distance.flatten()).values)
    NewDataDF3 =NewDataDF3.assign(Duration=pd.DataFrame(data=Duration.flatten()).values)
    NewDataDF3=NewDataDF3.loc[(NewDataDF3['Distance']!=0) & (NewDataDF3['Duration']!=0)].sort_values(['Duration','Space','Price'],ascending=[True,False,False])
    NewDataDF3=NewDataDF3.reset_index(drop=True)
    NewDataDF3['Index']= NewDataDF3.index.tolist() 
    NewDataDF3.to_csv('Data_test.csv',index = False) 

    NewDataDF4= NewDataDF3.to_dict()
    # Django Part 
    Room.objects.all().delete()
    SampleList = []
    for k in range(len(NewDataDF3.to_dict()['Index'])): 
        Sample =Room(Index=NewDataDF4['Index'][k],Title=NewDataDF4['Title'][k],SubURL=NewDataDF4['SubURL'][k],Image=NewDataDF4['Image'][k],Price=NewDataDF4['Price'][k],Space=NewDataDF4['Space'][k],RoomType=NewDataDF4['RoomType'][k],Floor=NewDataDF4['Floor'][k],Address=NewDataDF4['Address'][k])
        SampleList.append(Sample)
    Room.objects.bulk_create(SampleList) 
    driver.quit()
# Room.objects.all().in_bulk()


#Data handling #
# GroupBySpace = DataDF['Space']
#pandas.core.groupby.generic.DataFrameGroupBy


#engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}".format('使用者名稱', '登入密碼', '127.0.0.1:3306', '資料庫名','字元編碼'))
#con = engine.connect()#建立連線


if __name__ == '__main__':
    Rent()




