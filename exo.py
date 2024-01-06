#chapitreeeeeeeeeeeeeeeeeeeeeee 6
from PIL import Image, ImageEnhance
import io
import os
import PySimpleGUI as sg
import shutil
import tempfile


def enhance_color(input_path, enhace_factor, output_path):
    image_org = Image.open(input_path)
    img_enh = ImageEnhance.Color(image_org)
    finl_img = img_enh.enhance(enhace_factor)
    finl_img.save(output_path)

def cpntrast(input_path, factor, output_path):
    image_org = Image.open(input_path)
    img_cont = ImageEnhance.Contrast(image_org)
    img_f = img_cont.enhance(factor)
    img_f.save(output_path)

def brightness(input_path, factor, output_path):
    image_org = Image.open(input_path)
    img_b = ImageEnhance.Brightness(image_org)
    img_f = img_b.enhance(factor)
    img_f.save(output_path)


def sharpness(input_path, factor, outputpath):
    imgorg = Image.open(input_path)
    img_sh = ImageEnhance.Sharpness(imgorg)
    img_f = img_sh.enhance(factor)
    img_f.save(outputpath)


#"___________________________________"
file_types = [("JPEG(.jpg)", ".jpg"), ("All fiels (.)", ".*")]
tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
effect = {
    "Normal": shutil.copy,
    "Brightness": brightness,
    "Color": enhance_color,
    "Contrast": cpntrast,
    "Sharpness": sharpness
}

def effect_apply(values, window):
    select_effect = values ["-EFFECTS-"]
    image_file = values["-FILENAME-"]
    factor = values["-FACTORS-"]
    if os.path.exists(image_file):
        if select_effect == "Normal":
            effect[select_effect](image_file, tmp_file)
        else:
            effect[select_effect](image_file, factor, tmp_file)

        image = Image.open(tmp_file)
        image.thumbnail((400, 400))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        window['-IMAGE-'].update(data=bio.getvalue(), size=(400, 400))


def save_image(image_filename):
    save_filename = sg.popup_get_file("File", file_types=file_types, save_as=True, no_window=True, )
    if save_filename == image_filename:
        sg.popup_error("You are not allowed to overwrite the original image!")
    else:
        if save_filename:
            shutil.copy(tmp_file, save_filename)
            sg.popup(f"Saved: {save_filename}")


def main():
    effect_name = list(effect.keys())
    layout = [
        [sg.Image(key="-IMAGE-", size=(500, 500))],
        [sg.Text("Image File "),
         sg.Input(size=(25, 1), key="-FILENAME-"),
         sg.FileBrowse(file_types=file_types),
         sg.Button("Load image")

         ],
        [sg.Text(" Effect "), sg.Combo(
            effect_name, default_value="Normal", key="-EFFECTS-",
            enable_events=True, readonly=True), sg.Slider(range=(0, 5), default_value=2, resolution=0.1
                                                          , orientation="h", enable_events=True, key="-FACTORS-"),
         ],
        [sg.Button("Save")],]
    window = sg.Window("Image Enhancer",  layout, size=(600, 600))
    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event in ["Load image", "-EFFECTS-", "-FACTORS-"]:
            effect_apply(values, window)
        image_filename = values["-FILENAME-"]
        if event == 'Save' and image_filename:
            save_image(image_filename)
    window.close()


main()