from flask import jsonify, request

from db import db
from models.location import Location, location_schema, locations_schema
from models.quest import Quest
from util.reflection import populate_object


def create_location():
  post_data = request.form if request.form else request.get_json()
  new_location = Location.new_location_obj()
  populate_object(new_location, post_data)
  try:
    db.session.add(new_location)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to create record"}), 400
  return jsonify({"message": "location created", "result": location_schema.dump(new_location)}), 201


def get_location_by_id(location_id):
  query = db.session.query(Location).filter(Location.location_id == location_id).first()
  if not query:
    return jsonify({"message": "no result found for provided id"}), 404
  return jsonify({"message": "location found", "result": location_schema.dump(query)}), 200


def update_location_by_id(location_id):
  query = db.session.query(Location).filter(Location.location_id == location_id).first()
  post_data = request.form if request.form else request.get_json()
  if query:
    populate_object(query, post_data)
    db.session.commit()
    return jsonify({"message": "location updated", "result": location_schema.dump(query)}), 200
  return jsonify({"message": "unable to update record"}), 400


def delete_location_by_id(location_id):
  active_quests = db.session.query(Quest).filter(
    Quest.location_id == location_id,
    Quest.is_completed == False
  ).first()

  if active_quests:
    return jsonify({"message": "cannot delete location with active quests"}), 400
  
  query = db.session.query(Location).filter(Location.location_id == location_id).first()

  if query:
    db.session.delete(query)
    db.session.commit()
    return jsonify({"message": "location deleted"}), 200
  return jsonify({"message": "unable to delete location"}), 400