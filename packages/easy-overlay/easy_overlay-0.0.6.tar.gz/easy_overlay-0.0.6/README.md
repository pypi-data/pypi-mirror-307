# 🖼️ PyOverlay - Transparent Overlay for Windows 🎉

PyOverlay is a cool, Python-based tool that lets you create a transparent, always-on-top overlay on your screen. Imagine drawing lines, shapes, or even text over your screen without blocking your clicks. This overlay is perfect for creating visual aids in games, making tutorials, or just experimenting with graphics in Python! 

## 🚀 Requirements

To use PyOverlay, make sure you have:
- **Python 3.x** 🐍
- **pywin32** library: This library helps Python talk to Windows functions.

   To install `pywin32`, open your terminal (or Command Prompt) and type:#

      ```bash
       pip install pywin32
      ```
## 🔧 Getting Started

1. **Create an `Overlay` instance** - This sets up the overlay for you.
2. **Start the overlay** - Use `start()` to make the overlay window appear.
3. **Draw on the overlay** - Use the various draw methods to add shapes, lines, and text.
4. **Stop the overlay** - Call `stop()` to close the overlay when you're done.

Let’s walk through each feature step-by-step! 📜

---

## 🛠️ Overlay Class Methods

### 🔹 Initialization

- **Overlay()**: This creates a blank overlay for you to start drawing on.

   ```py
   overlay = Overlay()
   ```

---

### 🔹 Overlay Control Methods

#### 1. `start()` - Start the overlay 🖥️

This method shows the overlay on your screen. Call this before you start drawing.

   ```py
   overlay.start()
   ```

#### 2. `stop()` - Stop the overlay ❌

This method hides and closes the overlay. You should call this when you're finished to free up resources.

   ```py
   overlay.stop()
   ```

---

### 🖌️ Drawing Methods

Each of these drawing methods will add something to the overlay screen. You can call multiple drawing functions one after the other to create complex visuals!

#### 1. `draw_line(start_pos, end_pos, color=(255, 0, 0), thickness=2)` - Draw a line ➖

Draws a line from one point to another.

   **Parameters**:
   - `start_pos`: Starting position `(x, y)` of the line.
   - `end_pos`: Ending position `(x, y)` of the line.
   - `color`: RGB color for the line. `(255, 0, 0)` is red by default.
   - `thickness`: Width of the line in pixels. Default is `2`.

   **Example**:

   ```py
   overlay.draw_line((100, 100), (400, 400), color=(255, 0, 0), thickness=2)
   ```

#### 2. `draw_rectangle(start_pos, end_pos, color=(255, 0, 0), thickness=2)` - Draw a rectangle ▭

Draws a rectangle with two corners.

   **Parameters**:
   - `start_pos`: Top-left corner `(x, y)` of the rectangle.
   - `end_pos`: Bottom-right corner `(x, y)` of the rectangle.
   - `color`: RGB color for the rectangle. `(255, 0, 0)` is red by default.
   - `thickness`: Border thickness in pixels. Default is `2`.

   **Example**:

   ```py
   overlay.draw_rectangle((200, 200), (500, 500), color=(0, 255, 0), thickness=3)
   ```

#### 3. `draw_circle(center, radius, color=(255, 0, 0), thickness=2)` - Draw a circle ⚫

Draws a circle with a specific center and radius.

   **Parameters**:
   - `center`: Center `(x, y)` of the circle.
   - `radius`: Radius (size) of the circle.
   - `color`: RGB color for the circle. `(255, 0, 0)` is red by default.
   - `thickness`: Border thickness in pixels. Default is `2`.

   **Example**:

   ```py
   overlay.draw_circle((400, 400), 50, color=(0, 0, 255), thickness=2)
   ```

#### 4. `draw_text(text, pos, color=(255, 255, 255), size=16)` - Display text 📝

Draws text on the screen.

   **Parameters**:
   - `text`: The text you want to display.
   - `pos`: Position `(x, y)` for the text’s top-left corner.
   - `color`: RGB color for the text. `(255, 255, 255)` is white by default.
   - `size`: Font size. Default is `16`.

   **Example**:

   ```py
   overlay.draw_text("Hello, Overlay!", (300, 300), color=(255, 255, 255), size=24)
   ```

#### 5. `draw_crosshair(center, size=24, color=(0, 255, 0), thickness=1)` - Draw a crosshair 🎯

Draws a crosshair (like a sniper scope!) centered on a point.

   **Parameters**:
   - `center`: Center `(x, y)` of the crosshair.
   - `size`: The size of the crosshair. Default is `24`.
   - `color`: RGB color for the crosshair. `(0, 255, 0)` is green by default.
   - `thickness`: Line thickness for the crosshair. Default is `1`.

   **Example**:

   ```py
   overlay.draw_crosshair((500, 500), size=24, color=(0, 255, 0), thickness=1)
   ```

---

### 🔄 `clear()` - Clear the overlay 🔄

Removes all drawings from the overlay, leaving a blank transparent background.

   **Example**:

   ```py
   overlay.clear()
   ```

---

## 👶 Full Example: Putting It All Together

Here’s a complete example that shows how to use the overlay, draw on it, and stop it after a short delay:

   ```py
   from overlay import Overlay
   import time

   # Step 1: Create the overlay
   overlay = Overlay()

   # Step 2: Start the overlay
   overlay.start()

   # Step 3: Draw various shapes and text
   overlay.draw_line((100, 100), (400, 400), color=(255, 0, 0), thickness=2)
   overlay.draw_rectangle((200, 200), (500, 500), color=(0, 255, 0), thickness=3)
   overlay.draw_text("Hello, Overlay!", (300, 300), color=(255, 255, 255), size=24)
   overlay.draw_circle((400, 400), 50, color=(0, 0, 255), thickness=2)
   overlay.draw_crosshair((500, 500), size=24, color=(0, 255, 0), thickness=1)

   # Step 4: Keep the overlay for 5 seconds, then stop it
   time.sleep(5)
   overlay.stop()
   ```

This will create an overlay, draw a line, rectangle, text, circle, and crosshair, and then close the overlay after 5 seconds. 🎉

## ⚠️ Notes
- Make sure to **call `stop()`** to close the overlay and free resources.
- Each `draw_` method queues up a draw operation, which the overlay then renders.

---

Happy coding! 👾 Enjoy creating fun overlays with PyOverlay!
