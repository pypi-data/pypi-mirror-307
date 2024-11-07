from beni import bpath

_expand = ['aa', 'bb', 'cc', 123456, 'dd.dat']
_expandPath = '/'.join([str(x) for x in _expand])


def test_get():
    root = '/root'
    assert bpath.get(root, _expandPath) == bpath.get(root, *_expand)


def test_user():
    assert bpath.user(_expandPath) == bpath.user(*_expand)


def test_desktop():
    assert bpath.desktop(_expandPath) == bpath.desktop(*_expand)


def test_workspace():
    assert bpath.workspace(_expandPath) == bpath.workspace(*_expand)
