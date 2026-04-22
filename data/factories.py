import factory
from faker import Faker

fake = Faker()


class PostFactory(factory.Factory):
    class Meta:
        model = dict

    title = factory.LazyFunction(fake.sentence)    # runs fresh each time, every factory gets a unique title
    body = factory.LazyFunction(fake.paragraph)
    userId = factory.LazyFunction(lambda: fake.random_int(min=1, max=10))

class UserFactory(factory.Factory):
    class Meta:    # Factory Boy looks for this specifically by name: Configures the factory
        model = dict    # Tells the factory what type of object to build when called

    name = factory.LazyFunction(fake.name)
    email = factory.LazyFunction(fake.email)
    username = factory.LazyAttribute(lambda obj: obj.email.split("@")[0])
