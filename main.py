import requests
import os,re
import time
from PIL import Image
from lxml import etree
import json

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]" # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title) # 替换为下划线
    return new_title

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
            png_files.append(folder_path + "/" + file)
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

class BookDownloader():
    virtual_id = ''
    real_id = ''
    book_name = ''
    page_num = 0
    pixel=100
    is_large = False
    taskid = ''
    docid = ''
    start_page = 0
    end_page = 0
    default_path = './' #默认保存路径为运行目录
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

    def __init__(self,id):
        self.virtual_id = id
        self.id_convert()
        if not self.is_large:
            self.get_page_num()
        self.get_bookname()
        self.book_name = validateTitle(self.book_name)

    def get_bookname(self):

        cookies = {
            'JSESSIONID': '',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': f'https://book.sciencereading.cn/shop/book/Booksimple/show.do?id=%20{self.virtual_id}',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'id': self.virtual_id,
            'readMark': '0',
        }

        response = requests.get('https://book.sciencereading.cn/shop/book/Booksimple/onlineRead.do', params=params, cookies=cookies, headers=headers)
        if response.status_code == 200:
            page = etree.HTML(response.text)
            info = page.xpath('//div[@class="modal-body"]//text()')
            for i in info:
                if "书名" in i:
                    self.book_name = i.strip().split("：")[-1]
            print(f"获取到书名：{self.book_name}")
        else:
            print("获取书名失败")


    def id_convert(self):
        print('正在解析id...')
        data = {
            'params': '{"params":{"userName":"Guest","userId":"","file":"http://159.226.241.32:81/' + self.virtual_id + '.pdf"}}',
            'type': 'http',
        }

        response = requests.post(
            'https://wkobwp.sciencereading.cn/api/file/add', headers=self.headers, data=data)
        
        if response.status_code == 200 :
            res = response.json()['result']
            if res != "OutOfFileSizeLimit":
                print(f'解析成功,真实id:{res}')
                self.real_id = res
            else:
                self.is_large = True
                print("当前文库文件过大，请耐心等候解析(服务器处理响应较久，并非卡死)...")
                data = {
                    'filetype': 'http',
                    'zooms': '-1,100',
                    'tileRender': 'false',
                    'fileuri': '{"params":{"userName":"Guest","userId":"","file":"http://159.226.241.32:81/' + self.virtual_id + '.pdf"}}',
                    'pdfcache': 'true',
                    'callback': '',
                }

                response2 = requests.post(f'https://wkobwp.sciencereading.cn/spi/v2/doc/pretreat?r={int(time.time()*1000)}', headers=self.headers, data=data)
                if response2.json()["resultCode"] == "1":
                    self.taskid = response2.json()["resultBody"]["taskid"]
                    response3 = requests.get(f'https://wkobwp.sciencereading.cn/api/v2/task/{self.taskid}/query?r={int(time.time()*1000)}', headers=self.headers)
                    while "task in process" in response3.text:
                        response3 = requests.get(f'https://wkobwp.sciencereading.cn/api/v2/task/{self.taskid}/query?r={int(time.time()*1000)}', headers=self.headers)
                    print(f"解析成功,真实id:{response3.json()['resultBody']['uuid']}")
                    self.real_id = response3.json()['resultBody']['uuid']
                    self.docid = response3.json()['resultBody']['docid']
                    self.get_page_num()
                else:
                    print('解析Id出错!')
                    self.real_id = 'null'
        else:
            print('解析Id出错!')
            self.real_id = 'null'

    def get_page_num(self):
        print('正在获取页数（当文库为大文件时，获取时间较长，请耐心等待）...')
        data = {
            'startpage': '0',
            'endpage': '4',
            'zooms': '-1,100',
            'tileRender': 'false',
            'tileSize': '400',
            'uuid': self.real_id,
        }
        if self.is_large == True:
            response = requests.post(f'https://wkobwp.sciencereading.cn/api/v2/parser/{self.docid}/parse?r={int(time.time()*1000)}', headers=self.headers,data=data)
            while "taskid" not in response.text:
                response = requests.post(f'https://wkobwp.sciencereading.cn/api/v2/parser/{self.docid}/parse?r={int(time.time()*1000)}', headers=self.headers,data=data)
            self.taskid = response.json()['resultBody']['taskid']
            response = requests.get(f'https://wkobwp.sciencereading.cn/api/v2/task/{self.taskid}/query?r={int(time.time()*1000)}', headers=self.headers)
            while "pcount" not in response.text:
                response = requests.get(f'https://wkobwp.sciencereading.cn/api/v2/task/{self.taskid}/query?r={int(time.time()*1000)}', headers=self.headers)
            self.page_num = int(response.json()['resultBody']['pcount'])
        else:
            params = {
                'language': 'zh-CN',
            }

            response = requests.get('https://wkobwp.sciencereading.cn/asserts/' +
                                    self.real_id+'/manifest', params=params, headers=self.headers)
            while "docinfo" not in response.text:
                response = requests.get('https://wkobwp.sciencereading.cn/asserts/' +
                                    self.real_id+'/manifest', params=params, headers=self.headers)
            json1 = json.loads(response.json()['docinfo'])
            self.page_num = int(json1['PageCount'])
        if self.page_num != 0:
            print("获取到页数:", self.page_num)
        else:
            print("获取页数失败")

    def get_image(self,num=0):
        cookies = {
            'JSESSIONID': '',
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        response = requests.get(
            f'https://wkobwp.sciencereading.cn/asserts/{self.real_id}/image/{num}/{self.pixel}', cookies=cookies, headers=headers)
        try:
            if response.status_code == 200:
                if ('error' in response.text or response.status_code != 200):
                    print("获取图片异常，正在重试...")
                    while ('error' in response.text or response.status_code != 200):
                        response = requests.get(
                        f'https://wkobwp.sciencereading.cn/asserts/{self.real_id}/image/{num}/{self.pixel}', cookies=cookies, headers=headers)
                    
                save_path = "."
                if not os.path.exists(f'{save_path}\\{self.book_name}'):
                    os.mkdir(f'{save_path}\\{self.book_name}')
                with open(f'{save_path}\\{self.book_name}\\{str(num + 1).zfill(len(str(self.page_num)))}.png', 'wb') as img:
                    img.write(response.content)
                    print(f'第{num + 1}页图片，保存成功')
            else:
                print('获取文件失败')
        except:
            print("获取文件异常")

    def start(self):
        if self.real_id != 'null':

            x = input('是否下载全书(y/n):')
            while(x.upper().strip() != 'Y' and x.upper().strip() != 'N'):
                x = input('输入有误,重新选择是否下载全书(y/n):')
            if x.upper() == 'Y':
                self.start_page = 0
                self.end_page = self.page_num
            else:
                start = input('请输入开始页数(从1开始)：')
                end = input('请输入结束页数：')
                while (not start.isdigit() or not start.isdigit() or int(start) > int(end)):
                    start = input('序号输入有误,请输入开始页数(从1开始)：')
                    end = input('请输入结束页数：')
                self.start_page = int(start) - 1
                self.end_page = int(end)
            try:
                print("开始爬取图片...")
                for i in range(self.start_page, self.end_page):
                    print(f'正在获取第{i + 1}页图片...')
                    self.get_image(num=i)
                print("爬取完成，自动合并pdf...")
                folder = f'{self.default_path}{self.book_name}'
                pdfFile = folder + '/' + f'{self.book_name}.pdf'
                combine_imgs_pdf(folder, pdfFile)
            except Exception as error:
                print('获取或处理图片时发生异常')
                print(error)

def Painting():
    print('''
    
        ██╗    ██╗███████╗██████╗ ██████╗ ██████╗ ███████╗
        ██║    ██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝
        ██║ █╗ ██║█████╗  ██████╔╝██████╔╝██║  ██║█████╗  
        ██║███╗██║██╔══╝  ██╔══██╗██╔═══╝ ██║  ██║██╔══╝  
        ╚███╔███╔╝███████╗██████╔╝██║     ██████╔╝██║     By 顾笙 v1.3
        ╚══╝╚══╝ ╚══════╝╚═════╝ ╚═╝     ╚═════╝ ╚═╝      科学文库WebPdf下载助手
                                                        
    ''')


if __name__ == '__main__':
    Painting()
    file_id = input('请输入文章Id:')
    bookdownloader = BookDownloader(file_id)
    bookdownloader.start()
    os.system('pause')
