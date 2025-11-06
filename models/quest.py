import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from db import db

class Quest(db.Model):
  __tablename__ = 'Quests'
  
  quest_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  location_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Locations.location_id'), nullable=False)
  quest_name = db.Column(db.String(100), unique=True, nullable=False)
  difficulty = db.Column(db.String(50), default='Easy')
  reward_gold = db.Column(db.Integer, default=100)
  is_completed = db.Column(db.Boolean, default=False)
  
  location = db.relationship("Location", back_populates='quests')
  hero_quests = db.relationship('HeroQuest', back_populates='quest', cascade='all, delete-orphan')

  def __init__(self, quest_name, location_id, difficulty='Easy', reward_gold=100, is_completed=False):
    self.quest_name = quest_name
    self.location_id = location_id
    self.difficulty = difficulty
    self.reward_gold = reward_gold
    self.is_completed = is_completed


class QuestSchema(ma.Schema):
  class Meta:
    fields = ('quest_id', 'location_id', 'quest_name', 'difficulty', 'reward_gold', 'is_completed', 'location', 'heroes')
  
  quest_id = ma.fields.UUID(dump_only=True)
  location_id = ma.fields.UUID()
  quest_name = ma.fields.String(required=True)
  difficulty = ma.fields.String()
  reward_gold = ma.fields.Integer()
  is_completed = ma.fields.Boolean()
  
  location = ma.fields.Nested('LocationSchema', only=('location_id', 'location_name', 'danger_level'), dump_only=True)
  heroes = ma.fields.Method('get_heroes')
  
  def get_heroes(self, obj):
    from models.hero import HeroSchema
    hero_schema = HeroSchema(many=True, only=('hero_id', 'hero_name'))
    return hero_schema.dump([hq.hero for hq in obj.hero_quests])

quest_schema = QuestSchema()
quests_schema = QuestSchema(many=True)
