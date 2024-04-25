all:
	erlc chatroom.erl client.erl gui.erl lexgrm.erl main.erl server.erl
	erl -eval "lexgrm:start(), halt()" -noshell -detached

run: all
	erl

clean:
	rm -f *beam grm.erl lex.erl
