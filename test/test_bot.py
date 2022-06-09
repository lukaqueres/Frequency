from discord_bot.functions import get_time

def test_bot():
    assert str == type(get_time(specify="DT", return_type="str"))
