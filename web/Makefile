MAIN_JS = app
MAIN_CSS = style.styl
STATIC = index.html

MATERIAL = node_modules/material-design-lite/material.min
MATERIAL_CSS = $(MATERIAL).css
MATERIAL_JS = $(MATERIAL).js
MATERIAL_CSS_MAP = $(MATERIAL_CSS).map
MATERIAL_JS_MAP = $(MATERIAL_JS).map

SRC_DIR = src
IMG_DIR = img
BUILD_DIR = build
BUNDLE_JS = bundle.js

STYLUS = node_modules/.bin/stylus

.PHONY: default
default: deps build

.PHONY: build
build: pre html js css img

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)/*

.PHONY: pre
pre: clean
	mkdir -p $(BUILD_DIR)

.PHONY: html
html:
	cp $(SRC_DIR)/$(STATIC) $(BUILD_DIR)

.PHONY: js
js:
	jspm bundle-sfx $(SRC_DIR)/$(MAIN_JS) -o $(BUILD_DIR)/$(BUNDLE_JS)

.PHONY: css
css:
	$(STYLUS) $(SRC_DIR)/$(MAIN_CSS) -o $(BUILD_DIR)/

	cp $(MATERIAL_CSS) $(BUILD_DIR)/
	cp $(MATERIAL_CSS_MAP) $(BUILD_DIR)/

	cp $(MATERIAL_JS) $(BUILD_DIR)/
	cp $(MATERIAL_JS_MAP) $(BUILD_DIR)/

.PHONY: img
img:
	cp $(IMG_DIR)/* $(BUILD_DIR)/

.PHONY: check-deps
check-deps:
	which jspm
	which npm

.PHONY: deps
deps:	check-deps
	jspm install
	npm install

.PHONY: dev
dev: deps build
	stalk make src
