from django.db import models

# TODO: Update fields properties (max_length, null, ...) to comply more closely to requirements

class User(models.Model):
	'''
		User data.
	'''
	name_text = models.CharField(max_length=200)
	email_text = models.EmailField()
	phone_text = models.CharField(max_length=200)

	def __str__(self):
		return self.name_text

class Address(models.Model):
	'''
		Address data.
		Each user can have many addresses.
	'''
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	city_text = models.CharField(max_length=200)
	neighborhood_text = models.CharField(max_length=200)
	street_text = models.CharField(max_length=200)
	uf_code = models.CharField(max_length=200)
	zip_code = models.CharField(max_length=200)

	# Values to be updated after creation by the celery worker:
	latitude = models.DecimalField(decimal_places=6, max_digits=9, null=True)
	longitude = models.DecimalField(decimal_places=6, max_digits=9, null=True)

	def __str__(self):
		return '{city} - {street}'.format(city=self.city_text, street=self.street_text)

class Answer(models.Model):
	'''
		Answers for each question in an user questionaire.
		Each user can have many questions.
	'''

	user = models.ForeignKey(User, on_delete=models.CASCADE)

	question_text = models.CharField(max_length=200)
	answer_text = models.CharField(max_length=200)

	def __str__(self):
		return 'Q: {question} - A: {answer}'.format(question=self.question_text, answer=self.answer_text)
