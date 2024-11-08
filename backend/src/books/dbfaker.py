import os
import sys
import django
from random import randint, choice

from faker import Faker

# Dynamically add the project directory to the sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(project_path)
print(project_path)
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from books.models import Genre, Publisher, Book, Review
from django.contrib.auth import get_user_model

User = get_user_model()

def populate_genres(n):
    fake = Faker()
    for _ in range(n):
        name = fake.word()
        description = fake.text()
        Genre.objects.create(name=name, description=description)
    print(f"Successfully added {n} fake genres.")

def populate_publishers(n):
    fake = Faker()
    for _ in range(n):
        name = fake.company()
        description = fake.text()
        Publisher.objects.create(name=name, description=description)
    print(f"Successfully added {n} fake publishers.")

def populate_users(n):
    fake = Faker()
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        User.objects.create_user(username=username, email=email, password='password')
    print(f"Successfully added {n} fake users.")

def populate_books(n):
    fake = Faker()
    genres = list(Genre.objects.all())
    users = list(User.objects.filter(id__range=(11, 20)))
    publishers = list(Publisher.objects.all())
    for _ in range(n):
        title = fake.sentence(nb_words=4)
        author = choice(users)
        genres_list = [choice(genres) for _ in range(4)]
        publisher = choice(publishers)
        published_date = fake.date_this_century()
        description = fake.paragraph(nb_sentences=3)
        book = Book.objects.create(
            title=title,
            author=author,
            publisher=publisher,
            published_date=published_date,
            description=description
        )
        book.genres.set(set(genres_list))
    print(f"Successfully added {n} fake books.")

def populate_reviews(n):
    fake = Faker()
    users = list(User.objects.all())
    books = list(Book.objects.all())
    for _ in range(n):
        user = choice(users)
        book = choice(books)
        rating = randint(1, 5)  # Assuming a rating scale of 1 to 5
        comment = fake.paragraph(nb_sentences=2)
        Review.objects.create(
            user=user,
            book=book,
            rating=rating,
            comment=comment
        )
    print(f"Successfully added {n} fake reviews.")

if __name__ == "__main__":
    n = 10  # Specify how many items you want to create
    # populate_books(n)
    populate_reviews(n)