import requests
import os
from PIL import Image
from lxml import etree
import json


def combine_imgs_pdf(folder_path, pdf_file_path):
    """
    合成文件夹下的所有图片为pdf
    Args:
        folder_path (str): 源文件夹
        pdf_file_path (str): 输出路径
    """
    files = os.listdir(folder_path)
    png_files = []
    sources = []

    for file in files:
        if 'png' in file or 'jpg' in file:
            png_files.append(folder_path + "/"+file)
    png_files.sort()
    #print(png_files)
    output = Image.open(png_files[0])
    png_files.pop(0)
    for file in png_files:
        png_file = Image.open(file)
        if png_file.mode == "RGB":
            png_file = png_file.convert("RGB")
        sources.append(png_file)
    output.save(pdf_file_path, "pdf", save_all=True, append_images=sources)
    print(f'合并完成，已保存在运行目录下:{pdf_file_path}，请到保存目录查看...')


def img_get(file_id, num=0, pixel=100):
    global pagenum_len
    cookies = {
        'JSESSIONID': 'fogsowdtslb81e7ru5dy2xmlw',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'accessToken': 'accessToken',
        'formMode': 'true',
    }
    '''print(
        f'https://wkobwp.sciencereading.cn/asserts/{file_id}/image/{num}/{pixel}')'''
    response = requests.get(
        f'https://wkobwp.sciencereading.cn/asserts/{file_id}/image/{num}/{pixel}', params=params, cookies=cookies, headers=headers)
    try:
        if response.status_code == 200:
            if ('error' in response.text or response.status_code != 200):
                print("获取图片异常，正在重试...")
                while ('error' in response.text or response.status_code != 200):
                    response = requests.get(
                    f'https://wkobwp.sciencereading.cn/asserts/{file_id}/image/{num}/{pixel}', params=params, cookies=cookies, headers=headers)
                
            save_path = "."
            if not os.path.exists(f'{save_path}\\{file_id}'):
                os.mkdir(f'{save_path}\\{file_id}')
            with open(f'{save_path}\\{file_id}\\{str(num + 1).zfill(pagenum_len)}.png', 'wb') as img:
                img.write(response.content)
                print(f'第{num + 1}页图片，保存成功')
        else:
            print('获取文件失败')
    except:
        print("合并出现异常")


def book_name(id):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'cookie': 'JSESSIONID=471DC9810199EEB610AF83B8D2D840AB',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'id': id,
    }

    response = requests.get(
        'https://book.sciencereading.cn/shop/book/Booksimple/show.do', params=params, headers=headers)
    page = etree.HTML(response.text)
    print(response.text)
    name = page.xpath(
        '/html/body/div[1]/div/div/div/div[1]/div[2]/div[1]/span/b[1]/text()')
    unable_str = ['\\', '/', ':', '*', '?', '"', "<", ">", "|"]
    print("获取到书名:"+name)
    for i in name:
        if i in unable_str:
            name = name.replace(i, '_',)
    return name


def PageNum_get(file_id):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'Connection': 'keep-alive',
        'Origin': 'https://book.sciencereading.cn',
        'Referer': 'https://book.sciencereading.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'accessToken': 'accessToken',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-auth-doc': '',
    }

    params = {
        'language': 'zh-CN',
    }

    response = requests.get('https://wkobwp.sciencereading.cn/asserts/' +
                            file_id+'/manifest', params=params, headers=headers)
    json1 = json.loads(response.json()['docinfo'])
    return json1['PageCount']


def Crawler(file_id, end, start=0, pixel=100):
    try:
        print("开始爬取图片...")
        for i in range(int(start), int(end) + 1):
            print(f'正在获取第{i + 1}页图片...')
            img_get(file_id=file_id, num=i, pixel=pixel)
        print("爬取完成，自动合并pdf...")
        folder = f'./{file_id}'
        pdfFile = folder + '/' + f'{file_id}.pdf'
        combine_imgs_pdf(folder, pdfFile)
    except:
        print('获取图片发生异常')


def Id_convert(id):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://book.sciencereading.cn',
        'Referer': 'https://book.sciencereading.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'accessToken': 'accessToken',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'params': '{"params":{"userName":"Guest","userId":"","file":"http://159.226.241.32:81/' + id + '.pdf"}}',
        'type': 'http',
    }

    response = requests.post(
        'https://wkobwp.sciencereading.cn/api/file/add', headers=headers, data=data)
    if response.status_code == 200:
        res = response.json()['result']
        print(f'解析成功,真实id:{res}')
        return res
    else:
        return 'null'


def Painting():
    print('''
    __    __    ___  ____   ____  ___    _____ 
    |  |__|  |  /  _]|    \ |    \|   \  |     |
    |  |  |  | /  [_ |  o  )|  o  )    \ |   __|
    |  |  |  ||    _]|     ||   _/|  D  ||  |_  
    |  `  '  ||   [_ |  O  ||  |  |     ||   _] 
     \      / |     ||     ||  |  |     ||  |   By 顾笙 v1.1
      \_/\_/  |_____||_____||__|  |_____||__|   科学文库WebPdf下载助手
                                                

    ''')


if __name__ == '__main__':
    Painting()

    file_id = input('请输入文章Id:')
    print('正在解析id...')
    result = Id_convert(file_id)
    pagenum = PageNum_get(result)
    if pagenum != '0':
        print("获取到页数:", pagenum)
        pagenum_len = len(str(pagenum))
    # file_name = book_name(id)
    if result != 'null':
        file_id = result
        x = input('是否下载全书(y/n):')
        while(x.upper().strip() != 'Y' and x.upper().strip() != 'N'):
             x = input('输入有误,重新选择是否下载全书(y/n):')
        if x.upper() == 'Y':
            start = '1'
            end = pagenum
        else:
            start = input('请输入开始页数(从1开始)：')
            end = input('请输入结束页数：')
            while (not start.isdigit() or not start.isdigit() or int(start) > int(end)):
                start = input('序号输入有误,请输入开始页数(从1开始)：')
                end = input('请输入结束页数：')
        Crawler(file_id=file_id, end=str(int(end) - 1), start=str(int(start) - 1), pixel="200")
        os.system('pause')
    else:
        print('解析Id出错!')
