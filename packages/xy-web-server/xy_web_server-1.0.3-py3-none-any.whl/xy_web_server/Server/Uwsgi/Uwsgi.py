# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Uwsgi"
"""
  * @File    :   Uwsgi.py
  * @Time    :   2023/04/26 01:06:26
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""
import shutil

import tempfile
from pathlib import Path
import os


class Uwsgi:
    def initial_uwsgi(
        self,
        uwsgi_package_url: str = "https://projects.unbit.it/downloads/uwsgi-lts.tar.gz",
        plugin_path: Path = Path(
            "/usr/local/lib/{uwsgi_plugin_file}".format(
                uwsgi_plugin_file="python_plugin.so"
            )
        ),
    ):
        result = os.system("uwsgi -h 2>/dev/null 1>/dev/null")
        plugin_exist = plugin_path.exists()
        if result > 0 or not plugin_exist:
            temp_dir = tempfile.mkdtemp()
            uwsgi_package_saved_name = os.path.split(uwsgi_package_url)[-1]
            package_dir = tempfile.mkdtemp()
            os.system(
                "wget {uwsgi_package_url} -P {temp_dir}".format(
                    uwsgi_package_url=uwsgi_package_url, temp_dir=temp_dir
                )
            )
            os.system(
                "tar xvf {temp_dir}/{uwsgi_package_saved_name} -C {temp_dir}".format(
                    uwsgi_package_saved_name=uwsgi_package_saved_name, temp_dir=temp_dir
                )
            )
            os.system(
                "cp -rf {temp_dir}/*/* {package_dir}".format(
                    temp_dir=temp_dir, package_dir=package_dir
                )
            )
            os.system(
                "cd {package_dir};CFLAGS='-O3 -fPIC' CC=gcc python {package_dir}/uwsgiconfig.py --build core;".format(
                    package_dir=package_dir
                )
            )
            os.system(
                "cd {package_dir};CFLAGS='-O3 -fPIC' CC=gcc python {package_dir}/uwsgiconfig.py --plugin plugins/python core;".format(
                    package_dir=package_dir
                )
            )
            os.system(
                "sudo cp {package_dir}/python_plugin.so /usr/local/lib/".format(
                    package_dir=package_dir
                )
            )
            os.system(
                "sudo cp {package_dir}/uwsgi /usr/local/bin".format(
                    package_dir=package_dir
                )
            )
            shutil.rmtree(temp_dir)
            shutil.rmtree(package_dir)
