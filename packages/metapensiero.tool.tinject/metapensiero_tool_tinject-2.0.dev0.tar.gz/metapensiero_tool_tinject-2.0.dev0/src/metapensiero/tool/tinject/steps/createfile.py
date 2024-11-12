# -*- coding: utf-8 -*-
# :Project:   metapensiero.tool.tinject -- Create a file from a template
# :Created:   ven 22 apr 2016 09:04:39 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2018, 2024 Lele Gaifax
#

from pathlib import Path

from . import Step


class CreateFile(Step):
    def __init__(self, state, config):
        super().__init__(state, config)
        directory = state.render_string(config.get('directory', '.'))
        filename = state.render_string(config['filename'])
        self.overwrite = config.get('overwrite', self.state.overwrite)
        self.skip_existing = config.get('skip_existing', self.state.skip_existing)
        self.filename = Path(directory) / filename
        self.content = config['content']
        self.description = config.get('description')

    def announce(self):
        self.state.announce('*', "Create file %s", self.filename)

    def __call__(self, defaults, prompt_only=False, no_prompt=False):
        if prompt_only:
            return

        if self.filename.exists():
            if not self.overwrite and not self.skip_existing:
                raise RuntimeError("File %s already exists!" % self.filename)
            if self.skip_existing:
                return

        if not self.filename.parent.is_dir():
            raise RuntimeError("Directory %s does not exist!" % self.filename.parent)

        content = self.state.render_file_content(self.filename, self.content, self.description)

        if not self.state.dry_run:
            self.filename.write_text(content, 'utf-8')
