# -*- encoding: utf-8 -*-
from pg_ormapping.field import FieldBase, FieldType
from pg_ormapping.define import GlobalRedisKey, ObjectType
from pg_common.conf import RuntimeException, GLOBAL_DEBUG
from pg_common import log_info, datetime_2_str, str_2_datetime
from pg_redis import RedisManager, KEY_REDIS_DEFAULT_KEY
from pg_mongodb import MongoManager, KEY_MONGODB_DEFAULT_KEY, KEY_MONGODB_DEFAULT_DB
import json

__all__ = ["ObjectBase"]
__author__ = "baozilaji@gmail.com"

_DEBUG = False
_PRINT = False

__KEY_ORM__ = "__key_orm__"
__KEY_PRIMARY_KEY__ = "__key_primary_key__"
__KEY_REDIS_KEY__ = "__redis_key__"
__KEY_REDIS_EXPIRE_IN__ = "__redis_expire_in__"
__KEY_TABLE_NAME_KEY__ = "__table_name__"
__KEY_OBJ_TYPE__ = "__obj_type__"
__KEY_VALUES__ = "__key_values__"
__SELF_FIELDS__ = set([__KEY_VALUES__])


class ObjectBaseMetaclass(type):

    def __new__(mcs, name, bases, attrs):
        if name == "ObjectBase":
            return type.__new__(mcs, name, bases, attrs)
        else:
            if __KEY_OBJ_TYPE__ in attrs and not isinstance(attrs[__KEY_OBJ_TYPE__], ObjectType):
                raise RuntimeException("ObjectInitialize",
                                       f"Object: {name} attribute __obj_type__ must be ObjectType.")

            if __KEY_OBJ_TYPE__ in attrs:
                _obj_type = attrs[__KEY_OBJ_TYPE__]
                # redis数据类型，必须指定__redis_key__属性
                if _obj_type == ObjectType.REDIS or _obj_type == ObjectType.BOTH:

                    if __KEY_REDIS_KEY__ not in attrs or not isinstance(attrs[__KEY_REDIS_KEY__], GlobalRedisKey):
                        raise RuntimeException("ObjectInitialize",
                                               "Object: %s must define __redis_key__ attribute as GlobalRedisKey." % (
                                                   name,))

                    if __KEY_REDIS_EXPIRE_IN__ not in attrs or not isinstance(attrs[__KEY_REDIS_EXPIRE_IN__], int):
                        raise RuntimeException("ObjectInitialize", f"Object: {name} must define __redis_expire_in__ attribute as int")

                # mongo类型数据，必须指定__table_name__属性
                if _obj_type == ObjectType.MONGO or _obj_type == ObjectType.BOTH:
                    if __KEY_TABLE_NAME_KEY__ not in attrs or not isinstance(attrs[__KEY_TABLE_NAME_KEY__], str):
                        raise RuntimeException("ObjectInitialize", f"Object: {name} must define __table_name__ attribute as str")

            __orm__ = dict()
            __primary_key__ = []
            for _k, _v in attrs.items():
                if isinstance(_v, FieldBase):
                    __orm__[_k] = _v

                    if _v.primary_key:
                        __primary_key__.append(_k)

            for _k in __orm__.keys():
                attrs.pop(_k)

            attrs[__KEY_ORM__] = __orm__
            attrs[__KEY_PRIMARY_KEY__] = __primary_key__

            return type.__new__(mcs, name, bases, attrs)


