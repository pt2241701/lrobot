from geopy.geocoders import Bing
from geopy.distance import geodesic
from unidecode import unidecode
import requests
from time import sleep
import json
import requests
from geopy.geocoders import Bing

urlget = "http://localhost:5000/api?key=text"
BING_KEY = "SRxSaTOSZTxD1FISgsZ8~YxGH_4ZLnA0qG-96dWBv2Q~AvCaMJNdrPrKiQmq3BFY8cUOrS-br53kny0sp-oRbccGr90RfWHIsrXJrS0I4dwS"
response_get = requests.get(urlget)
if response_get.status_code == 200:
    json_data = response_get.json()
    lat = json_data.get('lat')
    long = json_data.get('long')
    geolocator = Bing(api_key=BING_KEY)
    g_now = geolocator.reverse((lat, long))
    print("Vị trí hiện tại:", g_now.address)
else:
    print(f"GET không thành công, mã trạng thái: {response_get.status_code}")

destination = "Sao Viet Hotel 15/D1 one quater, Long Binh Tan ward Bien Hoa"
g_dest = geolocator.geocode(destination)
print("Vị trí cần tới:", g_dest.address)
distance = geodesic((lat, long), (g_dest.latitude, g_dest.longitude)).meters
print(distance, "km")
urlpost = 'http://localhost:5000/api'
start_point = f"{lat},{long}"
end_point = f"{g_dest.latitude},{g_dest.longitude}"
url = f"http://dev.virtualearth.net/REST/V1/Routes/Walking?wp.0={start_point}&wp.1={end_point}&key={BING_KEY}"
response = requests.get(url)
km = [] 
route = []
if response.status_code == 200:
    data = json.loads(response.text)
    print("Đang GET res")
    for item in data["resourceSets"][0]["resources"][0]["routeLegs"][0]["itineraryItems"]:
        instruction = item["instruction"]["text"]
        distance = item["travelDistance"]
        route.append(instruction) 
        km.append(distance)
        print(instruction + "\n")
else:
    print("Không thể lấy lộ trình từ API")


print("Done!")
response_get = requests.get(urlget)
if response_get.status_code == 200:
    json_data = response_get.json() 
    if json_data.get('status') == "True":
        for i, j in zip(route, km):
            i_unaccented = unidecode(i)
            data = {"content": i_unaccented, "distance": j}
            response_post = requests.post(urlpost, data=data)
            if response_post.status_code == 200:
                print("POST thành công, đợi 10 giây!")
                sleep(10)
            else:
                print(f"POST không thành công, mã trạng thái: {response_post.status_code}")
    else:
        print("status không phải là True")
else:
    print(f"GET không thành công, mã trạng thái: {response_get.status_code}")
