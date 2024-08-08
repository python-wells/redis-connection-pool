from redisdemo import db


def test_set_get():
    db.set("a", 1)
    assert db.get("a") == "1"
    db.set("b", 2)
    assert db.get("b") == "2"
    db.set("a", 3)
    assert db.get("a") == "3"

    db.delete("a")
    db.delete("b")
    assert db.get("a") is None
    assert db.get("b") is None


def test_setm():
    db.setm({"a": 1, "b": 2, "c": 3})

    assert db.get("a") == "1"
    assert db.get("b") == "2"
    assert db.get("c") == "3"
