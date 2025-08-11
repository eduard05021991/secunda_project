INSERT INTO buildings (address, latitude, longitude) VALUES
('г. Москва, ул. Ленина 1, офис 3', 55.7558, 37.6173),
('г. Москва, ул. Блюхера 32/1', 55.7600, 37.6200);

INSERT INTO activities (name, parent_id, level) VALUES
('Еда', NULL, 1),
('Мясная продукция', 1, 2),
('Молочная продукция', 1, 2),
('Автомобили', NULL, 1),
('Грузовые', 4, 2),
('Легковые', 4, 2),
('Запчасти', 6, 3),
('Аксессуары', 6, 3);

INSERT INTO organizations (name, building_id) VALUES
('ООО Рога и Копыта', 1),
('ООО Вкусная Еда', 2);

INSERT INTO phone_numbers (organization_id, phone_number) VALUES
(1, '2-222-222'),
(1, '3-333-333'),
(2, '8-923-666-13-13');

INSERT INTO organization_activities (organization_id, activity_id) VALUES
(1, 2),
(1, 3),
(2, 1);
