import pytest
import datetime
import kenpompy.team as kpteam
import kenpompy.misc as kpmisc

def test_get_valid_teams(browser):
	expected = 357

	teams_2021 = kpteam.get_valid_teams(browser, season = '2021')
	assert len(teams_2021) == expected

	valid_2021_teams = ['Gonzaga', 'Penn St.', 'Florida', 'Xavier', 'VMI', 'Kennesaw St.', 'Wagner', 'Bucknell', 'Maryland Eastern Shore', 'Cal St. Fullerton']
	for team in valid_2021_teams:
		assert team in teams_2021

	invalid_2021_teams = ['Gonpraga', 'North Carolina    A&T', 'Bayton', 'LMU', 'Goopton']
	for team in invalid_2021_teams:
		assert team not in teams_2021

	teams_2003 = kpteam.get_valid_teams(browser, season = '2003')
	assert len(teams_2003) == 327

	valid_2003_teams = ['Kentucky', 'Kansas', 'Georgetown', 'Dayton', 'South Carolina', 'Fresno St.', 'Iowa', 'SMU', 'TCU', 'North Carolina A&T']
	for team in valid_2003_teams:
		assert team in teams_2003
	
	invalid_2003_teams = ['Loyola Marymnt University', 'YRU', 'Praget', 'Invalid U', 'SRTU', 'Kennesaw St.']
	for team in invalid_2003_teams:
		assert team not in teams_2003
	
	teams_2020 = kpteam.get_valid_teams(browser, season = '2020')
	for team in teams_2020:
		assert '*' not in team


def test_get_schedule(browser):
	expected = ['Sat Dec 15', '122', '286', 'Portland St.', 'W, 85-58', '70', 'Away', '10-1', '', 'None']

	df = kpteam.get_schedule(browser, team="Loyola Marymount", season = '2019')
	assert [str(i) for i in df[df.Date == 'Sat Dec 15'].iloc[0].to_list()] == expected
	assert df.shape == (34, 10)

	expected = ['Mon Apr 2', '1', '7', 'Michigan', 'W, 79-62', '67', 'Neutral', '36-4', '', 'NCAA']
	df = kpteam.get_schedule(browser, team='Villanova', season=2018)
	assert df[df.Date == 'Mon Apr 2'].iloc[0].to_list() == expected

	date = datetime.date.today()
	currentYear = kpmisc.get_current_season(browser)
	nextYear = str(int(currentYear)+1)

	with pytest.raises(ValueError):
		kpteam.get_schedule(browser, team="Iowa", season = '1998')

	with pytest.raises(ValueError):
		kpteam.get_schedule(browser, team="Kansas", season = nextYear)

	with pytest.raises(ValueError):
		kpteam.get_schedule(browser, season = "2009")

	with pytest.raises(ValueError):
		kpteam.get_schedule(browser, team='Merrimack', season=2019)

	with pytest.raises(ValueError):
		kpteam.get_schedule(browser, team='Incorrect Team Name', season=2017)

	centenary_expected = ['Sat Nov 11', '', '172', 'TCU', 'L, 72-66', '76', 'Away', '0-1', '', 'None']
	centenary_df = kpteam.get_schedule(browser, team='Centenary', season=2007)
	assert [str(i) for i in centenary_df[centenary_df.Date == 'Sat Nov 11'].iloc[0].to_list()] == centenary_expected
	assert centenary_df.shape == (31, 10)

	with pytest.raises(ValueError):
		kpteam.get_schedule(browser, team='Centenary', season=2017)

	# Make sure that the valid team check is triggered
	with pytest.raises(ValueError):
		kpteam.get_schedule(browser, season = '2013', team="LMU")

def test_get_scouting_report(browser):
	data = kpteam.get_scouting_report(browser, 'Purdue', season=2023)
	assert data['OE'] == 117.7
	assert data['APLD'] == 18.1
	# Not including SoS and Personnel (88 with)
	assert len(data) == 70

	data = kpteam.get_scouting_report(browser, 'Purdue', season=2023, conference_only=True)
	assert data['OE'] == 111.3
	assert data['APLD'] == 18.3
	# Not including SoS and Personnel (88 with)
	assert len(data) == 70

	data = kpteam.get_scouting_report(browser, 'Kansas', season=2009)
	assert data['OE'] == 114.5
	assert data['APLD'] == ''
	# Not including SoS and Personnel (88 with)
	assert len(data) == 70

	data = kpteam.get_scouting_report(browser, 'Kansas', season=2009, conference_only=True)
	assert data['OE'] == 109.5
	assert data['APLD'] == ''
	# Not including SoS and Personnel (88 with)
	assert len(data) == 70
