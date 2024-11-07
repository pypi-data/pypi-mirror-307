from datagarden_models import get_values_from_class


def test_values_from_class_returns_class_constants():
	class ConstClass:
		CONS1 = 'a'
		CONS2 = 'b'

	assert [v for v in get_values_from_class(ConstClass)] == ['a', 'b']