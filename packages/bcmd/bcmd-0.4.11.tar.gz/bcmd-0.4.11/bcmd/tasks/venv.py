import os
import platform
import re
import sys
from pathlib import Path
from typing import Final

import typer
from beni import bcolor, bexecute, bfile, bhttp, bpath, btask
from beni.bfunc import syncCall, textToAry
from beni.btype import Null
from prettytable import PrettyTable

from ..common import password
from ..common.func import checkFileOrNotExists, checkPathOrNotExists
from . import bin

app: Final = btask.app


@app.command()
@syncCall
async def venv(
    packages: list[str] = typer.Argument(None),
    path: Path = typer.Option(None, '--path', help='指定路径，默认当前目录'),
    isOfficial: bool = typer.Option(False, '--official', help='是否使用官方地址安装（https://pypi.org/simple）'),
    isUseBase: bool = typer.Option(False, '--use-base', help='是否强制使用基础库去安装'),
    isUseLock: bool = typer.Option(False, '--use-lock', help='是否使用锁定库安装'),
    isCleanup: bool = typer.Option(False, '--cleanup', help='是否先清空 venv 目录再执行'),
):
    'python 虚拟环境配置'
    btask.assertTrue(not (isUseBase == isUseLock == True), '2个选项只能选择其中一个 --use-base / --use-lock')
    path = path or Path(os.getcwd())
    binPath = path / 'bin'
    binListFile = bpath.get(path, 'bin.list')
    venvPath = bpath.get(path, 'venv')
    checkPathOrNotExists(venvPath)
    venvFile = bpath.get(path, '.venv')
    checkFileOrNotExists(venvFile)
    await _inputQiniuPassword(binListFile, binPath)
    if isCleanup:
        bpath.remove(venvPath)
        btask.assertTrue(not venvPath.exists(), f'无法删除 venv 目录 {venvPath}')
    packages = packages or []
    for i in range(len(packages)):
        package = packages[i]
        if package.endswith('==now'):
            ary = package.split('==')
            packages[i] = f'{ary[0]}=={await _getPackageLatestVersion(ary[0])}'
    if not venvPath.exists():
        await bexecute.run(f'python -m venv {venvPath}')
    if not venvFile.exists():
        await bfile.writeText(venvFile, '')
    basePackages, lockPackages = await getPackageList(venvFile)
    if isUseBase:
        installPackages = _mergePackageList(basePackages, packages)
    elif isUseLock:
        installPackages = _mergePackageList(lockPackages, packages)
    else:
        installPackages = _mergePackageList(lockPackages or basePackages, packages)
    installPackages = sorted(list(set(installPackages)))
    if sys.platform.startswith('win'):
        pip = bpath.get(venvPath, 'Scripts/pip.exe')
    else:
        pip = bpath.get(venvPath, 'bin/pip')
    await _pipInstall(pip, installPackages, isOfficial)
    with bpath.useTempFile() as tempFile:
        await bexecute.run(f'{pip} freeze > {tempFile}')
        basePackages = _mergePackageList(basePackages, packages)
        lockPackages = (await bfile.readText(tempFile)).strip().split('\n')
        await updatePackageList(venvFile, basePackages, lockPackages)

    # 下载 bin 文件
    if binListFile.exists():
        bin.download(
            names=Null,
            file=binListFile,
            output=binPath,
        )
    bcolor.printGreen('OK')


# ------------------------------------------------------------------------------------


async def _pipInstall(pip: Path, installPackages: list[str], disabled_mirror: bool):
    python = pip.with_stem('python')
    btask.assertTrue(python.is_file(), f'无法找到指定文件 {python}')
    btask.assertTrue(pip.is_file(), f'无法找到指定文件 {pip}')
    indexUrl = '-i https://pypi.org/simple' if disabled_mirror else ''
    with bpath.useTempFile() as file:
        await bfile.writeText(file, '\n'.join(installPackages))
        table = PrettyTable()
        table.add_column(
            bcolor.yellow('#'),
            [x + 1 for x in range(len(installPackages))],
        )
        table.add_column(
            bcolor.yellow('安装库'),
            [x for x in installPackages],
            'l',
        )
        print(table.get_string())

        btask.assertTrue(
            not await bexecute.run(f'{python} -m pip install --upgrade pip {indexUrl}'),
            '更新 pip 失败',
        )
        btask.assertTrue(
            not await bexecute.run(f'{pip} install -r {file} {indexUrl}'),
            '执行失败',
        )


async def _getPackageDict(venvFile: Path):
    content = await bfile.readText(venvFile)
    pattern = r'\[\[ (.*?) \]\]\n(.*?)(?=\n\[\[|\Z)'
    matches: list[tuple[str, str]] = re.findall(pattern, content.strip(), re.DOTALL)
    return {match[0]: [line.strip() for line in match[1].strip().split('\n') if line.strip()] for match in matches}


_baseName: Final[str] = 'venv'


def _getLockName():
    systemName = platform.system()
    return f'{_baseName}-{systemName}'


async def getPackageList(venvFile: Path):
    result = await _getPackageDict(venvFile)
    lockName = _getLockName()
    return result.get(_baseName, []), result.get(lockName, [])


async def updatePackageList(venvFile: Path, packages: list[str], lockPackages: list[str]):
    packageDict = await _getPackageDict(venvFile)
    lockName = _getLockName()
    packages.sort(key=lambda x: x.lower())
    lockPackages.sort(key=lambda x: x.lower())
    packageDict[_baseName] = packages
    packageDict[lockName] = lockPackages
    content = '\n\n\n'.join([f'\n[[ {key} ]]\n{'\n'.join(value)}' for key, value in packageDict.items()]).strip()
    await bfile.writeText(venvFile, content)


async def _getPackageLatestVersion(package: str):
    '获取指定包的最新版本'
    data = await bhttp.getJson(
        f'https://pypi.org/pypi/{package}/json'
    )
    return data['info']['version']


def _mergePackageList(basePackages: list[str], addPackages: list[str]):
    basePackagesDict = {_getPackageName(x): x for x in basePackages}
    addPackagesDict = {_getPackageName(x): x for x in addPackages}
    packagesDict = basePackagesDict | addPackagesDict
    return sorted([x for x in packagesDict.values()])


def _getPackageName(package: str):
    if '==' in package:
        package = package.split('==')[0]
    elif '>' in package:
        package = package.split('>')[0]
    elif '<' in package:
        package = package.split('<')[0]
    package = package.strip()
    if package.startswith('#'):
        package = package.replace('#', '', 1).strip()
    return package


async def _inputQiniuPassword(binListFile: Path, binPath: Path) -> None:
    '根据需要输入七牛云密码'
    if binListFile.exists():
        aaSet = set(textToAry(await bfile.readText(binListFile)))
        bbSet = set([x.name for x in bpath.listFile(binPath)])
        if aaSet != bbSet:
            await password.getQiniu()
