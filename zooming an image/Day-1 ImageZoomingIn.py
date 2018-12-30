import sys
import cv2
import numpy as np
from scipy.ndimage import zoom
import matplotlib.pyplot as plt
from PIL import Image

def clipped_zoom(img, zoom_factor, focuc_x, focus_y, **kwargs):
# width and height of the original image
	h, w = img.shape[:2]

    # width and height of the zoomed image
	zh = int(np.round(zoom_factor * h))
	zw = int(np.round(zoom_factor * w))
	
	zoom_tuple = (zoom_factor,) * 2 + (1,) * (img.ndim - 2)

    # zooming out
	if zoom_factor < 1:
		top = (h - zh) // 2
		left = (w - zw) // 2
		out = np.zeros_like(img)
		out[top:top+zh, left:left+zw] = zoom(img, zoom_tuple, **kwargs)

    # zooming in
	elif zoom_factor > 1:
		top = (zh - h) // 2  - focus_y
		left = (zw - w) // 2  - focuc_x
		if top < 0:
			top = 0
		if top > h:
			top = (zh - h) // 2 
		if left < 0:
			left = 0
		if left > w:
			left = (zw - w) // 2 
		out = zoom(img[top:top+zh, left:left+zw], zoom_tuple, **kwargs)
        
        # `out` might still be slightly larger than `img` due to rounding, so
        # trim off any extra pixels at the edges
		trim_top = ((out.shape[0] - h) // 2)
		trim_left = ((out.shape[1] - w) // 2)
		out = out[trim_top:trim_top+h, trim_left:trim_left+w]
        
        
    # if zoom_factor == 1, just return the input array
	else:
		out = img
	return out

if __name__ == "__main__":
	img = cv2.imread(str(sys.argv[1]))
	zoom = clipped_zoom(img, float(sys.argv[2]), int (sys.argv[3]), int (sys.argv[4]))
	Image.fromarray(zoom).save('zoomed_picture.png')
	
	plt.subplot(121),plt.imshow(img),plt.title('Original')
	plt.subplot(122),plt.imshow(zoom),plt.title('Zoomed')    
	
	plt.show()