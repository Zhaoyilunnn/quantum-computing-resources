# Install nix

- https://nixos.org/download


# Install DAX

Refer to the [official document](https://m-labs.hk/artiq/manual/installing.html#installing-via-nix-linux)

```bash
mkdir -p ~/.config/nix
echo "experimental-features = nix-command flakes" > ~/.config/nix/nix.conf
```

Install ARTIQ

```bash

nix profile install git+https://github.com/m-labs/artiq.git\?ref=release-7
```

Install dax according to [dax wiki](https://gitlab.com/duke-artiq/dax/-/wikis/DAX/Installation)

```bash
git clone https://gitlab.com/duke-artiq/dax.git
cd dax
nix develop

```

Afterwards, run [dax-example](https://gitlab.com/duke-artiq/dax-example) similarly

```bash
git clone https://gitlab.com/duke-artiq/dax-example.git
cd dax-example/
nix develop
artiq_session

```


# Install QCoDeS

[15-minutes-to-QCoDeS](https://github.com/microsoft/Qcodes/blob/main/docs/examples/15_minutes_to_QCoDeS.ipynb)
