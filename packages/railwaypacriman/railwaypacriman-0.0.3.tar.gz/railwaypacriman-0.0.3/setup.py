from setuptools import setup, find_packages

setup(
    name='railwaypacriman',  # パッケージ名（pip listで表示される）
    version='0.0.3',  # バージョン
    description="Railway-related-activity progress manager",  # 説明
    author='IppeiKISHIDA',  # 作者名
    #author_email='your.email@example.com',
    packages=find_packages(),  # 使うモジュール一覧を指定する
    license='MIT',  # ライセンス

    include_package_data=True,
    package_data={
        'railwaypacriman': [ 'railwaypacriman/ekidatajp/*.csv']
    },

    install_requires=[  # 依存パッケージ
        'graphviz',
        'networkx',
        'pandas',
    ],

    entry_points={
        'console_scripts': [
            'rpinfo=railwaypacriman.rpinfo:rpinfo', 
            'rpprogress=railwaypacriman.rpprogress:rpprogress', 
        ],
    },

    #long_description=open('README.md').read(),
    #long_description_content_type='text/markdown',
    #url='https://github.com/yourusername/your_package',  # プロジェクトのURL
    #classifiers=[
    #    'Programming Language :: Python :: 3',
    #    'License :: OSI Approved :: MIT License',
    #    'Operating System :: OS Independent',
    #],
    #python_requires='>=3.6',  # 対応するPythonバージョン
)


