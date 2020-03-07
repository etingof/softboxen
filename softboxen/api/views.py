#
# This file is part of softboxen software.
#
# Copyright (c) 2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/softboxen/LICENSE.rst
#

import flask
from sqlalchemy import func
from werkzeug import exceptions

from softboxen.api import app
from softboxen.api import db
from softboxen.api import models
from softboxen.api import schemas

PREFIX = '/softboxen/v1'


@app.errorhandler(exceptions.HTTPException)
def flask_exception_handler(exc):
    app.logger.error(exc)
    err = {
        'status': exc.code,
        'message': exc.description
    }
    response = flask.jsonify(err)
    response.status_code = exc.code
    return response


@app.errorhandler(Exception)
def all_exception_handler(exc):
    app.logger.error(exc)
    err = {
        'status': 400,
        'message': getattr(exc, 'message', str(exc))
    }
    response = flask.jsonify(err)
    response.status_code = 400
    return response


def search_model(model, query):

    known_columns = model.__table__.columns.keys()

    for search_column in flask.request.args:
        if search_column not in known_columns:
            raise exceptions.NotFound(
                'Search term %s is not supported' % search_column)

        search_terms = flask.request.args.getlist(search_column)
        if search_terms:
            search_terms = [term.lower() for term in search_terms]
            query = query.filter(
                func.lower(getattr(model, search_column)).in_(search_terms))

    return query


@app.route(PREFIX + '/')
def show_root():
    response = {
        'description': 'Softboxen CLI simulation REST API '
        '(http://snmplabs.com/softboxen)',
        'boxen': {
            '_links': {
                'self': flask.url_for('show_boxen')
            }
        }
    }

    schema = schemas.RootSchema()
    return schema.jsonify(response), 200


@app.route(PREFIX + '/boxen')
def show_boxen():
    boxen_query = (
        models.Box
        .query)

    boxen_query = search_model(models.Box, boxen_query)

    boxen = boxen_query.all()
    response = {
        'members': boxen,
        'count': len(boxen)
    }

    schema = schemas.BoxenSchema()
    return schema.jsonify(response), 200


@app.route(PREFIX + '/boxen/<id>', methods=['GET'])
def show_box(id):
    box = (
        models.Box
        .query
        .filter_by(id=id)
        .first())

    if not box:
        raise exceptions.NotFound('Box not found')

    schema = schemas.BoxSchema()
    return schema.jsonify(box), 200


@app.route(PREFIX + '/boxen', methods=['POST'])
def new_box():
    req = flask.request.json

    box = models.Box(**req)
    db.session.add(box)

    db.session.commit()

    schema = schemas.BoxSchema()
    return schema.jsonify(box), 201


@app.route(PREFIX + '/boxen/<id>', methods=['DELETE'])
def del_box(id):
    box = (
        models.Box
        .query
        .filter_by(id=id)
        .first())

    if not box:
        raise exceptions.NotFound('Box not found')

    db.session.delete(box)
    db.session.commit()

    return flask.Response(status=204)


@app.route(PREFIX + '/boxen/<box_id>/credentials')
def show_credentials(box_id):
    credentials_query = (
        models.Credential
        .query
        .filter_by(box_id=box_id))

    credentials_query = search_model(models.Credential, credentials_query)

    schema = schemas.CredentialsSchema()
    credentials = credentials_query.all()
    response = {
        'members': credentials,
        'count': len(credentials),
        'box_id': box_id
    }

    return schema.jsonify(response), 200


@app.route(PREFIX + '/boxen/<box_id>/credentials/<id>', methods=['GET'])
def show_credential(box_id, id):
    credential = (
        models.Credential
        .query
        .filter_by(box_id=box_id, id=id)
        .first())

    if not credential:
        raise exceptions.NotFound('Credentials not found')

    schema = schemas.CredentialSchema()
    return schema.jsonify(credential), 200


@app.route(PREFIX + '/boxen/<box_id>/credentials', methods=['POST'])
def new_credential(box_id):
    req = flask.request.json

    credential = models.Credential(box_id=box_id, **req)
    db.session.add(credential)

    db.session.commit()

    schema = schemas.CredentialSchema()
    return schema.jsonify(credential), 201


@app.route(PREFIX + '/boxen/<box_id>/credentials/<id>', methods=['DELETE'])
def del_credential(box_id, id):
    credential = (
        models.Credential
        .query
        .filter_by(box_id=box_id, id=id)
        .first())

    if not credential:
        raise exceptions.NotFound('Credentials not found')

    db.session.delete(credential)
    db.session.commit()

    return flask.Response(status=204)


@app.route(PREFIX + '/boxen/<box_id>/ports')
def show_ports(box_id):
    ports_query = (
        models.Port
        .query
        .filter_by(box_id=box_id))

    ports_query = search_model(models.Port, ports_query)

    ports = ports_query.all()
    response = {
        'members': ports,
        'count': len(ports),
        'box_id': box_id
    }

    schema = schemas.PortsSchema()
    return schema.jsonify(response), 200


