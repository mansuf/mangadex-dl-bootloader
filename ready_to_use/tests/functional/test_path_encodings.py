#-----------------------------------------------------------------------------
# Copyright (c) 2005-2023, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License (version 2
# or later) with exception for distributing the bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# SPDX-License-Identifier: (GPL-2.0-or-later WITH Bootloader-exception)
#-----------------------------------------------------------------------------

import subprocess

import pytest

from PyInstaller.utils.tests import importorskip


def test_ascii_path(pyi_builder):
    dist_dir = str(pyi_builder._dist_dir)

    dist_dir_ascii = dist_dir.encode('ascii', 'replace').decode('ascii')
    if dist_dir != dist_dir_ascii:
        pytest.skip(reason="Default build path not ASCII, skipping...")

    pyi_builder.test_script('pyi_path_encoding.py')


@pytest.mark.linux
def test_linux_non_unicode_path(pyi_builder, monkeypatch):
    # If we set the locale to 'C', mbstowcs should be completely useless. This test verifies that _Py_char2wchar will
    # decode the "undecodable" bytes and will decode even filenames that weren't encoded with the locale encoding.
    unicode_filename = 'ěščřžýáíé日本語'

    pyi_builder._dist_dir = pyi_builder._dist_dir / unicode_filename

    tmp = pyi_builder._tmp_path / f"{unicode_filename}_TMP"
    monkeypatch.setenv('LC_ALL', 'C')
    monkeypatch.setenv('TMPDIR', str(tmp))
    monkeypatch.setenv('TMP', str(tmp))

    pyi_builder.test_script('pyi_path_encoding.py')


@pytest.mark.darwin
@pytest.mark.linux
def test_osx_linux_unicode_path(pyi_builder, monkeypatch):
    # Mac and Linux should handle 'unicode' type filenames without problem.
    unicode_filename = 'ěščřžýáíé日本語'

    pyi_builder._dist_dir = pyi_builder._dist_dir / unicode_filename

    tmp = pyi_builder._tmp_path / f"{unicode_filename}_TMP"
    monkeypatch.setenv('TMPDIR', str(tmp))
    monkeypatch.setenv('TMP', str(tmp))

    pyi_builder.test_script('pyi_path_encoding.py')


@pytest.mark.win32
def test_win_codepage_path(pyi_builder, monkeypatch):
    # Create some bytes and decode with the current codepage to get a filename that is guaranteed to encode with the
    # current codepage. Assumes a one-byte codepage, i.e., not cp937 (shift-JIS) which is multibyte.
    cp_filename = bytes(bytearray(range(0x80, 0x86))).decode('mbcs')

    pyi_builder._dist_dir = pyi_builder._dist_dir / cp_filename

    tmp = pyi_builder._tmp_path / f"{cp_filename}_TMP"
    monkeypatch.setenv('TMPDIR', str(tmp))
    monkeypatch.setenv('TMP', str(tmp))

    pyi_builder.test_script('pyi_path_encoding.py')


@pytest.mark.win32
def test_win_codepage_path_disabled_shortfilename(pyi_builder, monkeypatch):
    # Create some bytes and decode with the current codepage to get a filename that is guaranteed to encode with the
    # current codepage. Assumes a one-byte codepage, i.e., not cp937 (shift-JIS) which is multibyte.
    cp_filename = bytes(bytearray(range(0x80, 0x86))).decode('mbcs')

    pyi_builder._dist_dir = pyi_builder._dist_dir / cp_filename

    # Try to remove ShortFileName from this folder using `fsutil`. Requires admin privileges, so `xfail` if we do not
    # have them. `8dot3name strip` only affects subfolders, so pass the folder containing our codepage filename.
    pyi_builder._dist_dir.mkdir(parents=True)  # Ensure directory exists so we can modify it with `fsutil`.
    if subprocess.call(['fsutil', '8dot3name', 'strip', str(pyi_builder._dist_dir)]):
        pytest.xfail("Administrator privileges required to strip ShortFileName.")

    tmp = pyi_builder._tmp_path / f"{cp_filename}_TMP"
    monkeypatch.setenv('TMPDIR', str(tmp))
    monkeypatch.setenv('TMP', str(tmp))

    pyi_builder.test_script('pyi_path_encoding.py')


@pytest.mark.win32
def test_win_non_codepage_path(pyi_builder, monkeypatch):
    # Both eastern European and Japanese characters - no codepage should encode this.
    non_cp_filename = 'ěščřžýáíé日本語'

    # Codepage encoding would replace some of these chars with "???".
    pyi_builder._dist_dir = pyi_builder._dist_dir / non_cp_filename

    # To test what happens with a non-ANSI tempdir, we will also need to pass the TMP environ as wide chars.
    tmp = pyi_builder._tmp_path / f"{non_cp_filename}_TMP"
    monkeypatch.setenv('TMPDIR', str(tmp))
    monkeypatch.setenv('TMP', str(tmp))

    pyi_builder.test_script('pyi_path_encoding.py')


@pytest.mark.win32
@importorskip('win32api')
def test_win_py3_no_shortpathname(pyi_builder):
    pyi_builder.test_script('pyi_win_py3_no_shortpathname.py')


@pytest.mark.win32
@importorskip('win32api')
def test_win_TEMP_has_shortpathname(pyi_builder, monkeypatch, tmp_path):
    """
    Test if script if pass if $TMP holds a short path name.
    """
    tmp = tmp_path / "longlongfilename" / "xxx"
    tmp.mkdir(parents=True, exist_ok=True)
    import win32api
    tmp = win32api.GetShortPathName(str(tmp))
    monkeypatch.setenv("TMP", tmp)
    monkeypatch.setenv("TEMP", tmp)
    pyi_builder.test_script('pyi_win_py3_no_shortpathname.py')
