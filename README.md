# TkinterRealTimeData
Real time data displayed via Matplotlib on a Tkinter frame and therefore can be used for interactive testing.

## Python Version
3+

## Modules
import matplotlib<br>
import threading<br>                                                                                         
import time <br>
import tkinter as tk <br>
import matplotlib <br>
import matplotlib.pyplot as plt <br> 
import numpy as np <br>
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

## Usage
The cool thing about this project is that one can hardcore determine the
time after that the plot is updated. **But** in contrast to the animation method that
is already on the market this project works via threading, which means that even
if there is lots of code behind this GUI going on the plot should be updated with
good precision on the wanted time scale which is not true for the animation method that is
already on the market.

## License
(None)

## Creator
[Leon Renn](https://github.com/leonrenn)
