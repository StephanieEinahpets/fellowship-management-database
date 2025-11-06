from flask import jsonify, request

from db import db
from models.quest import Quest, quest_schema, quests_schema
from util.reflection import populate_object


def create_quest():
  post_data = request.form if request.form else request.get_json()
  new_quest = Quest.new_quest_obj()
  populate_object(new_quest, post_data)
  try:
    db.session.add(new_quest)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to create record"}), 400
  return jsonify({"message": "quest created", "result": quest_schema.dump(new_quest)}), 201


def get_quest_by_difficulty(difficulty_level):
  query = db.session.query(Quest).filter(Quest.difficulty == difficulty_level).all()
  if not query:
    return jsonify({"message": "no quests found with that difficulty"}), 404
  return jsonify({"message": "quests found", "results": quests_schema.dump(query)}), 200


def get_quest_by_id(quest_id):
  query = db.session.query(Quest).filter(Quest.quest_id == quest_id).first()
  if not query:
    return jsonify({"message": "no result found for provided id"}), 404
  return jsonify({"message": "quest found", "result": quest_schema.dump(query)}), 200


def update_quest_by_id(quest_id):
  query = db.session.query(Quest).filter(Quest.quest_id == quest_id).first()
  post_data = request.form if request.form else request.get_json()
  if query:
    populate_object(query, post_data)
    db.session.commit()
    return jsonify({"message": "quest updated", "result": quest_schema.dump(query)}), 200
  return jsonify({"message": "unable to update record"}), 400


def mark_quest_complete(quest_id):
  query = db.session.query(Quest).filter(Quest.quest_id == quest_id).first()
  if query:
    query.is_completed = True
    db.session.commit()
    return jsonify({"message": "quest marked as completed", "result": quest_schema.dump(query)}), 200
  return jsonify({"message": "quest not found"}), 404


def delete_quest_by_id(quest_id):
  query = db.session.query(Quest).filter(Quest.quest_id == quest_id).first()
  if query:
    db.session.delete(query)
    db.session.commit()
    return jsonify({"message": "quest deleted"}), 200
  return jsonify({"message": "unable to delete quest"}), 400