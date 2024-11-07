import logging
import fireplan


def test_init_success(requests_mock, caplog):
    caplog.set_level(logging.INFO)
    secret = "BA4568A-F5A89EF"
    division = "Musterhausen"
    token = "eyJhbGciOiJodHRwOi8vd3d3pnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTI1NiIsInR5cCI6IkpXVCJ9.eyJDWFNlY3JldCI6IkR6eUNJQUtKOXViMlE0eW1qRnV5Z2V2eGorWHQ4eGx3WkNLR0l6M3g3KzRCRlEwSDV0bGU2SUlhYWtwUVlaRXUiLCJBYnRlaWx1bmciOiJ0T1g0V1lyQVAyQkFCb0VMN1ZIay9zU1VGMXNRYWIzbFRMbnl3SWdaUXRrPSIsIkNvbm5TdHJpbmciOiJDRzl5bkJRTEZtNHlxb1NPclhZMU1iL20xemZMSXk2amdpOHFhVFFNZ21rbDhQVGRPT3hyeVpMNEFSVW9hRDVWTk1FNUVlNjcwVUpodjM3SFQ3Skp6VjJONG1USkVwdXBqVWxHcGYxWWhidktNb0Nrd09jcVVEaFQ2SitrL0FWQTR2SWhRSXJ5NEM1bGtCV3R2bkdPY295RU1jek1oWnBydVpvTC9hb2xZRzZwZ3JUTHNkRUlVNnZrbnRSVnpjRkVKTHd5eDEwYWZLYTZSTVB5eEUxbFdIU015dDZkZCsrU2FVSW92MnIrM09WTmdNV0RGMWhudVF4akNKaVV1S2hPSFo4WTZGQmNBc1E3bU1KWlF4ZW5GSnY0K0wwUTNxOEQ2elVEWUJlVnhia0NPeWk4MTdoUkdDeUp4VThyMUJGZWRDUk4yaVRDT1ZZazYyTmhoZ2F3bkE9PSIsIkFwcGxpY2F0aW9uIjoiQ0c5eW5CUUxGbTR5cW9TT3JYWTFNYi9tMXpmTEl5NmpnaThxYVRRTWdta2w4UFRkT094cnlaTDRBUlVvYUQ1Vk5NRTVFZTY3MFVKaHYzN0hUN0pKelYyTjRtVEpFcHVwalVsR3BmMVloYnZLTW9Da3dPY3FVRGhUNkoray9BVkE0dkloUUlyeTRDNWxrQld0dm5HT2NveUVNY3pNaFpwcnVab0wvYW9sWUc2cGdyVExzZEVJVTZ2a250UlZ6Y0ZFSkx3eXgxMGFmS2E2Uk1QeXhFMWxXSFNNeXQ2ZGQrK1NhVUlvdjJyKzNPVk5nTVdERjFobnVReGpDSmlVdUtoT0haOFk2RkJjQXNRN21NSlpReGVuRkp2NCtMMFEzcThENnpVRFlCZVZ4YmtDT3lpODE3aFJHQ3lKeFU4cjFCRmVkQ1JOMmlUQ09WWWs2Mk5oaGdhd25BPT0iLCJFeHBpcmVzIjo2Nzc1NDgwNTYxOTI4NDU3MTh9.3PKeYh1gknE707eCXA1kpgv3cuaSXm6YAER8EklGW5E"
    requests_mock.get(
        "https://fireplanapi.azurewebsites.net/api/registerV2",
        text=token,
        status_code=200,
    )
    fp = fireplan.Fireplan(secret, division)
    assert requests_mock.called is True
    assert requests_mock.last_request.headers["cxsecret"] == secret
    assert requests_mock.last_request.headers["abteilung"] == division
    assert "User Token erfolgreich generiert!" in caplog.text
    assert fp.headers["utoken"] == token


def test_init_fail(requests_mock, caplog):
    secret = "INVALID-SECRET"
    division = "Musterhausen"
    requests_mock.get(
        "https://fireplanapi.azurewebsites.net/api/registerV2", text="", status_code=401
    )
    fp = fireplan.Fireplan(secret, division)
    assert requests_mock.called is True
    assert requests_mock.last_request.headers["cxsecret"] == secret
    assert requests_mock.last_request.headers["abteilung"] == division
    assert "Fehler beim generieren des User Token!" in caplog.text
    assert fp.headers["utoken"] is None
