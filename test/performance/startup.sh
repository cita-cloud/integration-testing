#!/bin/bash
#
# Copyright Rivtower Technologies LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
set -x

pwd=`pwd`
dir=`dirname $0`
path=$pwd/$dir/scripts
source $pwd/test/utils/set_context.sh

for file in `ls "$path"`; do
  ret=$(python "$path/$file")
  if [ $ret = "0" ]; then
    echo "exec $file successful"
  else
    echo "exec $file failed, ret = $ret"
    exit 1
  fi
done
