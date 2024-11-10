from setuptools import setup, find_packages

setup(
    name='chinu9653s_tool',  # 패키지 이름
    version='0.0.2',  # 버전
    packages=find_packages(),  # 패키지 자동 검색
    install_requires=[  # 의존성 라이브러리
        "json5"
    ],
    description='This is a sample Python package.',
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author='Chinu9653',
    author_email='juyoung9653@gamil.com',
    url='https://github.com/juyoung9653/chinu9653s_tool',
    classifiers=[  # 패키지 정보
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',  # 최소 파이썬 버전
)
