import sys
sys.path.append('/home/xethrus/paidProject/AvaliablilityProgram')

from calendar_event_checker import configure_timezone_to_UTC_if_naive
from calendar_event_checker import attempt_convert_to_datetime_if_not

def test_timezone_configurer():
    naive_datetime = datetime.datetime(2023,2,13,10,30,0)
    utc_datetime = datetime.datetime(2023,2,13,10,30,0, tzinfo=pytz.utc)
    test_naive_to_utc = configure_timezone_to_UTC_if_naive(naive_datetime)
    if naive_datetime != utc_datetime:
        raise TypeError("same value, change not viable")
    if test_naive_to_utc == utc_datetime:
        print ("naive to utc test passed")
    test_no_change = configure_timezone_to_UTC_if_naive(utc_datetime)
    if test_no_change == utc_datetime:
        print ("no change utc to utc test passed")
    return


def test_convert_string_to_datetime():
    datetime_string_utc = "2023-02-13 17:21:03.123456 UTC"
    datetime_string_naive = "2023-02-13 17:21:03.123456" 
    datetime_expected = datetime.datetime(2023,2,13,17,21,3,123456, tzinfo=pytz.utc)
    datetime_utc_converted = configure_timezone_to_UTC_if_naive(datetime_string_utc)
    datetime_naive_converted = configure_timezone_to_UTC_if_naive(datetime_string_naive)
    
    if datetime_utc_converted == datetime_expected:
        print("utc datetime string to utc datetime test passed")
    else:
        print("utc datetime string to utc datetime test failed")

    if datetime_naive_converted == datetime_expected:
        print("naive datetime string to utc datetime test passed")
    else:
        print("naive datetime string to utc datetime test failed")

