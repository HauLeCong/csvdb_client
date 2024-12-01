import pytest

from dbcsv.encoder import Encoder


@pytest.mark.parametrize(
    "test_str, expected",
    [
        ("abc", "abc"),
        (None, "NULL"),
        ("I'am", "I\\'am"),
        ('Double quote "', 'Double quote \\"'),
        ("New line \r\n", "New line \\r\\n"),
        ("Backsplash \\", "Backsplash \\\\"),
    ],
)
def test_encoder_a_string_input_val(test_str, expected):
    encoder = Encoder()
    f_str = encoder.escape_item(test_str)
    assert f_str == expected
    sql_str = "select * from abc where a=%s" % f_str
    print(sql_str)


@pytest.mark.parametrize(
    "test_number, expected", [(123, "123"), (0.123, "0.123e0"), (0.123, "0.123e0")]
)
def test_encoder_number(test_number, expected):
    encoder = Encoder()
    f_num = encoder.escape_item(test_number)
    assert f_num == expected
    sql_str = "select * from abc where num=%s" % f_num
    print(sql_str)
