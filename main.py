import os
import dotenv

if __name__ == '__main__':
    dotenv.load_dotenv('.env')
    inst_param = {
        'username': os.getenv('USERNAME')
        'enc_password': os.getenv('ENC_PASSWORD')
    }
    