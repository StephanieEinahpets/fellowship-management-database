from flask import jsonify, request

from db import db
from models.hero import Hero, hero_schema, heroes_schema
from models.hero_quest import HeroQuest
from models.quest import Quest
from util.reflection import populate_object


def create_hero():
    post_data = request.form if request.form else request.get_json()
    new_hero = Hero.new_hero_obj()
    populate_object(new_hero, post_data)

    try:
        db.session.add(new_hero)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "hero created", "result": hero_schema.dump(new_hero)}), 201

def add_hero_to_quest():
    post_data = request.form if request.form else request.get_json()
    hero_id = post_data.get("hero_id")
    quest_id = post_data.get("quest_id")

    hero_query = db.session.query(Hero).filter(Hero.hero_id == hero_id).first()
    quest_query = db.session.query(Quest).filter(Quest.quest_id == quest_id).first()

    if not hero_query:
        return jsonify({"message": "hero not found"}), 404

    if not quest_query:
        return jsonify({"message": "quest not found"}), 404
    
    existing = db.session.query(HeroQuest).filter_by(hero_id=hero_id, quest_id=quest_id).first()
    if existing:
        return jsonify({"message": "hero already added to this quest"}), 400

    new_quest = HeroQuest(hero_id=hero_id, quest_id=quest_id)
    db.session.add(new_quest)
    db.session.commit()
    return jsonify({"message": "hero added to quest", "result": hero_schema.dump(hero_query)}), 200


def get_all_heroes():
    query = db.session.query(Hero).all()
    if not query:
        return jsonify({"message": "no heroes found"}), 404
    return jsonify({"message": "heroes found", "results": heroes_schema.dump(query)}), 200

def get_alive_heroes():
    alive_heroes_query = db.session.query(Hero).filter(Hero.is_alive == True).all()
    if not alive_heroes_query:
        return jsonify({"message": "no alive heroes found"}), 404
    return jsonify({"message": "heroes found", "results": heroes_schema.dump(alive_heroes_query)}), 200

def get_hero_by_id(hero_id):
    query = db.session.query(Hero).filter(Hero.hero_id == hero_id).first()
    if not query:
        return jsonify({"message": "no result found for provided id"}), 404
    return jsonify({"message": "hero found", "result": hero_schema.dump(query)}), 200

def get_quests_by_hero(hero_id):
    from models.quest import quests_schema
    hero_query = db.session.query(Hero).filter(Hero.hero_id == hero_id).first()

    if not hero_query:
        return jsonify({"message": "no result found"}), 404
    
    quests_list = [hq.quest for hq in hero_query.hero_quests]

    if not quests_list:
        return jsonify({"message": "no quests found for this hero"}), 404
    
    return jsonify({"message": "quests found", "results": quests_schema.dump(quests_list)}), 200


def update_hero_by_id(hero_id):
    query = db.session.query(Hero).filter(Hero.hero_id == hero_id).first()
    post_data = request.form if request.form else request.get_json()

    if query:
        populate_object(query, post_data)
        db.session.commit()
        return jsonify({"message": "hero updated", "result": hero_schema.dump(query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400


def delete_hero_by_id(hero_id):
    query = db.session.query(Hero).filter(Hero.hero_id == hero_id).first()
    if query:
        db.session.delete(query)
        db.session.commit()
        return jsonify({"message": "hero deleted"}), 200
    return jsonify({"message": "unable to delete hero"}), 400