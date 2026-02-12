#!/usr/bin/env python3

import io
import subprocess

import click
import distro

from launchpadlib.launchpad import Launchpad
from launchpadlib.credentials import UnencryptedFileCredentialStore
import os


def lp_login():
    """
    Login to Launchpad and return the launchpad object
    """
    try:
        # Login with default credential store
        launchpad = Launchpad.login_with(
            "add-private-ppa",
            "production",
            version='devel'
        )
        return launchpad
        
    except Exception as e:
        print(f"✗ Failed to login to Launchpad: {e}")
        raise SystemExit(1)


@click.command()
@click.option(
    '-s', '--series',
    default=distro.codename(),
    help='Ubuntu series codename (default: current system codename)')
@click.argument('ppa')
def main(series, ppa):
    lp = lp_login()
    (ppa_owner, ppa_name) = ppa.lstrip("ppa:").split("/")

    lp_ppa = lp.people[ppa_owner].getPPAByName(name=ppa_name)
    if not lp_ppa.private:
        print(f"✗ PPA {ppa} is not private, cannot add to subscriptions")
        raise SystemExit(2)

    subscriptions = lp.me.getArchiveSubscriptions()
    found_url = False
    for url in lp.me.getArchiveSubscriptionURLs():
        if url.endswith(f"launchpadcontent.net/{ppa_owner}/{ppa_name}/ubuntu"):
            found_url = True
            subscription_url = url
            break

    if not found_url:
        print(f"✗ No subscription URL found for PPA {ppa}, please subscribe to it first")
        raise SystemExit(3)

    armored_key = lp_ppa.getSigningKeyData()

    entry = io.StringIO()
    entry.write(f"Types: deb deb-src\n")
    entry.write(f"URIs: {subscription_url}\n")
    entry.write(f"Suites: {series}\n")
    entry.write(f"Components: main\n")
    entry.write("Signed-By: \n")
    for line in armored_key.splitlines():
        if line:
            entry.write(f"  {line}\n")
        else:
            entry.write("  .\n")

    entry.seek(0)
    print(entry.read())


if __name__ == '__main__':
    main()
