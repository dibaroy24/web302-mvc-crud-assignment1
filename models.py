from utilities import filter_input, format_name

# Create a class for our Model which will represent the data we are using in
# our app
class Car:
    """
    This class defines a car.
    """

    def __init__(self, form):
        self.name = form.name.data
        self.image = form.image.data
        self.topspeed = form.topspeed.data

    # In order to keep our attributes encapsulated we will want to use
    # properties with getters and setters

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = format_name(value)
        # self.__name = value
        return self.__name

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value
        return self.__image

    @property
    def topspeed(self):
        return self.__topspeed

    @topspeed.setter
    def topspeed(self, value):
        self.__topspeed = value
        return self.__topspeed
