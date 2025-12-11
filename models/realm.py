import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class Realm(db.Model):
  __tablename__ = "Realms"
  
  realm_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  realm_name = db.Column(db.String(100), nullable=False, unique=True)
  ruler = db.Column(db.String(100), default='')

  locations = db.relationship(
    "Location",
    back_populates='realm',
    cascade='all, delete-orphan'
  )

  def __init__(self, realm_name='', ruler=''):
    self.realm_name = realm_name
    self.ruler = ruler

  def new_realm_obj():
    return Realm(realm_name='', ruler='')

class RealmSchema(ma.Schema):
  class Meta:
    fields = ['realm_id', 'realm_name', 'ruler', 'locations']
  
  realm_id = ma.fields.UUID(dump_only=True)
  realm_name = ma.fields.String(required=True)
  ruler = ma.fields.String(allow_none=True)
  locations = ma.fields.Nested(
    'LocationSchema',
    many=True,
    only=('location_id', 'location_name', 'danger_level'),
    dump_only=True
  )

realm_schema = RealmSchema()
realms_schema = RealmSchema(many=True)
