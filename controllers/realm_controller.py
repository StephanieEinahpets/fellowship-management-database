from flask import jsonify, request

from db import db
from models.realm import Realm, realm_schema, realms_schema
from util.reflection import populate_object


def create_realm():
  post_data = request.form if request.form else request.get_json()
  new_realm = Realm.new_realm_obj()
  populate_object(new_realm, post_data)

  try:
    db.session.add(new_realm)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to create record"}), 400

  return jsonify({"message": "realm created", "result": realm_schema.dump(new_realm)}), 201


def get_realm_by_id(realm_id):
  query = db.session.query(Realm).filter(Realm.realm_id == realm_id).first()
  if not query:
    return jsonify({"message": "no result found for provided id"}), 404
  return jsonify({"message": "realm found", "result": realm_schema.dump(query)}), 200


def update_realm_by_id(realm_id):
  query = db.session.query(Realm).filter(Realm.realm_id == realm_id).first()
  post_data = request.form if request.form else request.get_json()

  if query:
    populate_object(query, post_data)
    db.session.commit()
    return jsonify({"message": "realm updated", "result": realm_schema.dump(query)}), 200

  return jsonify({"message": "unable to update record"}), 400


def delete_realm_by_id(realm_id):
  query = db.session.query(Realm).filter(Realm.realm_id == realm_id).first()
  if query:
    if query.locations:
      return jsonify({"message": "cannot delete realm with associated locations"}), 400
    db.session.delete(query)
    db.session.commit()
    return jsonify({"message": "realm deleted"}), 200
  return jsonify({"message": "unable to delete realm"}), 400