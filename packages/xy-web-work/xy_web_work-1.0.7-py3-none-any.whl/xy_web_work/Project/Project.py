# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Work"
"""
  * @File    :   Work.py
  * @Time    :   2023/04/26 00:45:15
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, Ship of Ocean
  * @Desc    :   None
"""
import os
import re
from pathlib import Path
from argparse import ArgumentParser
import shutil

from xy_file.Object.File import File

from xy_web_settings.Mode import Mode
from xy_web_settings.ModuleData import ModuleData as xyWebSettingsModuleData

from xy_web_work.ModuleData import ModuleData
from xy_web_work.Settings.Settings import Settings
from xy_web_work.WebWork import WebWork


class Project(WebWork):
    settings: Settings | None = None

    def project(self, *args, **kwargs):
        prog: str = kwargs.get(self.prog)
        description: str = kwargs.get(self.description)

        project_parser: ArgumentParser = kwargs.get(self.parser_key)
        if not project_parser:
            project_parser = self.argparser_make(
                prog=prog,
                description=description,
                args=args,
                kwargs=kwargs,
            )
        project_parser.add_argument(
            "-n",
            "--name",
            type=str,
            help="""
                项目名称 仅支持英文:
            """,
            required=True,
        )
        name = project_parser.parse_args().name
        project_parser.add_argument(
            "-m",
            "--mode",
            type=int,
            help="""
                创建模式:
                默认 => 0: 
                0 => full, 默认模式，将加载所有web项目信息
                1 => simple, 简易模式，仅创建项目信息
            """,
            required=False,
            default=0,
        )
        mode = Mode(project_parser.parse_args().mode)
        if not name:
            raise ValueError("传入的项目名称参数 -n/--name 仅支持英文")
        zh_pattern = re.compile("[\u4e00-\u9fa5]+")
        match = zh_pattern.search(name)
        if match:
            raise ValueError("传入符合要求的项目名称参数 -n/--name 仅支持英文")

        cwd_path = Path.cwd()
        if (
            os.access(cwd_path, os.R_OK)
            and os.access(cwd_path, os.W_OK)
            and os.access(cwd_path, os.X_OK)
        ):
            project_path = cwd_path.joinpath(name)
            if project_path.exists():
                raise FileExistsError(
                    f"工程目录 [ {project_path} ] 已存在，请进入到其他符合要求的目录进行项目创建"
                )
            config_path = project_path.joinpath("config")
            settings_toml_path = config_path.joinpath("xy_web.toml")
            if settings_toml_path.exists():
                raise FileExistsError(
                    f"""
                        配置文件 [ {settings_toml_path} ] 已存在。
                        请进入到其他符合需求的目录进行工程创建。
                    """
                )
            module_data = ModuleData()
            xy_web_settings_module_data = xyWebSettingsModuleData()
            self.settings = Settings()

            match mode:
                case Mode.SIMPLE:
                    settings_toml_template_string = (
                        xy_web_settings_module_data.simple_settings_toml_template.read_text()
                    )
                    settings_toml_string = settings_toml_template_string.format(
                        xy_web_work_project_name=name,
                        xy_web_work_project_identifier=self.settings.project.identifier,
                        xy_web_work_project_verbose_name=name,
                        xy_web_work_project_description=name,
                        xy_web_work_project_path=project_path,
                        xy_web_work_runner_path=self.settings.runner.path,
                        xy_web_work_runner_runner=self.settings.runner.runner,
                    )
                case _:
                    settings_toml_template_string = (
                        xy_web_settings_module_data.full_settings_toml_template.read_text()
                    )
                    settings_toml_string = settings_toml_template_string.format(
                        xy_web_work_project_name=name,
                        xy_web_work_project_identifier=self.settings.project.identifier,
                        xy_web_work_project_verbose_name=name,
                        xy_web_work_project_description=name,
                        xy_web_work_project_path=project_path,
                        xy_web_work_runner_path=self.settings.runner.path,
                        xy_web_work_runner_runner=self.settings.runner.runner,
                    )

            if (
                mode == Mode.FULL
                and module_data.project_path
                and module_data.project_path.exists()
            ):
                try:
                    project_path.mkdir()
                    template_project_path = module_data.project_path
                    for project_work_path in template_project_path.glob("**/*"):
                        if (
                            project_work_path.parent == template_project_path
                            and not project_work_path.stem.startswith(".")
                        ):
                            shutil.copytree(project_work_path, project_path)
                            print(f"创建项目工程成功!!!")
                except:
                    shutil.rmtree(project_path)
                    raise OSError("创建项目工程失败!!!")
            settings_toml_path = File.touch(settings_toml_path)
            if (
                isinstance(settings_toml_path, Path)
                and settings_toml_path.exists()
                and settings_toml_path.is_file()
            ):
                try:
                    settings_toml_path.write_text(settings_toml_string)
                except:
                    shutil.rmtree(project_path)
                    raise IOError(
                        f"创建项目失败,写入配置信息到项目配置文件失败! WebServer.toml => {settings_toml_path}"
                    )
            else:
                shutil.rmtree(project_path)
                raise FileNotFoundError("项目创建失败 => 原因: 创建项目配置文件失败!!!")
        else:
            raise PermissionError("请保证用户对当前目录拥有 [可读, 可写, 可执行] 的权限")
