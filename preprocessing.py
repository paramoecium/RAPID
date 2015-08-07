import numpy as np
from scipy import misc #imread, imresize
from PIL import Image #
import matplotlib.pyplot as plt
from skimage.transform import resize
import random
import os

def normalize_size(image, size=256, trans='c'):
	## 'c':central crop, 'w':warp, 'p':padding
	o_shape = image.shape
	assert o_shape[0] > size and o_shape[1] > size
	if trans == 'c':
		if o_shape[0] > o_shape[1]:
			dh = int( (o_shape[0] - o_shape[1])/2 )
			image = image[dh:dh+o_shape[1],:]
		else:
			dw = int( (o_shape[1] - o_shape[0])/2 )
			image = image[:,dw:dw+o_shape[0]]		
		new_shape = image.shape
		assert new_shape[0] == new_shape[1]
		image = resize(image, (size,size), order=3, preserve_range=False)
	elif trans == 'w':
		image = resize(image, (size,size), order=3, preserve_range=False)
	elif trans == 'p':
		background = np.zeros((size, size, 3))
		if o_shape[0] > o_shape[1]:
			new_shape = (size,size*o_shape[1]/o_shape[0])
			dh = 0
			dw = (size - new_shape[1])/2
		else:
			new_shape = (size*o_shape[0]/o_shape[1],size)
			dh = (size - new_shape[0])/2
			dw = 0
		image = resize(image, (new_shape[0],new_shape[1]), order=0, preserve_range=False)
		background[dh:dh+new_shape[0],dw:dw+new_shape[1],:] = image[:,:,:]
		image = background
	else:
		print "ERROR:undesignated transformation"
	return image

def random_crop(image, w=224, h=224):
	o_shape = image.shape # probably 256X256
	assert o_shape[0] > h and o_shape[1] > w
	dh = random.randint(0, (o_shape[0] - h))
	dw = random.randint(0, (o_shape[1] - w))
	return image[dh:dh+h,dw:dw+w]

def global_view(image, size=224, trans='w'):
	assert size < 256
	image = normalize_size(image, 256, trans)
	return image
	#return random_crop(image, 224, 224)

def local_view(image, size=224):
	return random_crop(image, size, size)

def test():
	image_dir_base = "/home/yuchen/Desktop/RAPID/dataset_image"
	image_category = "animal_test"
	image_id = 598172
	image_path = "{}/{}/{}.jpg".format(image_dir_base, image_category, image_id)
	image = misc.imread(image_path)
	image_g = global_view(image, 224,'p')
	image_l = local_view(image, 224)
	print image.shape, image.dtype
	print image_g.shape, image_g.dtype
	print image_l.shape, image_l.dtype

	plt.subplot(131) #1X2 , 1
	plt.imshow(image)
	plt.subplot(132) #1X2 , 2
	plt.imshow(image_g)
	plt.subplot(133) #1X3 , 3
	plt.imshow(image_l)
	plt.show()
	

if __name__=='__main__':
	image_dir_base = "/home/yuchen/Desktop/RAPID/dataset_image"
	output_dir_base = "/home/yuchen/Desktop/RAPID/processed_image"
	if not os.path.exists(output_dir_base):
		os.makedirs(output_dir_base)
	for input_dir_name in os.listdir(image_dir_base):
		for job in [{'type':'global','func':global_view},{'type':'local','func':local_view}]:
			print "processing {} view image for images of {}".format(job['type'],input_dir_name)
			output_dir_path = "{}/{}/{}".format(output_dir_base, job['type'], input_dir_name)
			if not os.path.exists(output_dir_path):
					os.makedirs(output_dir_path)
			for imagefile in os.listdir("{}/{}".format(image_dir_base,input_dir_name)):
				image_path = "{}/{}/{}".format(image_dir_base,input_dir_name,imagefile)
				image = misc.imread(image_path)
				try:
					image_g = job['func'](image, 224)
				except:
					print "failed:",imagefile
				misc.imsave("{}/{}".format(output_dir_path,imagefile),image_g)


			
