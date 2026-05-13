from PIL import Image, ImageDraw, ImageFont
import os

def create_pdf(output_path):
    # Create an image with white background
    img = Image.new('RGB', (800, 400), color='white')
    d = ImageDraw.Draw(img)

    # Try to load a Hebrew-supporting font if possible, else default
    # Note: the default font won't really render Hebrew perfectly but
    # it's just for testing the pipeline end-to-end
    try:
        # Many systems have this font
        font = ImageFont.truetype("DejaVuSans.ttf", 40)
    except:
        font = ImageFont.load_default()

    text = "שלום עולם" # "Hello World" in Hebrew
    d.text((50, 150), text, fill=(0, 0, 0), font=font)

    # Save as PDF
    img.save(output_path, "PDF", resolution=100.0)
    print(f"Test PDF generated at {output_path}")

if __name__ == "__main__":
    create_pdf("test_hebrew.pdf")
