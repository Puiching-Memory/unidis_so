import os

import torch
from setuptools import find_packages, setup
from torch.utils.cpp_extension import BuildExtension, CppExtension, CUDAExtension


def make_cuda_ext(
    name, module, sources, sources_cuda=[], extra_args=[], extra_include_path=[]
):

    define_macros = []
    extra_compile_args = {"cxx": [] + extra_args}

    if torch.cuda.is_available() or os.getenv("FORCE_CUDA", "0") == "1":
        define_macros += [("WITH_CUDA", None)]
        extension = CUDAExtension
        extra_compile_args["nvcc"] = extra_args + [
            "-D__CUDA_NO_HALF_OPERATORS__",
            "-D__CUDA_NO_HALF_CONVERSIONS__",
            "-D__CUDA_NO_HALF2_OPERATORS__",
        ]
        sources += sources_cuda
    else:
        print("Compiling {} without CUDA".format(name))
        extension = CppExtension
        # raise EnvironmentError('CUDA is required to compile MMDetection!')

    return extension(
        name="{}.{}".format(module, name),
        sources=[os.path.join(*module.split("."), p) for p in sources],
        include_dirs=extra_include_path,
        define_macros=define_macros,
        extra_compile_args=extra_compile_args,
    )


setup(
    name="unidis_so",
    version="0.0.1",
    author="Sail2Dream",
    author_email="1138663075@qq.com",
    description="idk",
    url=None,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    ext_modules=[
        make_cuda_ext(
            name="voxel_pooling_ext",
            module="unidis_so.voxel_pooling",
            sources=["src/voxel_pooling_forward.cpp"],
            sources_cuda=["src/voxel_pooling_forward_cuda.cu"],
        ),
        make_cuda_ext(
            name="iou3d_nms_cuda",
            module="unidis_so.iou3d_nms",
            sources=[
                "src/iou3d_cpu.cpp",
                "src/iou3d_nms_api.cpp",
                "src/iou3d_nms.cpp",
            ],
            sources_cuda=["src/iou3d_nms_kernel.cu"],
        ),
        make_cuda_ext(
            name="roiaware_pool3d_cuda",
            module="unidis_so.roiaware_pool3d",
            sources=["src/roiaware_pool3d.cpp"],
            sources_cuda=["src/roiaware_pool3d_kernel.cu"],
        ),
    ],
    cmdclass={"build_ext": BuildExtension},
)
