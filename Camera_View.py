import tkinter as tk
from PIL import ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CameraView(object):

    def __init__(self):
        self.stats_canvas = None
        self.text_label_sum = None
        self.person_sum_label = None
        self._show_gui()

    def _show_gui(self):
        self.window = tk.Tk()
        self.window.title("Video Feeds")

        self.canvases = []

        # Get the dimensions of the screen
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # Set the size of the window to the maximum available size
        self.window.geometry("{}x{}".format(self.screen_width, self.screen_height))

        self.video_box_width = self.screen_width // 2
        self.video_box_height = self.screen_height // 2

        self.create_camera_feeds()
        self.create_stats_canvas()
        self.create_plots()
        # self.create_information_elements()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_camera_feeds(self):
        for i in range(2):
            print(i)
            canvas = tk.Canvas(self.window, width=self.video_box_width, height=self.video_box_height, bg="white")
            canvas.grid(row=0, column=i)
            self.canvases.append(canvas)

    def update_feeds(self, frame, i):
        img = ImageTk.PhotoImage(frame.resize(
            (self.video_box_width, self.video_box_height), reducing_gap=1.0))

        if img is not None:
            self.canvases[i].create_image(0, 0, image=img, anchor=tk.NW)
            self.canvases[i].image = img

    def create_stats_canvas(self):
        self.stats_canvas = tk.Canvas(self.window, width=self.screen_width,
                                      height=self.screen_height - self.video_box_height, bg="white")
        self.stats_canvas.grid(row=1, column=0, columnspan=2)

    def create_plots(self):
        figure1 = Figure(figsize=(6, 4), dpi=100)
        self.ax1 = figure1.add_subplot(111)

        figure2 = Figure(figsize=(6, 4), dpi=100)
        self.ax2 = figure2.add_subplot(111)

        figure3 = Figure(figsize=(6, 4), dpi=100)
        self.ax3 = figure3.add_subplot(111)

        self.plot_canvas1 = FigureCanvasTkAgg(figure1, master=self.stats_canvas)
        self.plot_canvas2 = FigureCanvasTkAgg(figure2, master=self.stats_canvas)
        self.plot_canvas3 = FigureCanvasTkAgg(figure3, master=self.stats_canvas)

        self.plot_canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
        self.plot_canvas2.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)
        self.plot_canvas3.get_tk_widget().grid(row=0, column=2, padx=10, pady=10)

    def run(self):
        self.window.mainloop()

    def on_close(self):
        self.window.destroy()
