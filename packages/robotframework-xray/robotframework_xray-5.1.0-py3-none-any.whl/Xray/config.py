import os
from os.path import join
from dotenv import load_dotenv

class Config:
    def get(value: str):
        load_dotenv(join(os.path.abspath(os.curdir), '.env'))
        return os.getenv(value)
    
    def debug() -> bool:
        try:
            return os.getenv('XRAY_DEBUG', Config.get('XRAY_DEBUG')).lower().capitalize() == "True"
        except:
            return False
    
    def project_key():
        try:
            return os.getenv('PROJECT_KEY', Config.get('PROJECT_KEY'))
        except Exception as error:
            print("A propriedade PROJECT_KEY não encontra-se nas variaveis!")

    def test_plan():
        try:
            return os.getenv('TEST_PLAN', Config.get('TEST_PLAN'))
        except Exception as error:
            print("A propriedade TEST_PLAN não encontra-se nas variaveis!")
    
    def xray_api():
        try:
            return os.getenv('XRAY_API', Config.get('XRAY_API'))
        except Exception as error:
            print("A propriedade XRAY_API não encontra-se nas variaveis!")
    
    def xray_client_id():
        try:
            return os.getenv('XRAY_CLIENT_ID', Config.get('XRAY_CLIENT_ID'))
        except Exception as error:
            print("A propriedade XRAY_CLIENT_ID não encontra-se nas variaveis!")
    
    def xray_client_secret():
        try:
            return os.getenv('XRAY_CLIENT_SECRET', Config.get('XRAY_CLIENT_SECRET'))
        except Exception as error:
            print("A propriedade XRAY_CLIENT_SECRET não encontra-se nas variaveis!")
    
    def cucumber_path():
        try:
            return os.getenv('CUCUMBER_PATH', Config.get('CUCUMBER_PATH'))
        except Exception as error:
            print("A propriedade CUCUMBER_PATH não encontra-se nas variaveis!")