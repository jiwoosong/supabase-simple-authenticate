import os
import platform
import subprocess
import sys
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

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

# 변환할 파일 목록
py_files = ["./SupaSimpleAuth/client.py", "./SupaSimpleAuth/admin.py"]
ext_modules = cythonize([
    Extension("SupaSimpleAuth.client", ["./SupaSimpleAuth/client.py"]),
    Extension("SupaSimpleAuth.admin", ["./SupaSimpleAuth/admin.py"])
], compiler_directives={'language_level': "3"})

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
)

# 🔹 운영체제별 확장자 설정
ext = ".pyd" if sys.platform == "win32" else ".so"

# ✅ 빌드 후 Python 소스 파일 삭제 (패키지 내부에 남지 않도록)
for py_file in py_files:
    encrypt_file = py_file.replace('.py', ext)
    if os.path.exists(encrypt_file):
        if os.path.exists(py_file):
            os.remove(py_file)
