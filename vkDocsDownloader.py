import vk_api
import requests
import time
import os
import sys


phone = ''
password = ''

if(len(sys.argv) == 3):
    phone = str(sys.argv[1])
    password = str(sys.argv[2])
else:
    print("Please, run with two args - vkDocsDownloader <phone> <password>")
    sys.exit()


try:
    vk_session = vk_api.VkApi(phone, password)
    vk_session.auth()
except:
    print("Something broke on auth. Please, check you phone/password")
    sys.exit()

vk = vk_session.get_api()


search_type = ".jpg"

#last offset 0

last_search_begin = "-180311475_497458882";

search = vk.docs.search(q=search_type, count= 1000)

images = {"IMG", "DSC", "MG", "KEM", "EM", "SAM", "WP", "Screenshot", "HDR", "img", "2019", "DJI", "Снимок", "Безымянный", "P90", "B612"}

sort_by = images

count = 1

dir = "vk_photos\\"

work_start_time = time.time()

for photo in search["items"]:
    start_download_time = time.time()
    
    maybe_break = str(photo["owner_id"])+"_"+str(photo["id"])
    if maybe_break == last_search_begin:
        print("REACHED LAST SEARCH BEGIN. BREAK DOWNLOADING")
        break
    
    print("(" + str(count) +"|"+str(len(search["items"])) + ") Download - " + "id"+str(photo["owner_id"])+"_"+str(photo["id"])+"_"+str(photo["title"]))

    photo_title = "id"+str(photo["owner_id"])+"_"+str(photo["id"])+"_"+str(photo["title"])

    r = requests.get(photo["url"])

    find = 0
    found = ""
    for s in sort_by:
        if photo["title"].find(s) > -1:
            find = 1
            found = s
            break;
        
    file_name = ""
    if find == 0:
        file_name = dir+photo_title
    else:
        file_name = dir+"sorted_title\\"+photo_title
        print("MOVE TO SORTED FILES ("+s+")")

    file_name = file_name.replace(' ', '_')

    with open(file_name, "wb") as code:
            code.write(r.content)
            code.close()

    stat = os.stat(file_name)          
    size = stat.st_size
    size /= 1024
    size /= 1024
    
         

    print("DOWNLOADED")

    elapsed_time = time.time()-start_download_time
    
    print("%.2f MB" % size)
    print("%.3f s." % elapsed_time)

    
    print("")
    count += 1

total_time_sec = time.time()-work_start_time;
total_time_min = total_time_sec / 60;
total_time_sec %= 60


print("ALL DOWNLOADS DONE in %.0f m. %.3f s." % (total_time_min,total_time_sec))
print("STOP POINT FOR NEXT SEARCH IS " + str(search["items"][0]["owner_id"])+"_"+str(search["items"][0]["id"]))
    
