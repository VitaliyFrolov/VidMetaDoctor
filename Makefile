# ---------- DEVELOPMENT ----------
dev-start:
	python src/app.py


# ---------- BUILD MACOS USING SPEC ----------
build-mac:
	pyinstaller VidMetaEdit.spec
	@echo "macOS build complete. Find binary in dist/VidMetaEdit"


# ---------- BUILD WINDOWS ----------
build-win:
	pyinstaller --onefile --name VidMetaEdit.exe src/app.py
	@echo "Windows build complete. Find binary in dist/VidMetaEdit.exe"


# ---------- CLEAN ----------
clean:
	rm -rf build dist *.spec
	@echo "Cleaned build artifacts"