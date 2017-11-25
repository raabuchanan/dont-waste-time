#!/usr/bin/env python


import os
import sys

sys.path.append(os.path.dirname(__name__))

from webapp.webapp import create_app

# create an app instance
app = create_app()

app.run(debug=True)