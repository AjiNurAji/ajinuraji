import os
import math
from PIL import Image, ImageDraw, ImageFont

def create_banner():
    width = 900
    height = 220
    corner_r = 16

    banner_src = r"C:\Users\HP\Documents\projects\portfolio-website\public\assets\images\banner-desk-retro.webp"
    
    # Destination files
    out_files_gif = [
        r"C:\Users\HP\Documents\projects\ajinuraji\banner.gif",
        r"C:\Users\HP\Documents\projects\ajinuraji\nurabyte-banner.gif"
    ]
    out_files_png = [
        r"C:\Users\HP\Documents\projects\ajinuraji\banner.png",
        r"C:\Users\HP\Documents\projects\ajinuraji\nurabyte-banner.png"
    ]

    # Load and scale retro desk banner
    raw_banner = Image.open(banner_src).convert("RGB")
    scale = width / raw_banner.width
    new_h = int(raw_banner.height * scale)
    banner_resized = raw_banner.resize((width, new_h), Image.Resampling.LANCZOS)
    
    # Center-vertical crop to exactly width x height
    top_offset = int((new_h - height) * 0.38)
    base_banner = banner_resized.crop((0, top_offset, width, top_offset + height))

    # Grid / cell parameters for ASCII overlay
    cell_w, cell_h = 8, 11
    cols = width // cell_w
    rows = height // cell_h
    sample_img = base_banner.resize((cols, rows), Image.Resampling.BOX)
    pixels = sample_img.load()

    GLYPH_CHARS = ["·", ":", "0", "1", "3", "5", "8", "9", "X", "B", "#", "0x", "88", "00"]

    # Fonts
    f_mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 11)
    f_mono_sm = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 10)
    f_ascii = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 9)

    raw_frames = []
    num_frames = 12

    for frame_idx in range(num_frames):
        t = (frame_idx / num_frames) * (math.pi * 2)

        # Base banner layer
        banner_layer = base_banner.copy()
        b_draw = ImageDraw.Draw(banner_layer)

        # Render dynamic ASCII glyphs over illuminated monitors, lamps, keyboards
        for r in range(rows):
            pos_y = r * cell_h + 1
            for c in range(cols):
                red, green, blue = pixels[c, r]
                lum = 0.299 * red + 0.587 * green + 0.114 * blue
                if lum < 92:
                    continue

                norm_lum = min(1.0, max(0.0, (lum - 92) / 163.0))
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

        # Top-left Floating Badge: "● ajinuraji.my.id"
        pill_tl_box = (20, 16, 175, 42)
        b_draw.rounded_rectangle(pill_tl_box, radius=13, fill=(12, 12, 15), outline=(42, 42, 48), width=1)
        pulse = 0.75 + 0.25 * math.sin(t)
        green_r = int(34 * pulse)
        green_g = int(197 * pulse + 50 * (1 - pulse))
        green_b = int(94 * pulse)
        b_draw.ellipse((32, 26, 38, 32), fill=(green_r, green_g, green_b))
        b_draw.text((46, 22), "ajinuraji.my.id", font=f_mono, fill=(244, 244, 245))

        # Top-right Floating Badge: "PORTFOLIO IDENTITY • 2026"
        pill_tr_box = (width - 235, 16, width - 20, 42)
        b_draw.rounded_rectangle(pill_tr_box, radius=13, fill=(12, 12, 15), outline=(42, 42, 48), width=1)
        b_draw.text((width - 222, 22), "PORTFOLIO IDENTITY • 2026", font=f_mono_sm, fill=(161, 161, 170))


        # Rounded corners & hairline border
        card_mask = Image.new("L", (width, height), 0)
        c_draw = ImageDraw.Draw(card_mask)
        c_draw.rounded_rectangle((0, 0, width, height), radius=corner_r, fill=255)

        out_frame = Image.new("RGB", (width, height), (13, 17, 23)) # dark GitHub background
        out_frame.paste(banner_layer, (0, 0), card_mask)

        # Hairline card border
        border_draw = ImageDraw.Draw(out_frame)
        border_draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=corner_r, outline=(42, 42, 48), width=1)

        raw_frames.append(out_frame)

    # Save PNGs
    for p in out_files_png:
        raw_frames[0].save(p, format="PNG")
        print(f"Saved PNG to {p}")

    # Optimize GIF palette (~160 KB)
    palette_img = raw_frames[0].convert("RGB").quantize(colors=128)
    opt_frames = [f.convert("RGB").quantize(colors=128, palette=palette_img, dither=Image.Dither.NONE) for f in raw_frames]

    for g in out_files_gif:
        opt_frames[0].save(
            g,
            save_all=True,
            append_images=opt_frames[1:],
            duration=110,
            loop=0,
            optimize=True,
        )
        print(f"Saved GIF to {g} ({os.path.getsize(g)} bytes)")

if __name__ == "__main__":
    create_banner()
