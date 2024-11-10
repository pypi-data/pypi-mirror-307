# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "ModuleData"
"""
  * @File    :   ModuleData.py
  * @Time    :   2023/04/24 15:51:36
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, Ship of Ocean
  * @Desc    :   None
"""

from pathlib import Path
from importlib_resources import files
import xy_work


class ModuleData:
    def __init__(self) -> None:
        self.data_path: Path = files(xy_work.__name__).joinpath("data")  # type: ignore
        self.template_path = self.data_path.joinpath("template")

        ############################## Config #############################

        self.config_path = self.template_path.joinpath("config")

        self.work_toml_template_path = self.config_path.joinpath(
            "xy_work_toml.template"
        )

        ############################## Runner #############################

        self.runner_path = self.template_path.joinpath("runner")

        self.runner_py_template_path = self.runner_path.joinpath("runner_py.template")
