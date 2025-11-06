from flask import Blueprint
import controllers

location = Blueprint('warranty', __name__)


@location.route('/location', methods=['POST'])
def create_location_route():
   return controllers.create_location()

@location.route('/location/<location_id>', methods= ['GET'])
def get_location_by_id_route(location_id):
    return controllers.get_location_by_id(location_id)

@location.route('/location/<location_id>', methods=['PUT'])
def update_location_by_id_route(location_id):
   return controllers.update_location_by_id(location_id)

@location.route('/location/delete/<location_id>', methods=['DELETE'])
def delete_location_by_id_route(warranty_id):
   return controllers.delete_location_by_id(warranty_id)