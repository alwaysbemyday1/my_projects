from pkg_resources import safe_extra
import requests
import json
import uuid

def save_json(data, filename):
    with open(filename, "a", encoding="UTF-8") as fileout:
        json.dump(data, fileout, ensure_ascii=False, indent=4)

def load_json(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)

SECRETS = load_json('secrets.json')
SERVICE_KEY = SECRETS['SECRET_KEY']

def get_areacode():
    url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaCode'
    areacode = 1
    while True:
        # params for /areaCode
        params = {"ServiceKey": SERVICE_KEY,"numOfRows": "20","pageNo": "1","MobileOS": "ETC","MobileApp": "Pintween","areaCode" : areacode,"_type": "json",}
        response = requests.get(url, params=params)

        if eval(response.text)["response"]["body"]["totalCount"] == 0:
            pass
        else:
            print(f"{areacode}\n{response.text}\n")
        areacode += 1
        if areacode >= 40:
            break


def get_kto_poi():
    AREA_CODE = {1:"서울::Seoul", 2:"인천::Incheon", 3:"대전::Daejeon", 4:"대구::Daegu", 5:"광주::Gwangju", 6:"부산::Busan", 7:"울산::Ulsan", 8:"세종특별자치시::Sejong", 31:"경기도::Gyeonggi-do", 32:"강원도::Gangwon-do", 33:"충청북도::Chungcheongbuk-do", 34:"충청남도::Chungcheongnam-do", 35:"경상북도::Gyeongsangbuk-do", 36:"경상남도::Gyeongsangnam-do", 37:"전라북도::Jeollabuk-do", 38:"전라남도::Jeollanam-do", 39:"제주도::Jeju-do"}
    url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList'
    for area_code, city_name in AREA_CODE:
        params = {'serviceKey' : SERVICE_KEY,'pageNo' : '','numOfRows' : '10000','MobileApp' : 'AppTest','MobileOS' : 'ETC','arrange' : 'A','cat1' : '','contentTypeId' : '32','areaCode' : area_code,'sigunguCode' : '4','cat2' : '','cat3' : '','listYN' : 'Y','modifiedtime' : '','_type':'json'}
        response = requests.get(url, params=params)
        print(type(response.text))


def make_kto_json():
    AREA_CODE = {1:"서울::Seoul", 2:"인천::Incheon", 3:"대전::Daejeon", 4:"대구::Daegu", 5:"광주::Gwangju", 6:"부산::Busan", 7:"울산::Ulsan", 8:"세종특별자치시::Sejong", 31:"경기도::Gyeonggi-do", 32:"강원도::Gangwon-do", 33:"충청북도::Chungcheongbuk-do", 34:"충청남도::Chungcheongnam-do", 35:"경상북도::Gyeongsangbuk-do", 36:"경상남도::Gyeongsangnam-do", 37:"전라북도::Jeollabuk-do", 38:"전라남도::Jeollanam-do", 39:"제주도::Jeju-do"}
    url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList'

    for area_code, city_name in AREA_CODE.items():
        params = {'serviceKey' : SERVICE_KEY,'pageNo' : '','numOfRows' : 10000,'MobileApp' : 'AppTest','MobileOS' : 'ETC','arrange' : 'A','cat1' : '','contentTypeId' : '','areaCode' : area_code,'sigunguCode' : '','cat2' : '','cat3' : '','listYN' : 'Y','modifiedtime' : '','_type':'json'}
        city_name_en = city_name.split("::")[-1]
        response = requests.get(url, params=params)
        result_list = []

        for i in eval(response.text)["response"]["body"]["items"]["item"]:
            result_list.append(i)

        save_json(result_list, f"poi_{city_name_en}.json")


def main():
    poi_list= load_json("kto_poi/poi_Daegu.json")
    url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailCommon'
    result_list = []
    count = 0
    for poi in poi_list:
        count +=1
        params = {'serviceKey' : SERVICE_KEY,'contentId': poi["contentid"], 'MobileApp':'AppTest', 'MobileOS':'ETC','defaultYN':'Y','addrinfoYN':'Y','overviewYN':'Y', '_type':'json'}
        res = requests.get(url, params=params)
        poi_info = eval(res.text)["response"]["body"]["items"]["item"]
        try:
            poi["zipcode"] = poi_info["zipcode"]
        except:
            poi["zipcode"] = ""
        try:
            poi["tel"] = poi_info["tel"]
        except:
            poi["tel"] = ""
        try:
            poi["telname"] = poi_info["telname"]
        except:
            poi["telname"] = ""
        try:
            poi["overview"] = poi_info["overview"]
        except:
            poi["overvies"] = ""
        result_list.append(poi)
        if count%100==0:
            print(f"{poi_list.index(poi)+1} / {len(poi_list)}")
    save_json(result_list,"poi_Daegu")

if __name__ == "__main__":
    main()

