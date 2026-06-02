PANDOC ?= pandoc
PDF_ENGINE ?= xelatex
BUILD_DIR := build

BOOK_FILES := $(shell cat book-files.txt)
EXISTING_FILES := $(shell cat book-files-existing-only.txt)

.PHONY: all pdf pdf-existing tex tex-existing proposal clean

all: pdf

pdf:
	mkdir -p $(BUILD_DIR)
	$(PANDOC) metadata.yaml $(BOOK_FILES) \
	  --from markdown+raw_tex+fenced_code_attributes \
	  --top-level-division=part \
	  --pdf-engine=$(PDF_ENGINE) \
	  -o $(BUILD_DIR)/snodec-book.pdf

pdf-existing:
	mkdir -p $(BUILD_DIR)
	$(PANDOC) metadata.yaml $(EXISTING_FILES) \
	  --from markdown+raw_tex+fenced_code_attributes \
	  --top-level-division=part \
	  --pdf-engine=$(PDF_ENGINE) \
	  -o $(BUILD_DIR)/snodec-book-existing-only.pdf

tex:
	mkdir -p $(BUILD_DIR)
	$(PANDOC) metadata.yaml $(BOOK_FILES) \
	  --from markdown+raw_tex+fenced_code_attributes \
	  --top-level-division=part \
	  -o $(BUILD_DIR)/snodec-book.tex

tex-existing:
	mkdir -p $(BUILD_DIR)
	$(PANDOC) metadata.yaml $(EXISTING_FILES) \
	  --from markdown+raw_tex+fenced_code_attributes \
	  --top-level-division=part \
	  -o $(BUILD_DIR)/snodec-book-existing-only.tex

proposal:
	mkdir -p $(BUILD_DIR)
	$(PANDOC) metadata.yaml proposal/book-proposal-package.md \
	  --from markdown+raw_tex+fenced_code_attributes \
	  --pdf-engine=$(PDF_ENGINE) \
	  -o $(BUILD_DIR)/book-proposal-package.pdf

clean:
	rm -rf $(BUILD_DIR)/*
