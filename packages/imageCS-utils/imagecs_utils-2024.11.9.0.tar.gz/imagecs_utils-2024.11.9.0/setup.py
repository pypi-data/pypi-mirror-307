import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imageCS_utils",
    version="2024.10.31.0",
    author="Liao Chen",
    author_email="liaochen@bjtu.edu.cn",
    description="Some useful utils for deep learning (PyTorch) image compressive sensing (CS).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/FengodChen",
    url="https://github.com/",
    install_requires=[
        "torch",
        "torchvision",
        "torchaudio",
        "timm",
        "einops",
        "thop",
        "pytorch-fid",
        "opencv-python",
        "matplotlib",
        "scikit-image",
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)