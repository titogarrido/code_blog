CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

MONGODB_SETTINGS = {'DB': "testing", "host":'mongodb://127.0.0.1:27017/testing'}
#MONGODB_HOST = '10.211.55.22'
#MONGODB_PORT = '27017'
#MONGODB_DATABASE = 'testing'
#MONGODB_USERNAME = 'root'
#MONGODB_PASSWORD = ''

#UPLOADED_FILES_DEST='.uploads/'
#UPLOADED_FILES_URL = 'uploads/'
UPLOADS_DEFAULT_DEST = 'uploads/'

SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = 'ieie'

SECURITY_REGISTERABLE = True
SECURITY_POST_LOGIN_VIEW = '/admin'

# At top of file

# After 'Create app'
#MAIL_SERVER = 'smtp.gmail.com'
#MAIL_PORT = 465
#MAIL_USE_SSL = True
#MAIL_USERNAME = 'titogarrido@gmail.com'
#MAIL_PASSWORD = ''