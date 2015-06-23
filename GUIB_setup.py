# mysetup.py
from distutils.core import setup
import py2exe

setup(   
    options = {"py2exe":
           {"compressed": 1, #压缩
            "optimize": 2,
            "bundle_files": 2, #所有文件打包成一个exe文件
            "dist_dir":"ZinsGUIB"
            }
            },
    #zipfile = None,
    name = 'ZinsGUIB',
    version = '1.0.2',
    console=["zinsc.py"],
    windows=[{
    "script":"zinsGUI_B.py",
    "icon_resources":[(0,'./ico/ico_48X48.ico')]
    }],
    data_files=[("ico",["ico/ico_64X64.ico", "ico/zinsb.gif", "ico/zinsg.gif"])])