@app.route(PREFIX + '/boxen/<box_id>/ports/<id>', methods=['GET'])
def show_port(box_id, id):
    port = (
        models.Port
        .query
        .filter_by(box_id=box_id, id=id)
        .first())

    if not port:
        raise exceptions.NotFound('Port not found')

    schema = schemas.PortSchema()
    return schema.jsonify(port), 200


@app.route(PREFIX + '/boxen/<box_id>/ports', methods=['POST'])
def new_port(box_id):
    req = flask.request.json

    port = models.Port(box_id=box_id, **req)
    db.session.add(port)

    db.session.commit()

    schema = schemas.PortSchema()
    return schema.jsonify(port), 201


@app.route(PREFIX + '/boxen/<box_id>/ports/<id>', methods=['DELETE'])
def del_port(box_id, id):
    port = (
        models.Port
        .query
        .filter_by(box_id=box_id, id=id)
        .first())

    if not port:
        raise exceptions.NotFound('Port not found')

    db.session.delete(port)
    db.session.commit()

    return flask.Response(status=204)


@app.route(PREFIX + '/boxen/<box_id>/ports/<port_id>/vlan/<role>')
def show_vlan_ports(box_id, port_id, role):
    vlan_ports_query = (
        models.VlanPort
        .query
        .filter_by(box_id=box_id, port_id=port_id, role=role))

    vlan_ports_query = search_model(models.VlanPort, vlan_ports_query)

    vlan_ports = vlan_ports_query.all()
    response = {
        'members': vlan_ports,
        'count': len(vlan_ports),
        'box_id': box_id,
        'role': role,
        'port_id': port_id
    }

    schema = schemas.VlanPortsSchema()
    return schema.jsonify(response), 200


@app.route(
    PREFIX + '/boxen/<box_id>/ports/<port_id>/vlan/<role>/<id>',
    methods=['GET'])
def show_vlan_port(box_id, port_id, role, id):
    vlan_port = (
        models.VlanPort
        .query
        .filter_by(box_id=box_id, port_id=port_id, role=role, id=id)
        .first())

    if not vlan_port:
        raise exceptions.NotFound('VLAN port not found')

    schema = schemas.VlanPortSchema()
    return schema.jsonify(vlan_port), 200


@app.route(
    PREFIX + '/boxen/<box_id>/ports/<port_id>/vlan/<role>',
    methods=['POST'])
def new_vlan_port(box_id, port_id, role):
    req = flask.request.json

    vlan_port = models.VlanPort(
        box_id=box_id, port_id=port_id, **dict(req, role=role))
    db.session.add(vlan_port)

    db.session.commit()

    schema = schemas.VlanPortSchema()
    return schema.jsonify(vlan_port), 201


@app.route(
    PREFIX + '/boxen/<box_id>/ports/<port_id>/vlan/<role>/<id>',
    methods=['DELETE'])
def del_vlan_port(box_id, port_id, role, id):
    vlan_port = (
        models.VlanPort
        .query
        .filter_by(box_id=box_id, port_id=port_id, role=role, id=id)
        .first())

    if not vlan_port:
        raise exceptions.NotFound('VLAN port not found')

    db.session.delete(vlan_port)
    db.session.commit()

    return flask.Response(status=204)


@app.route(PREFIX + '/boxen/<box_id>/routes')
def show_routes(box_id):
    routes_query = (
        models.Route
        .query
        .filter_by(box_id=box_id))

    routes_query = search_model(models.Route, routes_query)

    routes = routes_query.all()
    response = {
        'members': routes,
        'count': len(routes),
        'box_id': box_id
    }

    schema = schemas.RoutesSchema()
    return schema.jsonify(response), 200


@app.route(PREFIX + '/boxen/<box_id>/routes/<id>', methods=['GET'])
def show_route(box_id, id):
    route = (
        models.Route
        .query
        .filter_by(box_id=box_id, id=id)
        .first())

    if not route:
        raise exceptions.NotFound('Routes not found')

    schema = schemas.RouteSchema()
    return schema.jsonify(route), 200


@app.route(PREFIX + '/boxen/<box_id>/routes', methods=['POST'])
def new_route(box_id):
    req = flask.request.json

    route = models.Route(box_id=box_id, **req)
    db.session.add(route)

    db.session.commit()

    schema = schemas.RouteSchema()
    return schema.jsonify(route), 201


@app.route(PREFIX + '/boxen/<box_id>/routes/<id>', methods=['DELETE'])
def del_route(box_id, id):
    route = (
        models.Route
        .query
        .filter_by(box_id=box_id, id=id)
        .first())

    if not route:
        raise exceptions.NotFound('Routes not found')

    db.session.delete(route)
    db.session.commit()

    return flask.Response(status=204)
