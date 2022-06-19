from bluebird import call_remote_func
import numpy as np
import cv2


if __name__ == '__main__':
	img = cv2.imread('./lenna.png')

	result = call_remote_func(host='localhost', port=12345,
							  func='inverse', args={'img': img}, send_bufsize=65536)

	cv2.imshow('Result', result)
	cv2.waitKey(0)
