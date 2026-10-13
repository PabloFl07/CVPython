import marimo

__generated_with = "0.25.1"
app = marimo.App(width="full")


@app.cell
def _():
    import cv2
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return cv2, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Color spaces
    """)
    return


@app.cell
def _(cv2, mo):
    img_path = "New_Zealand_Lake.jpg"
    original = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
    mo.stop(original is None, mo.md("Could not read the Image"))
    return (original,)


@app.cell
def _(np, plt):
    GRAY = "gray"
    CYCLIC = "hsv"
    DIVERGING = "coolwarm"
    FULL = (0, 255)
    HUE = (0, 179)  # Hue channel in OpenCV is [0, 179] for uint8 images
    NEUTRAL = 128  # Neutral value of chroma channels (Cr, Cb, a*, b*) in uint8

    def centered_range(channel, center=NEUTRAL):
        """Symmetric display range around `center` that covers all values of `channel`."""
        low = int(np.min(channel))
        high = int(np.max(channel))
        half_width = max(abs(low - center), abs(high - center), 1)
        return (center - half_width, center + half_width)

    def show_channels(image, channels, titles, colormaps, ranges):
        """Show the original BGR image next to each channel, with a colorbar per channel."""

        n_panels = len(channels) + 1
        fig, axes = plt.subplots(1, n_panels, figsize=(5 * n_panels, 5))

        axes[0].imshow(image[:, :, ::-1])  # BGR -> RGB for matplotlib
        axes[0].set_title("Original")
        axes[0].axis("off")

        for ax, channel, title, colormap, (vmin, vmax) in zip(axes[1:], channels, titles, colormaps, ranges):
            im = ax.imshow(channel, vmin=vmin, vmax=vmax, cmap=colormap)
            ax.set_title(title)
            ax.axis("off")
            fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        fig.tight_layout()
        return fig

    return CYCLIC, DIVERGING, FULL, GRAY, HUE, centered_range, show_channels


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Notes

    **Code**

    - Private variables (`_h`, `_s`, `_v`, …): in marimo, a name that starts with `_` is private to its cell and is not exported to the notebook.
    Since each cell defines its own channels, there is no need to invent unique names for each one.
    If they were defined without `_`, marimo would raise an error for variables defined in more than one cell.

    **Colormaps**

    - `CYCLIC` (`"hsv"`) is used for hue. Hue is circular: 0 and 179 (0° and 358°) are both red, so the cyclic colormap makes both ends match in color.
    - `DIVERGING` (`"coolwarm"`) is used for channels centered on a neutral value (Cr, Cb, a*, b*).
    Their values deviate in two directions from neutral (for example, red versus green), and the diverging colormap shows each side with a different color and the midpoint in light gray.
    - `GRAY` is used for the remaining channels (intensities, luminances, saturations), which have a single direction of magnitude.

    **Display ranges**

    - Gray and hue channels use their full range, so the brightness of the image is comparable across channels.
    - Chroma channels use a range **symmetric around 128** (`centered_range`). In natural images they concentrate in a narrow band around the neutral value;
    with the full range $[0, 255]$ almost every pixel would map to the light-gray midpoint and the information would be invisible.
    Because the range is symmetric, its center is exactly 128. Check the colorbar: its limits change from channel to channel.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## RGB

    OpenCV stores a read image as **BGR** instead of **RGB**.
    """)
    return


@app.cell
def _(FULL, GRAY, cv2, original, show_channels):
    _b, _g, _r = cv2.split(original)  # BGR order: no conversion needed
    show_channels(
        original,
        [_r, _g, _b],
        ["Red Channel", "Green Channel", "Blue Channel"],
        [GRAY, GRAY, GRAY],
        [FULL, FULL, FULL],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## HSV

    **Hue is undefined when saturation is low.** For a gray pixel ($S = 0$) there is no dominant color, so $H$ has no meaning: OpenCV assigns $H = 0$ (red).

    For pixels with very low $S$, $H$ is defined but extremely sensitive to noise, because a tiny change in R, G or B can rotate the hue completely.

    Whitish or grayish regions (bright sky, clouds, snow) therefore look red or noisy in the hue channel. This is why hue-based segmentation usually also requires a minimum saturation (and value).
    """)
    return


@app.cell
def _(CYCLIC, FULL, GRAY, HUE, cv2, original, show_channels):
    _h, _s, _v = cv2.split(cv2.cvtColor(original, cv2.COLOR_BGR2HSV))
    show_channels(
        original,
        [_h, _s, _v],
        ["Hue Channel", "Saturation Channel", "Value Channel"],
        [CYCLIC, GRAY, GRAY],
        [HUE, FULL, FULL],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## HSL

    OpenCV calls this space **HLS** and returns the channels in that order: $H$, $L$, $S$.
    """)
    return


