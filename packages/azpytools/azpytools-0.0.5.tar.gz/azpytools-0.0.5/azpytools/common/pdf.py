# 安装pdfkit
# pip install pdfkit
# 2、安装wkhtmltopdf
# 下载地址:https://wkhtmltopdf.org/downloads.html
import os
import pdfkit
from PIL import Image
class PDF:
    # 每个url的最大页数为50
    options = {'disable-smart-shrinking':'',
                'lowquality': '',
                'image-quality': 60,
                'page-height': str(1349.19*0.26458333),
                'page-width': '291',
                'margin-bottom': '0',
                'margin-top': '0',
                }

    @staticmethod
    def htmlToPdfFromFile(htmlfile,pdffile):
        pdfkit.from_file(htmlfile, pdffile, options= PDF.options)

    @staticmethod
    def htmlToPdfFromUrl(url,pdffile):
        pdfkit.from_url(url, pdffile)

    @staticmethod
    def htmlToPdfFromString(htmlstring,pdffile):
        pdfkit.from_string(htmlstring,pdffile, options= PDF.options)
    
    @staticmethod
    def imageToPDF(pdfFileName,imgPath,fileList):
            namelist = fileList 
            firstimg = Image.open(os.path.join(imgPath,namelist[0]))
            firstimg = firstimg.convert('RGB')
            # firstimg.mode = 'RGB'
            imglist = []
            for imgname in namelist[1:]:
                img = Image.open(os.path.join(imgPath,imgname))
                img = img.convert("RGB")
                img.load()
                if img.mode != 'RGB':  # png图片的转为RGB mode,否则保存时会引发异常
                    img.mode = 'RGB'
                imglist.append(img)

            savepath = pdfFileName
            firstimg.save(savepath, "PDF", resolution=100.0,
                        save_all=True, append_images=imglist)
        
