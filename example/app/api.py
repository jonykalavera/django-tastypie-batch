# -*- coding: utf-8 -*-
from tastypie.bundle import Bundle
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import Resource


# We need a generic object to shove data in/get data from.
# Riak generally just tosses around dictionaries, so we'll lightly
# wrap that.
class DataObject(object):
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data


class DataResource(Resource):
    data = [
        {
            'id': 1,
            'name': 'hello'
            
        },
        {
            'id': 2,
            'name': 'world'
            
        }
    ]

    id = fields.IntegerField(attribute='id')
    name = fields.CharField(attribute='name')

    class Meta:
        object_class = DataObject
        authorization = Authorization()

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id

        return kwargs

    def get_object_list(self, request):
        results = [DataObject(x) for x in self.data]
        return results

    def obj_get_list(self, bundle, **kwargs):
        # Filtering disabled for brevity...
        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        try:
            obj = [x for x in self.data if x.id == kwargs['pk']][0]
        except IndexError:
            obj = None
        return DataObject(initial=obj)

    def obj_create(self, bundle, **kwargs):
        bundle.obj = DataObject(initial=kwargs)
        bundle = self.full_hydrate(bundle)
        self.data.append(bundle.obj)
        return bundle

    def obj_update(self, bundle, **kwargs):
        return self.obj_create(bundle, **kwargs)

    def obj_delete_list(self, bundle, **kwargs):
        for key in self.get_keys():
            self.data = [x for x in self.data if x.get('pk') != key]


    def obj_delete(self, bundle, **kwargs):
        self.data = [x for x in self.data if x.get('pk') != kwargs['pk']]

    def rollback(self, bundles):
        pass


class FooResource(DataResource):

    class Meta:
        resource_name = 'foo'

class BarResource(DataResource):

    class Meta:
        resource_name = 'bar'