@app.cell
def _(CYCLIC, FULL, GRAY, HUE, cv2, original, show_channels):
    _h, _l, _s = cv2.split(cv2.cvtColor(original, cv2.COLOR_BGR2HLS))  # OpenCV returns H, L, S!
    show_channels(
        original,
        [_h, _l, _s],
        ["Hue Channel", "Lightness Channel", "Saturation Channel"],
        [CYCLIC, GRAY, GRAY],
        [HUE, FULL, FULL],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## YCbCr

    OpenCV calls this space **YCrCb** and returns the channels in that order: $Y'$, $C_r$, $C_b$.
    It uses the **BT.601** coefficients in **full range** $[0, 255]$, as in JPEG, not the studio range $[16, 235]$ used in video.
    """)
    return


@app.cell
def _(DIVERGING, FULL, GRAY, centered_range, cv2, original, show_channels):
    _y, _cr, _cb = cv2.split(cv2.cvtColor(original, cv2.COLOR_BGR2YCrCb))  # OpenCV returns Y, Cr, Cb!
    show_channels(
        original,
        [_y, _cr, _cb],
        ["Luma Channel (Y')", "Red-difference Chroma (Cr)", "Blue-difference Chroma (Cb)"],
        [GRAY, DIVERGING, DIVERGING],
        [FULL, centered_range(_cr), centered_range(_cb)],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lab

    `COLOR_BGR2Lab` assumes the input is **sRGB** (it undoes the gamma before computing XYZ) and uses the **D65** reference white. For input that is already linear, use `COLOR_LBGR2Lab`.
    """)
    return


@app.cell
def _(DIVERGING, FULL, GRAY, centered_range, cv2, original, show_channels):
    _l, _a, _b = cv2.split(cv2.cvtColor(original, cv2.COLOR_BGR2Lab))
    show_channels(
        original,
        [_l, _a, _b],
        ["Lightness Channel (L*)", "a* Channel (green - red)", "b* Channel (blue - yellow)"],
        [GRAY, DIVERGING, DIVERGING],
        [FULL, centered_range(_a), centered_range(_b)],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## BGR/RGB conversions

    | Result     | `uint8` (input in $[0, 255]$)                   | `float32` (input in $[0, 1]$)          |
    | ---------- | ----------------------------------------------- | -------------------------------------- |
    | HSV / HLS  | $H \in [0, 179]$, rest $[0, 255]$               | $H \in [0, 360)$, rest $[0, 1]$        |
    | HSV / HLS `_FULL` | $H \in [0, 255]$, rest $[0, 255]$        | same as without `_FULL`                |
    | YCrCb      | $[0, 255]$, chroma centered at 128              | $[0, 1]$, chroma centered at 0.5       |
    | Lab        | $L^* \cdot 255/100$, $a^* + 128$, $b^* + 128$   | $L^* \in [0, 100]$ and $a^*, b^*$ real |

    - `COLOR_BGR2HSV_FULL` / `COLOR_BGR2HLS_FULL` map the hue to the whole `uint8` range: steps of $360/256 \approx 1.41°$ instead of $2°$.
    The inverse conversion must also be the `_FULL` one (`COLOR_HSV2BGR_FULL`).
    - YCrCb: BT.601 coefficients, full range (JPEG convention).
    - Lab: input assumed sRGB, D65 reference white (`COLOR_LBGR2Lab` for linear input).

    Passing a `float32` in $[0, 255]$ (instead of $[0, 1]$) does not raise an error, but produces incorrect results. Before converting: `img.astype(np.float32) / 255.0`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Quantization losses

    Every conversion with `uint8` output rounds. Chaining conversions accumulates error:

    - **HSV/HLS**: hue is represented with 180 levels, that is, steps of $2°$ (or $\approx 1.41°$ with `_FULL`).
    - **Lab**: $L^*$ is rescaled to 256 levels ($\approx 0.39$ units per level, no appreciable loss); $a^*$ and $b^*$ are shifted by $+128$ and rounded to integers, so sub-unit differences are lost.

    If several operations are going to be chained, work in `float32` and convert to `uint8` only at the end.

    The figure below shows it: the image is converted BGR → HSV → BGR in both ways, and each map shows how many levels each pixel differs from the original.
    """)
    return


@app.cell
def _(cv2, np):
    def roundtrip_uint8(image):
        """Brute force: convert directly in uint8 (rounds at every step)."""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def roundtrip_float32(image):
        """Correct: normalize to float32 in [0, 1], convert, round only at the end."""
        work = image.astype(np.float32) / 255.0
        hsv = cv2.cvtColor(work, cv2.COLOR_BGR2HSV)
        back = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return np.clip(np.round(back * 255.0), 0, 255).astype(np.uint8)

    return roundtrip_float32, roundtrip_uint8


@app.cell
def _(np, original, plt, roundtrip_float32, roundtrip_uint8):
    # int16 so that the subtraction can be negative; max over B, G, R
    _diff_u8 = np.abs(roundtrip_uint8(original).astype(np.int16) - original.astype(np.int16)).max(axis=2)
    _diff_f = np.abs(roundtrip_float32(original).astype(np.int16) - original.astype(np.int16)).max(axis=2)

    _vmax = max(int(_diff_u8.max()), 1)  # same scale in both panels

    plt.figure(figsize=(12, 5))
    plt.subplot(121)
    plt.imshow(_diff_u8, vmin=0, vmax=_vmax, cmap="magma")
    plt.title("Brute force (uint8)")
    plt.colorbar()
    plt.subplot(122)
    plt.imshow(_diff_f, vmin=0, vmax=_vmax, cmap="magma")
    plt.title("Correct (float32)")
    plt.colorbar()
    plt.gcf()
    return


if __name__ == "__main__":
    app.run()
