import os
# renames the images gathered from google-images-download
def rename(folder):
	for path, subdirs, files in os.walk(folder):
		for name in files:
			os.rename(os.path.join(path,name), os.path.join(path, str(hash(name)) + '.jpg'))
rename('app/test_images')