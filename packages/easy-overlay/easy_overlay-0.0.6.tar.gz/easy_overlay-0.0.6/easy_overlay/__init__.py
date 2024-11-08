import win32gui
import win32con
import win32api
from ctypes import windll, Structure, byref, create_string_buffer, create_unicode_buffer
from ctypes.wintypes import DWORD, LONG, BYTE, WCHAR, UINT, HANDLE, POINT
import threading
import time

dwmapi = windll.dwmapi

class LOGFONT(Structure):
    _fields_ = [
        ('lfHeight', LONG),
        ('lfWidth', LONG),
        ('lfEscapement', LONG),
        ('lfOrientation', LONG),
        ('lfWeight', LONG),
        ('lfItalic', BYTE),
        ('lfUnderline', BYTE),
        ('lfStrikeOut', BYTE),
        ('lfCharSet', BYTE),
        ('lfOutPrecision', BYTE),
        ('lfClipPrecision', BYTE),
        ('lfQuality', BYTE),
        ('lfPitchAndFamily', BYTE),
        ('lfFaceName', WCHAR * 32)
    ]

class Overlay:
    def __init__(self):
        self._running = False
        self._hwnd = None
        self._thread = None
        self._dc = None
        self._width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self._height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        self._draw_queue = []
        self._lock = threading.Lock()

    def _create_window(self):
        wc = win32gui.WNDCLASS()
        wc.lpszClassName = "PyOverlayClass"
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = self._wnd_proc

        win32gui.RegisterClass(wc)

        style = win32con.WS_POPUP | win32con.WS_VISIBLE
        style_ex = (win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | 
                   win32con.WS_EX_TOPMOST)

        self._hwnd = win32gui.CreateWindowEx(
            style_ex,
            wc.lpszClassName,
            "PyOverlay",
            style,
            0, 0,
            self._width, self._height,
            0, 0,
            0, None
        )

        win32gui.SetLayeredWindowAttributes(
            self._hwnd,
            win32api.RGB(0, 0, 0),
            0,
            win32con.LWA_COLORKEY
        )

        win32gui.ShowWindow(self._hwnd, win32con.SW_SHOW)
        self._dc = win32gui.GetDC(self._hwnd)

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def start(self):
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._window_loop)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
            win32gui.ReleaseDC(self._hwnd, self._dc)
            win32gui.DestroyWindow(self._hwnd)

    def _window_loop(self):
        self._create_window()
        
        while self._running:
            try:
                msg = win32gui.PeekMessage(None, 0, 0, 0)
                if msg[0]:
                    win32gui.TranslateMessage(msg[1])
                    win32gui.DispatchMessage(msg[1])

                with self._lock:
                    for draw_func in self._draw_queue:
                        try:
                            draw_func(self._dc)
                        except Exception as e:
                            print(f"Draw error: {e}")
                    self._draw_queue.clear()
                
                # Sync with DWM
                dwmapi.DwmFlush()

            except Exception as e:
                pass

            # Minimal sleep to prevent CPU overuse while still maintaining responsiveness
            time.sleep(0.0001)

    def draw_line(self, start_pos, end_pos, color=(255, 0, 0), thickness=2):
        def _draw(dc):
            pen = win32gui.CreatePen(win32con.PS_SOLID, thickness, 
                                   win32api.RGB(*color))
            old_pen = win32gui.SelectObject(dc, pen)
            
            win32gui.MoveToEx(dc, int(start_pos[0]), int(start_pos[1]))
            win32gui.LineTo(dc, int(end_pos[0]), int(end_pos[1]))
            
            win32gui.SelectObject(dc, old_pen)
            win32gui.DeleteObject(pen)

        with self._lock:
            self._draw_queue.append(_draw)

    def draw_rectangle(self, start_pos, end_pos, color=(255, 0, 0), thickness=2):
        def _draw(dc):
            pen = win32gui.CreatePen(win32con.PS_SOLID, thickness, 
                                   win32api.RGB(*color))
            old_pen = win32gui.SelectObject(dc, pen)
            
            null_brush = win32gui.GetStockObject(win32con.NULL_BRUSH)
            old_brush = win32gui.SelectObject(dc, null_brush)
            
            win32gui.Rectangle(dc, 
                             int(start_pos[0]), int(start_pos[1]),
                             int(end_pos[0]), int(end_pos[1]))
            
            win32gui.SelectObject(dc, old_pen)
            win32gui.SelectObject(dc, old_brush)
            win32gui.DeleteObject(pen)

        with self._lock:
            self._draw_queue.append(_draw)
    
    def draw_circle(self, center, radius, color=(255, 0, 0), thickness=2):
        def _draw(dc):
            pen = win32gui.CreatePen(win32con.PS_SOLID, thickness, 
                                win32api.RGB(*color))
            old_pen = win32gui.SelectObject(dc, pen)
            
            left = int(center[0] - radius)
            top = int(center[1] - radius)
            right = int(center[0] + radius)
            bottom = int(center[1] + radius)
            
            win32gui.Arc(dc, left, top, right, bottom,
                        left, top, left, top)
            
            win32gui.SelectObject(dc, old_pen)
            win32gui.DeleteObject(pen)

        with self._lock:
            self._draw_queue.append(_draw)

    def draw_text(self, text, pos, color=(255, 255, 255), size=16):
        def _draw(dc):
            lf = LOGFONT()
            lf.lfHeight = size
            lf.lfWidth = 0
            lf.lfWeight = 400
            lf.lfQuality = win32con.ANTIALIASED_QUALITY
            lf.lfCharSet = win32con.ANSI_CHARSET
            
            font_name = create_unicode_buffer("Arial")
            lf.lfFaceName = font_name.value

            hfont = windll.gdi32.CreateFontIndirectW(byref(lf))
            old_font = win32gui.SelectObject(dc, hfont)
            
            windll.gdi32.SetTextColor(dc, win32api.RGB(*color))
            windll.gdi32.SetBkMode(dc, win32con.TRANSPARENT)
            
            text_buffer = create_unicode_buffer(text)
            windll.gdi32.TextOutW(dc, int(pos[0]), int(pos[1]), text_buffer, len(text))
            
            win32gui.SelectObject(dc, old_font)
            win32gui.DeleteObject(hfont)

        with self._lock:
            self._draw_queue.append(_draw)

    def clear(self):
        def _draw(dc):
            rect = win32gui.GetClientRect(self._hwnd)
            brush = win32gui.CreateSolidBrush(win32api.RGB(0, 0, 0))
            win32gui.FillRect(dc, rect, brush)
            win32gui.DeleteObject(brush)

        with self._lock:
            self._draw_queue.append(_draw)

    def draw_crosshair(self, center, size=24, color=(0, 255, 0), thickness=1):
        def _draw(dc):
            pen = win32gui.CreatePen(win32con.PS_SOLID, thickness, 
                                    win32api.RGB(*color))
            old_pen = win32gui.SelectObject(dc, pen)
            
            radius = size // 2
            left = int(center[0] - radius)
            top = int(center[1] - radius)
            right = int(center[0] + radius)
            bottom = int(center[1] + radius)
            
            win32gui.Arc(dc, left, top, right, bottom,
                        left, top, left, top)
            
            dot_radius = 1
            dot_left = int(center[0] - dot_radius)
            dot_top = int(center[1] - dot_radius)
            dot_right = int(center[0] + dot_radius)
            dot_bottom = int(center[1] + dot_radius)
            
            brush = win32gui.CreateSolidBrush(win32api.RGB(*color))
            old_brush = win32gui.SelectObject(dc, brush)
            
            win32gui.Ellipse(dc, dot_left, dot_top, dot_right, dot_bottom)
            
            win32gui.SelectObject(dc, old_pen)
            win32gui.SelectObject(dc, old_brush)
            win32gui.DeleteObject(pen)
            win32gui.DeleteObject(brush)

        with self._lock:
            self._draw_queue.append(_draw)

    def draw_filled_rectangle(self, start_pos, end_pos, color=(255, 0, 0), alpha=128):
        def _draw(dc):
            brush = win32gui.CreateSolidBrush(win32api.RGB(*color))
            old_brush = win32gui.SelectObject(dc, brush)
            
            pen = win32gui.CreatePen(win32con.PS_SOLID, 1, win32api.RGB(*color))
            old_pen = win32gui.SelectObject(dc, pen)
            
            win32gui.Rectangle(dc, 
                             int(start_pos[0]), int(start_pos[1]),
                             int(end_pos[0]), int(end_pos[1]))
            
            win32gui.SelectObject(dc, old_pen)
            win32gui.SelectObject(dc, old_brush)
            win32gui.DeleteObject(pen)
            win32gui.DeleteObject(brush)

        with self._lock:
            self._draw_queue.append(_draw)

    def draw_filled_circle(self, center, radius, color=(255, 0, 0), alpha=128):
        def _draw(dc):
            brush = win32gui.CreateSolidBrush(win32api.RGB(*color))
            old_brush = win32gui.SelectObject(dc, brush)
            
            pen = win32gui.CreatePen(win32con.PS_SOLID, 1, win32api.RGB(*color))
            old_pen = win32gui.SelectObject(dc, pen)
            
            left = int(center[0] - radius)
            top = int(center[1] - radius)
            right = int(center[0] + radius)
            bottom = int(center[1] + radius)
            
            win32gui.Ellipse(dc, left, top, right, bottom)
            
            win32gui.SelectObject(dc, old_pen)
            win32gui.SelectObject(dc, old_brush)
            win32gui.DeleteObject(pen)
            win32gui.DeleteObject(brush)

        with self._lock:
            self._draw_queue.append(_draw)

    def draw_arrow(self, start_pos, end_pos, color=(255, 0, 0), thickness=2, arrow_size=10):
        def _draw(dc):
            import math
            
            pen = win32gui.CreatePen(win32con.PS_SOLID, thickness, win32api.RGB(*color))
            old_pen = win32gui.SelectObject(dc, pen)
            
            win32gui.MoveToEx(dc, int(start_pos[0]), int(start_pos[1]))
            win32gui.LineTo(dc, int(end_pos[0]), int(end_pos[1]))
            
            angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
            arrow_angle = math.pi / 6
            
            x1 = end_pos[0] - arrow_size * math.cos(angle - arrow_angle)
            y1 = end_pos[1] - arrow_size * math.sin(angle - arrow_angle)
            x2 = end_pos[0] - arrow_size * math.cos(angle + arrow_angle)
            y2 = end_pos[1] - arrow_size * math.sin(angle + arrow_angle)
            
            win32gui.MoveToEx(dc, int(end_pos[0]), int(end_pos[1]))
            win32gui.LineTo(dc, int(x1), int(y1))
            win32gui.MoveToEx(dc, int(end_pos[0]), int(end_pos[1]))
            win32gui.LineTo(dc, int(x2), int(y2))
            
            win32gui.SelectObject(dc, old_pen)
            win32gui.DeleteObject(pen)

        with self._lock:
            self._draw_queue.append(_draw)

    def draw_text_box(self, text, pos, color=(255, 255, 255), bg_color=(0, 0, 0), 
                     size=16, padding=5):
        def _draw(dc):
            lf = LOGFONT()
            lf.lfHeight = size
            lf.lfWidth = 0
            lf.lfWeight = 400
            lf.lfQuality = win32con.ANTIALIASED_QUALITY
            font_name = create_unicode_buffer("Arial")
            lf.lfFaceName = font_name.value
            
            hfont = windll.gdi32.CreateFontIndirectW(byref(lf))
            old_font = win32gui.SelectObject(dc, hfont)
            
            text_width, text_height = win32gui.GetTextExtentPoint32(dc, text)
            
            brush = win32gui.CreateSolidBrush(win32api.RGB(*bg_color))
            win32gui.SelectObject(dc, brush)
            win32gui.Rectangle(dc,
                             int(pos[0] - padding),
                             int(pos[1] - padding),
                             int(pos[0] + text_width + padding),
                             int(pos[1] + text_height + padding))
            
            windll.gdi32.SetTextColor(dc, win32api.RGB(*color))
            windll.gdi32.SetBkMode(dc, win32con.TRANSPARENT)
            
            win32gui.DrawText(dc, text, -1, 
                            (int(pos[0]), int(pos[1]), 
                             int(pos[0] + text_width), 
                             int(pos[1] + text_height)),
                            win32con.DT_LEFT | win32con.DT_TOP)
            
            win32gui.SelectObject(dc, old_font)
            win32gui.DeleteObject(hfont)
            win32gui.DeleteObject(brush)

        with self._lock:
            self._draw_queue.append(_draw)
