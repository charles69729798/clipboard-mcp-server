from PIL import Image, ImageDraw, ImageFont
import io
import win32clipboard
from PIL import ImageGrab

# Create test image
img = Image.new('RGB', (400, 200), color='white')
draw = ImageDraw.Draw(img)
draw.text((50, 80), "C:\\ MCP Server Test", fill='red')

# Copy to clipboard
output = io.BytesIO()
img.convert('RGB').save(output, 'BMP')
data = output.getvalue()[14:]  # Remove BMP header
output.close()

win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
win32clipboard.CloseClipboard()

print("Test image copied to clipboard!")

# Now try to read it back
clipboard_img = ImageGrab.grabclipboard()
if clipboard_img:
    print(f"Successfully read back image: {clipboard_img.size}")
else:
    print("Failed to read clipboard image")
