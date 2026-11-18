from app.verification import verifier_email, verifier_str, verifier_date


def test_email_valide():
    assert verifier_email("ali@gmail.com") == "OK"


def test_email_sans_arobase():
    assert verifier_email("aligmail.com") != "OK"


def test_str_vide():
    assert verifier_str("", "nom") != "OK"


def test_date_valide():
    assert verifier_date(15, 6, 2025) == "OK"


def test_29_fevrier_annee_non_bissextile():
    assert verifier_date(29, 2, 2025) != "OK"