from PIL import Image, ImageDraw, ImageFont, ImageOps
import os


def circular_avatar(image_path, size):
    try:
        img = Image.open(image_path).convert("RGBA")
        img = ImageOps.fit(img, (size, size), Image.Resampling.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, size, size), fill=255)
        output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        output.paste(img, (0, 0), mask)
        return output
    except:
        return None


def desenhar_conversa(script_data):
    width, height = 1920, 1080
    frames = []
    canvas_color = (0, 0, 0)
    bg_color = (49, 51, 56)
    color_text = "white"
    color_time = "#949ba4"
    color_name = "white"
    font_dir = "assets/fonts"
    bold_path = os.path.join(font_dir, "ggsans-Bold.ttf")
    normal_path = os.path.join(font_dir, "ggsans-Normal.ttf")

    try:
        font_user = ImageFont.truetype(bold_path, 45)
        font_message = ImageFont.truetype(normal_path, 42)
        font_time = ImageFont.truetype(normal_path, 30)
    except:
        font_user = font_message = font_time = ImageFont.load_default()

    messages_in_view = []
    for i in range(len(script_data)):
        current_msg = script_data[i]
        if not current_msg["texto"].startswith("__"):
            messages_in_view = [current_msg]
        else:
            messages_in_view.append(current_msg)
        padding_extra = 80
        msg_full_height = 145
        msg_conn_height = 55
        total_h = 0
        last_u = None
        for m in messages_in_view:
            is_conn = m["texto"].startswith("__")
            if is_conn and m["usuario"] == last_u:
                total_h += msg_conn_height
            else:
                total_h += msg_full_height
            last_u = m["usuario"]
        stripe_h = total_h + padding_extra
        stripe_y = (height // 2) - (stripe_h // 2)
        img = Image.new("RGB", (width, height), color=canvas_color)
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, stripe_y, width, stripe_y + stripe_h], fill=bg_color)
        y_cursor = stripe_y + (padding_extra // 2)
        last_u = None
        for m in messages_in_view:
            is_conn = m["texto"].startswith("__")
            user_same = m["usuario"] == last_u
            final_text = m["texto"][2:] if is_conn else m["texto"]
            margin_x = 250
            if is_conn and user_same:
                draw.text(
                    (margin_x + 180, y_cursor),
                    final_text,
                    font=font_message,
                    fill=color_text,
                )
                y_cursor += msg_conn_height
            else:
                avatar_size = 140
                av_path = os.path.join("input/avatares", m.get("avatar", ""))
                circ_av = circular_avatar(av_path, avatar_size)
                if circ_av:
                    img.paste(circ_av, (margin_x, int(y_cursor)), circ_av)
                else:
                    draw.ellipse(
                        [
                            margin_x,
                            y_cursor,
                            margin_x + avatar_size,
                            y_cursor + avatar_size,
                        ],
                        fill="gray",
                    )
                name_x = margin_x + avatar_size + 40
                draw.text(
                    (name_x, y_cursor), m["usuario"], font=font_user, fill=color_name
                )
                try:
                    u_w = draw.textlength(m["usuario"], font=font_user)
                except:
                    u_w = 100
                draw.text(
                    (name_x + u_w + 20, y_cursor + 12),
                    m["time"],
                    font=font_time,
                    fill=color_time,
                )
                draw.text(
                    (name_x, y_cursor + 65),
                    final_text,
                    font=font_message,
                    fill=color_text,
                )
                y_cursor += msg_full_height
                last_u = m["usuario"]
        frames.append(img)
    return frames
