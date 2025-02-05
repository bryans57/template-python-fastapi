from enum import Enum


class TestDB(Enum):  # pylint: disable=too-few-public-methods
    PERSON = """
                CREATE TABLE public.person (
                    id serial4 NOT NULL,
                    identification varchar(50) NOT NULL,
                    first_name varchar(100) NOT NULL,
                    last_name varchar(100) NOT NULL,
                    weight numeric(5, 2) NULL,
                    height numeric(5, 2) NULL,
                    age int4 NULL,
                    city varchar(100) NULL,
                    country varchar(100) NULL,
                    email varchar(255) NULL,
                    phone varchar(15) NULL,
                    address text NULL,
                    created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
                    CONSTRAINT person_age_check CHECK ((age >= 0)),
                    CONSTRAINT person_email_key UNIQUE (email),
                    CONSTRAINT person_identification_key UNIQUE (identification),
                    CONSTRAINT person_pkey PRIMARY KEY (id)
                );
                   """
