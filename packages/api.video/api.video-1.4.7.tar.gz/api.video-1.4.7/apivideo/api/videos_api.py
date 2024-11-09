"""
    api.video

    api.video is an API that encodes on the go to facilitate immediate playback, enhancing viewer streaming experiences across multiple devices and platforms. You can stream live or on-demand online videos within minutes.  # noqa: E501

    Contact: ecosystem@api.video
"""

import os  # noqa: F401
import re  # noqa: F401
import sys  # noqa: F401
from types import MethodType
from types import FunctionType

from apivideo.api_client import ApiClient
from apivideo.endpoint import EndPoint as _EndPoint, ChunkIO
from apivideo.model.video_id import VideoId
from apivideo.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from apivideo.exceptions import ApiTypeError, ApiValueError
from apivideo.model.bad_request import BadRequest
from apivideo.model.conflict_error import ConflictError
from apivideo.model.discarded_video_update_payload import DiscardedVideoUpdatePayload
from apivideo.model.not_found import NotFound
from apivideo.model.too_many_requests import TooManyRequests
from apivideo.model.video import Video
from apivideo.model.video_creation_payload import VideoCreationPayload
from apivideo.model.video_status import VideoStatus
from apivideo.model.video_thumbnail_pick_payload import VideoThumbnailPickPayload
from apivideo.model.video_update_payload import VideoUpdatePayload
from apivideo.model.videos_list_response import VideosListResponse


class VideosApi(_EndPoint):

    def create(
            self,
            video_creation_payload,
            **kwargs
        ):
            """Create a video object  # noqa: E501

            Creates a video object. More information on video objects can be found [here](https://docs.api.video/reference/api/Videos).   # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.create(video_creation_payload, async_req=True)
            >>> result = thread.get()

            Args:
                video_creation_payload (VideoCreationPayload): video to create

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                async_req (bool): execute request asynchronously

            Returns:
                Video
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['video_creation_payload'] = \
                video_creation_payload

            params_map = {
                'all': [
                    'video_creation_payload',
                    'async_req',
                    '_preload_content',
                    '_request_timeout',
                    '_return_http_data_only'
                ],
                'required': [
                    'video_creation_payload',
                ],
                'nullable': [
                    '_request_timeout'
                ],
                'enum': [
                ],
                'validation': [
                ]
            }
            validations = {
            }
            allowed_values = {
            }
            openapi_types = {
                'video_creation_payload':
                    (VideoCreationPayload,),
                'async_req': (bool,),
                '_preload_content': (bool,),
                '_request_timeout': (none_type, int, (int,), [int]),
                '_return_http_data_only': (bool,)
            }
            attribute_map = {
            }
            location_map = {
                'video_creation_payload': 'body',
            }
            collection_format_map = {
            }

            for key, value in kwargs.items():
                if key not in params_map['all']:
                    raise ApiTypeError(
                        "Got an unexpected parameter '%s'"
                        " to method `create`" %
                        (key, )
                    )
                if (key not in params_map['nullable'] and value is None):
                    raise ApiValueError(
                        "Value may not be None for non-nullable parameter `%s`"
                        " when calling `create`" %
                        (key, )
                    )

            for key in params_map['required']:
                if key not in kwargs.keys():
                    raise ApiValueError(
                        "Missing the required parameter `%s` when calling "
                        "`create`" % (key, )
                    )

            self._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
            params = self._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)
            return self.api_client.call_api(
                "/videos",
                "POST",
                params['path'],
                params['query'],
                params['header'],
                body=params['body'],
                post_params=params['form'],
                files=params['file'],
                response_type=(Video,),
                async_req=kwargs['async_req'],
                _return_http_data_only=kwargs['_return_http_data_only'],
                _preload_content=kwargs['_preload_content'],
                _request_timeout=kwargs['_request_timeout'],
                collection_formats=params['collection_format'])

    def upload(
            self,
            video_id,
            file,
            **kwargs
        ):
            """Upload a video  # noqa: E501

            To upload a video to the videoId you created. You can only upload your video to the videoId once.



We offer 2 types of upload: 

* Regular upload 

* Progressive upload

