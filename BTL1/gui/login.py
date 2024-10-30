from pathlib import Path
import os, threading
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, messagebox


def GUILOGIN(login, tracker_conn, goRegister):
    global status_register
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    

    window = Tk()
    window.title("LOGIN - BK FILE SHARING")
    window.geometry("1200x700")
    window.configure(bg = "#FFFFFF")

    # def on_close(tracker_conn):
    #     window.quit()
    #     window.destroy()
    #     tracker_conn.close()
    #     # os._exit(0)

    # window.protocol("WM_DELETE_WINDOW", lambda: on_close(tracker_conn))


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
        600.0,
        0.0,
        1200.0,
        700.0,
        fill="#EBF5F5",
        outline="")

    canvas.create_text(
        126.0,
        120.0,
        anchor="nw",
        text="ĐĂNG NHẬP VÀO HỆ THỐNG",
        fill="#0688B4",
        font=("Inter", 26, "bold")
    )

    canvas.create_text(
        90.0,
        254.0,
        anchor="nw",
        text="Email",
        fill="#000000",
        font=("Inter Medium", 20 * -1)
    )

    canvas.create_text(
        90.0,
        361.0,
        anchor="nw",
        text="Mật khẩu",
        fill="#000000",
        font=("Inter Medium", 20 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: threading.Thread(target=login, args=(tracker_conn, entry_1.get(), entry_2.get(), window), daemon=True).start(),
        relief="flat"
    )
    button_1.place(
        x=90.0,
        y=482.0,
        width=440.0,
        height=50.0
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        310.0,
        311.0,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        insertwidth=3,         
        insertbackground="#0688B4", 
        insertofftime=200, 
        insertontime=500,
        font=("Inter", 16)
    )
    entry_1.place(
        x=100.0,
        y=288.0,
        width=420.0,
        height=46.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        310.0,
        418.0,
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
        font=("Inter", 16)
    )
    entry_2.place(
        x=100.0,
        y=395.0,
        width=420.0,
        height=46.0
    )

    canvas.create_text(
        150.0,
        557.0,
        anchor="nw",
        text="Bạn chưa có tài khoản?",
        fill="#6F6F6F",
        font=("Inter Light", 18 * -1)
    )

    register_label = Label(
        text="Đăng ký ngay!",
        font=("Inter Light", 18),
        fg="#0688B4",
        bg="#FFFFFF",
        cursor="hand2" 
    )

    register_label.bind("<Button-1>", lambda e: threading.Thread(target=goRegister, args=(window,), daemon=True).start())

    canvas.create_window(
        340.0, 553.0,
        anchor="nw",
        window=register_label
    )



    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        308.0,
        192.0,
        image=image_image_1
    )

    canvas.create_text(
        831.0,
        120.0,
        anchor="nw",
        text="WELCOME",
        fill="#0688B4",
        font=("Inter", 26, "bold")
    )

    canvas.create_text(
        693.0,
        168.0,
        anchor="nw",
        text="Chào mừng bạn đến với hệ thống chúng tôi!",
        fill="#6F6F6F",
        font=("Inter", 20)
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        900.0,
        430.0,
        image=image_image_2
    )
    window.resizable(False, False)
    window.mainloop()