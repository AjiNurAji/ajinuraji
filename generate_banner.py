import os
import math
from PIL import Image, ImageDraw, ImageFont

def draw_briefcase(draw, x, y, color):
    draw.rounded_rectangle((x, y + 2, x + 12, y + 10), radius=1, outline=color, width=1)
    draw.rounded_rectangle((x + 3, y, x + 9, y + 3), radius=1, outline=color, width=1)
    draw.line([(x, y + 5), (x + 12, y + 5)], fill=color, width=1)

def draw_mappin(draw, x, y, color):
    draw.ellipse((x, y, x + 8, y + 8), outline=color, width=1)
    draw.polygon([(x + 1, y + 5), (x + 7, y + 5), (x + 4, y + 11)], fill=color)
    draw.point((x + 4, y + 4), fill=(14, 14, 18))

def draw_code(draw, x, y, color):
    draw.line([(x + 2, y + 2), (x, y + 6), (x + 2, y + 10)], fill=color, width=1)
    draw.line([(x + 5, y + 10), (x + 8, y + 2)], fill=color, width=1)
    draw.line([(x + 10, y + 2), (x + 12, y + 6), (x + 10, y + 10)], fill=color, width=1)

def draw_shield(draw, x, y, color):
    draw.polygon([(x, y), (x + 10, y), (x + 10, y + 6), (x + 5, y + 11), (x, y + 6)], outline=color)

