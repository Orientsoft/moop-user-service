from flask import Blueprint, jsonify, request
from application.user_app import user_app
from auth import raise_status

users = Blueprint('users', __name__)


@users.route('/login', methods=['POST'])
def user_login():
    requestObj = {
        'name': request.json.get('name'),
        'key': request.json.get('key')
    }
    user = user_app(requestObj=requestObj).login()
    if type(user) == dict:
        return jsonify(user)
    else:
        return user


@users.route('/users', methods=['GET'])
def users_list():
    requestObj = {}
    page = int(request.args.get('page', '1'))
    pageSize = int(request.args.get('pageSize', '20'))
    queries = ['name', 'role', 'certification']
    for query in queries:
        value = request.args.get(query)
        if value:
            if query == 'role':
                requestObj[query] = int(value)
            else:
                requestObj[query] = value
    if request.args.get('all'):
        page = pageSize = None
    else:
        count = user_app(requestObj=requestObj).user_count()
        if count % pageSize == 0:
            totalPage = count // pageSize
        else:
            totalPage = (count // pageSize) + 1
        if page > totalPage:
            return raise_status(400, '页数超出范围')
    users_list = user_app(requestObj=requestObj).user_find_all(page, pageSize)
    user_ln_list = []
    for user in users_list:
        re = user_app().get_return(user=user)
        user_ln_list.append(re)
    returnObj = {}
    if not request.args.get('all'):
        returnObj['meta'] = {'page': page, 'pageSize': pageSize, 'total': count, 'totalPage': totalPage}
    returnObj['users'] = user_ln_list
    return jsonify(returnObj)


@users.route('/users', methods=['POST'])
def user_sign():
    requestObj = request.json
    returnObj = {}
    try:
        if type(requestObj) == list:
            returnObj['users'] = []
            for insertObj in requestObj:
                user_model = user_app(requestObj=insertObj).user_insert()
                returnObj['users'].append(user_app().get_return(user_model))
        elif type(requestObj) == dict:
            user_model = user_app(requestObj, 'user').user_insert()
            returnObj['users'] = user_app().get_return(user_model)
        return jsonify(returnObj)
    except Exception as e:
        print(e)
        return jsonify(raise_status(400, '创建失败'))


@users.route('/users/<userId>', methods=['GET'])
def user_get_by_id(userId):
    from bson import ObjectId

    requestObj = {'_id': ObjectId(userId)}
    try:
        user = user_app(requestObj=requestObj).user_find_one()
    except Exception:
        return raise_status(400, '无效的Id')
    re = user_app().get_return(user=user)
    return jsonify(re)


@users.route('/users/<userId>', methods=['PUT'])
def user_update_totally(userId):
    from bson import ObjectId

    requestObj = {'_id': ObjectId(userId)}
    updateObj = request.json()
    fields_list = ['name', 'key', 'role', 'mobile', 'email', 'remark', 'certification', 'thumb']
    for i in fields_list:
        if i not in updateObj.keys():
            return raise_status(400, '信息不全')
    try:
        user_app(requestObj=requestObj, updateObj=updateObj).user_update()
    except Exception as e:
        print('user_update_totally error:', e)
        return raise_status(500, '后台异常')
    return raise_status(200)


@users.route('/users/<userId>', methods=['PATCH'])
def user_update_by_set(userId):
    from bson import ObjectId

    requestObj = {'_id': ObjectId(userId)}
    updateObj = request.json()
    try:
        user_app(requestObj=requestObj, updateObj=updateObj).user_update()
    except Exception as e:
        print('user_update_totally error:', e)
        return raise_status(500, '后台异常')
    return raise_status(200)

@users.route('/users/<userId>', methods=['DELETE'])
def user_delete(userId):
    from bson import ObjectId

    requestObj = {'_id': ObjectId(userId)}
    updateObj = {'delete': True}
    user_app(requestObj=requestObj, updateObj=updateObj).user_update()
