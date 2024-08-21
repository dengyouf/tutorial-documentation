# tutorial-documentation

## 创建文档布局

``` 
(.venv) PS C:\Users\dengyouf\PycharmProjects\tutorial-documentation> sphinx-quickstart.exe .
Welcome to the Sphinx 7.3.7 quickstart utility.

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

Selected root path: .

You have two options for placing the build directory for Sphinx output.
Either, you use a directory "_build" within the root path, or you separate
"source" and "build" directories within the root path.
> Separate source and build directories (y/n) [n]: y 

The project name will occur in several places in the built documentation.
> Project name: DevOps 工程
> Author name(s): dengyouf
> Project release []: v0.0.1 
```

## 配置config.py

```commandline
extensions = ['recommonmark','sphinx_markdown_tables']

templates_path = ['_templates']
exclude_patterns = []

language = 'zh-CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_search_language = 'zh'
```

## 清理缓存

```commandline

```

## 构建并启动服务

```commandline
sphinx-autobuild.exe source build
```

## 添加 .readthedocs.yaml到仓库

```

```

## 上传项目到github

```commandline
git add .
git commit -m 'first commit'
git push 
```

## 导入到 ReadtheDocs

- 使用github 账号登陆 https://readthedocs.org/accounts/login/?next=/dashboard/
    - 导入项目
    - 点击构建
    - 访问：`https://DOCNAME.readthedocs.io/`



