# ulauncher-two-factor-authenticator

This Ulauncher extension briges two-factor-authenticator cli application and Ulauncher, bringing the
safety of the cli tool to Ulauncher to generate OTP code.

## Install

Open Ulauncher preferences window > extensions > add extension and paste the following url:

    https://github.com/endorama/ulauncher-two-factor-authenticator

To use it you need to have [`two-factor-authenticator`](https://github.com/endorama/two-factor-authenticator) installed.  
Look there for futher information.

## Usage

Open Ulauncher, write `2fa` (default keyword) and a list of account available will be shown. Click
on one of them to copy the OTP token.

Fuzzy searching is available.

## Development

    git clone https://github.com/brpaz/ulauncher-tilix
    make link
    # in a separate terminal
    ./run-ulauncher.sh
    # back to the first
    ./run.sh

The make link command will symlink the cloned repo into the appropriate location on the Ulauncher extensions folder.

When done, to remove it from the available extensions you can run `make unlink`.

## Contributing

* Fork it!
* Create your feature branch: git checkout -b my-new-feature
* Commit your changes: git commit -am 'Add some feature'
* Push to the branch: git push origin my-new-feature
* Submit a pull request :D

## License

MPL (c) Edoardo Tenani 2019
