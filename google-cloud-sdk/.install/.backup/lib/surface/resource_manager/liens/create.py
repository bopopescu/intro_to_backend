# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command to create a new Lien."""

from googlecloudsdk.api_lib.resource_manager import error
from googlecloudsdk.api_lib.resource_manager import liens
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.resource_manager import liens_base
from googlecloudsdk.core import properties


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Create(liens_base.LienCommand):
  """Create a new lien.

  Creates a new lien to be applied to a project.
  """

  @staticmethod
  def Args(parser):
    base.Argument(
        '--restrictions',
        required=True,
        help='Comma separated list of IAM permissions to curtail').AddToParser(
            parser)
    base.Argument(
        '--reason',
        required=True,
        help='A human-readable description of why this lien is being applied.'
    ).AddToParser(parser)
    base.Argument(
        '--origin',
        required=False,
        help='The originator of for this Lien. Defaults to user identy.'
    ).AddToParser(parser)

  @error.EmitErrorDetails
  def Run(self, args):
    parent = 'projects/' + properties.VALUES.core.project.Get(required=True)

    # Origin is a required field which will default to the account property if
    # not specified.
    origin = args.origin
    if not origin:
      origin = properties.VALUES.core.account.Get(required=True)

    messages = liens.LiensMessages()
    return liens.LiensService().Create(
        messages.Lien(
            parent=parent,
            restrictions=args.restrictions.split(','),
            origin=origin,
            reason=args.reason))
