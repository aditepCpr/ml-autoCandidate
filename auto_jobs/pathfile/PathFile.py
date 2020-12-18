import os
from sys import platform

try:
    # Windows
    script_dir = os.path.dirname(__file__)
    if platform == "win32":
        READFILE_MODEL = script_dir + "\\..\\Storage\\Model\\"
        READFILE_MODEL_COST = script_dir + "\\..\\Storage\\Model\\Cost\\"
        READFILE_MODEL_PRODUCT = script_dir + "\\..\\Storage\\Model\\Product\\"
        READFILE_MODEL_PRODUCT_BIGFARM = script_dir + "\\..\\Storage\\Model\\Product\\Bigfarm\\"
        READFILE_MODEL_PRODUCT_PRODUCTION = script_dir + "\\..\\Storage\\Model\\Product\\Production\\"
        READFILE_MODEL_PRICE = script_dir + "\\..\\Storage\\Model\\Price\\"
        READFILE_EXCEL = script_dir + "\\..\\Storage\\Excel\\"
        READFILE_PARAMETER = script_dir + '\\..\\Storage\\Parameter\\'
        READFILE_CLUSTER = script_dir + '\\..\\Storage\\Cluster\\'
        READFILE_IMAGE = script_dir + "\\..\\Storage\\Image\\"
        READFILE_TEST = script_dir + "\\..\\Storage\\Test\\"
    else:
        READFILE_IMAGE = script_dir + "/../Storage/Image/"
        READFILE_EXCEL = script_dir + "/../Storage/Excel/"
        READFILE_MODEL = script_dir + "/../Storage/Model/"
        READFILE_MODEL_COST = script_dir + "/../Storage/Model/Cost/"
        READFILE_MODEL_PRODUCT = script_dir + "/../Storage/Model/Product/"
        READFILE_MODEL_PRODUCT_BIGFARM = script_dir + "/../Storage/Model/Product/Bigfarm/"
        READFILE_MODEL_PRODUCT_PRODUCTION = script_dir + "/../Storage/Model/Product/Production/"
        READFILE_MODEL_PRICE = script_dir + "/../Storage/Model/Price/"
        READFILE_PARAMETER = script_dir + '/../Storage/Parameter/'
        READFILE_CLUSTER = script_dir + '/../Storage/Cluster/'
        READFILE_TEST = script_dir + '/../Storage/Test/'
except ImportError as e:
    print('Error:')
    raise e
