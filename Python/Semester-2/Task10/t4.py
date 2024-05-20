import numpy as np
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')


def update(val):
    amp1 = samp1.val
    freq1 = sfreq1.val
    amp2 = samp2.val
    freq2 = sfreq2.val
    y1 = amp1 * np.sin(freq1 * x)
    y2 = amp2 * np.sin(freq2 * x)
    y_sum = y1 + y2
    line1.set_ydata(y1)
    line2.set_ydata(y2)
    line_sum.set_ydata(y_sum)
    fig.canvas.draw_idle()


if __name__ == '__main__':
    fig, (ax1, ax2, ax_sum) = plt.subplots(3, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [1, 1, 1.5]})

    amp1_init = 1
    freq1_init = 1
    amp2_init = 1
    freq2_init = 1

    x = np.linspace(0, 2 * np.pi, 1000)
    y1 = amp1_init * np.sin(freq1_init * x)
    y2 = amp2_init * np.sin(freq2_init * x)
    y_sum = y1 + y2

    line1, = ax1.plot(x, y1, label='Wave 1')
    line2, = ax2.plot(x, y2, label='Wave 2')
    line_sum, = ax_sum.plot(x, y_sum, label='Sum of Waves')

    ax1.set_ylim(-2, 2)
    ax2.set_ylim(-2, 2)
    ax_sum.set_ylim(-4, 4)

    plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.4)

    axamp1 = plt.axes([0.15, 0.30, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    axfreq1 = plt.axes([0.15, 0.25, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    axamp2 = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    axfreq2 = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor='lightgoldenrodyellow')

    samp1 = Slider(axamp1, 'Amp 1', 0.1, 10.0, valinit=amp1_init)
    sfreq1 = Slider(axfreq1, 'Freq 1', 0.1, 10.0, valinit=freq1_init)
    samp2 = Slider(axamp2, 'Amp 2', 0.1, 10.0, valinit=amp2_init)
    sfreq2 = Slider(axfreq2, 'Freq 2', 0.1, 10.0, valinit=freq2_init)
    samp1.on_changed(update)

    sfreq1.on_changed(update)
    samp2.on_changed(update)
    sfreq2.on_changed(update)

    plt.show()
