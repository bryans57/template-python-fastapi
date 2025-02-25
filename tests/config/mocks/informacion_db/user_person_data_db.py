def insert_user_person():
    return """INSERT INTO person (identification,first_name,last_name,weight,height,
    age,city,country,email,phone,address,created_at) VALUES
             ('123456789','John','Doe',70.50,1.75,30,'New York','USA','john@mail.com',
             '3452359621','123 Main St, New York, NY 10030','2024-12-21 01:09:37.072'),
             ('987654321','Jane','Doe',60.50,1.65,25,'Los Angeles','USA','jane@mail.com',
             '3452359622','123 Main St, Los Angeles, CA 90030','2024-12-21 01:09:37.072');
        """
