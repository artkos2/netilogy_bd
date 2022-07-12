import psycopg2

conn = psycopg2.connect(database='postgres', user= 'postgres', password='')
def create_table():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                name VARCHAR(40),
                surname VARCHAR(40)
            );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts(
            id SERIAL PRIMARY KEY,
            email TEXT,
            telephone TEXT
            );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients_contacts(
            client_id SERIAL REFERENCES clients(id),
            contact_id SERIAL REFERENCES contacts(id)
            );
        """)
        conn.commit()

def create_client(name, surname, email, telephone = 'NULL'):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO clients(name, surname) VALUES (%s, %s) RETURNING id;
        """,(name, surname))
        client_id = cur.fetchone()
        cur.execute("""
        INSERT INTO contacts(email, telephone) VALUES (%s, %s) RETURNING id;
        """,(email, telephone))
        contact_id = cur.fetchone()
        cur.execute("""
        INSERT INTO clients_contacts(client_id, contact_id) VALUES (%s, %s);
        """,(client_id, contact_id))
        conn.commit()

def add_telephone(client_id, telephone):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO contacts(telephone) VALUES (%s) RETURNING id;
        """,(telephone,))
        contact_id = cur.fetchone()
        cur.execute("""
        INSERT INTO clients_contacts(client_id, contact_id) VALUES (%s, %s);
        """,(client_id, contact_id))
        conn.commit()
def update_client(client_id, new_name, new_surname):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE clients SET name=%s, surname=%s WHERE id=%s
        """,(new_name, new_surname, client_id))
        conn.commit()

def delete_telephone(client_id):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT contact_id FROM clients_contacts WHERE client_id=%s;
        """, (client_id,))
        contact_id = cur.fetchone()
        cur.execute("""
        UPDATE contacts SET telephone = %s WHERE id=%s;
        """, ('',contact_id))
        conn.commit()

def delete_client(client_id):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT contact_id FROM clients_contacts WHERE client_id=%s;
        """, (client_id,))
        contact_id_list = cur.fetchall()
        for contact_id in contact_id_list:
            cur.execute("""
            DELETE FROM clients_contacts WHERE contact_id=%s;
            """, (contact_id[0],))
            cur.execute("""
            DELETE FROM contacts WHERE id=%s;
            """, (contact_id[0],))
        cur.execute("""
        DELETE FROM clients WHERE id=%s;
        """, (client_id,))
        conn.commit()


def find_client(text):
    text = '%'+text+'%'
    with conn.cursor() as cur:
        cur.execute("""
        SELECT id FROM clients WHERE name LIKE %s OR surname LIKE %s
        """, (text,text))
        return_ids = cur.fetchall()
        cur.execute("""
        SELECT id FROM contacts WHERE email LIKE %s OR telephone LIKE %s
        """, (text,text))
        return__contact_ids = cur.fetchall()
        for id in return_ids:
            cur.execute("""
            SELECT name,surname FROM clients WHERE id =  %s
            """, (id,))
            print(cur.fetchone())
        for contact_id in return__contact_ids:
            cur.execute("""
            SELECT client_id FROM clients_contacts WHERE contact_id = %s
            """, (contact_id,))
            client_id = cur.fetchone()
            cur.execute("""
            SELECT name,surname FROM clients WHERE id =  %s
            """, (client_id,))
            print(cur.fetchone())

create_table()
create_client('Иван','Петров','ivan123@yandex.ru','+79098745698')
create_client('Петя','Сидоров','ivan123@yandex.ru','+79098747745')
add_telephone(2,'+79065458777')
delete_telephone(1)
update_client(1,'Петр', 'Петрович')
delete_client(1)
find_client('Сидор')
find_client('7745')
conn.close()