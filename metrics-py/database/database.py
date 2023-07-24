from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# por enquanto coloquei o banco de dados como sqlite, mas podemos mudar para mysql
# só precisamos mudar a uri 
engine = create_engine('sqlite:///youtube_data.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
