from setuptools import setup, find_packages
import pathlib

# 現在のファイルの場所を取得
here = pathlib.Path(__file__).parent.resolve()

# 長い説明を README.md から読み込み
long_description = (here / 'README.md').read_text(encoding='utf-8')

# 開発者情報を追加
developer_info = (
    "Creator/Inventor: NPO_KS_903.lnc (President: Takeshi Kumura, Director: Takuma Ozawa)\n"
    "Developer: NPO_KS_903.lnc (President: Takeshi Kumura, Director: Takuma Ozawa)\n"
    "Designer/Architect: NPO_KS_903.lnc (President: Takeshi Kumura, Director: Takuma Ozawa)\n"
    "Founder: NPO_KS_903.lnc (President: Takeshi Kumura, Director: Takuma Ozawa)\n"
)

with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

setup(
    name='KS903NaturalIntonationAIVoice_vr_2',
    version='2.0.1',
    description="say's speech NaturalIntonation AI Voice library for KS903 __Versions_2.0.1__",
    long_description=f"{long_description}\n\n{developer_info}",
    long_description_content_type='text/markdown',
    url="https://github.com/NPO_KS903_KATUYOSHI/say's_speech_NaturalIntonation_AI_Voice_library_for_KS903__Versions_2.0.1__",
    license='MIT',
    author='NPO_KS_903.lnc(President: Takeshi Kumura, Director: Takuma Ozawa)',
    author_email='xksxkatuyoshi0009@gmail.com',
    
    keywords="say's speech NaturalIntonation AI Voice for KS903",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    
    packages=find_packages(),
    install_requires=[
        'pyttsx3',
        'pandas',
        'python-docx',
        'PyPDF2',
        'pillow',
        'pytesseract'

    ],
)









# from setuptools import setup, find_packages
# import pathlib
# here = pathlib.Path(__file__).parent.resolve()
# long_descriptiption = (here / 'README.md').read_text(encoding='utf-8')
# setup(
#     name='KS903_animethion_icon_GIF',
#     version='1.0.0',
#     description='anmimete_icon_gif of the to_on The Library'
#     long_descriptiption=long_descriptiption,
#     long_descriptiption_contents_type='text/markdown',
#     url='github.com/NPO_KS903_KATUYOSHI/KS903_animethion_icon_GIF',
#     license='MIT',
#     packages=find_packages(),
#     install_requires=[
#         'pillow',
# ],
# )

# from setuptools import setup, find_packages
# import pathlib

# # 現在のファイルの場所を取得
# here = pathlib.Path(__file__).parent.resolve()

# # 長い説明を README.md から読み込み
# long_description = (here / 'README.md').read_text(encoding='utf-8')

# setup(
#     name='KS903_animethion_icon_GIF',
#     version='1.0.0',
#     description='Animation icon GIF library for KS903',
#     long_description=long_description,
#     long_description_content_type='text/markdown',
#     url='https://github.com/NPO_KS903_KATUYOSHI/KS903_animethion_icon_GIF',
#     license='MIT',
#     author='NPO_KS_903.lnc',
#     author_email='xksxkatuyoshi0009@gmail.com',
#     author= 'NPO_KS_903.lnc',
#     author_email='xksxkatuyoshi0009@gmail.com',
#     Creator_or_Inventor='NPO_KS_903.lnc:President:Takeshi Kumura, Director: Takuma Ozawa,',
#     Developer= 'NPO_KS_903.lnc:President:Takeshi Kumura, Director: Takuma Ozawa,',
#     Designer_or_Architect= 'NPO_KS_903.lnc:President:Takeshi Kumura, Director: Takuma Ozawa,',
#     Founder=  'NPO_KS_903.lnc:President:Takeshi Kumura, Director: Takuma Ozawa,',
    
    
#     # キーワードや説明をカスタムとしてコメントに入れる
#     keywords='animation icon gif KS903',
#     classifiers=[
#         'Development Status :: 3 - Alpha',
#         'Intended Audience :: Developers',
#         'License :: OSI Approved :: MIT License',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.8',
#     ],
    
#     # パッケージと依存パッケージを指定
#     packages=find_packages(),
#     install_requires=[
#         'pillow',
#     ],
# )









# from setuptools import setup, find_packages
# import pathlib
# here = pathlib.Path(__file__).parent.resolve()
# long_descriptiption = (here / 'README.md').read_text(encoding='utf-8')
# setup(
#     name='KS903_animethion_icon_GIF',
#     version='1.0.0',
#     description='anmimete_icon_gif of the to_on The Library'
#     long_descriptiption=long_descriptiption,
#     long_descriptiption_contents_type='text/markdown',
#     url='github.com/NPO_KS903_KATUYOSHI/KS903_animethion_icon_GIF',
#     license='MIT',
#     packages=find_packages(),
#     install_requires=[
#         'pillow',
# ],
# )

# from setuptools import setup, find_packages
# import pathlib

# # 現在のファイルの場所を取得
# here = pathlib.Path(__file__).parent.resolve()

# # 長い説明を README.md から読み込み
# long_description = (here / 'README.md').read_text(encoding='utf-8')

# setup(
#     name='KS903_animethion_icon_GIF',
#     version='1.0.0',
#     description='Animation icon GIF library for KS903',
#     long_description=long_description,
#     long_description_content_type='text/markdown',
#     url='https://github.com/NPO_KS903_KATUYOSHI/KS903_animethion_icon_GIF',
#     license='MIT',
#     author='NPO_KS_903.lnc',
#     author_email='xksxkatuyoshi0009@gmail.com',
#     author= 'NPO_KS_903.lnc',
#     author_email='xksxkatuyoshi0009@gmail.com',
#     Creator_or_Inventor='NPO_KS_903.lnc:President:Takeshi Kumura, Director: Takuma Ozawa,',
#     Developer= 'NPO_KS_903.lnc:President:Takeshi Kumura, Director: Takuma Ozawa,',
#     Designer_or_Architect= 'NPO_KS_903.lnc:President:Takeshi Kumura, Director: Takuma Ozawa,',
#     Founder=  'NPO_KS_903.lnc:President:Takeshi Kumura, Director: Takuma Ozawa,',
    
    
#     # キーワードや説明をカスタムとしてコメントに入れる
#     keywords='animation icon gif KS903',
#     classifiers=[
#         'Development Status :: 3 - Alpha',
#         'Intended Audience :: Developers',
#         'License :: OSI Approved :: MIT License',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.8',
#     ],
    
#     # パッケージと依存パッケージを指定
#     packages=find_packages(),
#     install_requires=[
#         'pillow',
#     ],
# )
