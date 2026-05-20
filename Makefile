l lint:
	@echo "Executing lint in backend code (pre-commit)"
	pre-commit run --show-diff-on-failure --color=always --all-files
