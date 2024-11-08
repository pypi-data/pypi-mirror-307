from setuptools import setup

setup(
    name='compjoules', # Paket adı
    version='0.1', # Paket sürüm numarası
    description='Package Description', # Paket açıklaması
    author='Murat Isik', # Yazar adı
    author_email='mrtisik@stanford.edu', # Yazar e-posta adresi
    packages=['compjoules'], # İçinde bulunan paketler
    install_requires=['pyJoules', 'torch', 'pandas'] # Gereksinimler
)