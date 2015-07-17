#!/usr/bin/env python

import ConfigParser
from urllib import urlencode
from urllib2 import Request, urlopen, HTTPError

# Amazon Cloud Drive api
import requests


class AmazonCloudDriveApi:
    def __init__(self, access_token=None, content_url=None, metadata_url=None):
        self.access_token = access_token
        self.content_url = content_url
        self.metadata_url = metadata_url

    # Account
    def get_account_info(self):
        return self._make_request('{{metadataUrl}}/account/info')

    def get_account_endpoint(self):
        return self._make_request('{{metadataUrl}}/account/endpoint')

    def get_account_quota(self):
        return self._make_request('{{metadataUrl}}/account/quota')

    def get_account_usage(self):
        return self._make_request('{{metadataUrl}}/account/usage')

    # Nodes
    # Files
    def upload_file(self, file, name, kind='FILE', labels=None, properties=None, parents=None, deduplication=False):
        params = {
            'metadata': {
                'name': name,
                'kind': kind,
                'labels': labels,
                'properties': properties,
                'parents': parents
            },
            'content': file
        }
        url = '{{contentUrl}}/nodes'
        if deduplication:
            url += '?suppress=deduplication'
        return self._make_request(url, data=params)

    def overwrite_file(self, file):
        # todo
        return self._make_request('{{contentUrl}}/nodes/{id}/content', data=file)

    def download_file(self, id):
        return self._make_request('{{contentUrl}}/nodes/{id}/content'.replace('{id}', id))

    def get_templink(self):
        # todo
        pass

    def get_file_metadata(self, id):
        return self._make_request('{{metadataUrl}}/nodes/{id}'.replace('{id}', id))

    def patch_file(self):
        # todo
        pass

    def list_all_files(self):
        return  self._make_request('{{metadataUrl}}/nodes?filters=kind:FILE')

    def list_all_assets(self):
        return  self._make_request('{{metadataUrl}}/nodes?filters=kind:ASSET')

    # Folders
    def create_folder(self, name):
        # todo
        return self._make_request('{{metadataUrl}}/nodes', data={})

    def get_folder_metadata(self, id):
        return self._make_request('{{metadataUrl}}/nodes/{id}'.replace('{id}', id))

    def patch_folder(self):
        # todo
        pass

    def list_all_folders(self):
        return  self._make_request('{{metadataUrl}}/nodes?filters=kind:FOLFDER')

    # Children
    def add_child(self, parent_id, child_id):
        return  self._make_request('{{metadataUrl}}/nodes/{parentId}/children/{childId}'
                                   .replace('{parentId}', parent_id)
                                   .replace('{childId}', child_id))

    def delete_child(self, parent_id, child_id):
        # todo
        return  self._make_request('{{metadataUrl}}/nodes/{parentId}/children/{childId}'
                                   .replace('{parentId}', parent_id)
                                   .replace('{childId}', child_id))

    def list_children(self, id):
        return  self._make_request('{{metadataUrl}}/nodes/{id}/children'.replace('{id}', id))

    # Properties
    # todo

    def _make_request(self, url, data=None):
        url.replace('{{metadataUrl}}', self.metadata_url)
        url.replace('{{contentUrl}}', self.content_url)
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        if data is None:
            return requests.get(url, headers=headers)
        else:
            return requests.post(url, data=data, headers=headers)