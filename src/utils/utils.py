# Copyright (c) 2021, Danish Technological Institute.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
# Author: Nicolai Anton Lynnerup <nily@dti.dk>

def stringify_dict(d):
    for k in d.keys():
        if isinstance(d[k], dict):
            v = stringify_dict(d[k])
        else:
            v = d[k]

        if not isinstance(k, str):
            try:
                d[str(k)] = v
            except Exception:
                pass
            del d[k]
    return d
