from flask import Blueprint

import controllers

hero = Blueprint('hero', __name__)

@hero.route('/hero', methods=['POST'])
def create_hero_route():
    return controllers.create_hero()

@hero.route('/hero-quest', methods=['POST'])
def add_hero_to_quest_route():
    return controllers.add_hero_to_quest()

@hero.route('/heroes', methods=['GET'])
def get_all_heroes_route():
    return controllers.get_all_heroes()

@hero.route('/heroes/alive', methods=['GET'])
def get_alive_heroes_route():
    return controllers.get_alive_heroes()

@hero.route('/hero/<hero_id>', methods=['GET'])
def get_hero_by_id_route(hero_id):
    return controllers.get_hero_by_id(hero_id)

@hero.route('/hero/<hero_id>/quests', methods=['GET'])
def get_quests_by_hero_route(hero_id):
    return controllers.get_quests_by_hero(hero_id)

@hero.route('/hero/<hero_id>', methods=['PUT'])
def update_hero_by_id_route(hero_id):
    return controllers.update_hero_by_id(hero_id)

@hero.route('/hero/delete/<hero_id>', methods=['DELETE'])
def delete_hero_by_id_route(hero_id):
    return controllers.delete_hero_by_id(hero_id)