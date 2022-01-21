from PIL import Image, ImageFilter, ImageDraw
from func import DesktopMobile
from re import sub

def CropCenter(pil_img, crop_width: int, crop_height: int) -> Image:
    """
    Функция для обрезки изображения по центру.
    """
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def ChoiceConvertImg(src: str) -> Image:
    if DesktopMobile(sub(', ', 'х',  str(Image.open(src).size))) == "#phone":
        i = 1
        return ConvertImg(src, i, 1100, 2350)
    else:
        i = 2
        return ConvertImg(src, i, 1060, 700)

def ConvertImg(src, i, screenWidth, screenHeght):

    im1 = Image.open(src)
    im2 = Image.open('electronic/{0}.png'.format(str(i)))

    width2, height2 = im2.size
    
    src = 'processed_photo/r1.png'
    #меняем размер фото до размера ЭКРАНА фото мобилы
    im_for_crop = im1.resize((width2, height2))
    im_crop = CropCenter(im_for_crop, screenWidth, screenHeght)
    #делаем маску
    mask = Image.new("L", im_crop.size, 0)
    #создаем "карандаш"
    draw = ImageDraw.Draw(mask)
    #заливаем маску белым цветом
    draw.rectangle((im_crop.size[0],0,0,im_crop.size[1]), fill="white")
    #добовляем альфаканал в вырезанную картинку
    im_crop_alpha = im_crop.putalpha(mask)
    #блюрим все фото полностью
    imMain = im1.filter(ImageFilter.GaussianBlur(radius=50))
    #меняем размер заблюриной фотки до размера фото мобилы
    imMain = imMain.resize((width2, height2))
    #вставляем фото размера экрана телефона
    imMain.paste(im_crop, ((imMain.size[0] - im_crop.size[0]) // 2, (imMain.size[1] - im_crop.size[1]) // 2), im_crop_alpha)
    #вставляем сам телефон
    imMain.paste(im2, (0,0), im2)
    #сохраняем фото
    imMain.save(src)

    return open(src, 'rb').read()