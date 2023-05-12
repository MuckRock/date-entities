try:
	python main.py \
		--base_uri https://api.dev.documentcloud.org/api/ \
	  --auth_uri https://dev.squarelet.com/api/ \
	 	--username $(DCUSER) --password "$(DCPASS)" 