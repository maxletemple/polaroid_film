from PIL import Image, ImageDraw, ImageFont
from movieList import *
import os


def template_standard(location, movie):
    width = 1004
    height = 1417
    margin_top = int(.5 * (height / 12.0))
    margin_side = int(.5 * (width / 8.5))

    result = Image.new("RGB",
                          (width, height),
                          (255, 255, 255))
    
    draw = ImageDraw.Draw(result)

    # Crop the image to a 4/3 aspect ratio
    pic = Image.open(location + movie.pic_url)
    if pic.width / pic.height > 4/3:
        width_diff = pic.width - pic.height * 4/3
        pic = pic.crop((width_diff / 2, 0, pic.width - width_diff / 2, pic.height))
    else:
        height_diff = pic.height - pic.width * 3/4
        pic = pic.crop((0, height_diff / 2, pic.width, pic.height - height_diff / 2))
    
    # Insert the image into the template
    pic = pic.resize((width - margin_side * 2, int((width - margin_side * 2) * 3/4)))
    result.paste(pic, (margin_side, margin_top))

    # Draw the text
    title_font = ImageFont.truetype("assets/NotoSansJP-Medium.ttf", 150)
    year_font = ImageFont.truetype("assets/Oswald-Regular.ttf", 50)
    info_font = ImageFont.truetype("assets/Teko-Regular.ttf", 50)
    data_font = ImageFont.truetype("assets/RobotoCondensed-Regular.ttf", 50)

    cursor_height = margin_top + pic.height
    cursor_width = margin_side
    title = movie.title.upper()
    half = -1
    while (title_font.getlength(title) > width - margin_side * 2 - 150):
        title_font = ImageFont.truetype("assets/NotoSansJP-Medium.ttf", title_font.size - 1)
        if (title_font.size < 90):
            cursor_height = margin_top + pic.height
            half = len(title) // 2
            while (title[half] != " "):
                half += 1
            title = title[:half] + "\n" + title[half + 1:]
            break
        cursor_height += 1
    draw.multiline_text((cursor_width, cursor_height), title, (0, 0, 0), font=title_font)

    cursor_width += title_font.getlength(title[half+1:]) + 20
    if half == -1:
        cursor_height = margin_top + pic.height + 100
    else:
        cursor_height = margin_top + pic.height + 150
    draw.text((cursor_width, cursor_height), movie.year.upper(), (0, 0, 0), font=year_font)
    
    cursor_height += 100
    cursor_width = margin_side
    draw.text((cursor_width, cursor_height), "running time", (0, 0, 0), font=info_font)
    cursor_width += info_font.getlength("running time") + 20
    draw.text((cursor_width, cursor_height), movie.duration + " MINUTES", (0, 0, 0), font=data_font)

    cursor_height += 60
    cursor_width = margin_side
    draw.text((cursor_width, cursor_height), "directed by", (0, 0, 0), font=info_font)
    cursor_width += info_font.getlength("directed by") + 20
    draw.text((cursor_width, cursor_height), movie.director.upper(), (0, 0, 0), font=data_font)

    cursor_height += 100
    cursor_width = margin_side
    starring_text = ("starring" if movie.format != "animated film" else "voice cast (FV)")
    draw.text((cursor_width, cursor_height), starring_text, (0, 0, 0), font=info_font)
    cursor_width += info_font.getlength(starring_text) + 20
    for actor in movie.actors:
        if data_font.getlength(actor.upper()) + cursor_width > width - margin_side:
            cursor_height += 60
            cursor_width = margin_side
        draw.text((cursor_width, cursor_height), actor.upper(), (0, 0, 0), font=data_font)
        cursor_width += data_font.getlength(actor.upper()) + 20
    
    cursor_height = height - margin_top - 50
    cursor_width = margin_side
    draw.text((cursor_width, cursor_height), "rating", (0, 0, 0), font=info_font)
    star = Image.open("assets/star.png")
    star = Image.composite(star, Image.new("RGB", star.size, (255, 255, 255)), star)
    star = star.resize((50, 50))
    cursor_width += int(info_font.getlength("rating") + 20)
    for i in range(int(movie.rating // 1)):
        result.paste(star, (cursor_width, cursor_height))
        cursor_width += 50 + 20
    frac = movie.rating - movie.rating // 1
    if frac > 0:
        star = star.crop((0, 0, int(50 * frac), 50))
        result.paste(star, (cursor_width, cursor_height))
        cursor_width += 50 + 20
    
    return result

def formatToPDF(path, pics):
    origins = [(2480 // 2 - 1004, 3508 // 2 - 1417),
               (2480 // 2, 3508 // 2 - 1417),
               (2480 // 2 - 1004, 3508 // 2),
               (2480 // 2, 3508 // 2)]
    pages = []
    for i in range(0, len(pics), 4):
        result = Image.new("RGB",
                           (2480, 3508),
                           (255, 255, 255))
        draw = ImageDraw.Draw(result)
        for j in range(4):
            if i + j < len(pics):
                result.paste(pics[i + j], origins[j])
                draw.rectangle([(origins[j][0], origins[j][1]),
                                (origins[j][0] + 1004, origins[j][1] + 1417)],
                               outline=(0, 0, 0),
                               width=1)
        pages.append(result)
    
    pages[0].save(path, save_all=True, append_images=pages[1:], resolution=300.0)

                

def exportMovieList(template, location, movieList):
    pics = []
    for movie in movieList:
        if not os.path.exists(location + movie.pic_url):
            print(f"Error: {location + movie.pic_url} does not exist!")
            continue
        pics.append(template(location, movie))
    
    formatToPDF(location + "polaroid.pdf", pics)