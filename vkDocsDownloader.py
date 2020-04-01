import vk_api
import requests
import time
import os
import cv2


auto_skip_delay = 1500

maxPreviewSize = [1024, 720]

vk_session = vk_api.VkApi('phone', 'password')
vk_session.auth()

vk = vk_session.get_api()

search_type = ".jpg"

#last offset 0

last_search_begin = "-180311475_497458882";

handle_mode = int(input("Enter download mode(0-all auto, 1-preview(BETA)) >>"))
if handle_mode == 1:
    input("Это работает через три пизды и медленно. У меня по крайней мере. Некоторые файлы хуй откроет из-за того, что там есть пробелы в названии. Жди патчей или не выёбывайся. А, и да, нажми эетер шоб продолжить")

search = vk.docs.search(q=search_type, count= 1000)

images = {"IMG", "DSC", "MG", "KEM", "EM", "SAM", "WP", "Screenshot", "HDR", "img", "2019", "DJI", "Снимок", "P90", "Безымянный", "B612"}

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

    if handle_mode == 1:
        img = cv2.imread(file_name)
        show = True
        
        try:
            height, width = img.shape[:2]
        except AttributeError:
            show = False
            print("Произошёл троллинг(ошибка на самом деле). Изображение показать не получится, т.к почему-то не получилось получить его размеры")

        if show == True:
            print("Orig size "+str(width)+"x"+str(height))
            
            if height > maxPreviewSize[1]:
                delta = height-maxPreviewSize[1]
                k = 1-(delta/height)
                img = cv2.resize(img, (int(width*k), int(height*k)), interpolation = cv2.INTER_CUBIC) 

                if width > maxPreviewSize[0]:
                    delta = width-maxPreviewSize[0]
                    k = 1-(delta/width)
                    img = cv2.resize(img, (int(width*k), int(height*k)), interpolation = cv2.INTER_CUBIC)


            cv2.namedWindow('Photo '+file_name, cv2.WINDOW_AUTOSIZE)
            cv2.moveWindow('Photo '+file_name, 0, 0)
        
            cv2.imshow('Photo '+file_name, img)
            print("ANY KEY TO CONTINUE...")
            key = cv2.waitKey(auto_skip_delay)
            if key == 32:
                print("MOVE TO MANUAL SORTED DIRECTORY...")
                os.rename(file_name, dir+"sorted_manual\\"+photo_title)
            cv2.destroyAllWindows()
        else:
            img = cv2.imread("stock\\error.jpg")
            cv2.namedWindow('ERROR', cv2.WINDOW_NORMAL)
            cv2.moveWindow('ERROR', 0, 0)
            cv2.imshow('ERROR', img)
            print("ANY KEY TO CONTINUE...")
            cv2.waitKey(auto_skip_delay)
            cv2.destroyAllWindows()
        
    print("")
    count += 1

total_time_sec = time.time()-work_start_time;
total_time_min = total_time_sec / 60;
total_time_sec %= 60

cv2.destroyAllWindows()

print("ALL DOWNLOADS DONE in %.0f m. %.3f s." % (total_time_min,total_time_sec))
print("STOP POINT FOR NEXT SEARCH IS " + str(search["items"][0]["owner_id"])+"_"+str(search["items"][0]["id"]))
    
