from flask import Blueprint

import controllers

realm = Blueprint('realm', __name__)

@realm.route('/realm', methods=['POST'])
def create_realm_route():
    return controllers.create_realm()

@realm.route('/realm/<realm_id>', methods=['GET'])
def get_realm_by_id_route(realm_id):
    return controllers.get_realm_by_id(realm_id)

@realm.route('/realm/<realm_id>', methods=['PUT'])
def update_realm_by_id_route(realm_id):
    return controllers.update_realm_by_id(realm_id)

@realm.route('/realm/delete/<realm_id>', methods=['DELETE'])
def delete_realm_by_id_route(realm_id):
    return controllers.delete_realm_by_id(realm_id)