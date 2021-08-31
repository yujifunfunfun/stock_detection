import re


url = 'https://item.rakuten.co.jp/vox-official-store/10000000/'

for i in range(0,3):
    target = '/'
    idx = url.find(target)
    url= url[idx+1:]  
 

target = '/'
idx = url.find(target)
url = url[:idx]  

print(url)