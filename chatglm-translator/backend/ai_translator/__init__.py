import os
from utils import  ConfigLoader
from model import GLMModel


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONF_FILE_DIR = os.path.join(BASE_DIR, 'config.yaml')

#翻译后文件的存放目录
RESULT_FILE_DIR = os.path.join(BASE_DIR, 'output_file').replace("backend","frontend")

#临时文件目录
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

CONFIG = ConfigLoader(CONF_FILE_DIR).load_config()

# model_name = CONFIG['OpenAIModel']['model']
# api_key = CONFIG['OpenAIModel']['api_key']
#
# OpenAIModel = OpenAIModel(model=model_name, api_key=api_key)

model_url = CONFIG['GLMModel']['model_url']
timeout = CONFIG['GLMModel']['timeout']

GLMModel = GLMModel(model_url=model_url, timeout=timeout)