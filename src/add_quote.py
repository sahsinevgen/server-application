from sqlalchemy.sql.expression import func
from base import Session

def add_quote(quote, name):
    session = Session()

    # _upload={'quote':quote, 'user_name':name}
    # a = session.execute(func.public.add_quote(*_upload.values()))
    a = session.execute(func.public.add_quote(quote, name))

    session.commit()
    session.close()

quote = input()
name = input()
add_quote(quote, name)
