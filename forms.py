# To accept data through forms we need to use Flask WTF and create some
# form classes for which we need to import the FlaskForm class from the
# flask_wtf package
from flask_wtf import FlaskForm
# Import the StringField, SelectField, BooleanField and
# HiddenField classes from the wtforms package and DataRequried from
# the validators property of the wtforms package
from wtforms import StringField, SelectField, BooleanField, HiddenField, IntegerField
from wtforms.validators import DataRequired, NumberRange

# This class will represent the form we are collecting car data from
# and will be a child class of the FlaskForm class
class CarForm(FlaskForm):
    # DataRequried indicates that a field is required and this form will not be
    # submitted unless the name has been filled out
    name = StringField('Name:', validators=[DataRequired()])
    image = SelectField('Image:', validators=[DataRequired()],
        choices=[
            ('hennessey-venom.jpg', 'HENNESSEY VENOM F5'),
            ('koennisig-agura-rs.jpg', 'KOENIGSEGG AGERA RS'),
            ('buggai-chiron.jpg', 'BUGATTI CHIRON'),
            ('scc-aero.jpg', 'SCC ULTIMATE AERO'),
            ('saleen-s7.jpg', 'SALEEN S7 TWIN TURBO'),
            ('mclaren-f1.jpg', 'MCLAREN F1')
        ]
    )
    # topspeed = SelectField('Speed:', validators=[DataRequired()],
    #     choices=[
    #         ('HENNESSEY VENOM F5', '301 MPH'),
    #         ('KOENIGSEGG AGERA RS', '278 MPH'),
    #         ('BUGATTI CHIRON', '261 MPH'),
    #         ('SCC ULTIMATE AERO', '256 MPH'),
    #         ('SALEEN S7 TWIN TURBO', '248 MPH'),
    #         ('MCLAREN F1', '241 MPH')
    #     ]
    # )

    # A text field, except all input is coerced to an integer. Erroneous input
    # is ignored and will not be accepted as a value.
    topspeed = IntegerField('Speed (in MPH):', validators=[NumberRange(min=100, max=350)])

# Create separate form classes for editing and deleting cars
class EditCarForm(CarForm):
    id = HiddenField(validators=[DataRequired()])

class DeleteCarForm(FlaskForm):
    id = HiddenField(validators=[DataRequired()])
