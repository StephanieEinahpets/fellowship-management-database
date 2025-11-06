import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from db import db

class Hero(db.Model):
  __tablename__ = 'Heroes'
  
  hero_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  race_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Races.race_id'), nullable=False)
  hero_name = db.Column(db.String(100), unique=True, nullable=False)
  age = db.Column(db.Integer, default=0)
  health_points = db.Column(db.Integer, default=100)
  is_alive = db.Column(db.Boolean, default=True)
  
  race = db.relationship('Race', back_populates='heroes')
  abilities = db.relationship('Ability', back_populates='hero', cascade='all, delete-orphan')
  hero_quests = db.relationship('HeroQuest', back_populates='hero', cascade='all, delete-orphan')

  def __init__(self, hero_name, race_id, age=0, health_points=100, is_alive=True):
    self.hero_name = hero_name
    self.race_id = race_id
    self.age = age
    self.health_points = health_points
    self.is_alive = is_alive


class HeroSchema(ma.Schema):
  class Meta:
    fields = ('hero_id', 'race_id', 'hero_name', 'age', 'health_points', 'is_alive', 'race', 'abilities', 'quests')
  
  hero_id = ma.fields.UUID(dump_only=True)
  race_id = ma.fields.UUID()
  hero_name = ma.fields.String(required=True)
  age = ma.fields.Integer()
  health_points = ma.fields.Integer()
  is_alive = ma.fields.Boolean()
  
  race = ma.fields.Nested('RaceSchema', only=('race_id', 'race_name', 'homeland'), dump_only=True)
  abilities = ma.fields.Nested('AbilitySchema', many=True, dump_only=True)
  quests = ma.fields.Method('get_quests')
  
  def get_quests(self, obj):
    from models.quest import QuestSchema
    quest_schema = QuestSchema(many=True, only=('quest_id', 'quest_name', 'difficulty'))
    return quest_schema.dump([hq.quest for hq in obj.hero_quests])

hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True)
