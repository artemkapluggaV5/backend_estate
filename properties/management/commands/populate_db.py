from django.core.management.base import BaseCommand
from users.models import CustomUser, Agent
from properties.models import Category, Amenity, Property, PropertyImage
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populates the database with mock data'

    def handle(self, *args, **kwargs):
        fake = Faker('ru_RU')

        self.stdout.write('Creating users...')
        admin = CustomUser.objects.create_superuser('admin', 'admin@example.com', 'adminpass', role='admin')
        realtor = CustomUser.objects.create_user('realtor1', 'realtor@example.com', 'realtorpass', role='realtor')
        agent_profile = Agent.objects.create(user=realtor, experience_years=5, rating=4.9)
        client = CustomUser.objects.create_user('client1', 'client@example.com', 'clientpass', role='client')

        self.stdout.write('Creating categories and amenities...')
        cat_flat = Category.objects.create(name='Квартира', description='Жилые квартиры в многоквартирных домах')
        cat_house = Category.objects.create(name='Дом', description='Частные дома и коттеджи')
        categories = [cat_flat, cat_house]

        amenities_names = ['Wi-Fi', 'Кондиционер', 'Парковка', 'Бассейн', 'Балкон', 'Мебель']
        amenities = [Amenity.objects.create(name=name) for name in amenities_names]

        flat_titles = ['Уютная 1-комнатная квартира', 'Светлая студия с современным ремонтом', 'Просторная 2-комнатная квартира в центре', 'Видовая 3-комнатная квартира в новом ЖК', 'Квартира с дизайнерским ремонтом', 'Отличная двушка для семьи']
        house_titles = ['Современный коттедж 150 м²', 'Уютный кирпичный дом с садом', 'Двухэтажный таунхаус', 'Просторный загородный дом', 'Дом с гаражом и баней', 'Элитный особняк в тихом районе']
        
        flat_photos = [
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1502672260266-1c1de242441c?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=800&q=80"
        ]
        
        house_photos = [
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1583608205776-bfd35f0d9f83?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1570129477492-45c003edd2be?auto=format&fit=crop&w=800&q=80"
        ]

        self.stdout.write('Creating properties...')
        for _ in range(15):
            cat = random.choice(categories)
            title = random.choice(flat_titles) if cat.name == 'Квартира' else random.choice(house_titles)
            photos_pool = flat_photos if cat.name == 'Квартира' else house_photos
            
            # Clean up price to be nice round numbers like 4 500 000
            price = random.randint(20, 150) * 100000
            
            prop = Property.objects.create(
                category=cat,
                agent=agent_profile,
                title=title,
                description="Отличное предложение на рынке недвижимости Белореченска! " + fake.text(),
                price=price,
                area=round(random.uniform(30, 150), 1),
                address=fake.address(),
                is_active=True
            )
            prop.amenities.set(random.sample(amenities, k=random.randint(2, 4)))
            
            # Photos
            PropertyImage.objects.create(
                property=prop,
                image_path=random.choice(photos_pool),
                is_main=True
            )
            for _ in range(2):
                PropertyImage.objects.create(
                    property=prop,
                    image_path=random.choice(photos_pool),
                    is_main=False
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database!'))
