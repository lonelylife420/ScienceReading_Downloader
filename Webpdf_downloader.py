import requests
import os
import time
from PIL import Image


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
    print(
        f'https://wkobwp.sciencereading.cn/asserts/{file_id}/image/{num}/{pixel}')
    response = requests.get(
        f'https://wkobwp.sciencereading.cn/asserts/{file_id}/image/{num}/{pixel}', params=params, cookies=cookies, headers=headers)
    try:
        if response.status_code == 200:
            while('error' in response.text or response.status_code != 200):
                print("获取图片异常，正在重试...")
                response = requests.get(
        f'https://wkobwp.sciencereading.cn/asserts/{file_id}/image/{num}/{pixel}', params=params, cookies=cookies, headers=headers)
            save_path = "."
            if not os.path.exists(f'{save_path}\\{file_id}'):
                os.mkdir(f'{save_path}\\{file_id}')
            with open(f'{save_path}\\{file_id}\\{num}.png', 'wb') as img:
                img.write(response.content)
                print(f'第{num + 1}页图片，保存成功')
        else:
            print('获取文件失败')
    except:
        print("出现异常")


def Crawler(file_id, end, start=0, pixel=100):
    try:
        print("开始爬取图片...")
        for i in range(int(start), int(end) + 1):
            print(f'正在获取第{i + 1}页图片...')
            accessToken()
            img_get(file_id=file_id, num=i, pixel=pixel)
            time.sleep(1)
        print("爬取完成，自动合并pdf...")
        folder = f'./{file_id}'
        pdfFile = folder + '/' + f'{file_id}.pdf'
        combine_imgs_pdf(folder, pdfFile)
    except:
        print('合并失败')


def accessToken():
    headers = {
        'Accept': '*/*',
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
    }

    params = {
        'accessToken': 'accessToken',
        'formMode': 'true',
    }

    response = requests.get(
        'https://wkobwp.sciencereading.cn/asserts/6ebba527a2ce4224b6aa65f532cd0925/image/0/100', params=params, headers=headers)


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
    try:
        print('正在解析id...')
        result = Id_convert(file_id)
        if result != 'null':
            file_id = result
            start = input('请输入开始序号(从0开始)：')
            end = input('请输入结束序号：')
            while (not start.isdigit() or not start.isdigit() or int(start) > int(end)):
                start = input('序号输入有误,请输入开始序号(从0开始)：')
                end = input('请输入结束序号：')
            Crawler(file_id=file_id, end=end, start=start,pixel="200")
            os.system('pause')
        else:
            print('解析Id出错!')
    except:
        print('运行异常!')
