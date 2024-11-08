# -*- coding: utf-8 -*-
# Copyright (C) 2023-2024 TUD | ZIH
# ralf.klammer@tu-dresden.de

import logging

import re
import requests

from copy import deepcopy
from lxml.etree import fromstring, ElementTree, tostring

log = logging.getLogger(__name__)


class XMLParserBase(object):

    def __init__(self, uri=None, tree=None, default_ns_prefix="tei"):
        self.uri = uri
        self.default_ns_prefix = default_ns_prefix
        self.tree = tree
        self.load_resource()

    def __repr__(self):
        return "<XSDParserBase: %s>" % self.uri

    @property
    def file_name(self):
        if self.uri:
            return self.uri.split("/")[-1]

    def load_resource(self):
        log.debug("XMLParserBase - load uri: %s" % self.uri)
        try:
            if self.tree is None:
                if self.uri.startswith("http"):
                    resource = requests.get(self.uri).content
                else:
                    with open(self.uri, "r") as file:
                        resource = file.read()
                resource = resource.replace("\t", "  ").encode()
                self.tree = fromstring(resource)
        except Exception as e:
            log.error(e)
            raise "Unable to load XML resource"

    def _decompose_search_string(self, search_string):
        attrib = None
        if search_string.find("/@") != -1:
            decomposed = search_string.split("/@")
            search_string = decomposed[0]
            attrib = decomposed[1]
        return search_string, attrib

    def _add_default_prefix(self, search_string):
        log.debug("_add_default_prefix")
        log.debug(f"before: {search_string}")

        # find all urls in search_string and replace them with a placeholder
        url_regex = r'(?<=\{)(https?://[^}]+)(?=\})|(?<=")(https?://[^"]+)(?=")|(?<=@{)(http[^}]+)(?=\})'
        urls_found = re.findall(url_regex, search_string)
        urls = [url for match in urls_found for url in match if url]
        for url in urls:
            search_string = search_string.replace(url, "preservedurls")

        if search_string.find("//") != -1:
            # remove all double slashes to avoid hitting them also in
            # the next step
            search_string = search_string.replace("//", "^^")
        # replace all '/' with '/prefix:'
        search_string = search_string.replace(
            "/", f"/{self.default_ns_prefix}:"
        )
        # bring back double slashes and add prefix
        search_string = search_string.replace(
            "^^", f"//{self.default_ns_prefix}:"
        )

        # replace all preservedurls with the original urls
        for i in range(0, len(urls)):
            search_string = search_string.replace("preservedurls", urls[i], 1)

        if search_string.startswith(".//"):
            search_string = search_string[1:]

        log.debug(f"after: {search_string}")

        return search_string

    @property
    def namespaces(self):
        ns = self.tree.nsmap.copy()
        if None in ns:
            ns[self.default_ns_prefix] = ns.pop(None)
        return ns

    def find(
        self,
        search_string,
        elem=None,
        text=None,
        return_text=False,
    ):
        search_string, attrib = self._decompose_search_string(search_string)

        search_string = self._add_default_prefix(search_string)

        result = (elem if elem is not None else self.tree).xpath(
            search_string, namespaces=self.namespaces
        )
        if len(result) > 0:
            result = deepcopy(result[0])
        else:
            result = None

        if result is not None and attrib:
            result.text = result.get(attrib)
        if text:
            if result.text == text:
                return tostring(result) if return_text else result
        else:
            return tostring(result) if return_text and result else result

    def findall(self, search_string, elem=None, text=None):
        search_string, attrib = self._decompose_search_string(search_string)

        search_string = self._add_default_prefix(search_string)

        results = (elem if elem is not None else self.tree).xpath(
            search_string, namespaces=self.namespaces
        )
        if attrib:
            return [result for result in results if result.get(attrib)]
        elif text:
            return [result for result in results if result.text == text]
        else:
            return results

    def write(self, filename):
        ElementTree(self.tree).write(
            filename, pretty_print=True, encoding="utf-8"
        )

    def print_tree(self):
        return tostring(self.tree).decode("utf-8")
