build:
	for dir in TotoBotKey TotoBotRec; do \
		cd "src/$$dir"; \
		make build; \
		cd ../../; \
	done
clean:
	for dir in TotoBotKey TotoBotRec; do \
		cd "src/$$dir"; \
		make clean; \
		cd  ../../; \
	done
