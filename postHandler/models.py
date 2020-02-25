from django.db import models

class User(models.Model):
	'''
		User.
	'''
	name_text = models.CharField(max_length=200)
	email_text = models.EmailField()
	phone_text = models.CharField(max_length=200)

	def __str__(self):
		return self.name_text

class Address(models.Model):
	'''
		Address.
		Each user can have many addresses.
	'''
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	city_text = models.CharField(max_length=200)
	neighborhood_text = models.CharField(max_length=200)
	street_text = models.CharField(max_length=200)
	uf_code = models.CharField(max_length=200)
	zip_code = models.CharField(max_length=200)

	latitude = models.DecimalField(decimal_places=6, max_digits=9)
	longitude = models.DecimalField(decimal_places=6, max_digits=9)

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
