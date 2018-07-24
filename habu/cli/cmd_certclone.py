import socket
import ssl

import click

from habu.lib.certclone import certclone


@click.command()
@click.argument('hostname')
@click.argument('port')
@click.argument('keyfile', type=click.File('w'))
@click.argument('certfile', type=click.File('w'))
@click.option('--copy-extensions', 'copy_extensions', is_flag=True, default=False, help='Copy certificate extensions (default: False)')
@click.option('--expired', 'expired', is_flag=True, default=False, help='Generate an expired certificate (default: False)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_certclone(hostname, port, keyfile, certfile, copy_extensions, expired, verbose):

    context = ssl.create_default_context()

    with socket.create_connection((hostname, port), timeout=3) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            original = ssock.getpeercert(binary_form=True)

    key, cert = certclone(original, copy_extensions=copy_extensions, expired=expired)

    keyfile.write(key)
    certfile.write(cert)


if __name__ == '__main__':
    cmd_certclone()
