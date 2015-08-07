from HTMLParser import HTMLParser
import urllib # load from URL
import os # read every file in the dir

class MyParse(HTMLParser):
	def handle_starttag(self, tag, attrs):
		# if tag=="div" and dict(attrs).get("class") == "imagetitle": print attrs
		if tag=="img":
			src = dict(attrs).get("src")
			if "http://images.dpchallenge.com/images_challenge" in src and dict(attrs).get("alt"):
				self.image_url = src

def get_image_url(page_url):
	parser = MyParse()
	page = urllib.urlopen(page_url).read()
	parser.feed(page)
	return parser.image_url

def get_image(page_url, output_path):
	image_url = get_image_url(page_url)
	urlLoader = urllib.URLopener()
	urlLoader.retrieve(image_url, output_path)

def get_dataset(list_dir = "aesthetics_image_lists"):
	lost_image_url = []
	for listfile_name in os.listdir(list_dir):
		file_path = "{}/{}".format(list_dir, listfile_name)
		image_dir = "/tmp2/yuchen/RAPID/dataset_image"
		page_url_base = "http://www.dpchallenge.com/image.php?IMAGE_ID="
		new_dir = listfile_name.split(".")[0]
		print new_dir
		image_path = "{}/{}".format(image_dir, new_dir)
		if not os.path.exists(image_path):
			os.makedirs(image_path)
		with open(file_path, 'r') as fr:
			for line in fr:
				image_id = int(line)
				output_path = "{}/{}.jpg".format(image_path, image_id)
				page_url = "{}{}".format(page_url_base, image_id)
				print "getting {} and saving file to {}".format(image_id, output_path)
				try:
					get_image(page_url, output_path)
				except:
					lost_image_url.append([page_url, output_path])
	return lost_image_url
def test():
	urlString = "http://www.dpchallenge.com/image.php?IMAGE_ID=359334"
	print get_image_url(urlString)

if __name__ == '__main__':
	lost_image_url = get_dataset("AVA_dataset/aesthetics_image_lists")
	with open("lostfile", 'w') as fw:
		for pair in lost_image_url:
			print "LOST:", pair[1]
			try:
				get_image(pair[0], pair[1])
				print "GET:", pair[1]
			except:
				print >> fw, " ".join( (pair[0], pair[1]) )
				print "LOST AGIN:", pair[1]
