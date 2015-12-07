# -*- coding: utf-8 -*-
try:
    import json
except ImportError:
    import simplejson as json
import re
import sys
import traceback

from django.conf import settings
from django.conf.urls import url, patterns, include

from django.http import HttpResponse, Http404
from django.test import Client

from tastypie.api import Api, NamespacedApi
from tastypie.exceptions import NotRegistered, BadRequest
from tastypie.utils import trailing_slash, is_valid_jsonp_callback_value
from tastypie.utils.mime import determine_format, build_content_type

from .settings import BATCH_API_MAX_REQUESTS


class BatchEndpointMixin(object):
    """
    Adds the batch endpoint to an api.
    """
    def __init__(self, *args, **kwargs):
        self.prefix = kwargs.get('prefix', r'^/api')
        return super(BatchEndpointMixin, self).__init__(*args, **kwargs)

    @property
    def client(self):
        """
        Django test client instance
        """
        if not hasattr(self, '_client'):
            setattr(self, '_client', Client())
        return self._client

    def prepend_urls(self):
        """
        add batch urls.
        """
        urlpatterns = super(BatchEndpointMixin, self).prepend_urls()
        urlpatterns += patterns('',
            url(r"^(?P<api_name>%s)/batch%s$" % (
                self.api_name,
                trailing_slash()
            ), self.wrap_view('batch'), name="api_%s_batch" % self.api_name)
        )
        # assert False, urlpatterns
        return urlpatterns

    def batch(self, request, api_name=None):
        """
        Make batch requests to the api.
        """
        # assert False, request
        if not request.method.lower() == 'post':
            raise Http404
        if api_name is None:
            api_name = self.api_name


        desired_format = determine_format(request, self.serializer)

        try:
            batch_requests = self.serializer.deserialize(
                request.body, desired_format)[:BATCH_API_MAX_REQUESTS]
        except ValueError:
            raise BadRequest('Bad data.')
        if not isinstance(batch_requests, list):
            raise BadRequest('Bad structure.')
        responses = []
        if not request.session.exists(request.session.session_key):
            request.session.create()
        # assert False, request.session.session_key
        self.client.cookies[settings.SESSION_COOKIE_NAME] = \
            request.session.session_key
        for req in batch_requests:
            path = req.get('path')
            params = {}
            params.update(req.get('params', {}))
            response_obj = {
                'path': path,
                'params': params,
            }
            valid_path = re.search(self.prefix, path)
            if valid_path:
                try:
                    response = self.client.get(req.get('path'), params)
                    # assert False, dir(response)
                    response_obj['status'] = response.status_code
                    response_obj['body'] = response.content
                    response_obj['headers'] = response._headers
                    response_obj['cookies'] = response.cookies
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    response_obj['error'] = {
                        'exc_type': exc_type,
                        'exc_value': exc_value
                    }
                    if settings.DEBUG:
                        response_obj['exc_traceback'] = traceback.format_exc(
                            exc_traceback)
            else:
                # response_obj['status'] = 404
                response_obj['error'] = 'Unknown resource uri.',
            responses.append(response_obj)


        options = {}

        if 'text/javascript' in desired_format:
            callback = request.GET.get('callback', 'callback')

            if not is_valid_jsonp_callback_value(callback):
                raise BadRequest('JSONP callback name is invalid.')

            options['callback'] = callback

        serialized = self.serializer.serialize(
            responses, desired_format, options)
        return HttpResponse(
            content=serialized, content_type=build_content_type(
                desired_format))


class BatchApi(BatchEndpointMixin, Api):
    """
    Override the default tastypie Api
    """


class NamespacedBatchApi(NamespacedApi, BatchEndpointMixin):
    """
    Override the default tastypie NamespacedApi
    """
