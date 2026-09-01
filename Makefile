DIST := dist

.PHONY: release skills plugins clean
release: clean plugins skills
	@echo; echo "== アカウントに上げるのはこの1つ =="; ls -1sh $(DIST)/studio.plugin
	@echo; echo "== 素の名前で呼びたいときだけ（Customize > Skills 用）=="; ls -1sh $(DIST)/skills/

## Cowork のプラグイン枠に上げる形式。hooks や agent を入れたときはこちら。
plugins:
	@mkdir -p $(DIST)
	@for p in plugins/*/; do n=$$(basename $$p); (cd $$p && zip -qr ../../$(DIST)/$$n.plugin . -x "*.DS_Store"); done

## Customize > Skills に上げる形式。スキル1本 = zip 1つ。
skills:
	@mkdir -p $(DIST)/skills
	@for d in plugins/*/skills/*/; do \
		n=$$(basename $$d); base=$$(dirname $$d); \
		(cd $$base && zip -qr ../../../$(DIST)/skills/$$n.zip $$n -x "*.DS_Store"); \
	done

clean:
	@rm -rf $(DIST)
