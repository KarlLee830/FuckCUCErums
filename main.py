import os
import base64
import datetime
from bs4 import BeautifulSoup
import img2pdf

def add_padding(base64_str):
    missing_padding = len(base64_str) % 4
    if missing_padding:
        base64_str += '=' * (4 - missing_padding)
    return base64_str

htmls_folder_path = './htmls'
print(f"读取HTML文件夹：{htmls_folder_path}")

html_files = [f for f in os.listdir(htmls_folder_path) if f.endswith('.html')]

for html_file in html_files:
    html_file_path = os.path.join(htmls_folder_path, html_file)
    print(f"读取HTML文件：{html_file_path}")
    
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    print("解析HTML文件")
    soup = BeautifulSoup(html_content, 'html.parser')

    img_tags = soup.find_all('img')
    print(f"找到 {len(img_tags)} 张图片")

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    folder_name = f'{os.path.splitext(html_file)[0]}_{timestamp}'
    os.makedirs(f'./image/{folder_name}', exist_ok=True)
    print(f"创建图片存储目录：./image/{folder_name}")

    img_files = []
    for i, img_tag in enumerate(img_tags):
        src = img_tag.get('src')
        if src and src.startswith("data:image"):
            print(f"处理第 {i+1} 张图片")
            mime, encoded_str = src.split(',', 1)
            img_data = base64.b64decode(add_padding(encoded_str))
            img_file_path = f'./image/{folder_name}/{i + 1}.jpg'
            with open(img_file_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f"保存图片到：{img_file_path}")
            img_files.append(img_file_path)

    os.makedirs(f'./pdf', exist_ok=True)  
    print(f"创建PDF存储目录：./pdf")

    pdf_file_path = f'./pdf/{folder_name}.pdf'
    with open(pdf_file_path, "wb") as pdf_file:
        pdf_file.write(img2pdf.convert(img_files))

    print(f"PDF 文件已保存到：{pdf_file_path}")