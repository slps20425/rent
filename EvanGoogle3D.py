#Editor Evan Lee

def Google3D(DDD):
    import googlemaps
    import os
    import string
    from urllib.parse import quote
    import simplejson
    import urllib
    import re
    import ssl
    import urllib.request
    

    from os.path import join, dirname
    from dotenv import load_dotenv, find_dotenv

    # dotenv_path = os.path.join(os.path.dirname('/Users/yi-hsuanlee/Desktop/Yi-Hsuan_Test/Django_project/LittleEvan/rent/HereGoRent'), '.env')
    # load_dotenv(dotenv_path, override=True)
    GOOGLE_DIRECTION_API_KEY = os.environ.get("GOOGLE_DIRECTION_API_KEY")
    # gmaps = googlemaps.Client(key=GOOGLE_DIRECTION_API_KEY)

    # now = datetime.now()
    # directions_ToSchool_result = gmaps.directions(test1,School,departure_time=now)
    # directions_ToOffice_result = gmaps.directions(test1,Office,departure_time=now)


    
    To_Office_Distance_List=[]
    To_Office_Duration_List=[]
    To_Office_Duration_in_traffic=[]
    To_School_Distance_List=[]
    To_School_Duration_List=[]
    To_School_Duration_in_traffic=[]

    for i in range(len(DDD)):
        
        ToOffice_URL ='https://maps.googleapis.com/maps/api/directions/json?origin='+str(DDD[i])+ '&destination=林口廣達電腦'+'&key='+str(GOOGLE_DIRECTION_API_KEY)+'&mode=driving&departure_time=now&traffic_model=pessimistic'
        ToSchool_URL =' https://maps.googleapis.com/maps/api/directions/json?origin='+str(DDD[i])+ '&destination=中壢中央大學'+'&key='+str(GOOGLE_DIRECTION_API_KEY)+'&mode=driving&departure_time=now&traffic_model=pessimistic'
        To_Office_url = quote(ToOffice_URL, safe = string.printable)
        context = ssl._create_unverified_context()
        result_Office =simplejson.load(urllib.request.urlopen(To_Office_url,context=context, timeout=20))
        
        if result_Office['status'] == 'ZERO_RESULTS':
            Distance = 'NaN'
            Duration = 'NaN'
            print('Letsgo')
            #Duration_in_traffic_Office= 'NaN'
        else:
            Distance=re.sub('[\sa-zA-Z]','',result_Office["routes"][0]["legs"][0]['distance']['text']) #Here is an bug
            Duration=re.sub('\D','',result_Office["routes"][0]["legs"][0]['duration']['text']) 
            print('Letsgo2',i,To_Office_Duration_List)
            #Duration_in_traffic_Office=re.sub('\D','',result_Office["routes"][0]["legs"][0]['duration_in_traffic']['text']) 
        To_Office_Distance_List.append(Distance)
        To_Office_Duration_List.append(Duration)

        To_School_url=quote(ToSchool_URL, safe = string.printable)
        context = ssl._create_unverified_context()
        result_School=simplejson.load(urllib.request.urlopen(To_School_url,context=context, timeout=20)) 
        if result_School['status'] == 'ZERO_RESULTS': 
            Distance_School ='NaN'
            Duration_School = 'NaN'
        else:
            Distance_School=re.sub('[\sa-zA-Z]','',result_School["routes"][0]["legs"][0]['distance']['text']) #Here is an bug
            Duration_School=re.sub('\D','',result_School["routes"][0]["legs"][0]['duration']['text'])
            print('ok',i,To_School_Duration_List)
        To_School_Distance_List.append(Distance_School) 
        To_School_Duration_List.append(Duration_School)          
    return(To_Office_Distance_List,To_Office_Duration_List,To_School_Distance_List,To_School_Duration_List)


if __name__ == '__main__':

    Google3D()
