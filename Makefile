PYTHON := python
REPOS_DIR := repos
CHECKPOINT_FILE := checkpoint.txt

run:
	@echo Running data.py...
	@$(PYTHON) data.py

# Target to clean up the repos directory and checkpoint file
clean:
	@echo Cleaning up...
	@if exist $(REPOS_DIR) (rmdir /S /Q $(REPOS_DIR) && echo Deleted $(REPOS_DIR) directory.) else (echo $(REPOS_DIR) directory not found.)
	@if exist $(CHECKPOINT_FILE) (del $(CHECKPOINT_FILE) && echo Deleted $(CHECKPOINT_FILE).) else (echo $(CHECKPOINT_FILE) not found.)

# Default target
all: clean run
