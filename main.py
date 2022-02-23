# MODULES

import threading
import time
import tkinter as tk
from pickletools import float8

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

# CLASSES


class Timer(threading.Thread):
    def __init__(self,
                 plotter: object,
                 event: threading.Event,
                 lock: threading.Lock,
                 update_interval: int = 1):
        """Timer that calls the plotting function
        when its time to

        Args:
            plotter (object): [class for the plotter]
            event (threading.Event): [events for controlling
            threading]
            lock (threading.Lock): [locking the thread
            for better control in case of multiple
            threads]
            update_interval (int, optional): [interval in seconds,
            determines how often the plot is updated].
            Defaults to 1.
        """
        threading.Thread.__init__(self)
        self.plotter = plotter
        self.event = event
        self.lock = lock
        self.update_interval = update_interval
        self.ID = threading.get_ident()

        self.__precision()

    def run(self) -> None:
        """Method that is activated when
        threading is started in the main
        function. Runs infinitely many times,
        until stopped by the setting
        of the event. Updates the plot.
        """
        START = round(time.time(), self.precision)
        step = START
        while True:
            self.lock.acquire()
            if self.event.isSet():
                print(f"Thread Clock: '{self.ID} is closed.'")
                self.lock.release()
                return
            else:
                next_step = round(
                    time.time() + self.update_interval, self.precision + 1)
                difference = next_step - step
                upper_border = self.update_interval + \
                    0.1 * (self.precision + 1)
                lower_border = self.update_interval - \
                    0.1 * (self.precision + 1)

                if difference < upper_border and difference > lower_border:
                    step = next_step
                    self.plotter.update_data(step-START)

                self.lock.release()
                time.sleep(self.sleep)

    def __precision(self):
        """Calculates the precision of that the user
        wants to update the plotting. For example
        if the default value of update_interval=1 is
        used. The plot is updated if the duration
        from the last updated is in [1-0.1*1, 1+0.1*1].
        """
        time_interval_list = str(self.update_interval).split(".")
        if len(time_interval_list) == 2:
            self.precision = len(time_interval_list[-1])
        else:
            self.precision = 0

        self.sleep = float("0." + (self.precision)*"0"+"1")
        return


class TimedPlotter(tk.Frame):
    def __init__(self,
                 master: tk.Frame,
                 figure_geometries: tuple):
        """Constructor for the Timed_Plotter class.
        Creates all needed variables.

        Args:
            master (tk.Frame): [tkinter frame in which the
            plot will be hosted]
            figure_geometries (tuple): [geometries of the mat-
            plotlib figure]
        """
        tk.Frame.__init__(self, master=master)

        self.master = master
        self.figure_geometries = figure_geometries

        self.x = np.array([0], dtype="float32")
        self.y = np.array([0], dtype="float32")

        font = {'family': 'sans-serif',
                'weight': 'normal',
                'size': 10}

        matplotlib.rc('font', **font)

        self.figure, self.axis = plt.subplots(figsize=self.figure_geometries)
        self.figure.set_tight_layout(True)
        self.axis.set_xlabel("Time")
        self.axis.set_ylabel("Y")
        self.line, = self.axis.plot(self.x,
                                    self.y,
                                    label="Data",
                                    linestyle="--")
        self.plot_canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.plot_canvas.get_tk_widget().pack()

    def update_data(self, time_step: float) -> None:
        """Method called by the clock the Timer.
        Updates the plot on the x, y axis and sets
        new limits which is mandatory.

        Args:
            time_step (float): [gives new time
            data for the x axis. the y coordinate
            is here purely random, but should normally
            be acquired from some test device]
        """
        self.x = np.append(self.x, time_step)
        self.y = np.append(self.y, np.random.rand())
        self.line.set_data(self.x, self.y)
        self.axis.set_xlim(0, self.x[-1])
        self.axis.set_ylim(-0.2, 1)
        self.figure.canvas.draw_idle()
        return

    def __del__(self):
        """Showed when instance is deleted.
        """
        print("Closed the plot")
        return

# FUNCTION


def close(threading_event) -> None:
    """Closes the tkinter program 
    after setting the event that stops 
    the threading class.

    Args:
        threading_event (threading.Event): [Event to stop
        threading class]
    """
    threading_event.set()
    time.sleep(1)
    exit()
    return


# MAIN FUNCTION


def main() -> int:

    # root

    root = tk.Tk()
    root.geometry("800x600")
    root.title("Timed Data Analysis with tkinter")

    # plotting canvas

    plotting_canvas = tk.Frame(root,
                               width=600,
                               height=400,
                               bg="white")
    plotting_canvas.place(x=100, y=100)

    # threading properties

    threading_event = threading.Event()
    threading_lock = threading.Lock()

    # close button

    tk.Button(root, command=lambda: close(threading_event), text="END").pack()

    # intialize instance

    update_interval = 1  # in seconds
    figure_geometries = (4, 3)

    plotter = TimedPlotter(plotting_canvas,
                           figure_geometries)

    t = Timer(plotter,
              threading_event,
              threading_lock,
              update_interval)
    t.start()

    # looping

    root.mainloop()
    return 0

# STARTING MAIN FUNCTION


if __name__ == "__main__":
    main()
