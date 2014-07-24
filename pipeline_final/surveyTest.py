def survey_rc3_test (survey):
	'''
	Comphrehensive Tester for user-defined Survey class 
	to ensure that the survey class meets the requirements 
	for mosaicing galaxies in the RC3 Catalog
	'''
	sourceConfusionTest(survey)


def sourceConfusionTest(survey):
	confused_sources=[RC3(),RC3()]
	# Verify Data Product
	
	# Remove file after testing