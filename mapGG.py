import googlemaps

# Nhập khóa API của bạn
gmaps = googlemaps.Client(key="AIzaSyA0zihibBXqU3_Fl5XsBoCHBofdt_c8YTk", timeout=30)

# Lấy vị trí hiện tại của người dùng
position = gmaps.geolocate()

# In tọa độ vĩ độ và kinh độ
print(position["location"]["lat"])
print(position["location"]["lng"])
