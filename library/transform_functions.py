import re

def age_in_years(age_string:"str|None") -> float:
    if age_string is None:
        return None

    years_match = re.match("^(\d+) years$", age_string)
    if years_match:
        return int(years_match.groups()[0])

    months_match = re.match("^(\d+) months$", age_string)
    if months_match:
        return round(int(months_match.groups()[0]) /12, 2)


def test_age_in_years():
    assert age_in_years("5 years") == 5
    assert age_in_years("50 years") == 50
    assert age_in_years("5 months") == 0.42

if __name__ == "__main__":
    test_age_in_years()
