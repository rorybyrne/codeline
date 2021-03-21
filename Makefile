.PHONY: install clean

BASE_PYTHON=python3.8

BASE_DIR=${HOME}/.local
SHARE_DIR=${BASE_DIR}/share/codeline
SYSTEMD_DIR=${BASE_DIR}/share/systemd/user

SERVICE_FILE=codeline.service

check-env:
ifndef HOME
	$(error Environment variable HOME is undefined)
endif

check-dirs:
	@test -d $(BASE_DIR) || (echo "Missing $(BASE_DIR) directory, which is base directory" && exit 1)
	@test -d $(INSTALL_DIR) || (echo "Missing the install directory: $(INSTALL_DIR)" && exit 1)

install: check-env check-dirs
	@echo "Make install not supported" && exit 1
	@echo "Installing to $(INSTALL_DIR)"
	install -d $(SHARE_DIR)
	install -m 0644 assets/share/* $(SHARE_DIR)
	install -d $(SYSTEMD_DIR)
	install -m 0644 assets/service/* $(SYSTEMD_DIR)
	$(BASE_PYTHON) -m venv $(SHARE_DIR)/venv
	$(SHARE_DIR)/venv/bin/python -m pip install -U pip
	$(SHARE_DIR)/venv/bin/python -m pip install .
	systemctl --user enable $(SERVICE_FILE) --now

uninstall:
	@echo "Make uninstall not supported" && exit 1
	@echo "Deleting share files..."
	@test -d $(SHARE_DIR) && \
		rm -rf $(SHARE_DIR) && \
		echo "Done..." || \
		echo "No share directory found"
	@echo "Deleting service file..."
	@systemctl --user disable $(SERVICE_FILE) --now || echo "Attempting to remove service file anyway..."
	@test -d $(SYSTEMD_DIR) && \
		cd $(SYSTEMD_DIR) && \
		rm -f $(SERVICE_FILE) && \
		echo "Done." || \
		echo "Could not delete service file."

run-local:
	@CL_DEBUG=1 poetry run python -m codeline