The latter allows you to split a video source into X chunks and send those chunks independently (concurrently or sequentially). The 2 main goals for our users are to

  * allow the upload of video sources > 200 MiB (200 MiB = the max. allowed file size for regular upload)

  * allow to send a video source "progressively", i.e., before before knowing the total size of the video.

  Once all chunks have been sent, they are reaggregated to one source file. The video source is considered as "completely sent" when the "last" chunk is sent (i.e., the chunk that "completes" the upload).

  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.upload(video_id, file, async_req=True)
            >>> result = thread.get()

            Args:
                video_id (str): Enter the videoId you want to use to upload your video.
                file (file_type): The path to the video you would like to upload. The path must be local. If you want to use a video from an online source, you must use the \\\"/videos\\\" endpoint and add the \\\"source\\\" parameter when you create a new video.

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _progress_listener (method): method called each time a chunk is uploaded. Takes 2 parameters:
                    the first one is the number of bytes uploaded, the second one is the total number of bytes.
                    Default is None.
                async_req (bool): execute request asynchronously

            Returns:
                Video
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['video_id'] = \
                video_id
            kwargs['file'] = \
                file

            params_map = {
                'all': [
                    'video_id',
                    'file',
                    'async_req',
                    '_preload_content',
                    '_request_timeout',
                    '_return_http_data_only',
                    '_progress_listener',
                ],
                'required': [
                    'video_id',
                    'file',
                ],
                'nullable': [
                    '_request_timeout'
                ],
                'enum': [
                ],
                'validation': [
                ]
            }
            validations = {
            }
            allowed_values = {
            }
            openapi_types = {
                'video_id':
                    (str,),
                'file':
                    (file_type,),
                'async_req': (bool,),
                '_preload_content': (bool,),
                '_request_timeout': (none_type, int, (int,), [int]),
                '_return_http_data_only': (bool,),
                '_progress_listener': (none_type, MethodType, FunctionType),
            }
            attribute_map = {
                'video_id': 'videoId',
                'file': 'file',
            }
            location_map = {
                'video_id': 'path',
                'file': 'form',
            }
            collection_format_map = {
            }

            for key, value in kwargs.items():
                if key not in params_map['all']:
                    raise ApiTypeError(
                        "Got an unexpected parameter '%s'"
                        " to method `upload`" %
                        (key, )
                    )
                if (key not in params_map['nullable'] and value is None):
                    raise ApiValueError(
                        "Value may not be None for non-nullable parameter `%s`"
                        " when calling `upload`" %
                        (key, )
                    )

            for key in params_map['required']:
                if key not in kwargs.keys():
                    raise ApiValueError(
                        "Missing the required parameter `%s` when calling "
                        "`upload`" % (key, )
                    )

            self._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
            params = self._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)
            res = None
            progress_listener = kwargs.get('_progress_listener', None)
            for content_range, chunk, isLast, offset, file_size in self._chunk_file(params['file']):
                if progress_listener is not None:
                    progress_listener(offset, file_size)
                res = self.api_client.call_api(
                    "/videos/{videoId}/source",
                    "POST",
                    params['path'],
                    params['query'],
                    {**params['header'], 'Content-Range': content_range},
                    body=params['body'],
                    post_params=params['form'],
                    files=chunk,
                    response_type=(Video,) if isLast else None,
                    async_req=kwargs['async_req'],
                    _return_http_data_only=kwargs['_return_http_data_only'],
                    _preload_content=kwargs['_preload_content'],
                    _request_timeout=kwargs['_request_timeout'],
                    collection_formats=params['collection_format'])
            return res  # return the last response


    def create_upload_progressive_session(self, video_id):
        class ProgressiveSession:
            current_part = 1
            parent = None
            video_id = None

            def __init__(self, parent, video_id):
                self.video_id = video_id
                self.parent = parent

            def uploadPart(self, file):
                return self.__upload(file, False)

            def uploadLastPart(self, file):
                return self.__upload(file, True)

            def __upload(self, file, is_last):
                kwargs = {}
                file.seek(0, 2)
                file_size = file.tell()
                file.seek(0, 0)
                kwargs['async_req'] = kwargs.get(
                    'async_req', False
                )
                kwargs['_return_http_data_only'] = kwargs.get(
                    '_return_http_data_only', True
                )
                kwargs['_preload_content'] = kwargs.get(
                    '_preload_content', True
                )
                kwargs['_request_timeout'] = kwargs.get(
                    '_request_timeout', None
                )

    
                kwargs['video_id'] = \
                    self.video_id
    
                kwargs['file'] = \
                    file

                params_map = {
                    'all': [
                        'video_id',
                            'file',
                            'async_req',
                        '_preload_content',
                        '_request_timeout',
                        '_return_http_data_only',
                        '_progress_listener',
                    ],
                    'required': [
                        'video_id',
                        'file',
                    ],
                    'nullable': [
                        '_request_timeout'
                    ],
                    'enum': [
                    ],
                    'validation': [
                    ]
                }
                validations = {
                }
                allowed_values = {
                }
                openapi_types = {
                    'video_id':
                        (str,),
                        'file':
                        (file_type,),
                        'async_req': (bool,),
                    '_preload_content': (bool,),
                    '_request_timeout': (none_type, int, (int,), [int]),
                    '_return_http_data_only': (bool,),
                    '_progress_listener': (none_type, MethodType, FunctionType),
                }
                attribute_map = {
                    'video_id': 'videoId',
                        'file': 'file',
                    }
                location_map = {
                    'video_id': 'path',
                        'file': 'form',
                    }
                collection_format_map = {
                }

                for key, value in kwargs.items():
                    if key not in params_map['all']:
                        raise ApiTypeError(
                            "Got an unexpected parameter '%s'"
                            " to method `upload`" %
                            (key, )
                        )
                    if (key not in params_map['nullable'] and value is None):
                        raise ApiValueError(
                            "Value may not be None for non-nullable parameter `%s`"
                            " when calling `upload`" %
                            (key, )
                        )

                for key in params_map['required']:
                    if key not in kwargs.keys():
                        raise ApiValueError(
                            "Missing the required parameter `%s` when calling "
                            "`upload`" % (key, )
                        )

                self.parent._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
                params = self.parent._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)

                part = self.current_part
                self.current_part = self.current_part + 1

                res = self.parent.api_client.call_api(
                    "/videos/{videoId}/source",
                    "POST",
                    params['path'],
                    params['query'],
                    {**params['header'], 'Content-Range': "part " + str(part) + "/" + ("*" if not is_last else str(part))},
                    body=params['body'],
                    post_params=params['form'],
                    files={"file": [ChunkIO(file.read(), file.name)]},
                    response_type=(Video,) if is_last else (VideoId,),
                    async_req=kwargs['async_req'],
                    _return_http_data_only=kwargs['_return_http_data_only'],
                    _preload_content=kwargs['_preload_content'],
                    _request_timeout=kwargs['_request_timeout'],
                    collection_formats=params['collection_format'])
                return res

        return ProgressiveSession(self, video_id)

    def upload_with_upload_token(
            self,
            token,
            file,
            **kwargs
        ):
            """Upload with an delegated upload token  # noqa: E501

            This method allows you to send a video using an upload token. Upload tokens are especially useful when the upload is done from the client side. If you want to upload a video from your server-side application, you'd better use the [standard upload method](#upload).  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.upload_with_upload_token(token, file, async_req=True)
            >>> result = thread.get()

            Args:
                token (str): The unique identifier for the token you want to use to upload a video.
                file (file_type): The path to the video you want to upload.

            Keyword Args:
                video_id (str): The video id returned by the first call to this endpoint in a large video upload scenario.. [optional]
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _progress_listener (method): method called each time a chunk is uploaded. Takes 2 parameters:
                    the first one is the number of bytes uploaded, the second one is the total number of bytes.
                    Default is None.
                async_req (bool): execute request asynchronously

            Returns:
                Video
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['token'] = \
                token
            kwargs['file'] = \
                file

            params_map = {
                'all': [
                    'token',
                    'file',
                    'async_req',
                    '_preload_content',
                    '_request_timeout',
                    '_return_http_data_only',
                    '_progress_listener',
                ],
                'required': [
                    'token',
                    'file',
                ],
                'nullable': [
                    '_request_timeout'
                ],
                'enum': [
                ],
                'validation': [
                ]
            }
            validations = {
            }
            allowed_values = {
            }
            openapi_types = {
                'token':
                    (str,),
                'file':
                    (file_type,),
                'async_req': (bool,),
                '_preload_content': (bool,),
                '_request_timeout': (none_type, int, (int,), [int]),
                '_return_http_data_only': (bool,),
                '_progress_listener': (none_type, MethodType, FunctionType),
            }
            attribute_map = {
                'token': 'token',
                'file': 'file',
            }
            location_map = {
                'token': 'query',
                'file': 'form',
            }
            collection_format_map = {
            }

            for key, value in kwargs.items():
                if key not in params_map['all']:
                    raise ApiTypeError(
                        "Got an unexpected parameter '%s'"
                        " to method `upload_with_upload_token`" %
                        (key, )
                    )
                if (key not in params_map['nullable'] and value is None):
                    raise ApiValueError(
                        "Value may not be None for non-nullable parameter `%s`"
                        " when calling `upload_with_upload_token`" %
                        (key, )
                    )

            for key in params_map['required']:
                if key not in kwargs.keys():
                    raise ApiValueError(
                        "Missing the required parameter `%s` when calling "
                        "`upload_with_upload_token`" % (key, )
                    )

            self._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
            params = self._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)
            res = None
            progress_listener = kwargs.get('_progress_listener', None)
            for content_range, chunk, isLast, offset, file_size in self._chunk_file(params['file']):
                if progress_listener is not None:
                    progress_listener(offset, file_size)
                res = self.api_client.call_api(
                    "/upload",
                    "POST",
                    params['path'],
                    params['query'],
                    {**params['header'], 'Content-Range': content_range},
                    body=params['body'],
                    post_params=params['form'],
                    files=chunk,
                    response_type=(Video,) if isLast else None,
                    async_req=kwargs['async_req'],
                    _return_http_data_only=kwargs['_return_http_data_only'],
                    _preload_content=kwargs['_preload_content'],
                    _request_timeout=kwargs['_request_timeout'],
                    collection_formats=params['collection_format'])
            return res  # return the last response


    def create_upload_with_upload_token_progressive_session(self, token, video_id=None):
        class ProgressiveSession:
            current_part = 1
            parent = None
            token = None
            video_id = None

            def __init__(self, parent, token, video_id=None):
                self.token = token
                self.video_id = video_id
                self.parent = parent

            def uploadPart(self, file):
                return self.__upload(file, False)

            def uploadLastPart(self, file):
                return self.__upload(file, True)

            def __upload(self, file, is_last):
                kwargs = {}
                file.seek(0, 2)
                file_size = file.tell()
                file.seek(0, 0)
                kwargs['async_req'] = kwargs.get(
                    'async_req', False
                )
                kwargs['_return_http_data_only'] = kwargs.get(
                    '_return_http_data_only', True
                )
                kwargs['_preload_content'] = kwargs.get(
                    '_preload_content', True
                )
                kwargs['_request_timeout'] = kwargs.get(
                    '_request_timeout', None
                )
                if self.video_id:
                    kwargs['video_id'] = \
                        self.video_id

    
                kwargs['token'] = \
                    self.token
    
                kwargs['file'] = \
                    file

                params_map = {
                    'all': [
                        'token',
                            'file',
    
                        'video_id',
                        'async_req',
                        '_preload_content',
                        '_request_timeout',
                        '_return_http_data_only',
                        '_progress_listener',
                    ],
                    'required': [
                        'token',
                        'file',
                    ],
                    'nullable': [
                        '_request_timeout'
                    ],
                    'enum': [
                    ],
                    'validation': [
                    ]
                }
                validations = {
                }
                allowed_values = {
                }
                openapi_types = {
                    'token':
                        (str,),
                        'file':
                        (file_type,),
    
                    'video_id':
                        (str,),
                    'async_req': (bool,),
                    '_preload_content': (bool,),
                    '_request_timeout': (none_type, int, (int,), [int]),
                    '_return_http_data_only': (bool,),
                    '_progress_listener': (none_type, MethodType, FunctionType),
                }
                attribute_map = {
                    'token': 'token',
                        'file': 'file',
    
                    'video_id': 'videoId',
                }
                location_map = {
                    'token': 'query',
                        'file': 'form',
    
                    'video_id': 'form',
                }
                collection_format_map = {
                }

                for key, value in kwargs.items():
                    if key not in params_map['all']:
                        raise ApiTypeError(
                            "Got an unexpected parameter '%s'"
                            " to method `upload_with_upload_token`" %
                            (key, )
                        )
                    if (key not in params_map['nullable'] and value is None):
                        raise ApiValueError(
                            "Value may not be None for non-nullable parameter `%s`"
                            " when calling `upload_with_upload_token`" %
                            (key, )
                        )

                for key in params_map['required']:
                    if key not in kwargs.keys():
                        raise ApiValueError(
                            "Missing the required parameter `%s` when calling "
                            "`upload_with_upload_token`" % (key, )
                        )

                self.parent._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
                params = self.parent._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)

                part = self.current_part
                self.current_part = self.current_part + 1

                res = self.parent.api_client.call_api(
                    "/upload",
                    "POST",
                    params['path'],
                    params['query'],
                    {**params['header'], 'Content-Range': "part " + str(part) + "/" + ("*" if not is_last else str(part))},
                    body=params['body'],
                    post_params=params['form'],
                    files={"file": [ChunkIO(file.read(), file.name)]},
                    response_type=(Video,) if is_last else (VideoId,),
                    async_req=kwargs['async_req'],
                    _return_http_data_only=kwargs['_return_http_data_only'],
                    _preload_content=kwargs['_preload_content'],
                    _request_timeout=kwargs['_request_timeout'],
                    collection_formats=params['collection_format'])

                if res.video_id is not None:
                    self.video_id = res.video_id

                return res

        return ProgressiveSession(self, token, video_id)

    def get(
            self,
            video_id,
            **kwargs
        ):
            """Retrieve a video object  # noqa: E501

            This call provides the same information provided on video creation. For private videos, it will generate a unique token url. Use this to retrieve any details you need about a video, or set up a private viewing URL.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get(video_id, async_req=True)
            >>> result = thread.get()

            Args:
                video_id (str): The unique identifier for the video you want details about.

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                async_req (bool): execute request asynchronously

            Returns:
                Video
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['video_id'] = \
                video_id

            params_map = {
                'all': [
                    'video_id',
                    'async_req',
                    '_preload_content',
                    '_request_timeout',
                    '_return_http_data_only'
                ],
                'required': [
                    'video_id',
                ],
                'nullable': [
                    '_request_timeout'
                ],
                'enum': [
                ],
                'validation': [
                ]
            }
            validations = {
            }
            allowed_values = {
            }
            openapi_types = {
                'video_id':
                    (str,),
                'async_req': (bool,),
                '_preload_content': (bool,),
                '_request_timeout': (none_type, int, (int,), [int]),
                '_return_http_data_only': (bool,)
            }
            attribute_map = {
                'video_id': 'videoId',
            }
            location_map = {
                'video_id': 'path',
            }
            collection_format_map = {
            }

            for key, value in kwargs.items():
                if key not in params_map['all']:
                    raise ApiTypeError(
                        "Got an unexpected parameter '%s'"
                        " to method `get`" %
                        (key, )
                    )
                if (key not in params_map['nullable'] and value is None):
                    raise ApiValueError(
                        "Value may not be None for non-nullable parameter `%s`"
                        " when calling `get`" %
                        (key, )
                    )

            for key in params_map['required']:
                if key not in kwargs.keys():
                    raise ApiValueError(
                        "Missing the required parameter `%s` when calling "
                        "`get`" % (key, )
                    )

            self._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
            params = self._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)
            return self.api_client.call_api(
                "/videos/{videoId}",
                "GET",
                params['path'],
                params['query'],
                params['header'],
                body=params['body'],
                post_params=params['form'],
                files=params['file'],
                response_type=(Video,),
                async_req=kwargs['async_req'],
                _return_http_data_only=kwargs['_return_http_data_only'],
                _preload_content=kwargs['_preload_content'],
                _request_timeout=kwargs['_request_timeout'],
                collection_formats=params['collection_format'])

    def update(
            self,
            video_id,
            video_update_payload,
            **kwargs
        ):
            """Update a video object  # noqa: E501

            Updates the parameters associated with a video ID. The video object you are updating is determined by the video ID you provide. 



NOTE: If you are updating an array, you must provide the entire array as what you provide here overwrites what is in the system rather than appending to it.

  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.update(video_id, video_update_payload, async_req=True)
            >>> result = thread.get()

            Args:
                video_id (str): The video ID for the video you want to update.
                video_update_payload (VideoUpdatePayload):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                async_req (bool): execute request asynchronously

            Returns:
                Video
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['video_id'] = \
                video_id
            kwargs['video_update_payload'] = \
                video_update_payload

            params_map = {
                'all': [
                    'video_id',
                    'video_update_payload',
                    'async_req',
                    '_preload_content',
                    '_request_timeout',
                    '_return_http_data_only'
                ],
                'required': [
                    'video_id',
                    'video_update_payload',
                ],
                'nullable': [
                    '_request_timeout'
                ],
                'enum': [
                ],
                'validation': [
                ]
            }
            validations = {
            }
            allowed_values = {
            }
            openapi_types = {
                'video_id':
                    (str,),
                'video_update_payload':
                    (VideoUpdatePayload,),
                'async_req': (bool,),
                '_preload_content': (bool,),
                '_request_timeout': (none_type, int, (int,), [int]),
                '_return_http_data_only': (bool,)
            }
            attribute_map = {
                'video_id': 'videoId',
            }
            location_map = {
                'video_id': 'path',
                'video_update_payload': 'body',
            }
            collection_format_map = {
            }

            for key, value in kwargs.items():
                if key not in params_map['all']:
                    raise ApiTypeError(
                        "Got an unexpected parameter '%s'"
                        " to method `update`" %
                        (key, )
                    )
                if (key not in params_map['nullable'] and value is None):
                    raise ApiValueError(
                        "Value may not be None for non-nullable parameter `%s`"
                        " when calling `update`" %
                        (key, )
                    )

            for key in params_map['required']:
                if key not in kwargs.keys():
                    raise ApiValueError(
                        "Missing the required parameter `%s` when calling "
                        "`update`" % (key, )
                    )

            self._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
            params = self._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)
            return self.api_client.call_api(
                "/videos/{videoId}",
                "PATCH",
                params['path'],
                params['query'],
                params['header'],
                body=params['body'],
                post_params=params['form'],
                files=params['file'],
                response_type=(Video,),
                async_req=kwargs['async_req'],
                _return_http_data_only=kwargs['_return_http_data_only'],
                _preload_content=kwargs['_preload_content'],
                _request_timeout=kwargs['_request_timeout'],
                collection_formats=params['collection_format'])

    def delete(
            self,
            video_id,
            **kwargs
        ):
            """Delete a video object  # noqa: E501

            If you do not need a video any longer, you can send a request to delete it. All you need is the videoId. By default, deleted videos cannot be recovered. If you have the Video Restore feature enabled, this operation will discard the video instead of permanently deleting it. Make sure you subscribe to the Video Restore feature if you want to be able to restore deleted videos! The Video Restore feature retains videos for 90 days, after which the videos are permanently deleted  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.delete(video_id, async_req=True)
            >>> result = thread.get()

            Args:
                video_id (str): The video ID for the video you want to delete.

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                async_req (bool): execute request asynchronously

            Returns:
                None
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['video_id'] = \
                video_id

            params_map = {
                'all': [
                    'video_id',
                    'async_req',
                    '_preload_content',
                    '_request_timeout',
                    '_return_http_data_only'
                ],
                'required': [
                    'video_id',
                ],
                'nullable': [
                    '_request_timeout'
                ],
                'enum': [
                ],
                'validation': [
                ]
            }
            validations = {
            }
            allowed_values = {
            }
            openapi_types = {
                'video_id':
                    (str,),
                'async_req': (bool,),
                '_preload_content': (bool,),
                '_request_timeout': (none_type, int, (int,), [int]),
                '_return_http_data_only': (bool,)
            }
            attribute_map = {
                'video_id': 'videoId',
            }
            location_map = {
                'video_id': 'path',
            }
            collection_format_map = {
            }

            for key, value in kwargs.items():
                if key not in params_map['all']:
                    raise ApiTypeError(
                        "Got an unexpected parameter '%s'"
                        " to method `delete`" %
                        (key, )
                    )
                if (key not in params_map['nullable'] and value is None):
                    raise ApiValueError(
                        "Value may not be None for non-nullable parameter `%s`"
                        " when calling `delete`" %
                        (key, )
                    )

            for key in params_map['required']:
                if key not in kwargs.keys():
                    raise ApiValueError(
                        "Missing the required parameter `%s` when calling "
                        "`delete`" % (key, )
                    )

            self._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
            params = self._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)
            return self.api_client.call_api(
                "/videos/{videoId}",
                "DELETE",
                params['path'],
                params['query'],
                params['header'],
                body=params['body'],
                post_params=params['form'],
                files=params['file'],
                response_type=None,
                async_req=kwargs['async_req'],
                _return_http_data_only=kwargs['_return_http_data_only'],
                _preload_content=kwargs['_preload_content'],
                _request_timeout=kwargs['_request_timeout'],
                collection_formats=params['collection_format'])

    def list(
            self,
            **kwargs
        ):
            """List all video objects  # noqa: E501

            This method returns a list of your videos (with all their details). With no parameters added, the API returns the first page of all videos. You can filter videos using the parameters described below.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.list(async_req=True)
            >>> result = thread.get()


            Keyword Args:
                title (str): The title of a specific video you want to find. The search will match exactly to what term you provide and return any videos that contain the same term as part of their titles.. [optional]
                tags ([str]): A tag is a category you create and apply to videos. You can search for videos with particular tags by listing one or more here. Only videos that have all the tags you list will be returned.. [optional]
                metadata ({str: (str,)}): Videos can be tagged with metadata tags in key:value pairs. You can search for videos with specific key value pairs using this parameter.. [optional]
                description (str): Retrieve video objects by `description`.. [optional]
                live_stream_id (str): Retrieve video objects that were recorded from a live stream by `liveStreamId`.. [optional]
                sort_by (str): Use this parameter to sort videos by the their created time, published time, updated time, or by title.. [optional]
                sort_order (str): Use this parameter to sort results. `asc` is ascending and sorts from A to Z. `desc` is descending and sorts from Z to A.. [optional]
                current_page (int): Choose the number of search results to return per page. Minimum value: 1. [optional] if omitted the server will use the default value of 1
                page_size (int): Results per page. Allowed values 1-100, default is 25.. [optional] if omitted the server will use the default value of 25
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                async_req (bool): execute request asynchronously

            Returns:
                VideosListResponse
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )

            params_map = {
                'all': [
                    'title',
                    'tags',
                    'metadata',
                    'description',
                    'live_stream_id',
                    'sort_by',
                    'sort_order',
                    'current_page',
                    'page_size',
                    'async_req',
                    '_preload_content',
                    '_request_timeout',
                    '_return_http_data_only'
                ],
                'required': [],
                'nullable': [
                    '_request_timeout'
                ],
                'enum': [
                    'sort_by',
                    'sort_order',
                ],
                'validation': [
                ]
            }
            validations = {
            }
            allowed_values = {
                ('sort_by',): {

                    "TITLE": "title",
                    "CREATEDAT": "createdAt",
                    "PUBLISHEDAT": "publishedAt",
                    "UPDATEDAT": "updatedAt"
                },
                ('sort_order',): {

                    "ASC": "asc",
                    "DESC": "desc"
                },
            }
            openapi_types = {
                'title':
                    (str,),
                'tags':
                    ([str],),
                'metadata':
                    ({str: (str,)},),
                'description':
                    (str,),
                'live_stream_id':
                    (str,),
                'sort_by':
                    (str,),
                'sort_order':
                    (str,),
                'current_page':
                    (int,),
                'page_size':
                    (int,),
                'async_req': (bool,),
                '_preload_content': (bool,),
                '_request_timeout': (none_type, int, (int,), [int]),
                '_return_http_data_only': (bool,)
            }
            attribute_map = {
                'title': 'title',
                'tags': 'tags[]',
                'metadata': 'metadata',
                'description': 'description',
                'live_stream_id': 'liveStreamId',
                'sort_by': 'sortBy',
                'sort_order': 'sortOrder',
                'current_page': 'currentPage',
                'page_size': 'pageSize',
            }
            location_map = {
                'title': 'query',
                'tags': 'query',
                'metadata': 'query',
                'description': 'query',
                'live_stream_id': 'query',
                'sort_by': 'query',
                'sort_order': 'query',
                'current_page': 'query',
                'page_size': 'query',
            }
            collection_format_map = {
                'tags': 'multi',
                'metadata': 'deepObject',
            }

            for key, value in kwargs.items():
                if key not in params_map['all']:
                    raise ApiTypeError(
                        "Got an unexpected parameter '%s'"
                        " to method `list`" %
                        (key, )
                    )
                if (key not in params_map['nullable'] and value is None):
                    raise ApiValueError(
                        "Value may not be None for non-nullable parameter `%s`"
                        " when calling `list`" %
                        (key, )
                    )

            for key in params_map['required']:
                if key not in kwargs.keys():
                    raise ApiValueError(
                        "Missing the required parameter `%s` when calling "
                        "`list`" % (key, )
                    )

            self._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
            params = self._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)
            return self.api_client.call_api(
                "/videos",
                "GET",
                params['path'],
                params['query'],
                params['header'],
                body=params['body'],
                post_params=params['form'],
                files=params['file'],
                response_type=(VideosListResponse,),
                async_req=kwargs['async_req'],
                _return_http_data_only=kwargs['_return_http_data_only'],
                _preload_content=kwargs['_preload_content'],
                _request_timeout=kwargs['_request_timeout'],
                collection_formats=params['collection_format'])

    def upload_thumbnail(
            self,
            video_id,
            file,
            **kwargs
        ):
            """Upload a thumbnail  # noqa: E501

            The thumbnail is the poster that appears in the player window before video playback begins.



