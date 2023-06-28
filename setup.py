import setuptools

# https://camillovisini.com/article/create-macos-menu-bar-app-pomodoro/
APP = ['menubar_app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': '1T2G.icns',
    'plist': {
        'CFBundleShortVersionString': '0.2.0',
        'LSUIElement': True,
    },
    'packages': ['rumps'],
}

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    app=APP,
    name="1T2G", # Replace with your own username
    data_files=DATA_FILES,
    version="0.1.0",
    author="J Mac",
    author_email="jmmcl2@unteer.net",
    description="A little focused To Do tracker for the Mac Menubar.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    project_urls={
        "Bug Tracker": "https://github.com/unteer/one-task-to-go/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps'],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
)