
import os
from PIL import Image
import tkinter as tk




def image_processor(img_src, img_dst, img_re_size):
    if not os.path.exists(img_src) and not os.path.exists(img_dst):
        log_text.insert("1.0", "输入与输出的路径均错误或均不存在！\n")
        os.makedirs(img_src)
        os.makedirs(img_dst)
    if not os.path.exists(img_dst):
        log_text.insert("1.0", "输出路径错误或不存在！\n")
        os.makedirs(img_dst)
    if not os.path.exists(img_src):
        log_text.insert("1.0", "输入路径错误或不存在！\n")
        os.makedirs(img_src)
    if img_re_size == "":
        img_re_size = 768
    img_list = [f for f in os.listdir(img_src) if f.endswith((".jpg", ".png", ".bmp", ".jpeg", ".gif", ".tiff"))]
    count = 0
    for i in img_list:
        count += 1
        # 读取图像
        img = Image.open(os.path.join(img_src, i))
        # 获取图像名称
        img_name = img.filename
        # 获取图像的尺寸
        width, height = img.size
        # 获取图片的信息字典
        info = img.info
        # 获取图片的 dpi 信息
        dpi_info = info.get('dpi', (96, 96))
        # 展示 log 信息
        log_text.insert("1.0", "\nProcessing..." + "Image No." + str(count) + "\nIAMGE: " + str(img_name) + "\nSIZE: " + str(img_re_size) + " x " + str(img_re_size) + "\nDPI: " + str(dpi_info) + "\n")
        log_text.update()
        # 判断图片长宽差异，并补齐至方形
        if width < height:
            new_height = height
            new_width = height
            x = (new_width - width)
            if x % 2 != 0:
                x += 1
            x = x//2
            y = (new_height - height)
            new_img = Image.new("RGBA", (new_width, new_height))
            new_img.putalpha(0)
            new_img.paste(img, (x, y))
        elif height < width:
            new_width = width
            new_height = width
            x = (new_width - width)
            y = (new_height - height)
            if y % 2 != 0:
                y += 1
            y = y//2
            new_img = Image.new("RGBA", (new_width, new_height))
            new_img.putalpha(0)
            new_img.paste(img, (x, y))
        elif width == height:
            new_width = width
            new_height = height
            x = (new_width - width)
            y = (new_height - height)
            new_img = Image.new("RGBA", (new_width, new_height))
            new_img.putalpha(0)
            new_img.paste(img, (x, y))
        # 指定拓展后的尺寸
        img_resized = new_img.resize((int(img_re_size), int(img_re_size)))
        # 获取图像的文件名（不包括扩展名）
        filename, _ = os.path.splitext(i)
        # 将图像保存为 PNG-24 格式
        img_resized.save(os.path.join(img_dst, filename + ".png"), "PNG", mode="CMYK", dpi=dpi_info)





if __name__ == "__main__":
    # 创建窗口
    window = tk.Tk(className="--Image Converter--")
    # 获取屏幕的宽度和高度
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = int(screen_width / 2)
    window_height = int(screen_height / 2)
    # 创建窗口
    window.geometry(f"{window_width}x{window_height}")

    # 计算窗口位置
    window_x = int((screen_width - window_width) / 2)
    window_y = int((screen_height - window_height) / 2)

    # 将窗口移动到屏幕中央
    window.geometry(f"+{window_x}+{window_y}")

    # 指定窗口颜色
    window.config(bg="black")

    # 基本说明
    greeting = tk.Label(text="快速转换图片至AI绘图所需规格：", foreground="white", background="black")
    # 设置 label 框的宽度、高度、水平位置和垂直位置
    greeting.place(width=(window_width*0.8), height=64, x=(window_width/2), y=(window_height-256))
    greeting.pack(padx=50, pady=4)

    # 创建三个储存文本的变量
    input_path = tk.StringVar()
    output_path = tk.StringVar()
    entered_to_size = tk.StringVar()

    # 创建三个 entry，并将变量作为 textvariable 参数传递给 entry
    input_entry = tk.Entry(window, textvariable=input_path)
    output_entry = tk.Entry(window, textvariable=output_path)
    to_size_entry = tk.Entry(window, textvariable=entered_to_size)

    # 为两个 entry 设置 trace 方法，用于更新储存文本的变量
    input_path.trace('w', lambda *args: input_path.set(input_entry.get()))
    output_path.trace('w', lambda *args: output_path.set(output_entry.get()))
    # 为 resize 设置 trace 方法，用于更新储存文本的变量
    entered_to_size.trace('w', lambda *_: entered_to_size.set(to_size_entry.get()))

    # 显示两个 entry
    ipath_txt = tk.Label(text="输入路径：", foreground="white", background="black")
    ipath_txt.pack(padx=50, pady=4)
    input_entry.pack(side="top", fill="x", padx=64, pady=16)
    opath_txt = tk.Label(text="输出路径：", foreground="white", background="black")
    opath_txt.pack(padx=50, pady=4)
    output_entry.pack(side="top", fill="x", padx=64, pady=16)
    # 显示 resize
    to_size = tk.Label(text="指定生成的图片尺寸为（方形，不填则为默认值：768）：", foreground="white", background="black")
    to_size.pack(padx=50, pady=4)
    to_size_entry.pack(side="top", fill="x", padx=64, pady=16)

    # 创建一个 Text 控件，用来展示 log 信息
    log_text_label = tk.Label(text="生成信息： ", foreground="white", background="black")
    log_text_label.pack(side="top", fill="x", padx=64, pady=4)
    log_text = tk.Text(window)
    log_text.pack(side="top", fill="x", padx=64, pady=4)

    # 创建按钮，并将函数作为 command 参数传递给按钮
    run_button = tk.Button(window, text="Run", command=lambda: image_processor(input_path.get(), output_path.get(), to_size_entry.get()), width=16, height=2)
    run_button.pack(side="left", fill="x", padx=window_width/8, pady=4)

    # 创建一个按钮，并将 quit 方法作为 command 参数传递给按钮
    close_button = tk.Button(window, text="Close", command=window.quit, width=16, height=2)
    close_button.pack(side="right", fill="x", padx=window_width/8, pady=4)

    # 运行窗口
    window.mainloop()









