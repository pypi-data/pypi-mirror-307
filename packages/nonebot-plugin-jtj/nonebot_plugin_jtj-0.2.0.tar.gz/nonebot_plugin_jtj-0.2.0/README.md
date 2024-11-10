<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-jtj

_✨ NoneBot 机厅管理上报插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Onimaimai/nonebot-plugin-jtj.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-jtj">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-jtj.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>



## 📖 介绍

这是一个基于JSON文件的 nonebot2 本地机厅管理人数上报插件

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-jtj

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-jtj
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-jtj
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-jtj
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-jtj
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_jtj"]

</details>



## 🎉 使用
### 指令表
| 指令 | 权限 | 说明 |
|:-----:|:----:|:----:|
| 地区列表 | 群员 |
| 绑定机厅<地区> | 群员 |
| 查询简称<名称><地区> | 群员 |
| 添加机厅<名称><地区><简称> | 群员 |
| 删除机厅<名称><地区> | 群员 |
| 添加简称<名称><地区><简称> | 群员 |
| 删除简称<名称><地区><简称> | 群员 |
| 随个机厅/去哪勤/勤哪/qn | 群员 |
| 机厅几/jtj/JTJ | 群员 |
| <简称>几/j/J | 群员 |
| <简称>数字/+-数字 | 群员 |
| 解绑机厅 | 群员 |
| 重置人数 | 主人、群管 | 清零本群机厅人数 |
| 重置机厅 | 主人 | 清零所有机厅人数 |
| 更新机厅 | 主人 | 手动同步机厅变更 |
### 效果图
![543f7ff7f37df7ff22c865e28e234882_720](https://github.com/user-attachments/assets/9e499a62-7f76-40c6-800d-66dcaf310ad8)

