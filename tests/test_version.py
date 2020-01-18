def test_version():
    import cogbooks

    assert isinstance(cogbooks.__version__, str)
    assert cogbooks.__version__
    assert "unknown" not in cogbooks.__version__
