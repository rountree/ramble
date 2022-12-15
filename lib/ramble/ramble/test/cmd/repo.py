# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# https://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or https://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.
import os.path

import pytest

from ramble.main import RambleCommand

repo = RambleCommand('repo')


def test_help_option():
    with pytest.raises(SystemExit):
        repo('--help')
    assert repo.returncode in (None, 0)


def test_create_add_list_remove(mutable_config, tmpdir):
    # Create a new repository and check that the expected
    # files are there
    repo('create', str(tmpdir), 'mockrepo')
    assert os.path.exists(os.path.join(str(tmpdir), 'repo.yaml'))

    # Add the new repository and check it appears in the list output
    repo('add', '--scope=site', str(tmpdir))
    output = repo('list', '--scope=site', output=str)
    assert 'mockrepo' in output

    # Then remove it and check it's not there
    repo('remove', '--scope=site', str(tmpdir))
    output = repo('list', '--scope=site', output=str)
    assert 'mockrepo' not in output
