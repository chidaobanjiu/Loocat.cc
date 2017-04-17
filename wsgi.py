import os
from app import create_app

application = create_app(os.getenv('MANA_CONFIG') or 'default')

if __name__=='__main__':
    application.run()
