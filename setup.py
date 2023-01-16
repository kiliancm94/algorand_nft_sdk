from setuptools import find_packages, setup


reqs = []
with open("requirements.txt", "r", encoding="utf-8") as f:
    reqs.extend([line for line in f.read().splitlines() if line])


setup(
    name="algorand_nft_sdk",
    version="0.1.0",
    packages=find_packages("./"),
    install_requires=reqs,
    entry_points="""
        [console_scripts]
        algonft=algorand_nft_sdk.cli:nft
    """,
)
