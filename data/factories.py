"""Factory Boy + Faker factories that generate realistic randomized payloads for API tests.

Each call to a factory produces a fresh dict with new fake values so parametrized
or repeated tests don't reuse identical inputs (which can hide validation bugs
that only trigger on certain shapes of data).
"""
import factory
from faker import Faker

fake = Faker()


class PostFactory(factory.Factory):
    """Build a dict shaped like a JSONPlaceholder post: random title, body, and a userId in 1-10."""

    class Meta:
        model = dict

    title = factory.LazyFunction(fake.sentence)
    body = factory.LazyFunction(fake.paragraph)
    userId = factory.LazyFunction(lambda: fake.random_int(min=1, max=10))


class UserFactory(factory.Factory):
    """Build a dict shaped like a JSONPlaceholder user. Username is derived from the email's local-part so the two fields stay internally consistent."""

    class Meta:  # Factory Boy looks for this specifically by name: Configures the factory
        model = dict  # Tells the factory what type of object to build when called

    name = factory.LazyFunction(fake.name)
    email = factory.LazyFunction(fake.email)
    username = factory.LazyAttribute(lambda obj: obj.email.split('@')[0])
