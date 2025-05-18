import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import boto3

# --- Helper Function ---
def MyImgByte(filepath):
    with open(filepath, 'rb') as imagefile:
        return imagefile.read()

# --- Textract + Image Handler ---
def funct_upload():
    # AWS setup using named profile (configured on your Mac via AWS CLI)
    session = boto3.session.Session(profile_name='demo_user')
    client = session.client(service_name='textract', region_name='us-east-1')

    global img  # To avoid garbage collection
    f_type = [('PNG Files', "*.png"), ('All Files', "*.*")]
    file = filedialog.askopenfile(filetypes=f_type)

    if file:
        filepath = file.name

        # Load and show image
        image_open = Image.open(filepath)
        image_resized = image_open.resize((400, 200))
        img = ImageTk.PhotoImage(image_resized)
        img_label.config(image=img)
        img_label.image = img

        # Get bytes for Textract
        imgbytes = MyImgByte(filepath)

        # Call AWS Textract
        response = client.detect_document_text(Document={'Bytes': imgbytes})
        extracted_text = ""
        for item in response['Blocks']:
            if item['BlockType'] == 'LINE':
                extracted_text += item['Text'] + '\n'
        
        print(extracted_text)

        # Show extracted text
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, extracted_text)

# --- Tkinter GUI ---
mywindow = tk.Tk()
mywindow.geometry("900x600")
mywindow.title("AWS Textract")

label1 = tk.Label(mywindow, text="Upload an Image babu", font=('roman', 17, 'bold'))
label1.pack(pady=10)

button1 = tk.Button(mywindow, text="Extract text", width=30, command=funct_upload)
button1.pack(pady=10)

img_label = tk.Label(mywindow)
img_label.pack(pady=10)

text_box = tk.Text(mywindow, height=10, width=80, wrap=tk.WORD)
text_box.pack(pady=10)

mywindow.mainloop()
