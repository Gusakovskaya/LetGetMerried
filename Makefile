.PHONY: update-ui
update-ui:
	cp -r ui /usr/share/nginx
	chmod -R 777 /usr/share/nginx/ui