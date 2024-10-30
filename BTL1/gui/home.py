from pathlib import Path
import os, threading
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, messagebox, scrolledtext

def GUIHOME(tracker_conn, S_EMAIL, HOSTNAME, LOCAL_SERVER_ADDRESS, LOCAL_SERVER_PORT, logout, publish, publish_piece, ping, download, openListPeer, saveterminal):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / "assets" / "frame2"

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title("HOME - BK FILE SHARING")
    window.geometry("1200x700")
    window.configure(bg = "#FFFFFF")

    def open_file_dialog():
        file_path = filedialog.askopenfilename(initialdir=".")
        if file_path:
            print("Selected file:", file_path)
            entry_5.delete(0, 'end')
            entry_5.insert(0, str(file_path))
            messagebox.showinfo("Thành công", "Chọn tệp thành công!")


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
        fill="#EBF5F5",
        outline="")

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
        334.0,
        34.0,
        anchor="nw",
        text="HỆ THỐNG CHIA SẺ TỆP BK FILE SHARING",
        fill="#FFFFFF",
        font=("Inter", 26, "bold")
    )

    canvas.create_rectangle(
        1.0,
        674.0,
        1201.0,
        700.0,
        fill="#6D98D7",
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
        120.0,
        anchor="nw",
        text="THÔNG TIN TÀI KHOẢN",
        fill="#0688B4",
        font=("Inter", 16, "bold")
    )

    canvas.create_text(
        31.0,
        193.0,
        anchor="nw",
        text="BẢNG ĐIỀU KHIỂN",
        fill="#0688B4",
        font=("Inter", 16, "bold")
    )

    # Ô terminal
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        600.5,
        590.5,
        image=entry_image_1
    )
    entry_1 = scrolledtext.ScrolledText(
        bd=0,
        bg="#FFFFFF",
        fg="#0688B4",
        highlightthickness=0,
        insertwidth=3,         
        insertbackground="#0688B4", 
        insertofftime=200, 
        insertontime=500,
        font=("Inter", 16)
    )
    entry_1.place(
        x=1.0,
        y=510.0,
        width=1199.0,
        height=161.0
    )
    saveterminal(entry_1)

    # Ô địa chỉ IP
    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        641.0,
        166.0,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.insert(0, str(LOCAL_SERVER_ADDRESS) + ':' + str(LOCAL_SERVER_PORT))
    entry_2.place(
        x=516.0,
        y=153.0,
        width=250.0,
        height=26.0
    )

    canvas.create_text(
        426.0,
        156.0,
        anchor="nw",
        text="Địa chỉ IP:",
        fill="#6F6F6F",
        font=("Inter Light", 16 * -1)
    )

    # nút đăng xuất
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: threading.Thread(target=logout, args=(window,)).start(),
        relief="flat"
    )
    button_1.place(
        x=1034.0,
        y=25.0,
        width=135.0,
        height=50.0
    )

    canvas.create_text(
        31.0,
        156.0,
        anchor="nw",
        text="Tài khoản:",
        fill="#6F6F6F",
        font=("Inter Light", 16 * -1)
    )

    # Ô tài khoản
    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        246.0,
        166.0,
        image=entry_image_3
    )
    entry_3 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_3.insert(0, S_EMAIL)
    entry_3.place(
        x=121.0,
        y=153.0,
        width=250.0,
        height=26.0
    )

    # ô hostname
    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        1034.0,
        166.0,
        image=entry_image_4
    )
    entry_4 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_4.insert(0, HOSTNAME)
    entry_4.place(
        x=909.0,
        y=153.0,
        width=250.0,
        height=26.0
    )

    canvas.create_text(
        813.0,
        156.0,
        anchor="nw",
        text="Hostname:",
        fill="#6F6F6F",
        font=("Inter Light", 16 * -1)
    )

    canvas.create_text(
        54.0,
        231.0,
        anchor="nw",
        text="TẢI TỆP LÊN",
        fill="#0688B4",
        font=("Inter", 16, "bold")
    )

    canvas.create_text(
        54.0,
        267.0,
        anchor="nw",
        text="Tệp tải lên:",
        fill="#6F6F6F",
        font=("Inter Light", 16 * -1)
    )

    # Ô tải tệp lên
    entry_image_5 = PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(
        265.0,
        277.0,
        image=entry_image_5
    )
    entry_5 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_5.place(
        x=159.0,
        y=264.0,
        width=212.0,
        height=26.0
    )

    # nút chọn tệp
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=open_file_dialog,
        relief="flat"
    )
    button_2.place(
        x=404.0,
        y=262.0,
        width=80.0,
        height=30.0
    )

    # # nút lấy data
    # button_image_3 = PhotoImage(
    #     file=relative_to_assets("button_3.png"))
    # button_3 = Button(
    #     image=button_image_3,
    #     borderwidth=0,
    #     highlightthickness=0,
    #     command=lambda: print("button_3 clicked"),
    #     relief="flat"
    # )
    # button_3.place(
    #     x=404.0,
    #     y=347.0,
    #     width=80.0,
    #     height=30.0
    # )

    # nút tách tệp
    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: threading.Thread(target=publish, args=(tracker_conn, entry_5.get(), entry_1, window,)).start(),
        relief="flat"
    )
    button_4.place(
        x=506.0,
        y=262.0,
        width=80.0,
        height=30.0
    )

    # nút tải về
    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: threading.Thread(target=download, args=(tracker_conn, str(entry_7.get()), entry_1, window,)).start(),
        relief="flat"
    )
    button_5.place(
        x=404.0,
        y=347.0,
        width=182.0,
        height=30.0
    )

    canvas.create_text(
        641.0,
        267.0,
        anchor="nw",
        text="Piece tải lên:",
        fill="#6F6F6F",
        font=("Inter Light", 16 * -1)
    )

    # ô piece tải lên
    entry_image_6 = PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(
        912.0,
        277.0,
        image=entry_image_6
    )
    entry_6 = Entry(
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
    entry_6.place(
        x=757.0,
        y=264.0,
        width=310.0,
        height=26.0
    )

    # nút chọn
    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: threading.Thread(target=publish_piece, args=(tracker_conn, entry_1, window,entry_6.get())).start(),
        relief="flat"
    )
    button_6.place(
        x=1090.0,
        y=262.0,
        width=61.0,
        height=30.0
    )

    canvas.create_text(
        54.0,
        312.0,
        anchor="nw",
        text="TẢI TỆP VỀ MÁY",
        fill="#0688B4",
        font=("Inter", 16, "bold")
    )

    canvas.create_text(
        54.0,
        352.0,
        anchor="nw",
        text="Tệp tải về:",
        fill="#6F6F6F",
        font=("Inter Light", 16 * -1)
    )

    # ô tệp tải về
    entry_image_7 = PhotoImage(
        file=relative_to_assets("entry_7.png"))
    entry_bg_7 = canvas.create_image(
        265.0,
        362.0,
        image=entry_image_7
    )
    entry_7 = Entry(
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
    entry_7.place(
        x=159.0,
        y=349.0,
        width=212.0,
        height=26.0
    )

    canvas.create_text(
        641.0,
        312.0,
        anchor="nw",
        text="PING HOSTNAME",
        fill="#0688B4",
        font=("Inter", 16, "bold")
    )

    canvas.create_text(
        722.0,
        352.0,
        anchor="nw",
        text="IP:",
        fill="#6F6F6F",
        font=("Inter Light", 16 * -1)
    )

    canvas.create_text(
        951.0,
        352.0,
        anchor="nw",
        text="Port:",
        fill="#6F6F6F",
        font=("Inter Light", 16 * -1)
    )

    # Ô ping ip
    entry_image_8 = PhotoImage(
        file=relative_to_assets("entry_8.png"))
    entry_bg_8 = canvas.create_image(
        837.0,
        362.0,
        image=entry_image_8
    )
    entry_8 = Entry(
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
    entry_8.place(
        x=757.0,
        y=349.0,
        width=160.0,
        height=26.0
    )

    # ô ping port
    entry_image_9 = PhotoImage(
        file=relative_to_assets("entry_9.png"))
    entry_bg_9 = canvas.create_image(
        1036.5,
        362.0,
        image=entry_image_9
    )
    entry_9 = Entry(
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
    entry_9.place(
        x=1012.0,
        y=349.0,
        width=50.0,
        height=26.0
    )

    # nút ping
    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    button_7 = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: threading.Thread(target=ping, args=(str(entry_8.get()), int(entry_9.get()), window, entry_1)).start(),
        relief="flat"
    )
    button_7.place(
        x=1090.0,
        y=347.0,
        width=61.0,
        height=30.0
    )

    canvas.create_text(
        54.0,
        398.0,
        anchor="nw",
        text="XEM THÔNG TIN",
        fill="#0688B4",
        font=("Inter", 16, "bold")
    )

    # nút xem peer
    button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    button_8 = Button(
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: openListPeer(tracker_conn, window),
        relief="flat"
    )
    button_8.place(
        x=404.0,
        y=432.0,
        width=182.0,
        height=30.0
    )

    # # nút xem tệp
    # button_image_9 = PhotoImage(
    #     file=relative_to_assets("button_9.png"))
    # button_9 = Button(
    #     image=button_image_9,
    #     borderwidth=0,
    #     highlightthickness=0,
    #     command=lambda: openListPeer(tracker_conn, window),
    #     relief="flat"
    # )
    # button_9.place(
    #     x=968.0,
    #     y=432.0,
    #     width=182.0,
    #     height=30.0
    # )

    canvas.create_text(
        54.0,
        437.0,
        anchor="nw",
        text="Xem danh sách các peer:",
        fill="#6F6F6F",
        font=("Inter Light", 16 * -1)
    )

    # canvas.create_text(
    #     641.0,
    #     437.0,
    #     anchor="nw",
    #     text="Xem danh sách các tệp có thể tải:",
    #     fill="#6F6F6F",
    #     font=("Inter Light", 16 * -1)
    # )

    canvas.create_text(
        31.0,
        478.0,
        anchor="nw",
        text="TERMINAL",
        fill="#0688B4",
        font=("Inter", 16, "bold")
    )
    window.resizable(False, False)
    window.mainloop()
