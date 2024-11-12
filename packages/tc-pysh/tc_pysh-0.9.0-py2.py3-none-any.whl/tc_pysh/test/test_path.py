from tc_pysh import AbsolutePath, RelativePath


def test_relative_one_common():
    a = AbsolutePath.from_str("/a/b/c")
    b = AbsolutePath.from_str("/a/g/h")
    assert str(b.relative_to(a)) == "../../g/h"


def test_relative_subdir():
    a = AbsolutePath.from_str("/a/b/c")
    b = AbsolutePath.from_str("/a/b/c/d/e")
    assert str(b.relative_to(a)) == "d/e"


def test_relative_updir():
    a = AbsolutePath.from_str("/a/b/c/d/e")
    b = AbsolutePath.from_str("/a/b/c")
    assert str(b.relative_to(a)) == "../.."


def test_relative_no_common():
    a = AbsolutePath.from_str("/a/b/c")
    b = AbsolutePath.from_str("/g/h/f")

    assert str(b.relative_to(a)) == "../../../g/h/f"


def test_relative_to_root():
    a = AbsolutePath.from_str("/")
    b = AbsolutePath.from_str("/g/h/f")

    assert str(b.relative_to(a)) == "g/h/f", f"{a} {b} {b.relative_to(a)}"


def test_relative_from_root():
    a = AbsolutePath.from_str("/g/h/f")
    b = AbsolutePath.from_str("/")

    assert str(b.relative_to(a)) == "../../..", f"{a} {b} {b.relative_to(a)}"


def test_root():
    p = AbsolutePath.from_str("/")
    assert str(p) == str(p.dir) == str(p.dir.dir)


def test_rel_root():
    p = RelativePath.from_str("")
    assert str(p) == "."
    assert str(p.dir) == ".."
    assert str(p.dir.dir) == "../.."
