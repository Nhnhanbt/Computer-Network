from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, scrolledtext
import threading

def GUITRACKER(TRACKER_ADDRESS, TRACKER_PORT, ping, openListPeer, saveterminal, saveliving):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / "assets" / "frame3"

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    window = Tk()
    window.title("TRACKER - BK FILE SHARING")
    window.geometry("1200x700")
    window.configure(bg = "#FFFFFF")


    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 700,
        width = 1200,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        100.0,
        1200.0,
        700.0,
        fill="#262A2E",
        outline="")

    canvas.create_text(
        62.0,
        155.0,
        anchor="nw",
        text="Địa chỉ IP:",
        fill="#FFFFFF",
        font=("Inter Light", 16 * -1)
    )

    # ô địa chỉ IP
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        454.0,
        165.0,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.insert(0, str(TRACKER_ADDRESS) + ':' + str(TRACKER_PORT))
    entry_1.place(
        x=319.0,
        y=152.0,
        width=270.0,
        height=26.0
    )

    canvas.create_rectangle(
        0.0,
        0.0,
        1200.0,
        100.0,
        fill="#0688B4",
        outline="")

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        66.0,
        50.0,
        image=image_image_1
    )

    canvas.create_text(
        278.0,
        34.0,
        anchor="nw",
        text="HỆ THỐNG CHIA SẺ TỆP BK FILE SHARING - ADMIN",
        fill="#FFFFFF",
        font=("Inter", 26, "bold")
    )

    canvas.create_rectangle(
        1.0,
        674.0,
        1201.0,
        700.0,
        fill="#111111",
        outline="")

    canvas.create_text(
        31.0,
        677.0,
        anchor="nw",
        text="COPYRIGHT 2024 BK FILE SHARING",
        fill="#FFFFFF",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        31.0,
        197.0,
        anchor="nw",
        text="BẢNG ĐIỀU KHIỂN",
        fill="#0688B4",
        font=("Inter", 16, "bold")
    )

    canvas.create_text(
        31.0,
        120.0,
        anchor="nw",
        text="THÔNG TIN TRACKER",
        fill="#0688B4",
        font=("Inter", 16, "bold")
    )

    canvas.create_text(
        62.0,
        238.0,
        anchor="nw",
        text="QUẢN LÝ NGƯỜI DÙNG",
        fill="#0688B4",
        font=("Inter", 16, "bold")
    )

    canvas.create_text(
        62.0,
        282.0,
        anchor="nw",
        text="Ping IP:",
        fill="#FFF6F6",
        font=("Inter Light", 16 * -1)
    )

    # ô ping ip
    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        454.0,
        292.0,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        insertwidth=3,         
        insertbackground="#0688B4", 
        insertofftime=200, 
        insertontime=500,
        font=("Inter", 14)
    )
    entry_2.place(
        x=319.0,
        y=279.0,
        width=270.0,
        height=26.0
    )

    # ô ping port
    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        842.0,
        292.0,
        image=entry_image_3
    )
    entry_3 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        insertwidth=3,         
        insertbackground="#0688B4", 
        insertofftime=200, 
        insertontime=500,
        font=("Inter", 14)
    )
    entry_3.place(
        x=707.0,
        y=279.0,
        width=270.0,
        height=26.0
    )

    # ô số lượng kết nối 
    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        454.0,
        349.0,
        image=entry_image_4
    )
    entry_4 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        insertwidth=3,         
        insertbackground="#0688B4", 
        insertofftime=200, 
        insertontime=500,
        font=("Inter", 14)
    )
    entry_4.insert(0, '0')
    entry_4.place(
        x=319.0,
        y=336.0,
        width=270.0,
        height=26.0
    )
    saveliving(entry_4)

    # ô thoát
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=window.destroy,
        relief="flat"
    )
    button_1.place(
        x=1034.0,
        y=25.0,
        width=135.0,
        height=50.0
    )

    canvas.create_text(
        648.0,
        339.0,
        anchor="nw",
        text="Xem danh sách các peer:",
        fill="#FFFFFF",
        font=("Inter Light", 16 * -1)
    )

    canvas.create_text(
        648.0,
        283.0,
        anchor="nw",
        text="Port:",
        fill="#FFFFFF",
        font=("Inter Light", 16 * -1)
    )

    # ô xem
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: openListPeer(window),
        relief="flat"
    )
    button_2.place(
        x=1026.0,
        y=334.0,
        width=119.0,
        height=30.0
    )

    canvas.create_text(
        62.0,
        339.0,
        anchor="nw",
        text="Số lượng kết nối hiện tại:",
        fill="#FFFFFF",
        font=("Inter Light", 16 * -1)
    )

    # nút kiểm tra
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: threading.Thread(target=ping, args=(str(entry_2.get()), int(entry_3.get()), window, entry_5)).start(),
        relief="flat"
    )
    button_3.place(
        x=1026.0,
        y=277.0,
        width=119.0,
        height=30.0
    )

    # ô terminal
    entry_image_5 = PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(
        599.5,
        591.5,
        image=entry_image_5
    )
    entry_5 = scrolledtext.ScrolledText(
        bd=0,
        bg="#313131",
        fg="#0688B4",
        highlightthickness=0,
        insertwidth=3,         
        insertbackground="#0688B4", 
        insertofftime=200, 
        insertontime=500,
        font=("Inter", 14)
    )
    entry_5.place(
        x=0.0,
        y=511.0,
        width=1199.0,
        height=161.0
    )
    saveterminal(entry_5)

    canvas.create_text(
        30.0,
        479.0,
        anchor="nw",
        text="TERMINAL",
        fill="#0688B4",
        font=("Inter", 16, "bold")
    )

    window.resizable(False, False)
    window.mainloop()
