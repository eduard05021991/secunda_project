from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from models import Activity, Building, Organization, PhoneNumber, OrganizationActivity
from db.session import Base


# Создаём подключение через sync SQLAlchemy, чтобы быстро выполнить вставки
engine = create_engine(settings.dsn.replace("+asyncpg", ""))  # sync драйвер
SessionLocal = sessionmaker(bind=engine)

def seed():
    session = SessionLocal()

    # Деятельности (иерархия)
    food = Activity(name="Еда", level=1)
    meat = Activity(name="Мясная продукция", parent=food, level=2)
    milk = Activity(name="Молочная продукция", parent=food, level=2)
    cars = Activity(name="Автомобили", level=1)
    trucks = Activity(name="Грузовые", parent=cars, level=2)
    light = Activity(name="Легковые", parent=cars, level=2)
    parts = Activity(name="Запчасти", parent=light, level=3)
    accessories = Activity(name="Аксессуары", parent=light, level=3)

    session.add_all([food, meat, milk, cars, trucks, light, parts, accessories])

    # Здания
    building1 = Building(address="г. Москва, ул. Ленина, 1", latitude=55.7558, longitude=37.6176)
    building2 = Building(address="г. Москва, ул. Блюхера, 32/1", latitude=55.7600, longitude=37.6200)

    session.add_all([building1, building2])
    session.flush()

    # Организации
    org1 = Organization(name="ООО Рога и Копыта", building_id=building1.id)
    org2 = Organization(name="АО Молочные радости", building_id=building2.id)

    session.add_all([org1, org2])
    session.flush()

    # Телефоны
    phones = [
        PhoneNumber(organization_id=org1.id, phone_number="2-222-222"),
        PhoneNumber(organization_id=org1.id, phone_number="3-333-333"),
        PhoneNumber(organization_id=org2.id, phone_number="8-923-666-13-13"),
    ]
    session.add_all(phones)

    # Привязка деятельностей
    session.add_all([
        OrganizationActivity(organization_id=org1.id, activity_id=meat.id),
        OrganizationActivity(organization_id=org1.id, activity_id=parts.id),
        OrganizationActivity(organization_id=org2.id, activity_id=milk.id),
    ])

    session.commit()
    session.close()
    print("Тестовые данные успешно загружены!")


if __name__ == "__main__":
    seed()
