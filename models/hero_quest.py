import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class HeroQuest(db.Model):
  __tablename__ = 'HeroQuests'
  
  hero_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Heroes.hero_id'), primary_key=True)
  quest_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Quests.quest_id'), primary_key=True)
  date_joined = db.Column(db.DateTime, default=datetime.utcnow)
  
  hero = db.relationship("Hero", back_populates="hero_quests")
  quest = db.relationship("Quest", back_populates="hero_quests")

  def __init__(self, hero_id=None, quest_id=None):
    self.hero_id = hero_id
    self.quest_id = quest_id

  def new_hero_quest_obj():
    return HeroQuest(hero_id=None, quest_id=None)

class HeroQuestSchema(ma.Schema):
  class Meta:
    fields = ('hero_id', 'quest_id', 'date_joined')
  
  hero_id = ma.fields.UUID()
  quest_id = ma.fields.UUID()
  date_joined = ma.fields.DateTime(dump_only=True)

hero_quest_schema = HeroQuestSchema()
hero_quests_schema = HeroQuestSchema(many=True)