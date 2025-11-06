from flask import jsonify, request

from db import db
from models.race import Race, race_schema, races_schema
from util.reflection import populate_object


def create_race():
  post_data = request.form if request.form else request.get_json()
  new_race = Race.new_race_obj()
  populate_object(new_race, post_data)

  try:
    db.session.add(new_race)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to create record"}), 400

  return jsonify({"message": "race created", "result": race_schema.dump(new_race)}), 201


def get_all_races():
  query = db.session.query(Race).all()
  if not query:
    return jsonify({"message": "no race found"}), 404
  return jsonify({"message": "races found", "results": races_schema.dump(query)}), 200


def get_race_by_id(race_id):
  query = db.session.query(Race).filter(Race.race_id == race_id).first()
  if not query:
    return jsonify({"message": "no result found for provided id"}), 404
  return jsonify({"message": "race found", "result": race_schema.dump(query)}), 200


def update_race_by_id(race_id):
  query = db.session.query(Race).filter(Race.race_id == race_id).first()
  post_data = request.form if request.form else request.get_json()

  if query:
    populate_object(race_query, post_data)
    db.session.commit()
    return jsonify({"message": "race updated", "result": race_schema.dump(query)}), 200

  return jsonify({"message": "unable to update record"}), 400


def delete_race_by_id(race_id):
  query = db.session.query(Race).filter(Race.race_id == race_id).first()
  
  if not query:
    return jsonify({"message": "race not found"}), 404
  
  if query.heroes:
    return jsonify({"message": "cannot delete race with associated heroes"}), 400

  db.session.delete(query)
  db.session.commit()
  return jsonify({"message": "race deleted"}), 200