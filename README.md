# Add Private PPA

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
