%predicados dinamicos
:-dynamic juego/2. %nombre y fecha de salida
:-dynamic estudio/1. %quien desarrolla
:-dynamic plataforma/1. %PC, Consola, Movil
:-dynamic desarrolla/2. %recibe juego y estudio
:-dynamic disponible/2. %recibe juego y plataforma

%reglas dinamicas
:- assertz((esJuego(J) :- juego(J,_))).
:- assertz((esEstudio(E) :- estudio(E))).
:- assertz((esPlataforma(P) :- plataforma(P))).
:- assertz((esDesarrollado(J,E) :- juego(J,_),
                                    estudio(E),
                                    desarrolla(J,E))).
:- assertz((estaDisponible(J,P) :- juego(J,_),
                                    plataforma(P),
                                    disponible(J,P))).

:- dynamic games_file/1.
:- dynamic studios_file/1.
:- dynamic platforms_file/1.
:- dynamic desarrollos_file/1.
:- dynamic disponibilidades_file/1.

% Cargar los datos dinámicamente según la ubicación de este archivo
:- prolog_load_context(directory, Dir),
   % juegos.pl
   atom_concat(Dir, '/juegos.pl', PathGames),
   assertz(games_file(PathGames)),
   (exists_file(PathGames) -> consult(PathGames) ; true),
   % estudios.pl
   atom_concat(Dir, '/estudios.pl', PathStudios),
   assertz(studios_file(PathStudios)),
   (exists_file(PathStudios) -> consult(PathStudios) ; true),
   % plataformas.pl
   atom_concat(Dir, '/plataformas.pl', PathPlatforms),
   assertz(platforms_file(PathPlatforms)),
   (exists_file(PathPlatforms) -> consult(PathPlatforms) ; true),
   % desarrollos.pl
   atom_concat(Dir, '/desarrollos.pl', PathDesarrollos),
   assertz(desarrollos_file(PathDesarrollos)),
   (exists_file(PathDesarrollos) -> consult(PathDesarrollos) ; true),
   % disponibilidades.pl
   atom_concat(Dir, '/disponibilidades.pl', PathDisponibilidades),
   assertz(disponibilidades_file(PathDisponibilidades)),
   (exists_file(PathDisponibilidades) -> consult(PathDisponibilidades) ; true).

