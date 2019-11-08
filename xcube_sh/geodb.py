# The MIT License (MIT)
# Copyright (c) 2019 by the xcube development team and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import os
import os.path
from typing import List, Dict, Any, Optional

GeoJSONObj = Dict[str, Any]


class GeoDB:

    def __init__(self):
        self._features = None

    def find_feature(self, query: str) -> Optional[GeoJSONObj]:
        features = self.find_features(query, max=1)
        return features[0] if features else None

    def find_features(self, query: str, max: int = -1) -> List[Dict[str, Any]]:
        compiled_query = compile(query, 'query', 'eval')
        result_set = []
        for feature in self.__features:
            # noinspection PyBroadException
            try:
                _locals = dict(id=feature.get('id')) if feature.get('id') else {}
                _locals.update(feature.get('properties', {}))
                result = eval(compiled_query, None, _locals)
            except Exception:
                result = False
            if result:
                result_set.append(feature)
                if len(result_set) >= max:
                    break
        return result_set

    @property
    def __features(self):
        if self._features is None:
            self._initialize_features()
        return self._features

    def _initialize_features(self):
        self._features = []
        source_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'geodb'))
        for filename in os.listdir(source_path):
            file_path = os.path.join(source_path, filename)
            if filename.endswith('.geojson') and os.path.isfile(file_path):
                with open(file_path) as fp:
                    geojson_dict = json.load(fp)
                    if 'type' in geojson_dict:
                        if geojson_dict['type'] == 'FeatureCollection' and geojson_dict.get('features'):
                            for feature in geojson_dict.get('features'):
                                self._features.append(feature)
                        if geojson_dict['type'] == 'Feature' and geojson_dict.get('geometry'):
                            self._features.append(geojson_dict)