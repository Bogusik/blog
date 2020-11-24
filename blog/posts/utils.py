import os
from flask import request
from blog import db
from blog.posts.models import Tag

def uploadFiles(form, path):
	if form.file.data:
		files = request.files.getlist('file')
		os.makedirs(path, exist_ok=True)
		for file in files:
			if file.filename != '':
				file.save(path+file.filename)

def conformTags(form):
	tags = []
	for tag in form.tags.data.replace(" ", "").split(","):
		if (tg := Tag.query.filter_by(title=tag.lower()).first()):
			tags.append(tg)
		else:
			temp = Tag(title=tag.lower())
			db.session.add(temp)
			db.session.commit()
			tags.append(temp)
	return tags

def listFiles(path):
	return os.listdir(path)

def deleteFile(path):
	print(os.getcwd() + "/blog/static/posts/" + path)
	os.remove(path)