import os
import platform
import subprocess
import sys
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

# Cython 자동 설치 (필요할 경우)
try:
    import Cython
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Cython"])
    import Cython

version = '0.0.1'
install_requires = ["requests"]

ext = ".pyd" if platform.system() == "Windows" else ".so"

py_files = ["./SupaSimpleAuth/client.py", "./SupaSimpleAuth/admin.py"]
c_files = ["./SupaSimpleAuth/client.c", "./SupaSimpleAuth/admin.c"]

# 🔹 만약 .c 파일이 존재하면 기존 C 코드 사용, 없으면 Cython으로 생성
if all(os.path.exists(c) for c in c_files):
    print("⚡ C files detected, using prebuilt C extensions...")
    ext_modules = [
        Extension("SupaSimpleAuth.client", ["./SupaSimpleAuth/client.c"]),
        Extension("SupaSimpleAuth.admin", ["./SupaSimpleAuth/admin.c"]),
    ]
else:
    print("🚀 Generating C files with Cython...")
    missing_files = [f for f in py_files if not os.path.exists(f)]
    if missing_files:
        raise FileNotFoundError(f"Missing required source files: {', '.join(missing_files)}")

    ext_modules = cythonize([
        Extension("SupaSimpleAuth.client", ["./SupaSimpleAuth/client.py"]),
        Extension("SupaSimpleAuth.admin", ["./SupaSimpleAuth/admin.py"])
    ], compiler_directives={'language_level': "3", "binding": False})

setup(
    name='SupaSimpleAuth',
    version=version,
    author='Jiwoo Song',
    description='Custom Authentication Tool',
    packages=find_packages(),
    include_package_data=True,
    ext_modules=ext_modules,
    package_data={"SupaSimpleAuth": ["*.pyd", "*.so"]},
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "supabase-client = SupaSimpleAuth.client:manage_license",
            "supabase-admin = SupaSimpleAuth.admin:admin_interface"
        ]
    },
)

# 🔥 빌드 후 .py 파일 삭제
for py_file in py_files:
    if os.path.exists(py_file):
        os.remove(py_file)

# # 🔥 .c 파일도 제거 (원하면 유지 가능)
# for c_file in c_files:
#     if os.path.exists(c_file):
#         os.remove(c_file)
