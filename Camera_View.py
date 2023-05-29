import tkinter as tk
from PIL import ImageTk
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import matplotlib.dates as mdates
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
        self.window.configure(bg="white")

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
                                      height=self.screen_height - self.video_box_height, bg="white", borderwidth=0,
                                      highlightthickness=0)
        self.stats_canvas.grid(row=1, column=0, columnspan=2)

    def create_plots(self):
        figure1 = Figure(figsize=(6, 4), dpi=100)
        self.ax1 = figure1.add_subplot(111)
        figure2 = Figure(figsize=(6, 4), dpi=100)
        self.ax2 = figure2.add_subplot(111)
        figure3 = Figure(figsize=(6, 4), dpi=100)
        self.ax3 = figure3.add_subplot(111)

        figure1.tight_layout()
        figure2.tight_layout()
        figure3.tight_layout()

        self.plot_canvas1 = FigureCanvasTkAgg(figure1, master=self.stats_canvas)
        self.plot_canvas2 = FigureCanvasTkAgg(figure2, master=self.stats_canvas)
        self.plot_canvas3 = FigureCanvasTkAgg(figure3, master=self.stats_canvas)

        self.plot_canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
        self.plot_canvas2.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)
        self.plot_canvas3.get_tk_widget().grid(row=0, column=2, padx=10, pady=10)

    def update_gender_plot(self, data):
        self.ax1.clear()
        categories = 'Men', 'Women'

        self.ax1.pie(data, radius=1, labels=categories, autopct='%1.1f%%',
                     pctdistance=1.25, labeldistance=.4, textprops={'fontsize': 16})

        self.ax1.set_aspect('equal')
        self.plot_canvas1.draw()

    def update_age_plot(self, data):
        self.ax2.clear()

        self.ax2.plot(data[0], data[1], linestyle='-')
        self.ax2.set_xlabel('Timestamp')
        self.ax2.set_ylabel('Age')
        self.ax2.set_ylim(0, 80)
        self.ax2.set_title('Age Graph')
        self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.ax2.tick_params(axis='x', rotation=45)
        self.plot_canvas2.draw()

    def run(self):
        self.window.mainloop()

    def on_close(self):
        self.window.destroy()
