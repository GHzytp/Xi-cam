def test_msg():
    from .. import msg
    msg.logMessage('this', 'is', 'a', 'test:', 42, level=msg.WARNING)
