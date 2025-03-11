import os
import platform
import subprocess
import sys
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
from setuptools.command.install import install

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


class CustomInstallCommand(install):
    """설치 완료 후 .py 파일을 자동 삭제하는 커스텀 명령어"""
    def run(self):
        install.run(self)  # 기본 설치 수행
        self.cleanup_files()  # 설치 완료 후 .py 삭제

    def cleanup_files(self):
        """설치 후 .py 파일 삭제"""
        package_dir = os.path.join(self.install_lib, "SupaSimpleAuth")
        for py_file in py_files:
            target_file = os.path.join(package_dir, os.path.basename(py_file))
            if os.path.exists(target_file):
                os.remove(target_file)
                print(f"Deleted after install: {target_file}")
            else:
                print(f"Warning: {target_file} not found. Skipping.")


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
    cmdclass={'install': CustomInstallCommand}  # ✅ 설치 후 `.py` 삭제하도록 설정
)
