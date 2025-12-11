import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class Location(db.Model):
  __tablename__ = 'Locations'
  
  location_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  realm_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Realms.realm_id'), nullable=False)
  location_name = db.Column(db.String(), nullable=False)
  danger_level = db.Column(db.Integer, default=1)
  
  realm = db.relationship('Realm', back_populates='locations')
  quests = db.relationship('Quest', back_populates='location', cascade='all, delete-orphan')

  def __init__(self, location_name='', realm_id=None, danger_level=1):
    self.location_name = location_name
    self.realm_id = realm_id
    self.danger_level = danger_level

  def new_location_obj():
    return Location(location_name='', realm_id=None, danger_level=1)
  
class LocationSchema(ma.Schema):
  class Meta:
    fields = ('location_id', 'realm_id', 'location_name', 'danger_level', 'realm', 'quests')
  
  location_id = ma.fields.UUID(dump_only=True)
  realm_id = ma.fields.UUID()
  location_name = ma.fields.String(required=True)
  danger_level = ma.fields.Integer(allow_none=True)
  
  realm = ma.fields.Nested('RealmSchema', only=('realm_id', 'realm_name'), dump_only=True)
  quests = ma.fields.Nested('QuestSchema', many=True, only=('quest_id', 'quest_name', 'difficulty'), dump_only=True)

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)
