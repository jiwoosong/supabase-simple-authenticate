import os
import platform
import subprocess
import sys
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
from setuptools.command.build_ext import build_ext

# Cython 자동 설치
try:
    import Cython
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Cython"])
    import Cython

version = '0.0.1'
install_requires = ["requests"]

# OS에 따라 확장자 결정
ext = ".pyd" if platform.system() == "Windows" else ".so"

# ✅ 변환할 파일 목록 (정확히 이 파일들만 삭제할 것)
py_files = ["SupaSimpleAuth/client.py", "SupaSimpleAuth/admin.py"]

# ✅ Cython 빌드 수행
ext_modules = cythonize([
    Extension("SupaSimpleAuth.client", ["SupaSimpleAuth/client.py"]),
    Extension("SupaSimpleAuth.admin", ["SupaSimpleAuth/admin.py"])
], compiler_directives={'language_level': "3"})


class CustomBuildExt(build_ext):
    """Cython 빌드 후 정확히 지정한 .py 파일만 삭제하는 커스텀 클래스"""

    def run(self):
        # 원래 Cython 빌드 실행
        build_ext.run(self)

        # ✅ 빌드 완료 후 특정 .py 파일만 삭제
        for py_file in py_files:
            if os.path.exists(py_file):
                os.remove(py_file)
                print(f"Deleted: {py_file}")
            else:
                print(f"Warning: {py_file} not found. Skipping.")


setup(
    name='SupaSimpleAuth',
    version=version,
    author='Jiwoo Song',
    description='Custom Authentication Tool',
    packages=find_packages(),
    include_package_data=True,
    ext_modules=ext_modules,
    package_data={"SupaSimpleAuth": [f"*.{ext}"]},  # ✅ 바이너리 파일만 포함
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "supabase-client = SupaSimpleAuth.client:manage_license",
            "supabase-admin = SupaSimpleAuth.admin:admin_interface"
        ]
    },
    cmdclass={'build_ext': CustomBuildExt}  # ✅ Cython 빌드 후 특정 .py 파일 삭제
)
