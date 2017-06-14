# -*- coding: utf-8 -*-

import os
import click

from typing import Tuple

import grout.core
import grout.core.backend


@click.command()
@click.option('--project', type=click.Path(dir_okay=False, exists=True), help='Path to project file')
@click.option('--skip', default=None, multiple=True, help='Skip a job by its name')
@click.option('--skip-environment', flag_value=True, help='Skip environment setup')
@click.option('--backend', default='lxc', type=click.Choice(('lxc', 'docker',)), help='Container backend to use')
@click.option('--name', help='Container backend name')
@click.option('--image', help='Container backend image')
@click.option('--arch', help='Container backend arch')
@click.option('--persistent', flag_value=False, help='Set container persistent')
def cli(project: str = None, skip: Tuple[str] = None, skip_environment: bool = False,
        backend: str = 'lxc', name: str = None, image: str = None,
        arch: str = None, persistent: bool = False):
    """Grout a simple tool and library for continuous, clean builds.

    Grout was primarily created to be used in combination with Snapcraft.
    """
    cwd = os.getcwd()
    if not project:
        project = os.path.join(cwd, 'project.yaml')
    if not os.path.isfile(project):
        raise click.ClickException('Project file "{}" does not exist.'.format(project))
    if not grout.core.backend.type_exists(backend):
        raise click.ClickException('The requested container backend "{}" could not be found.'.format(backend))
    backend_options = {
        'name': name,
        'image': image,
        'arch': arch,
        'ephemeral': not persistent
    }
    grout.core.run_declarative(
        project, backend_type=backend, backend_options=backend_options,
        skip_jobs=skip, skip_environment=skip_environment
    )


if __name__ == '__main__':
    cli()
