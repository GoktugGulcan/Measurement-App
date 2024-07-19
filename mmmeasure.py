import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

# Hücre boyutları ve fotoğraf boyutları
cell_width_mm = 182
cell_height_mm = 91
image_width_px = 2888
image_height_px = 1476

# Piksel başına düşen milimetre cinsinden ölçüleri hesapla
px_per_mm_width = image_width_px / cell_width_mm
px_per_mm_height = image_height_px / cell_height_mm

# Global değişkenler
drawing = False
x_init, y_init = -1, -1
top_left_pt, bottom_right_pt = (-1, -1), (-1, -1)
zoom_scale = 1.0
is_dragging = False
drag_start_x, drag_start_y = 0, 0
drag_offset_x, drag_offset_y = 0, 0
img_display = None
min_zoom_scale = 1.0
max_zoom_scale = 10.0

def update_display():
    global img_display, zoom_scale, drag_offset_x, drag_offset_y

    new_width = int(img.shape[1] * zoom_scale)
    new_height = int(img.shape[0] * zoom_scale)
    img_resized = cv2.resize(img, (new_width, new_height))

    x_start = max(0, min(drag_offset_x, new_width - image_width_px))
    y_start = max(0, min(drag_offset_y, new_height - image_height_px))
    x_end = x_start + image_width_px
    y_end = y_start + image_height_px

    img_display = img_resized[y_start:y_end, x_start:x_end]
    cv2.imshow('image', img_display)

def mouse_callback(event, x, y, flags, param):
    global x_init, y_init, drawing, top_left_pt, bottom_right_pt, img, zoom_scale, img_display
    global is_dragging, drag_start_x, drag_start_y, drag_offset_x, drag_offset_y

    if event == cv2.EVENT_LBUTTONDOWN:
        if flags == cv2.EVENT_FLAG_CTRLKEY:
            is_dragging = True
            drag_start_x, drag_start_y = x, y
        else:
            drawing = True
            x_init, y_init = int((x + drag_offset_x) / zoom_scale), int((y + drag_offset_y) / zoom_scale)

    elif event == cv2.EVENT_MOUSEMOVE:
        if is_dragging:
            dx = x - drag_start_x
            dy = y - drag_start_y
            drag_offset_x -= dx
            drag_offset_y -= dy
            drag_start_x, drag_start_y = x, y
            update_display()

        elif drawing:
            img_copy = img_display.copy()
            cv2.rectangle(img_copy, (int(x_init * zoom_scale - drag_offset_x), int(y_init * zoom_scale - drag_offset_y)), (x, y), (0, 255, 0), 2)
            cv2.imshow('image', img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        if is_dragging:
            is_dragging = False
        elif drawing:
            drawing = False
            top_left_pt, bottom_right_pt = (x_init, y_init), (int((x + drag_offset_x) / zoom_scale), int((y + drag_offset_y) / zoom_scale))
            update_display()
            cv2.rectangle(img_display, (int(top_left_pt[0] * zoom_scale - drag_offset_x), int(top_left_pt[1] * zoom_scale - drag_offset_y)),
                          (int(bottom_right_pt[0] * zoom_scale - drag_offset_x), int(bottom_right_pt[1] * zoom_scale - drag_offset_y)), (0, 255, 0), 2)

            # Seçilen alanın piksel boyutlarını hesapla
            width_px = abs(top_left_pt[0] - bottom_right_pt[0])
            height_px = abs(top_left_pt[1] - bottom_right_pt[1])
            
            # Piksel boyutlarını milimetreye dönüştür
            width_mm = width_px / px_per_mm_width*13
            height_mm = height_px / px_per_mm_height*13
            
            # Sonuçları görüntü üzerinde göster
            result_text = f"{width_mm:.2f} mm x {height_mm:.2f} mm"
            cv2.putText(img_display, result_text, (int(top_left_pt[0] * zoom_scale - drag_offset_x), int(top_left_pt[1] * zoom_scale - drag_offset_y) - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.imshow('image', img_display)
            print(f"Seçilen alanın boyutları: {width_mm:.2f} mm x {height_mm:.2f} mm")

    elif event == cv2.EVENT_MOUSEWHEEL:
        old_zoom_scale = zoom_scale
        if flags > 0:
            zoom_scale = min(zoom_scale * 1.1, max_zoom_scale)
        else:
            zoom_scale = max(zoom_scale / 1.1, min_zoom_scale)

        # Hesaplanan offset'i kullanarak görüntüyü zoom merkezine göre ayarla
        center_x = (x + drag_offset_x) / old_zoom_scale
        center_y = (y + drag_offset_y) / old_zoom_scale

        new_center_x = center_x * zoom_scale
        new_center_y = center_y * zoom_scale

        drag_offset_x = int(new_center_x - x)
        drag_offset_y = int(new_center_y - y)

        update_display()

# Tkinter'i kullanarak dosya seçici aç
Tk().withdraw()  # Tkinter penceresini gizle
image_path = askopenfilename(title="Bir görüntü dosyası seçin", filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])

# Görüntünün mevcut olup olmadığını kontrol et
if not os.path.isfile(image_path):
    print(f"Görüntü dosyası bulunamadı: {image_path}")
else:
    # Görüntüyü yükle
    img = cv2.imread(image_path)

    # Görüntünün başarıyla yüklenip yüklenmediğini kontrol et
    if img is None:
        print(f"Görüntü dosyası açılamadı: {image_path}")
    else:
        # Görüntüyü yeniden boyutlandır
        img = cv2.resize(img, (image_width_px, image_height_px))
        img_display = img.copy()

        # Pencere oluştur ve fare geri çağırma fonksiyonunu ayarla
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('image', mouse_callback)

        # Görüntüyü göster
        update_display()
        cv2.waitKey(0)
        cv2.destroyAllWindows()