This endpoint allows you to upload an image for the thumbnail.



To select a still frame from the video using a time stamp, use the [dedicated method](#pickThumbnail) to pick a time in the video.



Note: There may be a short delay before the new thumbnail is delivered to our CDN.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.upload_thumbnail(video_id, file, async_req=True)
            >>> result = thread.get()

            Args:
                video_id (str): Unique identifier of the chosen video 
                file (file_type): The image to be added as a thumbnail. The mime type should be image/jpeg, image/png or image/webp. The max allowed size is 8 MiB.

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                async_req (bool): execute request asynchronously

            Returns:
                Video
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['video_id'] = \
                video_id
            kwargs['file'] = \
                file

            params_map = {
                'all': [
                    'video_id',
                    'file',
                    'async_req',
                    '_preload_content',
                    '_request_timeout',
                    '_return_http_data_only'
                ],
                'required': [
                    'video_id',
                    'file',
                ],
                'nullable': [
                    '_request_timeout'
                ],
                'enum': [
                ],
                'validation': [
                ]
            }
            validations = {
            }
            allowed_values = {
            }
            openapi_types = {
                'video_id':
                    (str,),
                'file':
                    (file_type,),
                'async_req': (bool,),
                '_preload_content': (bool,),
                '_request_timeout': (none_type, int, (int,), [int]),
                '_return_http_data_only': (bool,)
            }
            attribute_map = {
                'video_id': 'videoId',
                'file': 'file',
            }
            location_map = {
                'video_id': 'path',
                'file': 'form',
            }
            collection_format_map = {
            }

            for key, value in kwargs.items():
                if key not in params_map['all']:
                    raise ApiTypeError(
                        "Got an unexpected parameter '%s'"
                        " to method `upload_thumbnail`" %
                        (key, )
                    )
                if (key not in params_map['nullable'] and value is None):
                    raise ApiValueError(
                        "Value may not be None for non-nullable parameter `%s`"
                        " when calling `upload_thumbnail`" %
                        (key, )
                    )

            for key in params_map['required']:
                if key not in kwargs.keys():
                    raise ApiValueError(
                        "Missing the required parameter `%s` when calling "
                        "`upload_thumbnail`" % (key, )
                    )

            self._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
            params = self._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)
            return self.api_client.call_api(
                "/videos/{videoId}/thumbnail",
                "POST",
                params['path'],
                params['query'],
                params['header'],
                body=params['body'],
                post_params=params['form'],
                files=params['file'],
                response_type=(Video,),
                async_req=kwargs['async_req'],
                _return_http_data_only=kwargs['_return_http_data_only'],
                _preload_content=kwargs['_preload_content'],
                _request_timeout=kwargs['_request_timeout'],
                collection_formats=params['collection_format'])

    def pick_thumbnail(
            self,
            video_id,
            video_thumbnail_pick_payload,
            **kwargs
        ):
            """Set a thumbnail  # noqa: E501

            Pick a thumbnail from the given time code. 



If you'd like to upload an image for your thumbnail, use the dedicated [method](#uploadThumbnail). 



There may be a short delay for the thumbnail to update.

  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.pick_thumbnail(video_id, video_thumbnail_pick_payload, async_req=True)
            >>> result = thread.get()

            Args:
                video_id (str): Unique identifier of the video you want to add a thumbnail to, where you use a section of your video as the thumbnail.
                video_thumbnail_pick_payload (VideoThumbnailPickPayload):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                async_req (bool): execute request asynchronously

            Returns:
                Video
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['video_id'] = \
                video_id
            kwargs['video_thumbnail_pick_payload'] = \
                video_thumbnail_pick_payload

            params_map = {
                'all': [
                    'video_id',
                    'video_thumbnail_pick_payload',
                    'async_req',
                    '_preload_content',
                    '_request_timeout',
                    '_return_http_data_only'
                ],
                'required': [
                    'video_id',
                    'video_thumbnail_pick_payload',
                ],
                'nullable': [
                    '_request_timeout'
                ],
                'enum': [
                ],
                'validation': [
                ]
            }
            validations = {
            }
            allowed_values = {
            }
            openapi_types = {
                'video_id':
                    (str,),
                'video_thumbnail_pick_payload':
                    (VideoThumbnailPickPayload,),
                'async_req': (bool,),
                '_preload_content': (bool,),
                '_request_timeout': (none_type, int, (int,), [int]),
                '_return_http_data_only': (bool,)
            }
            attribute_map = {
                'video_id': 'videoId',
            }
            location_map = {
                'video_id': 'path',
                'video_thumbnail_pick_payload': 'body',
            }
            collection_format_map = {
            }

            for key, value in kwargs.items():
                if key not in params_map['all']:
                    raise ApiTypeError(
                        "Got an unexpected parameter '%s'"
                        " to method `pick_thumbnail`" %
                        (key, )
                    )
                if (key not in params_map['nullable'] and value is None):
                    raise ApiValueError(
                        "Value may not be None for non-nullable parameter `%s`"
                        " when calling `pick_thumbnail`" %
                        (key, )
                    )

            for key in params_map['required']:
                if key not in kwargs.keys():
                    raise ApiValueError(
                        "Missing the required parameter `%s` when calling "
                        "`pick_thumbnail`" % (key, )
                    )

            self._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
            params = self._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)
            return self.api_client.call_api(
                "/videos/{videoId}/thumbnail",
                "PATCH",
                params['path'],
                params['query'],
                params['header'],
                body=params['body'],
                post_params=params['form'],
                files=params['file'],
                response_type=(Video,),
                async_req=kwargs['async_req'],
                _return_http_data_only=kwargs['_return_http_data_only'],
                _preload_content=kwargs['_preload_content'],
                _request_timeout=kwargs['_request_timeout'],
                collection_formats=params['collection_format'])

    def get_discarded(
            self,
            video_id,
            **kwargs
        ):
            """Retrieve a discarded video object  # noqa: E501

            This call provides the same information provided on video creation. For private videos, it will generate a unique token url. Use this to retrieve any details you need about a video, or set up a private viewing URL.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_discarded(video_id, async_req=True)
            >>> result = thread.get()

            Args:
                video_id (str): The unique identifier for the video you want details about.

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                async_req (bool): execute request asynchronously

            Returns:
                Video
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['video_id'] = \
                video_id

            params_map = {
                'all': [
                    'video_id',
                    'async_req',
                    '_preload_content',
                    '_request_timeout',
                    '_return_http_data_only'
                ],
                'required': [
                    'video_id',
                ],
                'nullable': [
                    '_request_timeout'
                ],
                'enum': [
                ],
                'validation': [
                ]
            }
            validations = {
            }
            allowed_values = {
            }
            openapi_types = {
                'video_id':
                    (str,),
                'async_req': (bool,),
                '_preload_content': (bool,),
                '_request_timeout': (none_type, int, (int,), [int]),
                '_return_http_data_only': (bool,)
            }
            attribute_map = {
                'video_id': 'videoId',
            }
            location_map = {
                'video_id': 'path',
            }
            collection_format_map = {
            }

            for key, value in kwargs.items():
                if key not in params_map['all']:
                    raise ApiTypeError(
                        "Got an unexpected parameter '%s'"
                        " to method `get_discarded`" %
                        (key, )
                    )
                if (key not in params_map['nullable'] and value is None):
                    raise ApiValueError(
                        "Value may not be None for non-nullable parameter `%s`"
                        " when calling `get_discarded`" %
                        (key, )
                    )

            for key in params_map['required']:
                if key not in kwargs.keys():
                    raise ApiValueError(
                        "Missing the required parameter `%s` when calling "
                        "`get_discarded`" % (key, )
                    )

            self._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
            params = self._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)
            return self.api_client.call_api(
                "/discarded/videos/{videoId}",
                "GET",
                params['path'],
                params['query'],
                params['header'],
                body=params['body'],
                post_params=params['form'],
                files=params['file'],
                response_type=(Video,),
                async_req=kwargs['async_req'],
                _return_http_data_only=kwargs['_return_http_data_only'],
                _preload_content=kwargs['_preload_content'],
                _request_timeout=kwargs['_request_timeout'],
                collection_formats=params['collection_format'])

    def get_status(
            self,
            video_id,
            **kwargs
        ):
            """Retrieve video status and details  # noqa: E501

            This method provides upload status & encoding status to determine when the video is uploaded or ready to playback. Once encoding is completed, the response also lists the available stream qualities.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_status(video_id, async_req=True)
            >>> result = thread.get()

            Args:
                video_id (str): The unique identifier for the video you want the status for.

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                async_req (bool): execute request asynchronously

            Returns:
                VideoStatus
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['video_id'] = \
                video_id

            params_map = {
                'all': [
                    'video_id',
                    'async_req',
                    '_preload_content',
                    '_request_timeout',
                    '_return_http_data_only'
                ],
                'required': [
                    'video_id',
                ],
                'nullable': [
                    '_request_timeout'
                ],
                'enum': [
                ],
                'validation': [
                ]
            }
            validations = {
            }
            allowed_values = {
            }
            openapi_types = {
                'video_id':
                    (str,),
                'async_req': (bool,),
                '_preload_content': (bool,),
                '_request_timeout': (none_type, int, (int,), [int]),
                '_return_http_data_only': (bool,)
            }
            attribute_map = {
                'video_id': 'videoId',
            }
            location_map = {
                'video_id': 'path',
            }
            collection_format_map = {
            }

            for key, value in kwargs.items():
                if key not in params_map['all']:
                    raise ApiTypeError(
                        "Got an unexpected parameter '%s'"
                        " to method `get_status`" %
                        (key, )
                    )
                if (key not in params_map['nullable'] and value is None):
                    raise ApiValueError(
                        "Value may not be None for non-nullable parameter `%s`"
                        " when calling `get_status`" %
                        (key, )
                    )

            for key in params_map['required']:
                if key not in kwargs.keys():
                    raise ApiValueError(
                        "Missing the required parameter `%s` when calling "
                        "`get_status`" % (key, )
                    )

            self._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
            params = self._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)
            return self.api_client.call_api(
                "/videos/{videoId}/status",
                "GET",
                params['path'],
                params['query'],
                params['header'],
                body=params['body'],
                post_params=params['form'],
                files=params['file'],
                response_type=(VideoStatus,),
                async_req=kwargs['async_req'],
                _return_http_data_only=kwargs['_return_http_data_only'],
                _preload_content=kwargs['_preload_content'],
                _request_timeout=kwargs['_request_timeout'],
                collection_formats=params['collection_format'])

    def list_discarded(
            self,
            **kwargs
        ):
            """List all discarded video objects  # noqa: E501

            This method returns a list of your discarded videos (with all their details). With no parameters added, the API returns the first page of all discarded videos. You can filter discarded videos using the parameters described below.  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.list_discarded(async_req=True)
            >>> result = thread.get()


            Keyword Args:
                title (str): The title of a specific video you want to find. The search will match exactly to what term you provide and return any videos that contain the same term as part of their titles.. [optional]
                tags ([str]): A tag is a category you create and apply to videos. You can search for videos with particular tags by listing one or more here. Only videos that have all the tags you list will be returned.. [optional]
                metadata ({str: (str,)}): Videos can be tagged with metadata tags in key:value pairs. You can search for videos with specific key value pairs using this parameter.. [optional]
                description (str): Retrieve video objects by `description`.. [optional]
                live_stream_id (str): Retrieve video objects that were recorded from a live stream by `liveStreamId`.. [optional]
                sort_by (str): Use this parameter to sort videos by the their created time, published time, updated time, or by title.. [optional]
                sort_order (str): Use this parameter to sort results. `asc` is ascending and sorts from A to Z. `desc` is descending and sorts from Z to A.. [optional]
                current_page (int): Choose the number of search results to return per page. Minimum value: 1. [optional] if omitted the server will use the default value of 1
                page_size (int): Results per page. Allowed values 1-100, default is 25.. [optional] if omitted the server will use the default value of 25
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                async_req (bool): execute request asynchronously

            Returns:
                VideosListResponse
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )

            params_map = {
                'all': [
                    'title',
                    'tags',
                    'metadata',
                    'description',
                    'live_stream_id',
                    'sort_by',
                    'sort_order',
                    'current_page',
                    'page_size',
                    'async_req',
                    '_preload_content',
                    '_request_timeout',
                    '_return_http_data_only'
                ],
                'required': [],
                'nullable': [
                    '_request_timeout'
                ],
                'enum': [
                    'sort_by',
                    'sort_order',
                ],
                'validation': [
                ]
            }
            validations = {
            }
            allowed_values = {
                ('sort_by',): {

                    "TITLE": "title",
                    "CREATEDAT": "createdAt",
                    "PUBLISHEDAT": "publishedAt",
                    "UPDATEDAT": "updatedAt"
                },
                ('sort_order',): {

                    "ASC": "asc",
                    "DESC": "desc"
                },
            }
            openapi_types = {
                'title':
                    (str,),
                'tags':
                    ([str],),
                'metadata':
                    ({str: (str,)},),
                'description':
                    (str,),
                'live_stream_id':
                    (str,),
                'sort_by':
                    (str,),
                'sort_order':
                    (str,),
                'current_page':
                    (int,),
                'page_size':
                    (int,),
                'async_req': (bool,),
                '_preload_content': (bool,),
                '_request_timeout': (none_type, int, (int,), [int]),
                '_return_http_data_only': (bool,)
            }
            attribute_map = {
                'title': 'title',
                'tags': 'tags[]',
                'metadata': 'metadata',
                'description': 'description',
                'live_stream_id': 'liveStreamId',
                'sort_by': 'sortBy',
                'sort_order': 'sortOrder',
                'current_page': 'currentPage',
                'page_size': 'pageSize',
            }
            location_map = {
                'title': 'query',
                'tags': 'query',
                'metadata': 'query',
                'description': 'query',
                'live_stream_id': 'query',
                'sort_by': 'query',
                'sort_order': 'query',
                'current_page': 'query',
                'page_size': 'query',
            }
            collection_format_map = {
                'tags': 'multi',
                'metadata': 'deepObject',
            }

            for key, value in kwargs.items():
                if key not in params_map['all']:
                    raise ApiTypeError(
                        "Got an unexpected parameter '%s'"
                        " to method `list_discarded`" %
                        (key, )
                    )
                if (key not in params_map['nullable'] and value is None):
                    raise ApiValueError(
                        "Value may not be None for non-nullable parameter `%s`"
                        " when calling `list_discarded`" %
                        (key, )
                    )

            for key in params_map['required']:
                if key not in kwargs.keys():
                    raise ApiValueError(
                        "Missing the required parameter `%s` when calling "
                        "`list_discarded`" % (key, )
                    )

            self._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
            params = self._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)
            return self.api_client.call_api(
                "/discarded/videos",
                "GET",
                params['path'],
                params['query'],
                params['header'],
                body=params['body'],
                post_params=params['form'],
                files=params['file'],
                response_type=(VideosListResponse,),
                async_req=kwargs['async_req'],
                _return_http_data_only=kwargs['_return_http_data_only'],
                _preload_content=kwargs['_preload_content'],
                _request_timeout=kwargs['_request_timeout'],
                collection_formats=params['collection_format'])

    def update_discarded(
            self,
            video_id,
            discarded_video_update_payload,
            **kwargs
        ):
            """Update a discarded video object  # noqa: E501

            Use this endpoint to restore a discarded video when you have the Video Restore feature enabled.

  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.update_discarded(video_id, discarded_video_update_payload, async_req=True)
            >>> result = thread.get()

            Args:
                video_id (str): The video ID for the video you want to restore.
                discarded_video_update_payload (DiscardedVideoUpdatePayload):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                async_req (bool): execute request asynchronously

            Returns:
                Video
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['video_id'] = \
                video_id
            kwargs['discarded_video_update_payload'] = \
                discarded_video_update_payload

            params_map = {
                'all': [
                    'video_id',
                    'discarded_video_update_payload',
                    'async_req',
                    '_preload_content',
                    '_request_timeout',
                    '_return_http_data_only'
                ],
                'required': [
                    'video_id',
                    'discarded_video_update_payload',
                ],
                'nullable': [
                    '_request_timeout'
                ],
                'enum': [
                ],
                'validation': [
                ]
            }
            validations = {
            }
            allowed_values = {
            }
            openapi_types = {
                'video_id':
                    (str,),
                'discarded_video_update_payload':
                    (DiscardedVideoUpdatePayload,),
                'async_req': (bool,),
                '_preload_content': (bool,),
                '_request_timeout': (none_type, int, (int,), [int]),
                '_return_http_data_only': (bool,)
            }
            attribute_map = {
                'video_id': 'videoId',
            }
            location_map = {
                'video_id': 'path',
                'discarded_video_update_payload': 'body',
            }
            collection_format_map = {
            }

            for key, value in kwargs.items():
                if key not in params_map['all']:
                    raise ApiTypeError(
                        "Got an unexpected parameter '%s'"
                        " to method `update_discarded`" %
                        (key, )
                    )
                if (key not in params_map['nullable'] and value is None):
                    raise ApiValueError(
                        "Value may not be None for non-nullable parameter `%s`"
                        " when calling `update_discarded`" %
                        (key, )
                    )

            for key in params_map['required']:
                if key not in kwargs.keys():
                    raise ApiValueError(
                        "Missing the required parameter `%s` when calling "
                        "`update_discarded`" % (key, )
                    )

            self._validate_inputs(kwargs, params_map, allowed_values, validations, openapi_types)
            params = self._gather_params(kwargs, location_map, attribute_map, openapi_types, collection_format_map)
            return self.api_client.call_api(
                "/discarded/videos/{videoId}",
                "PATCH",
                params['path'],
                params['query'],
                params['header'],
                body=params['body'],
                post_params=params['form'],
                files=params['file'],
                response_type=(Video,),
                async_req=kwargs['async_req'],
                _return_http_data_only=kwargs['_return_http_data_only'],
                _preload_content=kwargs['_preload_content'],
                _request_timeout=kwargs['_request_timeout'],
                collection_formats=params['collection_format'])

