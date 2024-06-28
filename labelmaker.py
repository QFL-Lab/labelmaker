#!/usr/bin/env python3
from flask import Flask, request, render_template
from labelle.lib.devices.device_manager import (
    DeviceManager, 
    DeviceManagerNoDevices
)
from labelle.lib.devices.dymo_labeler import DymoLabeler
from labelle.lib.render_engines import (
    HorizontallyCombinedRenderEngine,
    RenderContext,
    RenderEngine,
    TextRenderEngine,
    PrintPayloadRenderEngine,
)
from labelle.lib.constants import (
    Direction,
    DEFAULT_MARGIN_PX,
)
from labelle.lib.font_config import (
    DefaultFontStyle,
    NoFontFound,
    get_available_fonts,
    get_font_path,
)

app = Flask(__name__)


def get_device_manager() -> DeviceManager:
    device_manager = DeviceManager()
    try:
        device_manager.scan()
    except DeviceManagerNoDevices as e:
        print(f'Error with DeviceManager: {e}')
    return device_manager


def print_text(text, tape_size_mm=9):
    device_manager = get_device_manager()
    device = device_manager.find_and_select_device()
    device.setup()
    dymo_labeler = DymoLabeler(tape_size_mm=tape_size_mm, device=device)

    # use deault font
    font_path = get_font_path(font=None, style=DefaultFontStyle)

    lines = len(text.splitlines())
    print(lines)

    render_engines: list[RenderEngine] = []
    render_engines.append(
            TextRenderEngine(
                text_lines=text,
                font_file_name=font_path,
                frame_width_px=0,
                font_size_ratio=1/lines,
                align=Direction.LEFT,
            )
    )
    render_engine = HorizontallyCombinedRenderEngine(render_engines)
    render_context = RenderContext(
        background_color="white",
        foreground_color="black",
        height_px=dymo_labeler.height_px,
        preview_show_margins=False,
    )

    render = PrintPayloadRenderEngine(
            render_engine=render_engine,
            justify=Direction.LEFT,
            visible_horizontal_margin_px=DEFAULT_MARGIN_PX,
            labeler_margin_px=dymo_labeler.labeler_margin_px,
            max_width_px=None,
            min_width_px=0,
        )
    bitmap, _ = render.render_with_meta(render_context)

    dymo_labeler.print(bitmap)


@app.route('/', methods=['GET', 'POST'])
def handle_text():
    output = ""
    if request.method == 'POST':
        text_content = request.form['text_content']
        # Call the method that handles the text content
        try:
            print_text(text_content)
        except Exception as e:
            output = f"Error: {e}"
    return render_template('template.html', result=output)




if __name__ == '__main__':
    app.run(debug=True)


