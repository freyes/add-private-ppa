# Add Private PPA

## Install

### Python Package

``` sh
pipx install git+https://github.com/freyes/add-private-ppa.git
```

### Snap

``` sh
sudo snap install add-private-ppa
sudo snap connect add-private-ppa:password-manager-service
```

## Usage

``` sh
add-private-ppa --help
Usage: add_private_ppa.py [OPTIONS] PPA

Options:
  -s, --series TEXT  Ubuntu series codename (default: current system codename)
  --help             Show this message and exit.

```

## Examples

1. Add sources over SSH

``` sh
add-private-ppa --series noble ppa:some/ppa \
    | ssh ubuntu@foobar "cat - | sudo tee /etc/apt/sources.list.d/some-ppa.source"
```
