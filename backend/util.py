from models import Category, Question


def get_categories(category_id: int = None, formatted: bool = False):
	if category_id is None:
		categories = Category.query.order_by('id').all()
	else:
		categories = Category.query.filter_by(id=category_id).one_or_none()

	if formatted:
		return {category.id: category.type for category in categories}
	else:
		return categories


def get_questions(category_id: int = None, 
				  question_id: int = None, 
				  formatted: bool = False):
	if (category_id is None) and (question_id is None):
		questions = Question.query.order_by('id').all()
	elif (question_id is None) and (category_id is not None):
		questions = Question.query.filter_by(category=category_id).order_by('id').all()
	elif question_id is not None:
		questions = Question.query.filter_by(id=question_id).one_or_none()
	else:
		questions = []

	if formatted:
		return [question.format() for question in questions]
	else:
		return questions

