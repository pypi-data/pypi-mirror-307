from setuptools import setup, find_packages

setup(
    name='gmscloud',                          # Nama paket
    version='1.4',                          # Versi paket
    author='Fikri Hidayat',                     # Nama penulis
    author_email='fhidayat2206@gmail.com',       # Email penulis
    description='Aplikasi Print Dokumen',  # Deskripsi singkat
    packages=find_packages(),
    license='MIT',
    entry_points={                          # Menentukan entry point untuk konsol
        'console_scripts': [
            'gmscloud=gmscloud.main:main',   # Command line yang akan digunakan dan fungsi yang dipanggil
        ],
    },
    install_requires=[
    'pywin32',            # Untuk menangani interaksi printer di Windows
    'beautifultable',     # Untuk membuat tabel yang indah
    'requests',           # Untuk melakukan permintaan HTTP
],
    python_requires='>=3.9',               # Versi Python yang dibutuhkan
)
