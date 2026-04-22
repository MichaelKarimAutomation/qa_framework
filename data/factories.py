import factory
from faker import Faker

fake = Faker()


class PostFactory(factory.Factory):
    class Meta:
        model = dict

    title = factory.LazyFunction(fake.sentence)
    body = factory.LazyFunction(fake.paragraph)
    userId = factory.LazyFunction(lambda: fake.random_int(min=1, max=10))
    