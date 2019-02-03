# -*- coding: utf-8 -*-
import pytest

from insight.cli import sync

def mock_argv(**kwargs):
    return kwargs

def test_cli_sync(monkeypatch):
    monkeypatch.setattr('insight.API.sync', mock_argv)

    argv = '-o -f tests'.split()
    assert sync(argv) == {'folder': 'tests', 'overwrite': True}
