import views
from Greensys import app
import sys
import website

app.secret_key = "super secret key"
if __name__ == '__main__':
    # HOST = environ.get('SERVER_HOST', 'localhost')
    # try:
    #     PORT = int(environ.get('SERVER_PORT', '5555'))
    # except ValueError:
    #     PORT = 5555
    app.run(debug = True)
# cd Greensystem
#  venv\Scripts\activate
#  python runserver.py