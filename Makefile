all:
	STARBOARD_DATABASE=data/starboard.db sipy

watch:
	while true; do \
		make; \
		inotifywait -qre close_write .; \
	done
