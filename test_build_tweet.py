from tweet import build_tweet


def test_all_short():
    assert build_tweet(
        {'persons': [{'name': 'Demospeaker'}], 'room': 'Baumschule', 'title': 'This is my talk!'}
    ) == "Next up in Baumschule: »This is my talk!« by Demospeaker"


def test_multiple_speakers():
    assert build_tweet(
        {'persons': [{'name': 'Harry Potter'}, {'name': 'Ron Weasley'}],
         'room': 'Baumschule', 'title': 'This is my talk!'}
    ) == "Next up in Baumschule: »This is my talk!« by Harry Potter, Ron Weasley"


def test_multiple_speakers_long_title():
    assert build_tweet(
        {'persons': [{'name': 'Harry Potter'}, {'name': 'Ron Weasley'}],
         'room': 'Baumschule', 'title': 'This is my talk, and I will talk as long as I want, until it is over, '
                                        'really! I will do this all tweet long!'}
    ) == "Next up in Baumschule: »This is my talk, and I will talk as long as I want, until it is over, really! I will …« by Harry Potter, Ron Weasley"


def test_multiple_speakers_too_long():
    assert build_tweet(
        {'persons': [{'name': 'Karl-Theodor Maria Nikolaus Johann Jacob Philipp Franz Joseph Sylvester Buhl-Freiherr von und zu Guttenberg'}, {'name': 'Ron Weasley'}],
         'room': 'Baumschule', 'title': 'This is my talk, and I will talk as long as I want, until it is over, '
                                        'really! I will do this all tweet long!'}
    ) == "Next up in Baumschule: »This is my talk, and I will talk as long as I want, until it is over, " \
         "really! I will do this all tweet long!«"


def test_multiple_speakers_too_long_and_title_too_long():
    assert build_tweet(
        {'persons': [{'name': 'Karl-Theodor Maria Nikolaus Johann Jacob Philipp Franz Joseph Sylvester Buhl-Freiherr von und zu Guttenberg'}, {'name': 'Ron Weasley'}],
         'room': 'Baumschule', 'title': 'This is my talk, and I will talk as long as I want, until it is over, '
                                        'really! I will do this all tweet long if I want to, because I can!'}
    ) == "Next up in Baumschule: »This is my talk, and I will talk as long as I want, until it is over, " \
         "really! I will do this all tweet long if I w…«"


def test_no_speakers_and_title_too_long():
    assert build_tweet(
        {'persons': [],
         'room': 'Baumschule', 'title': 'This is my talk, and I will talk as long as I want, until it is over, '
                                        'really! I will do this all tweet long if I want to, because I can!'}
    ) == "Next up in Baumschule: »This is my talk, and I will talk as long as I want, until it is over, " \
         "really! I will do this all tweet long if I w…«"
