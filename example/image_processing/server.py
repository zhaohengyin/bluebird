from bluebird import FunctionServer
import numpy as np
import cv2


def gaussian(img, ksize=(13, 13), sigmaX=20):
	return cv2.GaussianBlur(img, ksize=ksize, sigmaX=sigmaX)


def inverse(img):
	return 255 - img


if __name__ == '__main__':
	server = FunctionServer(host = 'localhost', port = 12345)
	server.function_handler.add_func('gaussian', gaussian)
	server.function_handler.add_func('inverse', inverse)
	server.run(recv_bufsize = 65536, send_bufsize = 65536)

	img = cv2.imread('./lenna.png')
	img = inverse(img)
	cv2.imshow('result', img)
	cv2.waitKey(0)
