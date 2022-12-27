import dearpygui.dearpygui as dpg

def imagePopup():
    with dpg.window(label=""):
        dpg.add_input_text(tag="ImageName")
        dpg.add_button(label="Save", callback=loadImage)

def loadImage():
    width1, height1, channels1, data1 = dpg.load_image("resources/characters/" + dpg.get_value("ImageName"))

    with dpg.texture_registry():
        texture_id = dpg.add_static_texture(width1, height1, data1)

    with dpg.plot(label="Image Plot"):
        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvAxis, llabe="x axis")
        with dpg.plot_axis(dpg.mYAxis, label="y axis"):
            dpg.add_image_series(dpg.mvFontAtlas, [300, 300], [400, 400], label="font atlas")
            dpg.add_image(texture_id)
