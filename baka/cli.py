# -*- coding: utf-8 -*-

import os
import click

from typing import Tuple

import baka.core
import baka.core.backend


@click.command()
@click.option('--project', type=click.Path(dir_okay=False, exists=True), help='Path to project file')
@click.option('--artifacts', type=click.Path(file_okay=False, writable=True), help='Path to write build artifacts to')
@click.option('--skip', default=None, multiple=True, help='Skip a job by its name')
@click.option('--skip-environment', flag_value=True, help='Skip environment setup')
@click.option('--backend', default='lxc', type=click.Choice(('lxc', 'docker',)), help='Container backend to use')
@click.option('--name', help='Container backend name')
@click.option('--image', help='Container backend image')
@click.option('--arch', help='Container backend arch')
@click.option('--persistent', flag_value=True, help='Set container persistent')
@click.option('--nesting', flag_value=True, help='Allow container nesting (lxc only)')
def cli(project: str = None, artifacts: str = None, skip: Tuple[str] = None, skip_environment: bool = False,
        backend: str = 'lxc', name: str = None, image: str = None,
        arch: str = None, persistent: bool = False, nesting: bool = False):
    """Baka a simple tool and library for continuous, clean builds.

    Baka was primarily created to be used in combination with Snapcraft.
    """
    cwd = os.getcwd()
    if not project:
        project = os.path.join(cwd, 'baka.yml')
    if not os.path.isfile(project):
        raise click.ClickException('Project file "{}" does not exist.'.format(project))
    if not baka.core.backend.type_exists(backend):
        raise click.ClickException('The requested container backend "{}" could not be found.'.format(backend))
    if not artifacts:
        artifacts = os.path.join(cwd, '.baka')
    if not os.path.isdir(artifacts):
        os.makedirs(artifacts, exist_ok=True)
    if nesting and backend != 'lxc':
        raise click.ClickException('Nesting is only supported in for LXC containers.')
    backend_options = {
        'name': name,
        'image': image,
        'arch': arch,
        'ephemeral': not persistent,
        'nesting': nesting
    }
    baka.core.run_declarative(
        project, backend_type=backend, backend_options=backend_options,
        skip_jobs=skip, skip_environment=skip_environment, artifacts_path=artifacts
    )


if __name__ == '__main__':
    cli()
