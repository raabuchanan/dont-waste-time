import os
from flask import Flask, render_template, flash, url_for
from flask_bootstrap import Bootstrap


def create_app(configfile=None):
	app = Flask(__name__, static_url_path='/static')

	app.secret_key = 'rOUntXJb0UbnCBG5nzLYkNPs8ZW3O0'

	Bootstrap(app)

	@app.route('/', methods=('GET', 'POST'))
	def index():
		return render_template('index.html')



	@app.context_processor
	def override_url_for():
		return dict(url_for=dated_url_for)

	def dated_url_for(endpoint, **values):
		if endpoint == 'static':
			filename = values.get('filename', None)
			if filename:
				file_path = os.path.join(app.root_path, endpoint, filename)
				values['q'] = int(os.stat(file_path).st_mtime)
		return url_for(endpoint, **values)




	return app
