import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import torch
import torchvision.transforms as transforms
import torch.nn as nn
from torchvision.models import resnet18
import zipfile
import os

tab_control = None
tabs = {}
scrollable_frames = {}
img_label = None
class_names = {0: "bazofil", 1: "eozynofil", 2: "limfocyt", 3: "monocyt", 4: "neutrofil"}


def create_tabs():
    global tab_control, tabs, scrollable_frames
    tabs_names = {0: "bazofile", 1: "eozynofile", 2: "limfocyty", 3: "monocyty", 4: "neutrofile", 5: "statystyki"}
    tab_control = ttk.Notebook(root)
    tabs = {}
    scrollable_frames = {}
    for class_id, tabs_name in tabs_names.items():
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=tabs_name)
        tabs[class_id] = tab

        canvas = tk.Canvas(tab)
        if tabs_name == "statystyki":
            canvas.config(bg='white')
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda x, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        scrollable_frames[class_id] = scrollable_frame

    tab_control.pack(expand=1, fill="both")


def clear_tabs():
    global tab_control, tabs, scrollable_frames
    if tab_control:
        tab_control.destroy()
    tab_control = None
    tabs = {}
    scrollable_frames = {}


def create_table(class_confidence):
    data = {"Klasa": list(class_confidence.keys()),
            "Średnia pewność": [f"{sum(conf)/len(conf):.2f}%" if len(conf) > 0 else "0.00%" for conf in class_confidence.values()],
            "Liczba zdjęć": [len(conf) for conf in class_confidence.values()]}

    columns = ["Klasa", "Średnia pewność", "Liczba zdjęć"]
    tree = ttk.Treeview(scrollable_frames[5], columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=158)

    for i in range(len(data["Klasa"])):
        values = (data["Klasa"][i], data["Średnia pewność"][i], data["Liczba zdjęć"][i])
        tree.insert('', tk.END, values=values)

    style = ttk.Style()
    style.configure("Treeview", rowheight=30)
    style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

    tree.pack()


def classify_image():
    global img_label
    clear_tabs()
    result_label.config(text="")
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img = img.resize((224, 224))
        img_tk = ImageTk.PhotoImage(img)

        if img_label:
            img_label.destroy()

        img_label = ttk.Label(root, image=img_tk)
        img_label.image = img_tk
        img_label.pack()

        transform = transforms.Compose([
            transforms.Resize(size=(224, 224)),
            transforms.ToTensor()
        ])
        img_tensor = transform(img).unsqueeze(0)

        with torch.no_grad():
            output = model(img_tensor)
            probs = torch.nn.functional.softmax(output, dim=1)  # softmax returns probability of belonging to each class where scope of values is from 0 to 1
            max_prob, prediction = probs.max(dim=1)

        class_name = class_names[prediction.item()]
        confidence = max_prob.item() * 100  # this multiplication turns the previous scope into probability percentage

        result_label.config(text=f"Predykcja: {class_name} (Pewność: {confidence:.2f}%)")


def classify_images_in_zip():
    global img_label
    zip_path = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
    if zip_path:
        clear_tabs()
        create_tabs()
        if img_label:
            img_label.destroy()
            img_label = None

        result_label.config(text="")

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall("temp_images")

        class_confidence = {class_name: [] for class_name in class_names.values()}

        row_count = 0
        file_count = 0
        for root_dir, _, files in os.walk("temp_images"):
            for file in files:
                file_path = os.path.join(root_dir, file)
                img = Image.open(file_path)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img = img.resize((224, 224))

                transform = transforms.Compose([
                    transforms.Resize(size=(224, 224)),
                    transforms.ToTensor()
                ])
                img_tensor = transform(img).unsqueeze(0)

                with torch.no_grad():
                    output = model(img_tensor)
                    probabilities = torch.nn.functional.softmax(output, dim=1)
                    max_prob, prediction = probabilities.max(dim=1)

                class_id = prediction.item()
                class_name = class_names[class_id]
                confidence = max_prob.item() * 100

                class_confidence[class_name].append(confidence)

                img_tk = ImageTk.PhotoImage(img)
                frame = ttk.Frame(scrollable_frames[class_id])
                frame.grid(row=row_count, column=file_count % 2, padx=5, pady=10)

                label = tk.Label(frame, text=f"{file} (Pewność: {confidence:.2f}%)", anchor="w")
                label.pack(side="top")

                img_label = tk.Label(frame, image=img_tk)
                img_label.image = img_tk
                img_label.pack(side="top")

                file_count += 1
                if file_count % 2 == 0:
                    row_count += 1

        create_table(class_confidence)
        for root_dir, _, files in os.walk("temp_images", topdown=False):
            for file in files:
                os.remove(os.path.join(root_dir, file))
            os.rmdir(root_dir)


root = tk.Tk()
root.title("Klasyfikator białych krwinek")
root.geometry("498x650")

model = resnet18()
model.fc = nn.Sequential(nn.Dropout(p=0.2),
                         nn.Linear(in_features=512, out_features=5))

state_dict = torch.load("best_ResNet18_not_pretrained_Adam_lr_0.0005_epoch_47.pth", map_location=torch.device("cpu"), weights_only=True)  # because I don't possess GPU i map to CPU so the code can work in my laptop
model.load_state_dict(state_dict)
model.eval()

btn_single = tk.Button(root, text="Wybierz obraz", command=classify_image, width=15, height=2)
btn_single.pack()

btn_zip = tk.Button(root, text="Wybierz plik ZIP", command=classify_images_in_zip, width=15, height=2)
btn_zip.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
