import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from db import db

class Ability(db.Model):
  __tablename__ = 'Abilities'
  
  ability_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  hero_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Heroes.hero_id'), nullable=False)
  ability_name = db.Column(db.String(), nullable=False)
  power_level = db.Column(db.Integer, default=1)

  hero = db.relationship("Hero", back_populates="abilities")

  def __init__(self, hero_id, ability_name, power_level=1):
    self.hero_id = hero_id
    self.ability_name = ability_name
    self.power_level = power_level

  def new_ability_obj():
    return Ability(hero_id=None, ability_name='', power_level=1)

class AbilitySchema(ma.Schema):
  class Meta:
    fields = ('ability_id', 'hero_id', 'ability_name', 'power_level')
  
  ability_id = ma.fields.UUID(dump_only=True)
  hero_id = ma.fields.UUID()
  ability_name = ma.fields.String(required=True)
  power_level = ma.fields.Integer(allow_none=True)

ability_schema = AbilitySchema()
abilities_schema = AbilitySchema(many=True)
