from flask import jsonify, request

from db import db
from models.ability import Ability, ability_schema, abilities_schema
from util.reflection import populate_object


def create_ability():
  post_data = request.form if request.form else request.get_json()
  new_ability = Ability.new_ability_obj()
  populate_object(new_ability, post_data)

  try:
    db.session.add(new_ability)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to create record"}), 400

  return jsonify({"message": "ability created", "result": ability_schema.dump(new_ability)}), 201


def update_ability_by_id(ability_id):
  query = db.session.query(Ability).filter(Ability.ability_id == ability_id).first()
  post_data = request.form if request.form else request.get_json()

  if query:
    populate_object(query, post_data)
    db.session.commit()
    return jsonify({"message": "ability updated", "result": ability_schema.dump(ability_query)}), 200
  
  return jsonify({"message": "unable to update record"}), 400


def delete_ability_by_id(ability_id):
  query = db.session.query(Ability).filter(Ability.ability_id == ability_id).first()

  if query:
    db.session.delete(query)
    db.session.commit()
    return jsonify({"message": "ability deleted"}), 200
  
  return jsonify({"message": "unable to delete ability"}), 400