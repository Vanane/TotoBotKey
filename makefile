build: clean
	python3 -m build

# Install built packages in the local venv
install:
#	 for dir in TotoBotKey TotoBotRec; do
	for dir in TotoBotKey; do \
		cd "src/$$dir"; \
		make install; \
		cd ../../; \
	done

clean:
	for f in $$(find -name *input-event-codes.h); do rm -f "$$f"; done
	for dir in TotoBotKey TotoBotRec; do \
		cd "src/$$dir"; \
		make clean; \
		cd  ../../; \
	done
