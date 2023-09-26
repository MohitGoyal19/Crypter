from marshmallow import Schema, fields, validates, ValidationError

class LoginSchema(Schema):
	username = fields.Email(required=True)
	password = fields.Str(required=True)

	@validates('password')
	def validate_password(self, value):
		if not (7 < len(value.strip()) < 32):
			raise ValidationError('Invalid password provided')