class ObjectBase(object, metaclass=ObjectBaseMetaclass):
    def __init__(self):
        __orm__ = getattr(self, __KEY_ORM__)
        _values = {}
        for _k, _f in __orm__.items():
            _values[_k] = _f.dump()
        self[__KEY_VALUES__] = _values

    def __setattr__(self, key, value):
        __orm__ = getattr(self, __KEY_ORM__)

        if key not in __SELF_FIELDS__ and (not __orm__ or key not in __orm__):
            raise RuntimeException("setValue", f"attribute {key} not defined")

        if key not in __SELF_FIELDS__:
            if GLOBAL_DEBUG and _DEBUG:
                _field = __orm__[key]
                if not _field.check(value):
                    raise RuntimeException("setValue", f"key: {key}, "
                                                       f"value type error: {type(value)}, needs: {_field.type}")
            self[__KEY_VALUES__][key] = value
        else:
            self.__dict__[key] = value

        if _PRINT or (GLOBAL_DEBUG and _DEBUG):
            log_info(f"__setattr__ {key}: {value}")

    def __getattr__(self, item):
        _value = None
        if item not in __SELF_FIELDS__:
            if GLOBAL_DEBUG and _DEBUG:
                __orm__ = getattr(self, __KEY_ORM__)
                if not __orm__ or item not in __orm__:
                    raise RuntimeException("getValue", f"attribute {item} not defined")
            _value = self[__KEY_VALUES__][item]
        else:
            _value = self.__dict__[item]

        if _PRINT or (GLOBAL_DEBUG and _DEBUG):
            log_info(f"__getattr__ {item}: {_value}")
        return _value

    def __getattribute__(self, item):
        _value = object.__getattribute__(self, item)
        if _PRINT or (GLOBAL_DEBUG and _DEBUG):
            log_info(f"__getattribute__ {item}: {_value}")
        return _value

    def __setitem__(self, key, value):
        ObjectBase.__setattr__(self, key, value)

    def __getitem__(self, item):
        _value = ObjectBase.__getattr__(self, item)
        return _value

    def _get_redis_key(self, prefix=None):
        if prefix is not None:
            return "%s#%s" % (prefix, self._get_redis_base_key())
        return self._get_redis_base_key()

    def _get_pk_names(self):
        _pk = getattr(self, __KEY_PRIMARY_KEY__)
        if len(_pk) == 0:
            raise RuntimeException("getPrimaryKey", f"Object {self.__name__} do no have primary key defined.")
        return _pk

    def _get_mongo_pri_key(self):
        _pk = self._get_pk_names()

        return {_k: self[__KEY_VALUES__][_k] for _k in _pk}

    def _get_redis_base_key(self):
        _pk = self._get_pk_names()

        if any([not self[__KEY_VALUES__][_k] for _k in _pk]):
            raise RuntimeException("GetRedisKey", f"primary key val is default")

        _k_val = [str(self[__KEY_VALUES__][_k]) for _k in _pk]

        return "%s#%s" % (getattr(self, __KEY_REDIS_KEY__).value,
                         "#".join(_k_val))

    def to_dict(self, fields=None, save_all=True):
        _changed = set([])
        _keys = set(getattr(self, __KEY_PRIMARY_KEY__))
        if not save_all:
            if fields:
                if isinstance(fields, (tuple, list, set)):
                    _changed = set(fields)
                elif isinstance(fields, str):
                    _changed.add(fields)

        _out = {}
        _orm = getattr(self, __KEY_ORM__)
        for _f_name, _f_obj in _orm.items():
            _c = True if save_all else False
            if _f_name in _changed:
                _c = True
            if _c and _f_name not in _keys:
                if _f_obj.type == FieldType.LIST or _f_obj.type == FieldType.DICT:
                    _out[_f_name] = json.dumps(self[__KEY_VALUES__][_f_name])
                elif _f_obj.type == FieldType.SET:
                    _out[_f_name] = json.dumps(list(self[__KEY_VALUES__][_f_name]))
                elif _f_obj.type == FieldType.DATETIME:
                    _out[_f_name] = datetime_2_str(self[__KEY_VALUES__][_f_name], 0, _fmt=_f_obj.fmt)
                elif _f_obj.type == FieldType.OBJECT:
                    _o = self[__KEY_VALUES__][_f_name].to_dict(save_all=True)
                    _out[_f_name] = json.dumps(_o)
                else:
                    _out[_f_name] = self[__KEY_VALUES__][_f_name]
        return _out

    async def save(self, prefix=None, db_source=KEY_MONGODB_DEFAULT_KEY, db_name=KEY_MONGODB_DEFAULT_DB,
                   fields=None, save_all=True, redis_client=None, redis_server_name=KEY_REDIS_DEFAULT_KEY):
        _o_type = getattr(self, __KEY_OBJ_TYPE__)
        _data_update = self.to_dict(fields=fields, save_all=save_all)
        if _o_type == ObjectType.REDIS or _o_type == ObjectType.BOTH:
            _pri_key = self._get_redis_key(prefix=prefix)
            if redis_client is None:
                redis_client = await RedisManager.get_redis(svr_name=redis_server_name)
            await redis_client.hset(_pri_key, mapping=_data_update)
            _expire_in = getattr(self, __KEY_REDIS_EXPIRE_IN__)
            if _expire_in:
                await redis_client.expire(_pri_key, _expire_in)

        if _o_type == ObjectType.MONGO or _o_type == ObjectType.BOTH:
            _mongo_client = MongoManager.get_mongodb(svr_name=db_source)
            _db = _mongo_client[db_name]
            _tb_name = getattr(self, __KEY_TABLE_NAME_KEY__)
            _tb = _db[_tb_name]
            await _tb.update_one(self._get_mongo_pri_key(), {'$set': _data_update})
        return self

    async def load(self, prefix=None, db_source=KEY_MONGODB_DEFAULT_KEY, db_name=KEY_MONGODB_DEFAULT_DB,
                   redis_client=None, redis_server_name=KEY_REDIS_DEFAULT_KEY)->bool:
        _o_type = getattr(self, __KEY_OBJ_TYPE__)
        if _o_type == ObjectType.REDIS or _o_type == ObjectType.BOTH:
            _redis_pri_key = self._get_redis_key(prefix=prefix)
            if not redis_client:
                redis_client = await RedisManager.get_redis(svr_name=redis_server_name)
            _out = await redis_client.hgetall(_redis_pri_key)
            # 缓存中存在数据
            if _out:
                self.from_dict(_out)
                _expire_in = getattr(self, __KEY_REDIS_EXPIRE_IN__)
                if _expire_in:
                    await redis_client.expire(_redis_pri_key, _expire_in)
                return False
            else:
                # 缓存中不存在数据 且数据只存在于缓存中
                if _o_type == ObjectType.REDIS:
                    await redis_client.hset(_redis_pri_key, mapping=self.to_dict(fields=None, save_all=True))
                    return True

        if _o_type == ObjectType.MONGO or _o_type == ObjectType.BOTH:
            if not _out:
                _mongo_client = MongoManager.get_mongodb(svr_name=db_source)
                _db = _mongo_client[db_name]
                _table_name = getattr(self, __KEY_TABLE_NAME_KEY__)
                _table = _db[_table_name]
                _filter = self._get_mongo_pri_key()
                _doc = await _table.find_one(_filter)
                if not _doc:
                    # db中数据不存在
                    _data_update = self.to_dict(fields=None, save_all=True)
                    _filter.update(_data_update)
                    await _table.insert_one(_filter)

                    if _o_type == ObjectType.BOTH:
                        await redis_client.hset(_redis_pri_key, mapping=_data_update)

                    return True
                else:
                    # db中数据存在
                    # mongo自己生成的默认ID忽略掉
                    _doc.pop('_id')
                    self.from_dict(_doc)
                    if _o_type == ObjectType.BOTH:
                        await redis_client.hset(_redis_pri_key, mapping=_doc)

        return False

    """
    留一个函数，供业务测从数据层加载完成之后再做一些进一步的初始化工作
    """
    async def init_after_load(self, prefix=None, db_source=KEY_MONGODB_DEFAULT_KEY, db_name=KEY_MONGODB_DEFAULT_DB,
                        redis_server_name=KEY_REDIS_DEFAULT_KEY):
        pass

    def from_dict(self, data):
        if isinstance(data, dict):
            _orm = getattr(self, __KEY_ORM__)
            for _k, _f in _orm.items():
                if _f.primary_key:
                    continue
                if _k not in data:
                    continue
                if _f.type == FieldType.LIST or _f.type == FieldType.DICT:
                    self[__KEY_VALUES__][_k] = json.loads(data[_k])
                elif _f.type == FieldType.SET:
                    self[__KEY_VALUES__][_k] = set(json.loads(data[_k]))
                elif _f.type == FieldType.DATETIME:
                    self[__KEY_VALUES__][_k] = str_2_datetime(data[_k], _in_fmt=_f.fmt)
                elif _f.type == FieldType.OBJECT:
                    _j = json.loads(data[_k])
                    self[__KEY_VALUES__][_k].from_dict(_j)
                elif _f.type == FieldType.INT:
                    self[__KEY_VALUES__][_k] = int(data[_k])
                elif _f.type == FieldType.FLOAT:
                    self[__KEY_VALUES__][_k] = float(data[_k])
                else:
                    self[__KEY_VALUES__][_k] = data[_k]


if __name__ == "__main__":
    pass
