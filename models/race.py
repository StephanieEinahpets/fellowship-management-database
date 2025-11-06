import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class Race(db.Model):
  __tablename__ = 'Races'
  
  race_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  race_name = db.Column(db.String(), unique=True, nullable=False)
  homeland = db.Column(db.String())
  lifespan = db.Column(db.Integer())
  
  heroes = db.relationship('Hero', back_populates='race', cascade='all, delete-orphan')

  def __init__(self, race_name, homeland='', lifespan=0):
    self.race_name = race_name
    self.homeland = homeland
    self.lifespan = lifespan

  def new_race_obj():
    return Race(race_name='', homeland='', lifespan=0)

class RaceSchema(ma.Schema):
  class Meta:
    fields = ('race_id', 'race_name', 'homeland', 'lifespan', 'heroes')
  
  race_id = ma.fields.UUID(dump_only=True)
  race_name = ma.fields.String(required=True)
  homeland = ma.fields.String(allow_none=True)
  lifespan = ma.fields.Integer(allow_none=True)
  heroes = ma.fields.Nested('HeroSchema', many=True, only=('hero_id', 'hero_name'), dump_only=True)

race_schema = RaceSchema()
races_schema = RaceSchema(many=True)
