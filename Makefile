
EXT_NAME:=ulauncher-two-factor-authenticator
EXT_DIR:=$(shell pwd)

link:
	@ln -s ${EXT_DIR} ~/.cache/ulauncher_cache/extensions/${EXT_NAME}

unlink:
	@rm -r ~/.cache/ulauncher_cache/extensions/${EXT_NAME}