def create_banner():
    width = 900
    height = 320
    banner_h = 180
    corner_r = 16

    banner_src = r"C:\Users\HP\Documents\projects\portfolio-website\public\assets\images\banner-desk-retro.webp"
    avatar_src = r"C:\Users\HP\Documents\projects\ajinuraji\avatar.png"
    out_gif = r"C:\Users\HP\Documents\projects\ajinuraji\nurabyte-banner.gif"
    out_png = r"C:\Users\HP\Documents\projects\ajinuraji\nurabyte-banner.png"

    # Load and prepare banner image
    raw_banner = Image.open(banner_src).convert("RGB")
    scale = width / raw_banner.width
    new_h = int(raw_banner.height * scale)
    banner_resized = raw_banner.resize((width, new_h), Image.Resampling.LANCZOS)
    top_offset = int((new_h - banner_h) * 0.35)
    base_banner = banner_resized.crop((0, top_offset, width, top_offset + banner_h))

    # Grid / cell parameters for ASCII overlay (matching AsciiImage.vue on ajinuraji.my.id)
    cell_w, cell_h = 8, 11
    cols = width // cell_w
    rows = banner_h // cell_h
    sample_img = base_banner.resize((cols, rows), Image.Resampling.BOX)
    pixels = sample_img.load()

    GLYPH_CHARS = ["·", ":", "0", "1", "3", "5", "8", "9", "X", "B", "#", "0x", "88", "00"]

    # System Fonts
    f_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
    f_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
    f_pills = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11)
    f_mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 11)
    f_mono_sm = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 10)
    f_ascii = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 9)

    # Prepare avatar with squircle rounded corners
    raw_avatar = Image.open(avatar_src).convert("RGBA")
    av_size = 80
    avatar_resized = raw_avatar.resize((av_size, av_size), Image.Resampling.LANCZOS)
    
    # Avatar squircle mask
    av_mask = Image.new("L", (av_size, av_size), 0)
    av_mask_draw = ImageDraw.Draw(av_mask)
    av_mask_draw.rounded_rectangle((0, 0, av_size, av_size), radius=16, fill=255)
    avatar_crop = Image.new("RGBA", (av_size, av_size), (0, 0, 0, 0))
    avatar_crop.paste(avatar_resized, (0, 0), av_mask)

    raw_frames = []
    num_frames = 12

    for frame_idx in range(num_frames):
        t = (frame_idx / num_frames) * (math.pi * 2)

        # Base frame canvas (dark zinc/black #09090b)
        frame = Image.new("RGB", (width, height), (9, 9, 11))
        draw = ImageDraw.Draw(frame)

        # Draw subtle dotfield in lower section (mirroring DotField on ajinuraji.my.id)
        for y in range(banner_h + 10, height - 10, 15):
            for x in range(15, width - 15, 15):
                draw.point((x, y), fill=(26, 26, 32))

        # Copy banner crop
        banner_layer = base_banner.copy()
        b_draw = ImageDraw.Draw(banner_layer)

        # Render dynamic ASCII glyphs over illuminated desk monitors and lamps
        for r in range(rows):
            pos_y = r * cell_h + 1
            for c in range(cols):
                red, green, blue = pixels[c, r]
                lum = 0.299 * red + 0.587 * green + 0.114 * blue
                if lum < 95:
                    continue

                norm_lum = min(1.0, max(0.0, (lum - 95) / 160.0))
                wave = math.sin(c * 0.12 + t * 1.5) * 1.5 + math.cos(r * 0.25 - t * 1.2) * 1.5
                max_glyph_idx = min(len(GLYPH_CHARS) - 1, int(norm_lum * len(GLYPH_CHARS)))
                char_idx = abs(int(c * 3 + r * 7 + wave + t * 4)) % (max_glyph_idx + 1)
                glyph = GLYPH_CHARS[char_idx]
                pos_x = c * cell_w

                is_golden = (red > 120 and green > 110 and blue < 155)
                is_cyan = (blue > red + 10)
                boost = min(1.3, lum / 150.0 + 0.2)

                char_r = min(255, int(red * boost + (30 if is_golden else 0 if is_cyan else 20)))
                char_g = min(255, int(green * boost + (15 if is_golden else 25 if is_cyan else 10)))
                char_b = min(255, int(blue * boost + (-20 if is_golden else 40 if is_cyan else 15)))

                b_draw.text((pos_x, pos_y), glyph, font=f_ascii, fill=(char_r, char_g, char_b))

        # Paste banner layer
        frame.paste(banner_layer, (0, 0))

        # Hairline border separating banner from profile
        draw.line([(0, banner_h), (width, banner_h)], fill=(38, 38, 42), width=1)

        # Top-left Floating Badge: "● ajinuraji.my.id"
        pill_tl_box = (20, 16, 175, 42)
        draw.rounded_rectangle(pill_tl_box, radius=13, fill=(12, 12, 15), outline=(39, 39, 45), width=1)
        pulse = 0.75 + 0.25 * math.sin(t)
        green_r = int(34 * pulse)
        green_g = int(197 * pulse + 50 * (1 - pulse))
        green_b = int(94 * pulse)
        draw.ellipse((32, 26, 38, 32), fill=(green_r, green_g, green_b))
        draw.text((46, 22), "ajinuraji.my.id", font=f_mono, fill=(244, 244, 245))

        # Top-right Floating Badge: "PORTFOLIO IDENTITY • 2026"
        pill_tr_box = (width - 235, 16, width - 20, 42)
        draw.rounded_rectangle(pill_tr_box, radius=13, fill=(12, 12, 15), outline=(39, 39, 45), width=1)
        draw.text((width - 222, 22), "PORTFOLIO IDENTITY • 2026", font=f_mono_sm, fill=(161, 161, 170))

        # Avatar positioning: overlaps banner and profile
        av_x = 24
        av_y = banner_h - 44
        # Draw background border card behind avatar
        draw.rounded_rectangle(
            (av_x - 3, av_y - 3, av_x + av_size + 3, av_y + av_size + 3),
            radius=19,
            fill=(9, 9, 11),
            outline=(39, 39, 45),
            width=1,
        )
        # Paste avatar
        frame.paste(avatar_crop, (av_x, av_y), avatar_crop)

        # Profile Text section
        text_x = av_x + av_size + 18
        
        # Line 1: Name + Verified + Nurabyte Pill
        draw.text((text_x, banner_h + 12), "Aji Nur Aji", font=f_title, fill=(250, 250, 250))
        name_w = int(draw.textlength("Aji Nur Aji", font=f_title))

        # Verified badge (blue circle with checkmark)
        v_cx = text_x + name_w + 14
        v_cy = banner_h + 25
        v_r = 8
        draw.ellipse((v_cx - v_r, v_cy - v_r, v_cx + v_r, v_cy + v_r), fill=(0, 149, 246))
        # Draw small white checkmark
        draw.line([(v_cx - 4, v_cy), (v_cx - 1, v_cy + 3)], fill=(255, 255, 255), width=2)
        draw.line([(v_cx - 1, v_cy + 3), (v_cx + 4, v_cy - 3)], fill=(255, 255, 255), width=2)

        # Mini Brand Pill "NURABYTE"
        pill_brand_box = (v_cx + 16, v_cy - 9, v_cx + 86, v_cy + 9)
        draw.rounded_rectangle(pill_brand_box, radius=4, fill=(24, 24, 27), outline=(39, 39, 45), width=1)
        draw.text((v_cx + 23, v_cy - 7), "NURABYTE", font=f_mono_sm, fill=(161, 161, 170))

        # Right-side status tag (aligned cleanly with Line 1)
        status_text = "Available for Collabs"
        st_text_w = int(draw.textlength(status_text, font=f_pills))
        st_w = st_text_w + 32
        st_x = width - st_w - 24
        st_y = banner_h + 12
        draw.rounded_rectangle((st_x, st_y, st_x + st_w, st_y + 24), radius=12, fill=(14, 14, 18), outline=(39, 39, 45), width=1)
        draw.ellipse((st_x + 10, st_y + 8, st_x + 16, st_y + 14), fill=(34, 197, 94))
        draw.text((st_x + 22, st_y + 4), status_text, font=f_pills, fill=(52, 211, 153))

        # Line 2: Handle & Subtitle
        sub_text = "@nurabyte  •  Informatics Student  •  STMIK IKMI Cirebon"
        draw.text((text_x, banner_h + 42), sub_text, font=f_sub, fill=(161, 161, 170))

        # Line 3: Outline Tag Pills with custom vector icons (no broken emojis)
        pill_y = banner_h + 74
        pills_data = [
            ("briefcase", "Full-Stack Developer"),
            ("mappin", "Indonesia"),
            ("code", "Next.js • Laravel • Vue"),
            ("shield", "Cisco NetAcad"),
        ]
        curr_x = text_x
        icon_color = (161, 161, 170)
        text_color = (212, 212, 216)

        for icon_type, label in pills_data:
            lbl_w = int(draw.textlength(label, font=f_pills))
            pill_w = lbl_w + 34
            draw.rounded_rectangle((curr_x, pill_y, curr_x + pill_w, pill_y + 24), radius=6, fill=(14, 14, 18), outline=(39, 39, 45), width=1)
            
            # Draw vector icon
            if icon_type == "briefcase":
                draw_briefcase(draw, curr_x + 9, pill_y + 6, icon_color)
            elif icon_type == "mappin":
                draw_mappin(draw, curr_x + 10, pill_y + 6, icon_color)
            elif icon_type == "code":
                draw_code(draw, curr_x + 8, pill_y + 6, icon_color)
            elif icon_type == "shield":
                draw_shield(draw, curr_x + 10, pill_y + 6, icon_color)

            draw.text((curr_x + 25, pill_y + 4), label, font=f_pills, fill=text_color)
            curr_x += pill_w + 8

        # Card outer rounded corners mask & hairline border
        card_mask = Image.new("L", (width, height), 0)
        c_draw = ImageDraw.Draw(card_mask)
        c_draw.rounded_rectangle((0, 0, width, height), radius=corner_r, fill=255)

        out_frame = Image.new("RGB", (width, height), (13, 17, 23)) # dark GitHub background
        out_frame.paste(frame, (0, 0), card_mask)

        # Draw outer hairline border
        border_draw = ImageDraw.Draw(out_frame)
        border_draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=corner_r, outline=(39, 39, 45), width=1)

        raw_frames.append(out_frame)

    # Save static PNG (first frame)
    raw_frames[0].save(out_png, format="PNG")
    print(f"Saved PNG to {out_png}")

    # Optimize GIF palette to ~400KB
    palette_img = raw_frames[0].convert("RGB").quantize(colors=128)
    opt_frames = [f.convert("RGB").quantize(colors=128, palette=palette_img, dither=Image.Dither.NONE) for f in raw_frames]

    opt_frames[0].save(
        out_gif,
        save_all=True,
        append_images=opt_frames[1:],
        duration=110,
        loop=0,
        optimize=True,
    )
    print(f"Saved GIF to {out_gif} (Frames: {len(opt_frames)}, Size: {os.path.getsize(out_gif)} bytes)")

if __name__ == "__main__":
    create_banner()
